#!/usr/bin/env python3
"""Nonlinear 3-D classical lattice evolution of the real PTUM waterfall field.

This is a periodic finite-difference classical-field solver. It evolves a
homogeneous fuel field Phi, a real inhomogeneous psi(x), and the scale factor
self-consistently. Spatial gradients, the quartic interaction, the Phi-psi
force, and the Friedmann source are all included. Nonlinear mode coupling
therefore permits classical rescattering and Z2 wall formation for supplied
classical initial fields.

Scientific boundary:
- Initial psi(x) and psi_dot(x) are supplied by the caller. They are not
  generated from a quantum adiabatic vacuum.
- No vacuum counterterms or continuum renormalization are implemented.
- Results are finite-volume, finite-lattice classical results. They must not
  be interpreted as quantum-seeded waterfall predictions or relic abundances.
- A lattice/volume/time-step convergence study and a renormalized quantum
  initial-state prescription are required before physical claims.

Natural units are used. The comoving coordinates are measured in mu^{-1},
where mu=params.mu, and tau=mu*t. The scale factor is initialized to one.
"""
from __future__ import annotations

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
        nonzero = (field != 0.0) & (neighbour != 0.0)
        crossings += int(np.count_nonzero(
            nonzero & (np.signbit(field) != np.signbit(neighbour))
        ))
    return float(crossings / (field.size * dx * scale_factor))


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

    for index in range(n_times):
        field = field_history[index]
        velocity = velocity_history[index]
        rho_norm, pressure_norm, gradient_mean, _eta = energy_pressure(
            float(x_history[index]),
            float(u_history[index]),
            field,
            velocity,
            float(log_a_history[index]),
        )
        if not np.isfinite(rho_norm) or rho_norm <= 0.0:
            raise ValueError("non-positive lattice energy in output history")
        rho_history[index] = rho_norm * rho_scale
        pressure_history[index] = pressure_norm * rho_scale
        gradient_history[index] = (
            0.5 * rho_scale * gradient_mean / scale_factor_history[index]**2
        )
        hubble_history[index] = mu * hubble_prefactor * np.sqrt(rho_norm)
        wall_area_history[index] = _wall_area_density_over_mu(
            field, dx, float(scale_factor_history[index])
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
        "vacuum_renormalized": False,
        "continuum_limit_demonstrated": False,
        "sm_sector_included": False,
        "initial_seed_interpretation": "caller_supplied_classical_field",
    }
