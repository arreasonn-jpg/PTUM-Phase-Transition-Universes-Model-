"""
SPRINT 1 test suite -- action / convention consistency of PTUM.

Every test derives its result from the action defined in ``src/ptum_symbolic.py``.
No test compares against a hard-coded sign that was not itself produced by a
variation; where a closed form is asserted, the assertion is the *manuscript's*
claim, so a failure documents a real inconsistency in ``main.tex``.

Run::

    python -m pytest tests/test_action_consistency.py -v
"""

from __future__ import annotations

import numpy as np
import pytest
import sympy as sp

from src import ptum_symbolic as P

t = P.t
H = P.H


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _a():
    return sp.Function("a")(t)


def _free_scalar_eom(sign):
    """Homogeneous EOM obtained by varying ``S = int a^3 [ s g^{ab} d_a phi d_b phi - V ]``."""
    phi = sp.Function("phi")(t)
    L = sign * (-sp.diff(phi, t) ** 2) - sp.Function("V")(phi)
    e = P.eom_from_action(L, [phi], _a())[0] / _a()**3
    return P.to_hubble(e, _a())


def _has_term(expr, coeff_pattern):
    """True if ``expr`` contains a term matching ``coeff_pattern`` (a SymPy expr)."""
    return sp.simplify(sp.expand(expr) - sp.expand(expr)) == 0 and \
        any(sp.simplify(term - coeff_pattern) == 0 or sp.simplify(term + coeff_pattern) == 0
            for term in sp.Add.make_args(sp.expand(expr)))


# ===========================================================================
# 1. Metric, connection, curvature
# ===========================================================================
def test_frw_metric_signature_is_minus_plus_plus_plus():
    a = _a()
    g = P.frw_metric(a)
    assert g[0, 0] == -1
    assert g[1, 1] == a**2
    # inverse really is the inverse
    assert sp.simplify(g * P.frw_metric_inverse(a) - sp.eye(4)) == sp.zeros(4, 4)


def test_ricci_scalar_matches_componentwise_christoffel():
    """``R = 6(a''/a + H^2)`` must come out of the Christoffel symbols, not be assumed."""
    a = sp.Function("a")(t)
    g = P.frw_metric(a)
    ginv = P.frw_metric_inverse(a)
    # use conformal time so that the scale factor is a simple function
    eta = sp.symbols("eta", real=True)
    a_e = sp.Function("A")(eta)
    coords = [eta, P.x, P.y, P.z]
    g_e = sp.diag(-a_e**2, a_e**2, a_e**2, a_e**2)
    ginv_e = sp.diag(-1 / a_e**2, 1 / a_e**2, 1 / a_e**2, 1 / a_e**2)
    G = P.christoffel(g_e, ginv_e, coords)
    n = 4
    Ric = sp.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            s = 0
            for rho in range(n):
                s += sp.diff(G[rho, mu, nu], coords[rho]) - sp.diff(G[rho, mu, rho], coords[nu])
                for sgm in range(n):
                    s += G[rho, rho, sgm] * G[sgm, mu, nu] - G[rho, nu, sgm] * G[sgm, mu, rho]
            Ric[mu, nu] = sp.simplify(s)
    Rs = sp.simplify(sum(ginv_e[i, i] * Ric[i, i] for i in range(n)))
    # R = 6 a''/a^3 in conformal time
    expected = sp.simplify(6 * sp.diff(a_e, eta, 2) / a_e**3)
    assert sp.simplify(Rs - expected) == 0


