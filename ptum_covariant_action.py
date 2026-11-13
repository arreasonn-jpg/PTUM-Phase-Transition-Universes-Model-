"""Machine-checkable field and operator registry for the classical PTUM+SM EFT.

This module validates representation and canonical-dimension bookkeeping only.
It does not evolve Standard Model fields, compute quantum corrections, or
replace the variational derivation in main.tex.
"""
from fractions import Fraction


SM_FIELD_REPRESENTATIONS = {
    "Q_L": {"su3": "3", "su2": "2", "hypercharge": Fraction(1, 6), "dimension": Fraction(3, 2)},
    "u_R": {"su3": "3", "su2": "1", "hypercharge": Fraction(2, 3), "dimension": Fraction(3, 2)},
    "d_R": {"su3": "3", "su2": "1", "hypercharge": Fraction(-1, 3), "dimension": Fraction(3, 2)},
    "L_L": {"su3": "1", "su2": "2", "hypercharge": Fraction(-1, 2), "dimension": Fraction(3, 2)},
    "e_R": {"su3": "1", "su2": "1", "hypercharge": Fraction(-1, 1), "dimension": Fraction(3, 2)},
    "H": {"su3": "1", "su2": "2", "hypercharge": Fraction(1, 2), "dimension": Fraction(1, 1)},
    "H_tilde": {"su3": "1", "su2": "2", "hypercharge": Fraction(-1, 2), "dimension": Fraction(1, 1)},
}

PTUM_SCALAR_REPRESENTATIONS = {
    name: {
        "su3": "1",
        "su2": "1",
        "hypercharge": Fraction(0, 1),
        "dimension": Fraction(1, 1),
        "reality": "real",
    }
    for name in ("Phi", "psi", "chi", "Phi_res")
}


def _conjugate_representation(rep):
    if rep == "3":
        return "3bar"
    if rep == "3bar":
        return "3"
    return rep


def _contains_singlet(group, rep_a, rep_b):
    """Whether the listed pair contains a singlet for the representations used."""
    if rep_a == "1" and rep_b == "1":
        return True
    if group == "su3":
        return {rep_a, rep_b} == {"3", "3bar"}
    if group == "su2":
        # The SU(2) doublet is pseudoreal: 2 x 2 contains an epsilon singlet.
        return rep_a == "2" and rep_b == "2"
    raise ValueError(f"Unsupported gauge group: {group}")


def yukawa_hypercharge_residuals():
    """Return total U(1)_Y charge for each gauge-invariant SM Yukawa monomial."""
    y = {name: rep["hypercharge"] for name, rep in SM_FIELD_REPRESENTATIONS.items()}
    return {
        "down": -y["Q_L"] + y["H"] + y["d_R"],
        "up": -y["Q_L"] + y["H_tilde"] + y["u_R"],
        "charged_lepton": -y["L_L"] + y["H"] + y["e_R"],
    }


def yukawa_nonabelian_singlet_checks():
    """Check colour and weak-isospin singlet contractions in the three operators."""
    definitions = {
        "down": ("Q_L", "H", "d_R"),
        "up": ("Q_L", "H_tilde", "u_R"),
        "charged_lepton": ("L_L", "H", "e_R"),
    }
    checks = {}
    for name, (left, higgs, right) in definitions.items():
        left_rep = SM_FIELD_REPRESENTATIONS[left]
        higgs_rep = SM_FIELD_REPRESENTATIONS[higgs]
        right_rep = SM_FIELD_REPRESENTATIONS[right]
        checks[name] = {
            "su3": _contains_singlet(
                "su3", _conjugate_representation(left_rep["su3"]), right_rep["su3"]
            ),
            "su2": _contains_singlet(
                "su2", _conjugate_representation(left_rep["su2"]), higgs_rep["su2"]
            ),
        }
    return checks


def operator_mass_dimensions():
    """Canonical mass dimensions of all interaction monomials in the specified EFT."""
    d = {name: rep["dimension"] for name, rep in SM_FIELD_REPRESENTATIONS.items()}
    d.update({name: rep["dimension"] for name, rep in PTUM_SCALAR_REPRESENTATIONS.items()})
    return {
        "ordinary_down_yukawa": d["Q_L"] + d["H"] + d["d_R"],
        "ordinary_up_yukawa": d["Q_L"] + d["H_tilde"] + d["u_R"],
        "ordinary_charged_lepton_yukawa": d["L_L"] + d["H"] + d["e_R"],
        "psi_d5_down": d["psi"] - Fraction(1, 1) + d["Q_L"] + d["H"] + d["d_R"],
        "psi_d5_up": d["psi"] - Fraction(1, 1) + d["Q_L"] + d["H_tilde"] + d["u_R"],
        "psi_d5_charged_lepton": d["psi"] - Fraction(1, 1) + d["L_L"] + d["H"] + d["e_R"],
        "higgs_portal": 2 * d["psi"] + 2 * d["H"],
        "waterfall_portal": 2 * d["Phi"] + 2 * d["psi"],
        "dark_matter_portal": 2 * d["chi"] + 2 * d["Phi_res"],
        "gauge_kinetic": Fraction(4, 1),
        "fermion_kinetic": Fraction(1, 1) + d["Q_L"] + d["Q_L"],
        "higgs_mass_term": Fraction(2, 1) + 2 * d["H"],
        "higgs_quartic": 4 * d["H"],
    }


def validate_action_registry():
    """Return True only if gauge singlets and dimension-four Lagrangian terms check."""
    hypercharge_ok = all(value == 0 for value in yukawa_hypercharge_residuals().values())
    nonabelian_ok = all(
        all(group_checks.values())
        for group_checks in yukawa_nonabelian_singlet_checks().values()
    )
    dimensions_ok = all(
        value == Fraction(4, 1) for value in operator_mass_dimensions().values()
    )
    ptum_singlets_ok = all(
        rep["su3"] == "1"
        and rep["su2"] == "1"
        and rep["hypercharge"] == 0
        and rep["reality"] == "real"
        for rep in PTUM_SCALAR_REPRESENTATIONS.values()
    )
    return hypercharge_ok and nonabelian_ok and dimensions_ok and ptum_singlets_ok
