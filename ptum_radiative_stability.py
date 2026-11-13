"""Radiative-stability diagnostic for the residual-field/DM quadratic portal.

Assumes one real scalar chi with m_chi^2(phi)=m_chi^2+2 g_DM phi^2.
The finite one-loop threshold is evaluated at mu_R=m_chi. This is an
order-of-magnitude naturalness diagnostic, not a scheme-independent
prediction: UV matching or a symmetry can alter/cancel the threshold.
"""
from __future__ import annotations

import math

H0_GEV_DEFAULT = 1.437e-42
MPL_GEV = 2.435e18


def residual_portal_radiative_stability(
    m_chi_gev: float,
    g_dm: float,
    phi_amplitude_gev: float = MPL_GEV,
    h0_gev: float = H0_GEV_DEFAULT,
) -> dict:
    """Return one-loop mass correction and resonance/naturalness tension.

    For V_1 = m_chi(phi)^4/(64 pi^2) * [ln(m_chi(phi)^2/mu_R^2)-3/2],
    with m_chi(phi)^2=m_chi^2+2 g_DM phi^2 and mu_R=m_chi,
    delta m_phi^2 = -g_DM m_chi^2/(8 pi^2).

    eta = g_DM A_phi^2/(m_chi^2 + g_DM A_phi^2) is the fractional
    modulation of the chi mass-squared at oscillation amplitude A_phi.
    eta is a modulation diagnostic, not a Floquet-band calculation.
    """
    vals = (m_chi_gev, g_dm, phi_amplitude_gev, h0_gev)
    if not all(math.isfinite(float(x)) for x in vals):
        raise ValueError("all inputs must be finite")
    if m_chi_gev <= 0.0 or phi_amplitude_gev <= 0.0 or h0_gev <= 0.0:
        raise ValueError("m_chi, phi_amplitude and H0 must be positive")
    if g_dm < 0.0:
        raise ValueError("g_DM must be non-negative for this benchmark diagnostic")

    m2 = m_chi_gev**2
    phi2 = phi_amplitude_gev**2
    delta_m2 = -g_dm * m2 / (8.0 * math.pi**2)
    delta_m = math.sqrt(abs(delta_m2))
    natural_g_max = 8.0 * math.pi**2 * (h0_gev / m_chi_gev)**2
    naturalness_ratio = abs(delta_m2) / h0_gev**2
    modulation_fraction = (g_dm * phi2) / (m2 + g_dm * phi2)
    natural_modulation_fraction = (natural_g_max * phi2) / (
        m2 + natural_g_max * phi2
    )

    def coupling_for_modulation(eta: float) -> float:
        if not 0.0 < eta < 1.0:
            raise ValueError("eta must lie strictly between zero and one")
        return (eta / (1.0 - eta)) * (m2 / phi2)

    g_for_eta_10 = coupling_for_modulation(0.10)
    g_for_eta_50 = coupling_for_modulation(0.50)
    return {
        "matching_scale_gev": m_chi_gev,
        "delta_m_phi_sq_gev2": delta_m2,
        "delta_m_phi_scale_gev": delta_m,
        "naturalness_g_dm_max": natural_g_max,
        "naturalness_ratio_to_H0_sq": naturalness_ratio,
        "modulation_fraction_at_input_g": modulation_fraction,
        "modulation_fraction_at_naturalness_bound": natural_modulation_fraction,
        "g_dm_for_10pct_mass_modulation": g_for_eta_10,
        "g_dm_for_50pct_mass_modulation": g_for_eta_50,
        "tension_factor_for_10pct_modulation": g_for_eta_10 / natural_g_max,
        "tension_factor_for_50pct_modulation": g_for_eta_50 / natural_g_max,
        "assumptions": {
            "chi_degrees_of_freedom": 1,
            "renormalization_scale": "mu_R = m_chi",
            "phi_amplitude_is_benchmark_not_bound": True,
            "not_a_floquet_calculation": True,
        },
    }