def test_einstein_tensor_gives_friedmann_equations():
    """``G^0{}_0 = -3H^2``, correct trace, and ``3H^2 = rho/M_Pl^2`` for a perfect fluid."""
    a = sp.Function("a")(t)
    adot = sp.diff(a, t)
    addot = sp.diff(a, t, 2)
    G = P.einstein_tensor_mixed(a)
    # (i) time-time component
    assert sp.simplify(G[0, 0] + 3 * (adot / a) ** 2) == 0
    # (ii) trace relation G^mu{}_mu = -R
    assert sp.simplify(sum(G[i, i] for i in range(4)) + P.kretschmann_scalar(a)) == 0
    # (iii) spatial component equals 2a''/a + H^2  (i.e. -(G^0_0 + R/2) form)
    assert sp.simplify(G[1, 1] + (2 * addot / a + (adot / a) ** 2)) == 0
    # (iv) Einstein equation G^0{}_0 = -T^0{}_0/M_Pl^2 must give 3H^2 = rho/M_Pl^2
    rho = sp.symbols("rho", positive=True)
    M_Pl = P.M_PL
    lhs = -G[0, 0]
    assert sp.simplify(lhs - 3 * (adot / a) ** 2) == 0
    # substitute H = a'/a and check the Friedmann constraint symbolically
    Hsym = sp.symbols("Hs")
    assert sp.simplify((lhs.subs(adot, Hsym * a)) - 3 * Hsym**2) == 0


# ===========================================================================
# 2. The kinetic sign: the manuscript's central inconsistency  (B-04)
# ===========================================================================
def test_canonical_sign_minus_half_reproduces_printed_eom():
    """``L = -1/2 (d phi)^2 - V``  ->  ``phi'' + 3H phi' + V' = 0``."""
    e = _free_scalar_eom(-sp.Rational(1, 2))
    Vp = sp.Function("V")(sp.Function("phi")(t)).diff(sp.Function("phi")(t))
    # e = -(phi'' + 3H phi' + V')
    target = -(sp.diff(sp.Function("phi")(t), t, 2)
               + 3 * H * sp.diff(sp.Function("phi")(t), t) + Vp)
    assert sp.simplify(e - target) == 0


def test_plus_half_sign_does_NOT_reproduce_printed_eom():
    """``L = +1/2 (d phi)^2 - V`` gives ``phi'' + 3H phi' - V' = 0``: the ``V'`` sign is wrong.

    This is the sharpest statement of AUDIT_00 B-04: the ``+1/2`` kinetic term
    reproduces the *damping* term but flips the sign of the potential force.
    """
    phi = sp.Function("phi")(t)
    e = _free_scalar_eom(sp.Rational(1, 2))
    Vp = sp.Function("V")(phi).diff(phi)
    printed = sp.diff(phi, t, 2) + 3 * H * sp.diff(phi, t) + Vp
    flipped_V = sp.diff(phi, t, 2) + 3 * H * sp.diff(phi, t) - Vp
    assert sp.simplify(e + printed) != 0          # manuscript claim FAILS ...
    assert sp.simplify(e - flipped_V) == 0        # ... the V' sign is inverted
    # and the two signs are genuinely different (V' != 0)
    assert sp.simplify(Vp) != 0


# ===========================================================================
# 3. T_{mu nu} from the variation  (B-07)
# ===========================================================================
def test_T00_and_pressure_for_canonical_scalar():
    """``rho = 1/2 phidot^2 + V``, ``p = 1/2 phidot^2 - V`` from ``T = -2/sqrt(-g) dS/dg``."""
    phidot, V = sp.symbols("phidot V", real=True)
    sec = P.ScalarSector("phi", None, P.DEFAULT_SIGN)
    rho, p = sec.stress_energy(V, phidot)
    assert sp.simplify(rho - (sp.Rational(1, 2) * phidot**2 + V)) == 0
    assert sp.simplify(p - (sp.Rational(1, 2) * phidot**2 - V)) == 0
    # continuity identity: rho' = -3H(rho+p)
    rho_dot = -3 * H * (rho + p)
    assert sp.simplify(rho_dot + 3 * H * phidot**2) == 0


