"""Conversions between Delta N_eff and radiation energy fractions.

All ratios use rho_nu = (7/8)(4/11)^(4/3) N_eff rho_gamma.
"""
from __future__ import annotations

import math


C_NU = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)


def radiation_fractions(
    delta_neff: float,
    n_eff_standard: float = 3.044,
) -> dict[str, float]:
    """Return unambiguous radiation fractions for an extra fluid species.

    extra_over_standard_neutrino_equivalent is rho_extra/rho_nu,std.
    extra_over_standard_radiation is rho_extra/(rho_gamma+rho_nu,std).
    extra_fraction_including_itself divides by total radiation including
    the extra component itself.
    """
    delta = float(delta_neff)
    n_eff = float(n_eff_standard)
    if not math.isfinite(delta) or delta < 0.0:
        raise ValueError("delta_neff must be finite and non-negative")
    if not math.isfinite(n_eff) or n_eff <= 0.0:
        raise ValueError("n_eff_standard must be finite and positive")

    extra_over_standard_neutrino = delta / n_eff
    extra_over_standard_radiation = C_NU * delta / (1.0 + C_NU * n_eff)
    extra_fraction_total = C_NU * delta / (1.0 + C_NU * (n_eff + delta))
    return {
        "extra_over_standard_neutrino_equivalent": extra_over_standard_neutrino,
        "extra_over_standard_radiation": extra_over_standard_radiation,
        "extra_fraction_including_itself": extra_fraction_total,
    }
