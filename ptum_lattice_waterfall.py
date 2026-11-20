#!/usr/bin/env python3
"""Nonlinear 3-D classical lattice evolution of the real PTUM waterfall field.

This is a periodic finite-difference classical-field solver. It evolves a
homogeneous fuel field Phi, a real inhomogeneous psi(x), and the scale factor
self-consistently. Spatial gradients, the quartic interaction, the Phi-psi
force, and the Friedmann source are all included. Nonlinear mode coupling
therefore permits classical rescattering and Z2 wall formation for supplied
classical initial fields.

Scientific boundary:
- The optional first-order adiabatic-WKB helper draws bare Gaussian samples
  of the free-mode symmetrized covariance before the tachyonic threshold.
- These are classical-statistical initial fields, not quantum evolution.
  Their zero-point energy is retained; no vacuum subtraction, counterterms,
  or continuum renormalization are implemented.
- The initial Hubble derivatives use homogeneous Phi only and omit psi
  vacuum backreaction. The nonlinear evolution remains UV-cutoff dependent.
- Results are finite-volume, finite-lattice classical results and must not
  be interpreted as physical quantum-waterfall predictions or relic abundances.
- Lattice/volume/time/ensemble convergence and a renormalized initial-state
  prescription are required before physical claims.

Natural units are used. The comoving coordinates are measured in mu^{-1},
where mu=params.mu, and tau=mu*t. The scale factor is initialized to one.
"""
from __future__ import annotations

import hashlib
from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp

from ptum_task1_simulation import (
    M_PL,
    PTUMParameters,
    dveff_dphi,
    meff_sq_psi,
    veff_phi,
)