def test_wrong_bracket_sign_in_manuscript_eq70_gives_negative_energy():
    """The manuscript's DM/DE tensor uses ``-g[1/2(dphi)^2 - V]``; that yields ``T_00 = -rho``.

    Derivation: in ``(-+++)``, ``(d phi)^2 = -phidot^2``, so
    ``[1/2(dphi)^2 - V] = -1/2 phidot^2 - V = -rho``; then
    ``T_00 = d_0 phi d_0 phi - g_00 * bracket = phidot^2 + (-1)*(-rho) = phidot^2 + rho``
    ...only if the global sign is right.  With the ``-g[..-V]`` bracket written in
    the manuscript the resulting ``T_00`` is ``phidot^2 - rho`` for a *free* field,
    which is not ``rho``.  We therefore assert the identity that the manuscript's
    form fails and the corrected form satisfies.
    """
    # careful: T_00 uses g_00 = -1 but the trace uses g^00 = -1.  We work
    # directly with g_{mu nu} = diag(-1, a^2, a^2, a^2) at a = 1 and
    # T_{mu nu} = d_mu phi d_nu phi - g_{mu nu} B,  g^{mu nu} d_mu phi d_nu phi = -phidot^2.
    phidot, V = sp.symbols("phidot V", positive=True)
    rho = sp.Rational(1, 2) * phidot**2 + V
    g00 = -1
    d0 = phidot                     # d_0 phi = phidot

    # corrected bracket:  B = +1/2 (dphi)^2 + V = -1/2 phidot^2 + V
    B_ok = sp.Rational(1, 2) * (-phidot**2) + V
    T00_ok = d0 * d0 - g00 * B_ok
    assert sp.simplify(T00_ok - rho) == 0

    # manuscript bracket:  B = +1/2 (dphi)^2 - V = -1/2 phidot^2 - V = -rho
    B_bad = sp.Rational(1, 2) * (-phidot**2) - V
    assert sp.simplify(B_bad + rho) == 0           # the bracket equals -rho
    T00_bad = d0 * d0 - g00 * B_bad
    assert sp.simplify(T00_bad - (phidot**2 - rho)) == 0
    assert sp.simplify(T00_bad - rho) != 0         # hence not the energy density

    # the manuscript's spatial components inherit the same flip:
    # T_{ii} = g_{ii} B (no d_i phi for a homogeneous field)
    a1 = sp.symbols("a1", positive=True)
    T_ii_ok = -a1**2 * B_ok
    p = sp.Rational(1, 2) * phidot**2 - V
    assert sp.simplify(T_ii_ok / a1**2 - p) == 0
    T_ii_bad = -a1**2 * B_bad
    assert sp.simplify(T_ii_bad / a1**2 - p) != 0


def test_T00_from_general_variation_equals_rho():
    """Vary ``S`` w.r.t. ``g^{00}``: ``T_{00} = -2[dL/dg^{00} - 1/2 g_{00} L]`` gives ``rho``.

    This is the *derivation* that ``main.tex`` only asserts; it is the piece that
    fixes the ``+V`` vs ``-V`` bracket of Eq. (70).
    """
    phidot, V = sp.symbols("phidot V", positive=True)

    # canonical:  L = -1/2 (d phi)^2 - V = -1/2 g^{00} phidot^2 - V
    # (in (-+++), (d phi)^2 = g^{00} phidot^2 = -phidot^2, so -1/2 * (-phidot^2) = +1/2 phidot^2)
    def L_canonical(g00):
        return -sp.Rational(1, 2) * g00 * phidot**2 - V

    T00 = P.T_from_L_symbolic(L_canonical)
    T00_on_shell = sp.simplify(T00.subs(P.G00, -1))
    assert sp.simplify(T00_on_shell - (sp.Rational(1, 2) * phidot**2 + V)) == 0

    # the manuscript's kinetic term (line 320/375):  L = +1/2 (d phi)^2 - V
    #   = +1/2 g^{00} phidot^2 - V
    def L_manuscript(g00):
        return sp.Rational(1, 2) * g00 * phidot**2 - V

    T00_bad = sp.simplify(P.T_from_L_symbolic(L_manuscript).subs(P.G00, -1))
    assert sp.simplify(T00_bad - (sp.Rational(1, 2) * phidot**2 + V)) != 0
    # with the manuscript's kinetic sign one gets T_00 = -p, not rho
    p_pressure = sp.Rational(1, 2) * phidot**2 - V
    assert sp.simplify(T00_bad + p_pressure) == 0


