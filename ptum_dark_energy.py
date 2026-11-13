"""Dimensionally consistent residual dark-energy potential and derivatives."""
from __future__ import annotations

import math

M_PL_GEV = 2.435e18


def _validate(phi, W0, kappa, lambda_res, Lambda_np4, S_E, f_res):
    values = (phi, W0, kappa, lambda_res, Lambda_np4, S_E, f_res)
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("All residual-potential inputs must be finite")
    if W0 < 0.0 or kappa < 0.0 or lambda_res < 0.0 or Lambda_np4 < 0.0:
        raise ValueError("Potential scales and shape parameters must be non-negative")
    if f_res <= 0.0:
        raise ValueError("f_res must be positive")


def residual_potential(phi, W0, kappa, lambda_res, Lambda_np4=0.0, S_E=0.0, f_res=M_PL_GEV):
    """Evaluate W(phi) with dimensionless Planck-normalized exponentials.

    W0 and Lambda_np4 are in GeV^4; phi, f_res and M_PL_GEV are in GeV;
    kappa, lambda_res and S_E are dimensionless.
    """
    _validate(phi, W0, kappa, lambda_res, Lambda_np4, S_E, f_res)
    x = float(phi) / M_PL_GEV
    envelope = math.exp(-kappa * x * x) - math.exp(-(kappa + lambda_res) * x * x)
    instanton = Lambda_np4 * math.exp(-S_E) * math.cos(float(phi) / f_res)
    return W0 * envelope + instanton


def residual_potential_prime(phi, W0, kappa, lambda_res, Lambda_np4=0.0, S_E=0.0, f_res=M_PL_GEV):
    """First derivative dW/dphi in GeV^3."""
    _validate(phi, W0, kappa, lambda_res, Lambda_np4, S_E, f_res)
    x = float(phi) / M_PL_GEV
    envelope_prime = (2.0 * float(phi) / M_PL_GEV**2) * (
        (kappa + lambda_res) * math.exp(-(kappa + lambda_res) * x * x)
        - kappa * math.exp(-kappa * x * x)
    )
    instanton_prime = -Lambda_np4 * math.exp(-S_E) * math.sin(float(phi) / f_res) / f_res
    return W0 * envelope_prime + instanton_prime


def residual_potential_second(phi, W0, kappa, lambda_res, Lambda_np4=0.0, S_E=0.0, f_res=M_PL_GEV):
    """Second derivative d2W/dphi2 in GeV^2."""
    _validate(phi, W0, kappa, lambda_res, Lambda_np4, S_E, f_res)
    x = float(phi) / M_PL_GEV
    kp = kappa + lambda_res
    envelope_second = (2.0 / M_PL_GEV**2) * (
        kp * math.exp(-kp * x * x) * (1.0 - 2.0 * kp * x * x)
        - kappa * math.exp(-kappa * x * x) * (1.0 - 2.0 * kappa * x * x)
    )
    instanton_second = -Lambda_np4 * math.exp(-S_E) * math.cos(float(phi) / f_res) / f_res**2
    return W0 * envelope_second + instanton_second
