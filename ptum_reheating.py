#!/usr/bin/env python3
"""Conditional perturbative reheating widths for the PTUM dimension-five EFT.

The unbroken-phase result is for one massless chiral three-body channel
from L_int = -(C/Lambda) psi (bar f_L H f_R) + h.c.  The channel
multiplicity must explicitly count distinct colour, weak, flavour and
charge-conjugate final states.  It must not count coherent amplitudes as
independent channels.

The broken-phase result is the vacuum two-body width for a real scalar
quasiparticle coupled to one Dirac fermion by
-psi bar(f) (y_S + i y_P gamma5) f.

Neither function evolves a condensate, computes thermal blocking/enhancement,
includes the Higgs-portal pair processes, or replaces a coupled Boltzmann
and lattice calculation.  All masses, cutoffs, widths and temperatures
are in GeV (natural units).
"""
from __future__ import annotations

from math import pi, sqrt
from typing import Iterable, Mapping

REDUCED_PLANCK_MASS_GEV = 2.435e18
DEFAULT_BBN_TEMPERATURE_GEV = 5.0e-3
DEFAULT_ELECTROWEAK_CROSSOVER_GEV = 160.0


def _finite_real(name: str, value: object) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not result == result or result in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be a finite real number")
    return result


def _positive(name: str, value: object) -> float:
    result = _finite_real(name, value)
    if result <= 0.0:
        raise ValueError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: object) -> float:
    result = _finite_real(name, value)
    if result < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return result


def _positive_integer(name: str, value: object) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a positive integer")
    try:
        integer = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if integer != value or integer < 1:
        raise ValueError(f"{name} must be a positive integer")
    return integer