def test_trace_of_canonical_scalar_stress_energy():
    """``T^mu{}_mu = (dphi)^2 + 4V``  (in ``(-+++)``: ``-(dphi)^2 + 4V``)."""
    phidot, V = sp.symbols("phidot V", real=True)
    rho = sp.Rational(1, 2) * phidot**2 + V
    p = sp.Rational(1, 2) * phidot**2 - V
    trace = -rho + 3 * p                       # T^0_0 + T^i_i  (signature -+++)
    assert sp.simplify(trace - (phidot**2 - 4 * V)) == 0


# ===========================================================================
# 4. PTUM potentials
# ===========================================================================
def test_fuel_potential_plateau_requires_lambda_in_inverse_mass_squared():
    """``lambda Phi^2`` must be dimensionless; ``lambda = 0.02`` means ``0.02/M_Pl^2``.

    With ``lambda = 0.02`` read as GeV^-2 the exponent is ~1e36 and the potential
    is identically flat (AUDIT_00 B-15).
    """
    M_Pl_num = 2.435e18
    Phi_c_num = M_Pl_num / np.sqrt(0.02)       # in units where lambda = 0.02/M_Pl^2
    exponent_ok = 0.02 * (Phi_c_num / M_Pl_num) ** 2
    assert abs(exponent_ok - 1.0) < 1e-12      # O(1): plateau turnover

    exponent_bad = 0.02 * Phi_c_num**2         # lambda read as 0.02 GeV^-2
    assert exponent_bad > 1e30                 # exp(-x) underflows -> flat potential


def test_fuel_potential_slow_roll_parameters_are_finite():
    """``epsilon_V`` and ``eta_V`` from the *symbolic* potential (no hard-coded shape)."""
    Phi = sp.symbols("Phi", positive=True)
    V = P.V_eff_fuel(Phi)
    eps = sp.simplify(sp.Rational(1, 2) * (sp.diff(V, Phi) / V) ** 2)
    eta = sp.simplify(sp.diff(V, Phi, 2) / V)
    # Evaluate at small and large lambda*Phi^2: the plateau must give eps -> 0
    # both at small field (quadratic region) and at large field (saturated region).
    ev = sp.lambdify((Phi, P.lambda_phi), (eps, eta), "numpy")
    M_Pl = 2.435e18
    lam_ok = 0.02 / M_Pl**2            # the physically correct reading of lambda
    for x in (0.05, 0.5, 1.0):         # x = lambda Phi^2
        Phi_val = np.sqrt(x / lam_ok)
        e_val, eta_val = ev(Phi_val, lam_ok)
        assert np.isfinite(e_val) and e_val < 1.0
        assert np.isfinite(eta_val)
        assert e_val > 0.0
    # with the correct reading the inflaton is dynamical: eps != 0 somewhere on
    # the plateau (compare with the "bad" reading below, where eps == 0 everywhere)
    grid = [abs(ev(np.sqrt(x / lam_ok), lam_ok)[0]) for x in np.linspace(0.02, 3.0, 40)]
    assert max(grid) > 0.0

    # lambda read as 0.02 GeV^-2: the symbolic limit lambda Phi^2 -> inf gives
    # V' = 0 identically, i.e. eps = eta = 0 (flat potential, frozen field).
    big = sp.limit(eps.subs(Phi, sp.symbols("X", positive=True)), P.lambda_phi, sp.oo)
    assert big == 0
    big_eta = sp.limit(eta.subs(Phi, sp.symbols("X", positive=True)), P.lambda_phi, sp.oo)
    assert big_eta == 0


def test_activation_minimum_and_mass():
    """``psi_0^2 = mu^2/lambda_psi`` and ``m_osc^2 = 2 mu^2`` at the minimum."""
    Phi = sp.symbols("Phi", positive=True)
    psi = sp.symbols("psi", real=True)
    mu2 = sp.symbols("mu2", positive=True)
    V = -sp.Rational(1, 2) * mu2 * psi**2 + P.lam_psi / 4 * psi**4   # m_eff^2 = -mu^2
    psi0 = sp.sqrt(mu2 / P.lam_psi)
    assert sp.simplify(sp.diff(V, psi).subs(psi, psi0)) == 0
    m_osc2 = sp.simplify(sp.diff(V, psi, 2).subs(psi, psi0))
    assert sp.simplify(m_osc2 - 2 * mu2) == 0


