with open('ptum_task1_simulation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the whole main block
old = '''    print(f"\\nBaseline Parameters:")
    print(f"  V0 = {params.V0:.1e} GeV^4")
            print(f"  lambda_Phi = {params.lambda_phi}")
            print(f"  m_psi = {params.m_psi:.1e} GeV")
            print(f"  lambda_psi = {params.lambda_psi}")
            print(f"  alpha = {params.alpha:.1e}")
    print(f"  E_th = {params.E_th:.1e} GeV")
            print(f"  Phi_c = {params.Phi_c:.1e} GeV")
            print(f"  psi_0 = {params.psi_0:.1e} GeV")
            print(f"  H_star = {params.H_star:.1e} GeV")
            print(f"  mu = {np.sqrt(abs(params.mu_sq)):.1e} GeV")
            print(f"  mu/H_star = {np.sqrt(abs(params.mu_sq))/params.H_star:.2f}")
    
            # Test 1: Baseline initial conditions (psi=0, psi_dot=0 at threshold)
    print("\\n" + "=" * 60)
            print("Test 1: Baseline IC (psi=0, psi_dot=0 at Phi=Phi_c)")
    print("=" * 60)'''

new = '''    print(f"\\nBaseline Parameters:")
    print(f"  V0 = {params.V0:.1e} GeV^4")
    print(f"  lambda_Phi = {params.lambda_phi}")
    print(f"  m_psi = {params.m_psi:.1e} GeV")
    print(f"  lambda_psi = {params.lambda_psi}")
    print(f"  alpha = {params.alpha:.1e}")
    print(f"  E_th = {params.E_th:.1e} GeV")
    print(f"  Phi_c = {params.Phi_c:.1e} GeV")
    print(f"  psi_0 = {params.psi_0:.1e} GeV")
    print(f"  H_star = {params.H_star:.1e} GeV")
    print(f"  mu = {np.sqrt(abs(params.mu_sq)):.1e} GeV")
    print(f"  mu/H_star = {np.sqrt(abs(params.mu_sq))/params.H_star:.2f}")
    
    # Test 1: Baseline initial conditions (psi=0, psi_dot=0 at threshold)
    print("\\n" + "=" * 60)
    print("Test 1: Baseline IC (psi=0, psi_dot=0 at Phi=Phi_c)")
    print("=" * 60)'''

content = content.replace(old, new)
with open('ptum_task1_simulation.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')