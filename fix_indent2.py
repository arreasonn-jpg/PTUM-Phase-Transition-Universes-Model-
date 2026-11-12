with open('ptum_task1_simulation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all remaining indentation issues in the main block
replacements = [
    # Test 1 output
    ('            print(f"  Final <w> = {classification[\'w_final\']:.4f}")', '    print(f"  Final <w> = {classification[\'w_final\']:.4f}")'),
    ('            print(f"  psi_0 = {params.psi_0:.2e} GeV")', '    print(f"  psi_0 = {params.psi_0:.2e} GeV")'),
    ('            print(f"  Max |psi|/psi_0 = {np.max(np.abs(result[\'psi\']))/params.psi_0:.2f}")', '    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result[\'psi\']))/params.psi_0:.2f}")'),
    
    # Test 2 header
    ('            print("Test 2: Non-zero initial velocity (psi_dot = 0.1 mu psi_0)")', '    print("Test 2: Non-zero initial velocity (psi_dot = 0.1 mu psi_0)")'),
    
    # Test 2 output
    ('            print(f"  Final <w> = {classification2[\'w_final\']:.4f}")', '    print(f"  Final <w> = {classification2[\'w_final\']:.4f}")'),
    ('            print(f"  Max |psi|/psi_0 = {np.max(np.abs(result2[\'psi\']))/params.psi_0:.2f}")', '    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result2[\'psi\']))/params.psi_0:.2f}")'),
    
    # Test 3 header
    ('            # Test 3: Past threshold (Phi > Phi_c)', '    # Test 3: Past threshold (Phi > Phi_c)'),
    ('            print("Test 3: Past threshold (Phi = 1.01 Phi_c)")', '    print("Test 3: Past threshold (Phi = 1.01 Phi_c)")'),
    
    # Test 3 output
    ('            print(f"  Final <w> = {classification3[\'w_final\']:.4f}")', '    print(f"  Final <w> = {classification3[\'w_final\']:.4f}")'),
    ('            print(f"  Max |psi|/psi_0 = {np.max(np.abs(result3[\'psi\']))/params.psi_0:.2f}")', '    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result3[\'psi\']))/params.psi_0:.2f}")'),
    
    # Test 4 output
    ('            print(f"  Final <w> = {classification4[\'w_final\']:.4f}")', '    print(f"  Final <w> = {classification4[\'w_final\']:.4f}")'),
    ('            print(f"  Max |psi|/psi_0 = {np.max(np.abs(result4[\'psi\']))/params.psi_0:.2f}")', '    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result4[\'psi\']))/params.psi_0:.2f}")'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('ptum_task1_simulation.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done fixing all indentation')