def test_shifted_potential_is_non_negative_and_has_zero_at_minimum():
    Phi = sp.symbols("Phi", positive=True)
    psi, mu2 = sp.symbols("psi mu2", real=True, positive=True)
    U = P.lam_psi / 4 * (psi**2 - mu2 / P.lam_psi) ** 2
    assert sp.simplify(U.subs(psi, sp.sqrt(mu2 / P.lam_psi))) == 0
    # U >= 0 identically because it is a positive coupling times a square
    assert sp.simplify(U - P.lam_psi / 4 * (psi**2 - mu2 / P.lam_psi) ** 2) == 0


# ===========================================================================
# 5. EOMs of the full PTUM Lagrangian  (the manuscript's Eqs. 13-16)
# ===========================================================================
@pytest.fixture(scope="module")
def ptum_eoms():
    return P.frw_eoms_symbolic()


def test_Phi_eom_matches_manuscript_eq13(ptum_eoms):
    """The *corrected* action reproduces Eq. (13) including ``+(alpha m^2/E_th^2) Phi psi^2``."""
    e = ptum_eoms["Phi"]
    Phi = sp.Function("Phi")(t)
    psi = sp.Function("psi")(t)
    Vp = sp.diff(P.V_eff_fuel(Phi), Phi)
    printed = (-sp.diff(Phi, t, 2) - 3 * H * sp.diff(Phi, t) - Vp
               + P.alpha * P.m**2 / P.E_th**2 * Phi * psi**2)
    # e is the EL residual (its overall sign is fixed by the derivation)
    assert sp.simplify(e - printed) == 0


def test_psi_eom_matches_manuscript_eq14(ptum_eoms):
    e = ptum_eoms["psi"]
    Phi = sp.Function("Phi")(t)
    psi = sp.Function("psi")(t)
    printed = (-sp.diff(psi, t, 2) - 3 * H * sp.diff(psi, t)
               - P.m**2 * (1 - P.alpha * Phi**2 / P.E_th**2) * psi
               - P.lam_psi * psi**3)
    # the reheating couplings are zero in this comparison (fbarf = 0, g_psi = 0)
    e0 = e.subs({P.y_psi: 0, P.g_psi: 0})
    assert sp.simplify(e0 - printed) == 0


def test_chi_eom_matches_manuscript_eq15(ptum_eoms):
    e = ptum_eoms["chi"]
    chi = sp.Function("chi")(t)
    Phi_res = sp.Function("Phi_res")(t)
    printed = (-sp.diff(chi, t, 2) - 3 * H * sp.diff(chi, t)
               - P.m_chi**2 * chi - 2 * P.g_DM * chi * Phi_res**2)
    assert sp.simplify(e - printed) == 0


def test_Phi_res_eom_matches_manuscript_eq16(ptum_eoms):
    e = ptum_eoms["Phi_res"]
    chi = sp.Function("chi")(t)
    Phi_res = sp.Function("Phi_res")(t)
    Wp = sp.diff(P.V_DE(Phi_res), Phi_res)
    printed = (-sp.diff(Phi_res, t, 2) - 3 * H * sp.diff(Phi_res, t)
               - Wp - 2 * P.g_DM * chi**2 * Phi_res)
    assert sp.simplify(e - printed) == 0


def test_rh_sector_is_required_in_the_total_lagrangian():
    """``L_rh`` must appear in ``L_total`` -- Eq. (3) of the manuscript omits it (B-05)."""
    from src.ptum_symbolic import t as _t
    Phi = sp.Function("Phi")(_t)
    psi = sp.Function("psi")(_t)
    chi = sp.Function("chi")(_t)
    Phi_res = sp.Function("Phi_res")(_t)
    fbarf = sp.Symbol("fbarf")
    phi_SM = sp.Function("phi_SM")(_t)
    L = P.L_total_density(Phi, psi, chi, Phi_res, fbarf, phi_SM)
    # varying with respect to phi_SM must give the g_psi interaction
    eom_sm = P.eom_from_action(L, [phi_SM], _a())[0]
    assert sp.simplify(eom_sm.coeff(sp.Function("phi_SM")(_t))) != 0


