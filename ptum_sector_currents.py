"""Action-derived sector-transfer currents for the specified classical PTUM EFT.

Convention: metric signature (-+++). Every gradient argument is a contravariant
spacetime gradient, e.g. grad_Phi[0] = nabla^0 Phi = -dot(Phi) in homogeneous
FRW coordinates.

The interaction assignment follows the Hilbert-tensor split in main.tex:
  U_Phi_psi = alpha*m_psi^2*Phi^2*psi^2/(2*E_th^2) is assigned to T_psi;
  U_psi_H = g_psiH*psi^2*H^dagger H/2 is assigned to T_psi;
  U_Y = psi*O_SM/Lambda is assigned to T_SM;
  U_chi_r = g_DM*chi^2*Phi_res^2 is assigned to T_DM.

For an interaction U assigned to one sector, the on-shell divergence of a
different sector contains + (partial U / partial field) nabla^nu(field);
the owner sector receives the negative sum of those contributions. This
gives pairwise cancellation without assuming homogeneous fields.

This module evaluates the resulting currents. It is an algebraic audit layer,
not a field solver and not an independent derivation of the full SM Hilbert
tensor. The Higgs input is the gauge-invariant gradient nabla^nu(H^dagger H),
which equals H^dagger D^nu H + (D^nu H)^dagger H.
"""

from __future__ import annotations

import numpy as np


def _spacetime_gradient(value: object, name: str) -> np.ndarray:
    gradient = np.asarray(value, dtype=float)
    if gradient.shape != (4,):
        raise ValueError(f"{name} must be a contravariant four-vector")
    if not np.all(np.isfinite(gradient)):
        raise ValueError(f"{name} must contain only finite values")
    return gradient


def action_derived_sector_currents(
    *,
    Phi: float,
    psi: float,
    grad_Phi: object,
    grad_psi: object,
    grad_HdaggerH: object,
    chi: float,
    Phi_res: float,
    grad_Phi_res: object,
    O_SM: float,
    alpha: float,
    m_psi: float,
    E_th: float,
    g_psiH: float,
    g_DM: float,
    Lambda: float,
) -> dict[str, np.ndarray]:
    """Evaluate Q_i^nu from the declared interaction assignments.

    The returned sectors are Phi, psi, SM, DM and DE. The Higgs and fermions
    belong to the SM sector. Every returned value has mass dimension five
    when fields and gradients carry their canonical four-dimensional units.
    """
    scalar_values = {
        "Phi": Phi,
        "psi": psi,
        "chi": chi,
        "Phi_res": Phi_res,
        "O_SM": O_SM,
        "alpha": alpha,
        "m_psi": m_psi,
        "E_th": E_th,
        "g_psiH": g_psiH,
        "g_DM": g_DM,
        "Lambda": Lambda,
    }
    for name, value in scalar_values.items():
        if not np.isfinite(float(value)):
            raise ValueError(f"{name} must be finite")
    if float(E_th) <= 0.0 or float(Lambda) <= 0.0:
        raise ValueError("E_th and Lambda must be strictly positive")
    if float(alpha) < 0.0 or float(m_psi) < 0.0:
        raise ValueError("alpha and m_psi must be non-negative")

    grad_phi = _spacetime_gradient(grad_Phi, "grad_Phi")
    grad_psi_arr = _spacetime_gradient(grad_psi, "grad_psi")
    grad_higgs_norm = _spacetime_gradient(
        grad_HdaggerH, "grad_HdaggerH"
    )
    grad_phi_res = _spacetime_gradient(grad_Phi_res, "grad_Phi_res")

    # U_Phi_psi = alpha*m_psi^2*Phi^2*psi^2/(2*E_th^2),
    # assigned to T_psi.
    dU_dPhi = (
        float(alpha) * float(m_psi) ** 2 / float(E_th) ** 2
        * float(Phi) * float(psi) ** 2
    )
    q_phi_psi = dU_dPhi * grad_phi

    # U_psi_H = g_psiH*psi^2*(H^dagger H)/2, assigned to T_psi.
    # The gauge-invariant Higgs contraction is nabla^nu(H^dagger H).
    q_higgs = (
        0.5 * float(g_psiH) * float(psi) ** 2 * grad_higgs_norm
    )

    # U_Y = psi*O_SM/Lambda, assigned to T_SM.
    dU_Y_dpsi = float(O_SM) / float(Lambda)
    q_yukawa = dU_Y_dpsi * grad_psi_arr

    # U_chi_r = g_DM*chi^2*Phi_res^2, assigned to T_DM.
    dU_dPhi_res = (
        2.0 * float(g_DM) * float(chi) ** 2 * float(Phi_res)
    )
    q_dark_energy = dU_dPhi_res * grad_phi_res

    return {
        "Phi": q_phi_psi.copy(),
        "psi": (-q_phi_psi - q_higgs + q_yukawa).copy(),
        "SM": (q_higgs - q_yukawa).copy(),
        "DM": (-q_dark_energy).copy(),
        "DE": q_dark_energy.copy(),
    }


__all__ = ["action_derived_sector_currents"]