def _finite_complex(name: str, value: object) -> complex:
    try:
        result = complex(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite complex number") from exc
    if (not (result.real == result.real and result.imag == result.imag)
            or result.real in (float("inf"), float("-inf"))
            or result.imag in (float("inf"), float("-inf"))):
        raise ValueError(f"{name} must be a finite complex number")
    return result


def chiral_dimension_five_three_body_width(
    mediator_mass: float,
    wilson_coefficient: complex,
    cutoff: float,
    *,
    channel_multiplicity: int,
) -> float:
    r"""Vacuum width for massless chiral f, anti-f and Higgs final states.

    For one distinguishable chiral channel,
        |M|^2 = |C|^2 s / Lambda^2,
        d Phi_3 / ds = (M^2-s)/(128 pi^3 M^2),
    where s=(p_f+p_antif)^2 and 0<=s<=M^2.  Thus
        Gamma_1 = |C|^2 M^3/(1536 pi^3 Lambda^2).
    The explicit multiplicity counts orthogonal final-state channels,
    including the h.c. channel when it is physically distinct.
    """
    mass = _positive("mediator_mass", mediator_mass)
    coefficient = _finite_complex("wilson_coefficient", wilson_coefficient)
    scale = _positive("cutoff", cutoff)
    multiplicity = _positive_integer("channel_multiplicity", channel_multiplicity)
    if mass >= scale:
        raise ValueError("mediator_mass must lie below the EFT cutoff")
    return float(
        multiplicity * abs(coefficient) ** 2 * mass**3
        / (1536.0 * pi**3 * scale**2)
    )


def broken_phase_dirac_pair_width(
    mediator_mass: float,
    fermion_mass: float,
    scalar_coupling: float,
    pseudoscalar_coupling: float = 0.0,
    *,
    color_multiplicity: int = 1,
) -> float:
    r"""Vacuum width for psi -> f fbar in the broken electroweak phase.

    For L_int=-psi bar(f)(y_S+i y_P gamma5)f, the spin-summed scalar and
    pseudoscalar pieces do not interfere:
        Gamma = N_c M/(8 pi) [y_S^2 beta^3 + y_P^2 beta],
        beta = sqrt(1-4 m_f^2/M^2).
    The result is zero at and below threshold.  Couplings are real.
    """
    mass = _positive("mediator_mass", mediator_mass)
    fermion = _nonnegative("fermion_mass", fermion_mass)
    scalar = _finite_real("scalar_coupling", scalar_coupling)
    pseudoscalar = _finite_real("pseudoscalar_coupling", pseudoscalar_coupling)
    colors = _positive_integer("color_multiplicity", color_multiplicity)
    if mass <= 2.0 * fermion:
        return 0.0
    beta = sqrt(max(0.0, 1.0 - 4.0 * fermion**2 / mass**2))
    return float(
        colors * mass / (8.0 * pi)
        * (scalar**2 * beta**3 + pseudoscalar**2 * beta)
    )


def reheating_temperature_from_width(
    total_width: float,
    g_star: float,
    *,
    reduced_planck_mass: float = REDUCED_PLANCK_MASS_GEV,
) -> float:
    r"""Sudden-decay estimate T_RH=(90/(pi^2 g_*))^(1/4) sqrt(Mbar_Pl Gamma)."""
    width = _positive("total_width", total_width)
    degrees = _positive("g_star", g_star)
    planck = _positive("reduced_planck_mass", reduced_planck_mass)
    return float((90.0 / (pi**2 * degrees)) ** 0.25 * sqrt(planck * width))


def build_unbroken_phase_reheating_report(
    mediator_mass: float,
    channels: Iterable[Mapping[str, object]],
    *,
    g_star: float,
    minimum_bbn_temperature: float = DEFAULT_BBN_TEMPERATURE_GEV,
    electroweak_crossover_temperature: float = DEFAULT_ELECTROWEAK_CROSSOVER_GEV,
    reduced_planck_mass: float = REDUCED_PLANCK_MASS_GEV,
) -> dict[str, object]:
    """Build a transparent channel sum and conditional sudden-decay estimate.

    Each channel mapping must provide:
      name, wilson_coefficient, cutoff, channel_multiplicity.
    Channels are assumed orthogonal.  If two terms lead to the same final
    state, their amplitudes must be combined before calling this function.
    """
    mass = _positive("mediator_mass", mediator_mass)
    degrees = _positive("g_star", g_star)
    bbn_temperature = _positive("minimum_bbn_temperature", minimum_bbn_temperature)
    ew_temperature = _positive(
        "electroweak_crossover_temperature", electroweak_crossover_temperature
    )
    planck = _positive("reduced_planck_mass", reduced_planck_mass)
    entries = list(channels)
    if not entries:
        raise ValueError("at least one unbroken-phase decay channel is required")

    rows: list[dict[str, object]] = []
    total_width = 0.0
    for index, item in enumerate(entries):
        if not isinstance(item, Mapping):
            raise ValueError("each channel must be a mapping")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("each channel requires a non-empty name")
        cutoff = _positive("channel cutoff", item.get("cutoff"))
        coefficient = _finite_complex(
            "channel wilson_coefficient", item.get("wilson_coefficient")
        )
        multiplicity = _positive_integer(
            "channel channel_multiplicity", item.get("channel_multiplicity")
        )
        width = chiral_dimension_five_three_body_width(
            mass, coefficient, cutoff, channel_multiplicity=multiplicity
        )
        total_width += width
        rows.append({
            "index": index,
            "name": name,
            "wilson_coefficient_abs": float(abs(coefficient)),
            "cutoff_GeV": cutoff,
            "mediator_to_cutoff_ratio": mass / cutoff,
            "channel_multiplicity": multiplicity,
            "partial_width_GeV": width,
        })

    if total_width > 0.0:
        temperature = reheating_temperature_from_width(
            total_width, degrees, reduced_planck_mass=planck
        )
        for row in rows:
            row["branching_fraction"] = float(row["partial_width_GeV"] / total_width)
        bbn_compatible = bool(temperature >= bbn_temperature)
        above_ew = bool(temperature >= ew_temperature)
        below_cutoff = bool(all(
            temperature < float(row["cutoff_GeV"]) for row in rows
        ))
    else:
        temperature = None
        for row in rows:
            row["branching_fraction"] = None
        bbn_compatible = None
        above_ew = None
        below_cutoff = None

    return {
        "schema": "ptum.conditional_unbroken_phase_reheating",
        "schema_version": 1,
        "phase": "electroweak_symmetric_massless_final_state_approximation",
        "mediator_mass_GeV": mass,
        "g_star": degrees,
        "reduced_planck_mass_GeV": planck,
        "channels": rows,
        "total_width_GeV": float(total_width),
        "width_over_mediator_mass": float(total_width / mass),
        "sudden_decay_reheating_temperature_GeV": temperature,
        "minimum_bbn_temperature_GeV": bbn_temperature,
        "bbn_temperature_test_passes_under_sudden_decay_assumption": bbn_compatible,
        "electroweak_symmetric_approximation_consistent_with_T_RH": above_ew,
        "reheating_temperature_below_all_channel_cutoffs": below_cutoff,
        "assumptions": {
            "massless_final_states": True,
            "vacuum_matrix_elements": True,
            "thermal_blocking_and_enhancement": False,
            "condensate_depletion_and_boltzmann_evolution": False,
            "higgs_portal_pair_annihilation": False,
            "nonperturbative_preheating": False,
            "entropy_production_and_late_injection": False,
            "orthogonal_channels_only": True,
            "sudden_decay_at_H_equals_Gamma": True,
        },
        "interpretation": (
            "Conditional perturbative estimate for the electroweak-symmetric "
            "dimension-five operator. It is not a coupled PTUM reheating history. "
            "A physical result additionally requires specified Wilson matrices, "
            "cutoffs, the time-dependent mediator spectrum, thermal corrections, "
            "condensate evolution, competing channels and entropy accounting."
        ),
    }