def periodic_laplacian_and_gradient_energy(
    field: np.ndarray,
    dx: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the periodic 3-D central Laplacian and local forward-gradient norm.

    The two operators obey the discrete periodic integration-by-parts identity
    mean(field * laplacian(field)) = -mean(gradient_norm_squared).
    """
    values = np.asarray(field, dtype=float)
    spacing = float(dx)
    if values.ndim != 3 or min(values.shape) < 4:
        raise ValueError("field must be a 3-D array with at least four cells per axis")
    if not np.all(np.isfinite(values)):
        raise ValueError("field must contain only finite values")
    if not np.isfinite(spacing) or spacing <= 0.0:
        raise ValueError("dx must be finite and positive")

    laplacian = np.zeros_like(values)
    gradient_norm_squared = np.zeros_like(values)
    for axis in range(3):
        forward = np.roll(values, -1, axis=axis) - values
        backward = np.roll(values, 1, axis=axis) - values
        laplacian += (forward + backward) / spacing**2
        gradient_norm_squared += (forward / spacing) ** 2
    return laplacian, gradient_norm_squared


def _wall_area_density_over_mu(field: np.ndarray, dx: float, scale_factor: float) -> float:
    """Nearest-neighbour sign-crossing area per physical volume, in units of mu."""
    crossings = 0
    for axis in range(3):
        neighbour = np.roll(field, -1, axis=axis)
        # Treat exact zeros as the non-negative phase so a wall passing
        # through a lattice site is counted on one adjacent link, not lost.
        crossings += int(np.count_nonzero((field < 0.0) != (neighbour < 0.0)))
    return float(crossings / (field.size * dx * scale_factor))



def _array_sha256(values: np.ndarray) -> str:
    """Hash a canonical contiguous float array for initial-state provenance."""
    return hashlib.sha256(np.ascontiguousarray(values, dtype=float).tobytes()).hexdigest()


def _sample_real_gaussian_field_with_power(
    mode_power: np.ndarray,
    rng: np.random.Generator,
    dx: float,
) -> np.ndarray:
    """Draw a real periodic Gaussian field with <|q_k|^2>=mode_power[k].

    The Fourier convention is q(x)=V^(-1/2) sum_k q_k exp(i k.x),
    with V=(N*dx)^3. FFTs of real white noise enforce Hermitian symmetry.
    """
    power = np.asarray(mode_power, dtype=float)
    if power.ndim != 3 or len(set(power.shape)) != 1:
        raise ValueError("mode_power must be a cubic 3-D array")
    if not np.all(np.isfinite(power)) or np.any(power <= 0.0):
        raise ValueError("all Gaussian mode powers must be finite and positive")
    n = power.shape[0]
    volume = (n * float(dx)) ** 3
    white_noise = rng.standard_normal(power.shape)
    fourier = np.fft.fftn(white_noise)
    fourier *= np.sqrt((n**3 / volume) * power)
    return np.fft.ifftn(fourier).real


def sample_adiabatic_vacuum_initial_conditions(
    params: PTUMParameters,
    *,
    grid_size: int,
    box_size_over_mu: float,
    Phi_initial: float,
    Phi_dot_initial: float,
    seed: int | None,
    adiabaticity_tolerance: float = 0.1,
) -> dict[str, object]:
    """Draw a bare first-order adiabatic-WKB Gaussian sample for the free psi modes.

    The canonical variable is X=a^(3/2) psi/psi_0. In tau=mu*t units,
    X_k'' + Omega_k^2 X_k=0, with the exact central-difference lattice
    dispersion and the homogeneous-Phi-only FRW curvature terms. The
    sampled real fields reproduce the symmetrized two-point covariance
    of the first-order WKB state. They are classical-statistical samples,
    not quantum evolution. The bare zero-point energy is retained; no
    vacuum subtraction or renormalization is performed.

    The initial H and its derivatives use the single homogeneous Phi
    background and omit psi vacuum backreaction. Every lattice mode,
    including the zero mode, must be stable and adiabatic or the routine
    refuses to manufacture a vacuum sample.
    """
    if (isinstance(grid_size, (bool, np.bool_))
            or int(grid_size) != grid_size or grid_size < 4):
        raise ValueError("grid_size must be an integer >= 4")
    n = int(grid_size)
    box_length = float(box_size_over_mu)
    if not np.isfinite(box_length) or box_length <= 0.0:
        raise ValueError("box_size_over_mu must be finite and positive")
    if not np.isfinite(Phi_initial) or not np.isfinite(Phi_dot_initial):
        raise ValueError("initial Phi and Phi_dot must be finite")
    if seed is not None and (
        isinstance(seed, (bool, np.bool_))
        or not isinstance(seed, (int, np.integer))
    ):
        raise ValueError("seed must be an integer or None")
    tolerance = float(adiabaticity_tolerance)
    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("adiabaticity_tolerance must be finite and positive")

    mu = float(params.mu)
    psi0 = float(params.psi_0)
    if (not np.isfinite(mu) or mu <= 0.0 or not np.isfinite(psi0)
            or psi0 <= 0.0 or not np.isfinite(params.lambda_psi)
            or params.lambda_psi <= 0.0):
        raise ValueError("PTUM mass, field scale and quartic coupling must be positive")

    phi = float(Phi_initial)
    phi_dot = float(Phi_dot_initial)
    eta = float(meff_sq_psi(phi, params) / mu**2)
    if not np.isfinite(eta) or eta <= 0.0:
        raise ValueError(
            "adiabatic vacuum sampling is forbidden at or below the tachyonic threshold"
        )

    rho_phi = 0.5 * phi_dot**2 + float(veff_phi(phi, params))
    if not np.isfinite(rho_phi) or rho_phi <= 0.0:
        raise ValueError("homogeneous Phi background energy must be finite and positive")
    hubble = float(np.sqrt(rho_phi / (3.0 * M_PL**2)))
    h = hubble / mu
    h_prime = -0.5 * phi_dot**2 / (M_PL**2 * mu**2)
    phi_acceleration = -3.0 * hubble * phi_dot - float(dveff_dphi(phi, params))
    h_second = -phi_dot * phi_acceleration / (M_PL**2 * mu**3)
    eta_prime = (
        2.0 * params.m_psi**2 * params.alpha * phi * phi_dot
        / (mu**3 * params.E_th**2)
    )

    dx = box_length / n
    k_axis = 2.0 * np.pi * np.fft.fftfreq(n, d=dx)
    lattice_k_squared = np.zeros((n, n, n), dtype=float)
    for axis in range(3):
        shape = [1, 1, 1]
        shape[axis] = n
        k_component = k_axis.reshape(shape)
        lattice_k_squared += (
            4.0 * np.sin(0.5 * k_component * dx) ** 2 / dx**2
        )

    omega_squared = (
        lattice_k_squared + eta - 1.5 * h_prime - 2.25 * h**2
    )
    if not np.all(np.isfinite(omega_squared)) or np.any(omega_squared <= 0.0):
        raise ValueError(
            "no adiabatic vacuum exists for this finite lattice: "
            "at least one canonical mode has non-positive frequency squared"
        )
    omega = np.sqrt(omega_squared)
    omega_squared_prime = (
        -2.0 * h * lattice_k_squared
        + eta_prime
        - 1.5 * h_second
        - 4.5 * h * h_prime
    )
    omega_prime = 0.5 * omega_squared_prime / omega
    wkb_parameter = np.abs(omega_prime) / omega**2
    expansion_parameter = np.abs(h) / omega
    adiabaticity = np.maximum(wkb_parameter, expansion_parameter)
    max_wkb = float(np.max(wkb_parameter))
    max_expansion = float(np.max(expansion_parameter))
    max_adiabaticity = float(np.max(adiabaticity))
    if not np.isfinite(max_adiabaticity) or max_adiabaticity > tolerance:
        raise ValueError(
            "initial background is not adiabatic for every lattice mode: "
            f"maximum parameter {max_adiabaticity:.6g} exceeds {tolerance:.6g}"
        )

    # For X=a^(3/2)s, the first-order WKB covariance is
    # <XX*> = lambda_psi/(2 Omega), with the WKB amplitude derivative
    # included in the symmetrized X-X' covariance. Transforming back to
    # s gives the velocity shift below and an independent residual mode.
    q_power = params.lambda_psi / (2.0 * omega)
    residual_velocity_power = params.lambda_psi * omega / 2.0
    rng = np.random.default_rng(seed)
    s = _sample_real_gaussian_field_with_power(q_power, rng, dx)
    residual_velocity = _sample_real_gaussian_field_with_power(
        residual_velocity_power, rng, dx
    )
    velocity_shift = -0.5 * (omega_prime / omega + 3.0 * h)
    s_prime = velocity_shift * s + residual_velocity

    psi_initial = psi0 * s
    psi_dot_initial = mu * psi0 * s_prime
    if not np.all(np.isfinite(psi_initial)) or not np.all(np.isfinite(psi_dot_initial)):
        raise FloatingPointError("adiabatic vacuum sampler produced non-finite fields")

    metadata = {
        "kind": "bare_first_order_adiabatic_wkb_gaussian_classical_sample",
        "representation": "classical_statistical_sample_of_symmetrized_free_mode_covariance",
        "adiabatic_order": 1,
        "canonical_variable": "a^(3/2) psi/psi_0",
        "mode_frequency": "sqrt(khat^2/a^2 + m_eff^2/mu^2 - 3 h'/2 - 9 h^2/4)",
        "fourier_normalization": "psi(x)=V^(-1/2) sum_k psi_k exp(i k.x)",
        "grid_shape": [n, n, n],
        "box_size_over_mu": box_length,
        "dx_over_mu_inverse": dx,
        "seed": None if seed is None else int(seed),
        "Phi_initial_GeV": phi,
        "Phi_dot_initial_GeV2": phi_dot,
        "H_background_over_mu": h,
        "H_prime_over_mu2": h_prime,
        "H_second_over_mu3": h_second,
        "m_eff_squared_over_mu2": eta,
        "m_eff_squared_prime_over_mu2": eta_prime,
        "minimum_canonical_frequency_squared_over_mu2": float(np.min(omega_squared)),
        "minimum_canonical_frequency_over_mu": float(np.min(omega)),
        "maximum_canonical_frequency_over_mu": float(np.max(omega)),
        "maximum_abs_frequency_derivative_over_frequency_squared": max_wkb,
        "maximum_abs_H_over_frequency": max_expansion,
        "maximum_adiabaticity_parameter": max_adiabaticity,
        "adiabaticity_tolerance": tolerance,
        "all_modes_stable": True,
        "all_modes_adiabatic": True,
        "vacuum_subtraction_applied": False,
        "vacuum_renormalized": False,
        "zero_point_energy_retained": True,
        "full_quantum_evolution": False,
        "initial_background_approximation": (
            "homogeneous_Phi_only_FRW_without_psi_vacuum_backreaction"
        ),
        "initial_hubble_self_consistent_with_lattice": False,
        "subsequent_lattice_includes_bare_psi_energy": True,
        "psi_initial_sha256": _array_sha256(psi_initial),
        "psi_dot_initial_sha256": _array_sha256(psi_dot_initial),
    }
    return {
        "psi_initial": psi_initial,
        "psi_dot_initial": psi_dot_initial,
        "metadata": metadata,
        "diagnostics": {
            "lattice_k_squared_over_mu2": lattice_k_squared,
            "mode_frequency_over_mu": omega,
            "mode_frequency_derivative": omega_prime,
            "velocity_shift": velocity_shift,
            "adiabaticity_parameter": adiabaticity,
        },
    }


def run_lattice_waterfall(
    params: PTUMParameters,
    *,
    Phi_initial: float,
    Phi_dot_initial: float,
    psi_initial: Iterable[float] | np.ndarray,
    psi_dot_initial: Iterable[float] | np.ndarray,
    box_size_over_mu: float,
    tau_span: tuple[float, float],
    n_output_points: int = 101,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-11,
    max_rhs_evaluations: int | None = 200_000,
    initial_state_metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    """Evolve a periodic cubic 3-D classical psi lattice with FRW backreaction.

    The dimensionless variables are
      tau = mu*t, x = Phi/Phi_c, u = d x/d tau,
      s = psi/psi_0, v = d s/d tau, h = H/mu,
    where psi_0=mu/sqrt(lambda_psi). The comoving box length is
    box_size_over_mu and the initial scale factor is a=1.

    The fuel equation contains the spatially averaged force
      (m_psi^2 alpha/(lambda_psi E_th^2)) x <s^2>,
    while the psi equation contains the full local nonlinear term s^3 and
    the periodic lattice Laplacian. The Friedmann source includes the
    volume-averaged kinetic, gradient, mass and quartic energies. This is
    a classical nonlinear truncation, not a renormalized quantum simulation.
    """
    mu = float(params.mu)
    psi0 = float(params.psi_0)
    phi_scale = float(params.Phi_c)
    if (not np.isfinite(mu) or mu <= 0.0 or not np.isfinite(psi0)
            or psi0 <= 0.0 or not np.isfinite(phi_scale) or phi_scale <= 0.0):
        raise ValueError("PTUM mass and field scales must be finite and positive")
    if (not np.isfinite(params.lambda_psi) or params.lambda_psi <= 0.0
            or not np.isfinite(params.E_th) or params.E_th <= 0.0
            or not np.isfinite(params.V0) or params.V0 <= 0.0):
        raise ValueError("quartic coupling, threshold and V0 must be positive")

    psi0_field = np.asarray(psi_initial, dtype=float)
    psi0_velocity = np.asarray(psi_dot_initial, dtype=float)
    if (psi0_field.ndim != 3 or min(psi0_field.shape) < 4
            or psi0_velocity.shape != psi0_field.shape):
        raise ValueError("psi initial data must be matching cubic 3-D arrays, N>=4")
    if not np.all(np.isfinite(psi0_field)) or not np.all(np.isfinite(psi0_velocity)):
        raise ValueError("psi initial data must be finite")
    if len(set(psi0_field.shape)) != 1:
        raise ValueError("the periodic lattice must be cubic")
    if not np.isfinite(Phi_initial) or not np.isfinite(Phi_dot_initial):
        raise ValueError("initial Phi and Phi_dot must be finite")

    box_length = float(box_size_over_mu)
    if not np.isfinite(box_length) or box_length <= 0.0:
        raise ValueError("box_size_over_mu must be finite and positive")
    span = tuple(float(value) for value in tau_span)
    if len(span) != 2 or not np.all(np.isfinite(span)) or span[1] <= span[0]:
        raise ValueError("tau_span must contain two finite increasing values")
    if (isinstance(n_output_points, (bool, np.bool_))
            or int(n_output_points) != n_output_points or n_output_points < 3):
        raise ValueError("n_output_points must be an integer >= 3")
    if not np.isfinite(rtol) or rtol <= 0.0 or not np.isfinite(atol) or atol <= 0.0:
        raise ValueError("solver tolerances must be finite and positive")
    if max_rhs_evaluations is not None and (
        isinstance(max_rhs_evaluations, (bool, np.bool_))
        or int(max_rhs_evaluations) != max_rhs_evaluations
        or max_rhs_evaluations < 1
    ):
        raise ValueError("max_rhs_evaluations must be a positive integer or None")

    grid_size = psi0_field.shape[0]
    dx = box_length / grid_size
    cell_count = psi0_field.size
    seed_metadata = None
    if initial_state_metadata is not None:
        if not isinstance(initial_state_metadata, dict):
            raise ValueError("initial_state_metadata must be a dictionary")
        if initial_state_metadata.get("kind") != (
            "bare_first_order_adiabatic_wkb_gaussian_classical_sample"
        ):
            raise ValueError("unsupported initial-state provenance metadata")
        if initial_state_metadata.get("grid_shape") != list(psi0_field.shape):
            raise ValueError("initial-state metadata grid shape does not match fields")
        if not np.isclose(
            float(initial_state_metadata.get("box_size_over_mu", np.nan)),
            box_length, rtol=1.0e-14, atol=0.0
        ):
            raise ValueError("initial-state metadata box size does not match fields")
        if initial_state_metadata.get("all_modes_stable") is not True or (
            initial_state_metadata.get("all_modes_adiabatic") is not True
        ):
            raise ValueError("initial-state metadata does not establish stable adiabatic modes")
        if initial_state_metadata.get("vacuum_renormalized") is not False or (
            initial_state_metadata.get("vacuum_subtraction_applied") is not False
        ) or initial_state_metadata.get("full_quantum_evolution") is not False:
            raise ValueError("bare Gaussian samples cannot claim renormalized quantum evolution")
        if initial_state_metadata.get("initial_hubble_self_consistent_with_lattice") is not False or (
            initial_state_metadata.get("subsequent_lattice_includes_bare_psi_energy") is not True
        ):
            raise ValueError("bare test-field initial state must disclose its Hubble mismatch")
        if initial_state_metadata.get("psi_initial_sha256") != _array_sha256(psi0_field):
            raise ValueError("initial-state metadata psi field hash does not match")
        if initial_state_metadata.get("psi_dot_initial_sha256") != _array_sha256(psi0_velocity):
            raise ValueError("initial-state metadata psi velocity hash does not match")
        seed_metadata = dict(initial_state_metadata)
    rho_scale = mu**2 * psi0**2
    fuel_kinetic_coefficient = (phi_scale / psi0) ** 2
    phi_psi_force_coefficient = (
        params.m_psi**2 * params.alpha
        / (params.lambda_psi * params.E_th**2)
    )
    hubble_prefactor = psi0 / (np.sqrt(3.0) * M_PL)

    if not np.isfinite(rho_scale) or rho_scale <= 0.0:
        raise ValueError("the lattice energy scale is not finite and positive")

    def unpack(state: np.ndarray):
        x = float(state[0])
        u = float(state[1])
        field = state[2:2 + cell_count].reshape(psi0_field.shape)
        velocity = state[2 + cell_count:2 + 2 * cell_count].reshape(psi0_field.shape)
        log_a = float(state[-1])
        return x, u, field, velocity, log_a

    def energy_pressure(
        x: float,
        u: float,
        field: np.ndarray,
        velocity: np.ndarray,
        log_a: float,
    ) -> tuple[float, float, float, float]:
        scale_factor = float(np.exp(log_a))
        eta = float(meff_sq_psi(phi_scale * x, params) / mu**2)
        _, gradient_norm_squared = periodic_laplacian_and_gradient_energy(field, dx)
        gradient_mean = float(np.mean(gradient_norm_squared))
        potential_phi = float(veff_phi(phi_scale * x, params) / rho_scale)
        rho_phi_norm = 0.5 * fuel_kinetic_coefficient * u**2 + potential_phi
        rho_psi_norm = float(np.mean(
            0.5 * velocity**2
            + 0.5 * gradient_norm_squared / scale_factor**2
            + 0.5 * eta * field**2
            + 0.25 * field**4
        ))
        pressure_phi_norm = 0.5 * fuel_kinetic_coefficient * u**2 - potential_phi
        pressure_psi_norm = float(np.mean(
            0.5 * velocity**2
            - gradient_norm_squared / (6.0 * scale_factor**2)
            - 0.5 * eta * field**2
            - 0.25 * field**4
        ))
        rho_norm = rho_phi_norm + rho_psi_norm
        pressure_norm = pressure_phi_norm + pressure_psi_norm
        return rho_norm, pressure_norm, gradient_mean, eta

    field_initial = psi0_field / psi0
    velocity_initial = psi0_velocity / (mu * psi0)
    initial_state = np.concatenate((
        np.asarray([Phi_initial / phi_scale,
                    Phi_dot_initial / (mu * phi_scale)]),
        field_initial.ravel(),
        velocity_initial.ravel(),
        np.asarray([0.0]),
    ))
    tau_eval = np.linspace(span[0], span[1], int(n_output_points))
    rhs_evaluations = 0

    def rhs(_tau: float, state: np.ndarray) -> np.ndarray:
        nonlocal rhs_evaluations
        rhs_evaluations += 1
        if max_rhs_evaluations is not None and rhs_evaluations > max_rhs_evaluations:
            raise RuntimeError(
                f"lattice RHS evaluation budget exceeded: {max_rhs_evaluations}"
            )
        x, u, field, velocity, log_a = unpack(state)
        rho_norm, _pressure_norm, _gradient_mean, _eta = energy_pressure(
            x, u, field, velocity, log_a
        )
        if not np.isfinite(rho_norm) or rho_norm <= 0.0:
            raise ValueError("lattice evolution reached non-positive total energy")
        hubble_over_mu = hubble_prefactor * np.sqrt(rho_norm)
        scale_factor = float(np.exp(log_a))
        laplacian, _gradient_norm_squared = periodic_laplacian_and_gradient_energy(
            field, dx
        )
        phi = phi_scale * x
        phi_acceleration = (
            -3.0 * hubble_over_mu * u
            - float(dveff_dphi(phi, params)) / (mu**2 * phi_scale)
            - phi_psi_force_coefficient * x * float(np.mean(field**2))
        )
        eta = float(meff_sq_psi(phi, params) / mu**2)
        field_acceleration = (
            laplacian / scale_factor**2
            - 3.0 * hubble_over_mu * velocity
            - eta * field
            - field**3
        )
        return np.concatenate((
            np.asarray([u, phi_acceleration]),
            velocity.ravel(),
            field_acceleration.ravel(),
            np.asarray([hubble_over_mu]),
        ))

    solution = solve_ivp(
        rhs,
        span,
        initial_state,
        t_eval=tau_eval,
        method="DOP853",
        rtol=rtol,
        atol=atol,
    )
    if not solution.success or solution.y.shape[1] != len(tau_eval):
        raise RuntimeError(f"lattice integration failed: {solution.message}")

    n_times = len(tau_eval)
    x_history = solution.y[0]
    u_history = solution.y[1]
    field_history = solution.y[2:2 + cell_count].T.reshape(
        (n_times,) + psi0_field.shape
    )
    velocity_history = solution.y[2 + cell_count:2 + 2 * cell_count].T.reshape(
        (n_times,) + psi0_field.shape
    )
    log_a_history = solution.y[-1]
    scale_factor_history = np.exp(log_a_history)

    rho_history = np.empty(n_times)
    pressure_history = np.empty(n_times)
    gradient_history = np.empty(n_times)
    hubble_history = np.empty(n_times)
    wall_area_history = np.empty(n_times)
    psi_mean_history = np.empty(n_times)
    psi_rms_history = np.empty(n_times)
    psi_variance_history = np.empty(n_times)
    rhs_balance_relative_history = np.empty(n_times)

    for index in range(n_times):
        field = field_history[index]
        velocity = velocity_history[index]
        x_now = float(x_history[index])
        u_now = float(u_history[index])
        log_a_now = float(log_a_history[index])
        rho_norm, pressure_norm, gradient_mean, eta = energy_pressure(
            x_now, u_now, field, velocity, log_a_now
        )
        if not np.isfinite(rho_norm) or rho_norm <= 0.0:
            raise ValueError("non-positive lattice energy in output history")

        scale_factor_now = float(scale_factor_history[index])
        hubble_over_mu_now = hubble_prefactor * np.sqrt(rho_norm)
        phi_now = phi_scale * x_now
        laplacian, _gradient_norm_squared = periodic_laplacian_and_gradient_energy(
            field, dx
        )
        phi_acceleration = (
            -3.0 * hubble_over_mu_now * u_now
            - float(dveff_dphi(phi_now, params)) / (mu**2 * phi_scale)
            - phi_psi_force_coefficient * x_now * float(np.mean(field**2))
        )
        field_acceleration = (
            laplacian / scale_factor_now**2
            - 3.0 * hubble_over_mu_now * velocity
            - eta * field
            - field**3
        )
        eta_x = (
            2.0 * params.m_psi**2 * params.alpha * phi_scale**2 * x_now
            / (mu**2 * params.E_th**2)
        )
        gradient_dot = 0.0
        for axis in range(3):
            grad_field = np.roll(field, -1, axis=axis) - field
            grad_velocity = np.roll(velocity, -1, axis=axis) - velocity
            gradient_dot += float(np.mean(grad_field * grad_velocity) / dx**2)
        potential_derivative_norm = (
            float(dveff_dphi(phi_now, params)) * phi_scale / rho_scale
        )
        rho_derivative_norm = (
            fuel_kinetic_coefficient * u_now * phi_acceleration
            + potential_derivative_norm * u_now
            + float(np.mean(velocity * field_acceleration))
            + gradient_dot / scale_factor_now**2
            - hubble_over_mu_now * gradient_mean / scale_factor_now**2
            + 0.5 * eta_x * u_now * float(np.mean(field**2))
            + eta * float(np.mean(field * velocity))
            + float(np.mean(field**3 * velocity))
        )
        rhs_balance_residual = (
            rho_derivative_norm
            + 3.0 * hubble_over_mu_now * (rho_norm + pressure_norm)
        )
        rhs_balance_relative_history[index] = (
            abs(rhs_balance_residual)
            / max(abs(rho_norm), np.finfo(float).tiny)
        )

        rho_history[index] = rho_norm * rho_scale
        pressure_history[index] = pressure_norm * rho_scale
        gradient_history[index] = (
            0.5 * rho_scale * gradient_mean / scale_factor_now**2
        )
        hubble_history[index] = mu * hubble_over_mu_now
        wall_area_history[index] = _wall_area_density_over_mu(
            field, dx, scale_factor_now
        )
        physical_field = psi0 * field
        psi_mean_history[index] = float(np.mean(physical_field))
        psi_rms_history[index] = float(np.sqrt(np.mean(physical_field**2)))
        psi_variance_history[index] = float(np.var(physical_field))

    rho_norm_history = rho_history / rho_scale
    pressure_norm_history = pressure_history / rho_scale
    hubble_over_mu_history = hubble_history / mu
    continuity_residual = (
        np.gradient(rho_norm_history, tau_eval, edge_order=2)
        + 3.0 * hubble_over_mu_history
        * (rho_norm_history + pressure_norm_history)
    )
    continuity_relative = np.abs(continuity_residual) / np.maximum(
        np.abs(rho_norm_history), np.finfo(float).tiny
    )

    return {
        "success": True,
        "method": "periodic_3d_classical_scalar_lattice",
        "tau": tau_eval,
        "scale_factor": scale_factor_history,
        "Phi": phi_scale * x_history,
        "Phi_dot": mu * phi_scale * u_history,
        "psi": psi0 * field_history,
        "psi_dot": mu * psi0 * velocity_history,
        "H": hubble_history,
        "H_over_mu": hubble_over_mu_history,
        "rho_total": rho_history,
        "pressure_total": pressure_history,
        "psi_gradient_energy_density": gradient_history,
        "psi_mean": psi_mean_history,
        "psi_rms": psi_rms_history,
        "psi_variance": psi_variance_history,
        "wall_area_density_over_mu": wall_area_history,
        "continuity_residual_relative": continuity_relative,
        "max_abs_continuity_residual_relative": float(
            np.max(continuity_relative)
        ),
        "rhs_energy_balance_residual_relative": rhs_balance_relative_history,
        "max_abs_rhs_energy_balance_residual_relative": float(
            np.max(rhs_balance_relative_history)
        ),
        "grid_shape": list(psi0_field.shape),
        "box_size_over_mu": box_length,
        "dx_over_mu_inverse": dx,
        "rhs_evaluations": rhs_evaluations,
        "rtol": float(rtol),
        "atol": float(atol),
        "backreaction_included": True,
        "nonlinear_mode_coupling_included": True,
        "classical_rescattering_included": True,
        "quantum_vacuum_seeded": False,
        "bare_adiabatic_vacuum_sampled": seed_metadata is not None,
        "bare_zero_point_energy_present": (
            True if seed_metadata is not None else None
        ),
        "vacuum_renormalized": False,
        "continuum_limit_demonstrated": False,
        "sm_sector_included": False,
        "initial_seed_interpretation": (
            "bare_first_order_adiabatic_wkb_gaussian_classical_statistical_sample"
            if seed_metadata is not None else "caller_supplied_classical_field"
        ),
        "initial_state_metadata": seed_metadata,
        "initial_sampler_H_over_mu": (
            float(seed_metadata["H_background_over_mu"])
            if seed_metadata is not None else None
        ),
        "initial_lattice_H_over_mu": float(hubble_over_mu_history[0]),
        "initial_H_relative_mismatch_vs_sampler_background": (
            float(
                (hubble_over_mu_history[0] - float(seed_metadata["H_background_over_mu"]))
                / float(seed_metadata["H_background_over_mu"])
            )
            if seed_metadata is not None else None
        ),
        "initial_hubble_self_consistent_with_lattice": (
            False if seed_metadata is not None else None
        ),
        "subsequent_lattice_includes_bare_psi_energy": (
            True if seed_metadata is not None else None
        ),
    }