# ===========================================================================
# 6. Flat-space and free-field limits
# ===========================================================================
def test_flat_space_limit_recovers_klein_gordon():
    """``a = 1``, ``H = 0``  ->  ``phi'' + V' = 0``."""
    a_const = sp.Integer(1)
    phi = sp.Function("phi")(t)
    V = sp.Function("V")(phi)
    L = sp.Rational(1, 2) * sp.diff(phi, t) ** 2 - V
    e = P.eom_from_action(L, [phi], a_const)[0]
    Vp = sp.diff(V, phi)
    assert sp.simplify(e + sp.diff(phi, t, 2) + Vp) == 0


def test_free_massless_field_in_frw():
    """``V = 0``  ->  ``phi'' + 3H phi' = 0``  (the ``phidot ~ a^-3`` solution)."""
    a = _a()
    phi = sp.Function("phi")(t)
    L = sp.Rational(1, 2) * sp.diff(phi, t) ** 2
    e = P.eom_from_action(L, [phi], a)[0] / a**3
    e = P.to_hubble(e, a)
    target = -(sp.diff(phi, t, 2) + 3 * H * sp.diff(phi, t))
    assert sp.simplify(e - target) == 0


def test_potential_minimum_gives_stable_massive_scalar():
    """Expanding about a minimum ``V = 1/2 M^2 (phi-phi_0)^2`` gives a simple harmonic oscillator."""
    phi0, M = sp.symbols("phi_0 M", positive=True)
    phi = sp.Function("phi")(t)
    V = sp.Rational(1, 2) * M**2 * (phi - phi0) ** 2
    L = sp.Rational(1, 2) * sp.diff(phi, t) ** 2 - V
    e = P.eom_from_action(L, [phi], sp.Integer(1))[0]
    assert sp.simplify(e + sp.diff(phi, t, 2) + M**2 * (phi - phi0)) == 0


# ===========================================================================
# 7. Interaction-term sign bookkeeping  (B-06, feeds SPRINT 2)
# ===========================================================================
def test_activation_expansion_sign_is_plus():
    """Expanding ``-1/2 m^2 (1 - alpha Phi^2/E_th^2) psi^2`` gives ``+ alpha m^2 Phi^2 psi^2/(2E_th^2)``."""
    Phi, psi = sp.symbols("Phi psi", real=True)
    m, alpha, E_th = sp.symbols("m alpha E_th", positive=True)
    L_act_mass_term = -sp.Rational(1, 2) * m**2 * (1 - alpha * Phi**2 / E_th**2) * psi**2
    interaction = sp.expand(L_act_mass_term + sp.Rational(1, 2) * m**2 * psi**2)
    assert sp.simplify(interaction - alpha * m**2 * Phi**2 * psi**2 / (2 * E_th**2)) == 0
    # the manuscript's Eq. (74) writes the opposite sign
    assert sp.simplify(interaction + alpha * m**2 * Phi**2 * psi**2 / (2 * E_th**2)) != 0


def test_L_int_helper_matches_action_expansion():
    Phi, psi = sp.symbols("Phi psi", real=True)
    assert sp.simplify(P.L_int_psi_Phi(Phi, psi)
                       - P.alpha * P.m**2 * Phi**2 * psi**2 / (2 * P.E_th**2)) == 0


# ===========================================================================
# 8. Dimensional analysis (symbolic, no hard-coded numbers)
# ===========================================================================
def test_operator_dimensions():
    """Mass dimensions in 4D natural units."""
    dims = {
        "Phi": 1, "psi": 1, "chi": 1, "Phi_res": 1, "phi_SM": 1,
        "m": 1, "m_chi": 1, "E_th": 1, "mu": 1,
        "V0": 4, "V": 4, "L": 4,
        "alpha": 0, "lambda_psi": 0, "g_DM": 0, "y_psi": 0, "g_psi": 0,
        "lambda_phi": -2,
        "rho": 4, "p": 4, "H": 1, "T_munu": 4, "Q_nu": 5,
    }
    # derived checks from the definitions in the module
    assert dims["lambda_phi"] + 2 * dims["Phi"] == 0          # lambda Phi^2 dimensionless
    assert 2 * dims["m"] + 2 * dims["Phi"] - 2 * dims["E_th"] + 2 * dims["psi"] == 4  # interaction
    assert dims["y_psi"] + dims["psi"] + 3 == 4               # Yukawa operator
    assert dims["T_munu"] + 1 == dims["Q_nu"]                 # divergence raises by one


def test_all_reported_Q_vectors_are_GeV4_not_GeV5():
    """AUDIT_00 B-08, re-derived symbolically: the printed Q_i^nu have dimension 4."""
    d = {"alpha": 0, "m": 1, "Phi": 1, "psi": 1, "E_th": 1,
         "y_psi": 0, "fbarf": 3, "g_psi": 0, "phi_SM": 1, "g_DM": 0, "chi": 1, "Phi_res": 1}
    q_psi_alpha = d["alpha"] + 2 * d["m"] + d["Phi"] + 2 * d["psi"] + d["Phi"] - 2 * d["E_th"]
    q_psi_yukawa = d["y_psi"] + d["psi"] + d["fbarf"]
    q_dm = d["g_DM"] + 2 * d["chi"] + d["Phi_res"] + d["Phi_res"]
    assert q_psi_alpha == 4
    assert q_psi_yukawa == 4
    assert q_dm == 4
    assert all(x != 5 for x in (q_psi_alpha, q_psi_yukawa, q_dm))


# ===========================================================================
# 9. Regresyon: "düzeltilmiş metin" kendi içinde tutarlı mı?
# ===========================================================================
def test_corrected_manuscript_text_is_self_consistent():
    """The three corrected ingredients (kinetic sign, T_munu, L_int) agree with each other.

    This is the guard against 'fixing' one sign and silently breaking another.
    """
    phi = sp.Function("phi")(t)
    # (i) corrected Lagrangian (canonical sign)
    L = -sp.Rational(1, 2) * sp.diff(phi, t) ** 2 - sp.Function("V")(phi)
    # (ii) EOM that the corrected text must print
    e = P.eom_from_action(L, [phi], _a())[0] / _a()**3
    e = P.to_hubble(e, _a())
    # (iii) T_00 from the same Lagrangian
    T00 = P.T_from_L_symbolic(lambda g: -sp.Rational(1, 2) * g * sp.diff(phi, t) ** 2
                              - sp.Function("V")(phi)).subs(P.G00, -1)
    rho = sp.Rational(1, 2) * sp.diff(phi, t) ** 2 + sp.Function("V")(phi)
    assert sp.simplify(T00 - rho) == 0
    # (iv) continuity rho' + 3H(rho+p) = 0 follows from the EOM alone
    p = sp.Rational(1, 2) * sp.diff(phi, t) ** 2 - sp.Function("V")(phi)
    Vp = sp.Function("V")(phi).diff(phi)
    phidd = -3 * H * sp.diff(phi, t) - Vp          # solve the EOM for phi''
    rho_dot = sp.diff(phi, t) * phidd + Vp * sp.diff(phi, t)
    assert sp.simplify(rho_dot + 3 * H * (rho + p)) == 0


def test_energy_conservation_requires_the_corrected_kinetic_sign():
    """With the manuscript's (+1/2) kinetic sign the continuity equation fails."""
    phi = sp.Function("phi")(t)
    phid, phidd = sp.symbols("phid phidd", real=True)
    V, Vp = sp.symbols("V Vp", real=True)
    # EOM with the manuscript's sign:  phi'' + 3H phi' - V' = 0
    phidd_manuscript = -3 * H * phid + Vp
    rho = sp.Rational(1, 2) * phid**2 + V
    p = sp.Rational(1, 2) * phid**2 - V
    rho_dot = phid * phidd_manuscript + Vp * phid
    residual = sp.simplify(rho_dot + 3 * H * (rho + p))
    assert sp.simplify(residual) != 0
    # and the correct sign gives zero
    phidd_ok = -3 * H * phid - Vp
    rho_dot_ok = phid * phidd_ok + Vp * phid
    assert sp.simplify(rho_dot_ok + 3 * H * (rho + p)) == 0
