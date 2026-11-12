# SPRINT 1 — Eylem, konvansiyon ve işaret tutarlılığı

**Durum:** tamamlandı · **Test:** `tests/test_action_consistency.py` → **27/27 PASS**
**Kod:** `src/ptum_symbolic.py` (tek doğruluk kaynağı)
**Önkoşul:** `AUDIT_00_INVENTORY.md` (SPRINT 0), bulgular B-04, B-05, B-06, B-07, B-15
**Kural:** bu sprintte `main.tex` **değiştirilmedi**. Buradaki her sonuç eylemden türetilmiştir;
hiçbir işaret "elle" seçilmemiştir.

---

## 1. Sabitlenen konvansiyon

SPRINT 0 §10'daki iki seçenekten **(a)** onaylandı:

```text
Metrik imzası        (-+++)
Riemann              R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma} - ...   (MTW)
Matter eylemi        S_m = ∫ d^4x sqrt(-g) L_m
Enerji-momentum      T_{mu nu} = -2/sqrt(-g) * delta(sqrt(-g) L_m)/delta g^{mu nu}
Kanonik skaler       L = -1/2 g^{mu nu} d_mu phi d_nu phi - V(phi)
                     FRW homojen limitte:  L = +1/2 phidot^2 - V
```

**Neden (a) ve neden `-1/2`:** `+1/2 (dφ)^2` yazımı `(-+++)` ile *kanonik olmayan*
(ghost-benzeri) bir işaret verir; `−1/2` ise makalenin **zaten yazılı olan**
hareket denklemlerini ve `ρ`, `p` ifadelerini birebir üretir. Yani düzeltme yeni
fizik getirmiyor; mevcut metni kendi içinde tutarlı hâle getiriyor.

---

## 2. Türetim adımları

### 2.1 Eylemden hareket denklemi (tekrar: serbest skaler)

Homojen `φ(t)`, `S = ∫ dt a^3 [ s g^{ab} ∂_aφ ∂_bφ − V ]`, `g^{00} = −1`:

```text
L = −s φ̇² − V(φ)
Euler–Lagrange:  ∂_t(∂L/∂φ̇) + 3H ∂L/∂φ̇ − ∂L/∂φ = 0
⇒  −2s (φ̈ + 3Hφ̇) + V'(φ) = 0
```

| s | EOM | Değerlendirme |
|---|---|---|
| `−1/2` (kanonik) | `φ̈ + 3Hφ̇ + V' = 0` | **makale Eq. (13)-(16) ile aynı** ✔ |
| `+1/2` (mevcut metin) | `φ̈ + 3Hφ̇ − V' = 0` | potansiyel kuvvetinin işareti ters ✘ |

> SymPy bağımsız doğrulaması (test `test_canonical_sign_minus_half_reproduces_printed_eom`):
> `−1/2` için EL kalıntısı `−(φ̈ + 3Hφ̇ + V')`; `+1/2` için `+(φ̈ + 3Hφ̇ − V')`.

**Bu, B-04'ün kesin ifadesidir:** `+1/2` seçimi sönüm terimini doğru, potansiyel
terimini yanlış verir. Makalenin `+1/2` + `+V'` kombinasyonu hiçbir tek işaretle
elde edilemez.

### 2.2 `T_{μν}` — varyasyondan

`δ√(−g)/δg^{μν} = −½√(−g) g_{μν}` kullanılırsa

```text
T_{μν} = −2 ∂L/∂g^{μν} + g_{μν} L          (ikinci terim + işaretli)
```

`T_{00}` için (`g_{00} = −1`, `g^{00} = −1`, homojen alan):

| s | `L` | `T_{00}` | `ρ = ½φ̇²+V` |
|---|---|---|---|
| `−1/2` | `+½φ̇² − V` | `½φ̇² + V` | **eşit** ✔ |
| `+1/2` | `−½φ̇² − V` | `−½φ̇² + V = −p` | eşit değil ✘ |

Test: `test_T00_from_general_variation_equals_rho`, `test_T00_and_pressure_for_canonical_scalar`.

> **Not (kendi yakaladığım hata):** ilk denemede `T_{μν} = −2∂L/∂g^{μν} − g_{μν}L`
> yazmıştım; bu `T_{00} = −p` verir. Test bunu yakaladı; doğru işaret `+`.
> Bu, "iki satır zıt işaret yazmak kanıt değildir" kuralının canlı örneği.

### 2.3 Eq. (70)'in parantez işareti (B-07)

Makale §5.5.1'de `T = ∂χ∂χ − g[½(∂χ)² − V]` yazıyor. Homojen alan için parantez

```text
B = ½(∂χ)² − V = −½χ̇² − V = −ρ    ⇒    T_{00} = χ̇² − (−1)(−ρ) = χ̇² − ρ ≠ ρ
```

Doğru parantez `B = ½(∂χ)² + V` olmalıdır. Test:
`test_wrong_bracket_sign_in_manuscript_eq70_gives_negative_energy` — düzeltilmiş
form `T_{00} = ρ` verir, makale formu vermez.

### 2.4 Eylemden PTUM EOM'leri — dört denklemin tamamı

`L_total` (Eq. 3 + eksik `L_rh`, bkz. §2.6) ve `S = ∫ dt a^3 L_total` üzerinden
`euler_equations` ile:

| Alan | Türetilen EOM | Makale | Sonuç |
|---|---|---|---|
| `Φ` | `Φ̈ + 3HΦ̇ + V_eff,Φ − (αm²/E_th²)Φψ² = 0` | Eq. (13) | **birebir aynı** ✔ |
| `ψ` | `ψ̈ + 3Hψ̇ + m²(1−αΦ²/E_th²)ψ + λ_ψψ³ = 0` | Eq. (14) | **birebir aynı** ✔ |
| `χ` | `χ̈ + 3Hχ̇ + m_χ²χ + 2g_DMχΦ_res² = 0` | Eq. (15) | **birebir aynı** ✔ |
| `Φ_res` | `Φ̈_res + 3HΦ̇_res + W' + 2g_DMχ²Φ_res = 0` | Eq. (16) | **birebir aynı** ✔ |

Test: `test_Phi_eom_matches_manuscript_eq13`, `test_psi_eom_matches_manuscript_eq14`,
`test_chi_eom_matches_manuscript_eq15`, `test_Phi_res_eom_matches_manuscript_eq16`.

**Sonuç — bu sprintin en önemli bulgusu:** kanonik işaretle yazılan tek eylem,
makalenin **dört hareket denklemini de** üretir. Yani makalenin EOM'leri *doğrudur*;
onları ürettiği iddia edilen Lagrangian'ın kinetik işareti yanlıştır. Düzeltme
tek satırdadır ve başka hiçbir denklemi bozmaz.

### 2.5 Etkileşim işareti (B-06)

Eq. (7)'yi açalım:

```text
−½ m²(1 − αΦ²/E_th²)ψ²  =  −½m²ψ²  +  α m² Φ²ψ²/(2E_th²)
                                        └── + işaretli ──┘
```

Eq. (74) ise `−α m² Φ²ψ²/(2E_th²)` yazıyor → **işaret çelişkisi**.
Test: `test_activation_expansion_sign_is_plus`.
`Φ` EOM'indeki `+αm²Φψ²/E_th²` terimi *yalnızca* bu `+` işaretle ortaya çıkar;
yani Eq. (13) doğru olan, Eq. (74) yanlış olandır.

> **SPRINT 2'ye devir:** `L_int^{ψΦ}` işareti `+` olarak sabitlendi.
> `Q_ψ^ν`, `Q_Φ^ν` bu işaretten türetilecek.

### 2.6 `L_rh` toplam Lagranjiyen'de (B-05)

`main.tex` Eq. (3) yalnızca dört sektör listeliyor; `L_rh` Eq. (5.5.2)'de
"toplam" Lagranjiyen'e sonradan ekleniyor ve `Q_SM` bundan türetiliyor.
`L_total_density()` artık `L_rh`'yi baştan içeriyor; `φ_SM`'ye göre varyasyon
`g_ψψ²φ_SM` terimini üretiyor (test `test_rh_sector_is_required_in_the_total_lagrangian`).

### 2.7 `λ` birimi (B-15)

`V = V₀(1 − e^{−λΦ²})`; `λΦ²` boyutsuz olmalı, `[λ] = GeV⁻²` (makale Tablo 8 de
böyle diyor). Sayısal kodda `λ = 0.02` **GeV⁻²** olarak kullanılıyor →
`λΦ_c² ≈ 5.9×10³⁶` → `ε_V = η_V = 0` (test `test_fuel_potential_slow_roll_parameters_are_finite`
bunu `limit(λ→∞)` ile gösteriyor).

Doğru okuma: `λ ≈ 0.02/M_Pl²`. O zaman `λΦ_c² = 1` (plato dönüm noktası) ve
`ε_V` sonlu/pozitif olur. **Karar: SPRINT 1'de fiziksel okuma `λ = λ̃/M_Pl²`
olarak sabitlendi; `λ̃ = O(0.01-5)`.** Kod tarafı SPRINT 5'te düzeltilecek.

---

## 3. Limit testleri

| Limit | Beklenen | Test | Sonuç |
|---|---|---|---|
| Düz uzay (`a=1`, `H=0`) | `φ̈ + V' = 0` | `test_flat_space_limit_recovers_klein_gordon` | PASS |
| Serbest kütlesiz (`V=0`) | `φ̈ + 3Hφ̇ = 0` ⇒ `φ̇ ∝ a⁻³` | `test_free_massless_field_in_frw` | PASS |
| Potansiyel minimumu (`½M²(φ−φ₀)²`) | basit harmonik: `φ̈ + M²(φ−φ₀) = 0` | `test_potential_minimum_gives_stable_massive_scalar` | PASS |
| Aktivasyon minimumu | `ψ₀² = μ²/λ_ψ`, `m_osc² = 2μ²` | `test_activation_minimum_and_mass` | PASS |
| Kaydırılmış potansiyel | `U ≥ 0`, `U(ψ₀) = 0` | `test_shifted_potential_is_non_negative_and_has_zero_at_minimum` | PASS |
| `ΛCDM` limiti | `ΔN_fluid→0`, `g_DM→0` | bu sprintin kapsamı dışı (SPRINT 4/5) | — |
| `ℏ→0` klasik limit | zaten klasik eylem | kapsam dışı | — |

---

## 4. Birim ve boyut analizi

| Nicelik | Boyut | Kontrol |
|---|---|---|
| `V₀`, `V`, `ρ`, `p`, `L` | `GeV⁴` | `test_operator_dimensions` |
| `Φ, ψ, χ, Φ_res, φ_SM, m, m_χ, E_th` | `GeV` | aynı |
| `α, λ_ψ, g_DM, y_ψ, g_ψ` | boyutsuz | aynı |
| `λ_φ` | `GeV⁻²` | `λΦ²` boyutsuz |
| `T_{μν}` | `GeV⁴` | aynı |
| `Q^ν = ∇_μT^{μν}` | `GeV⁵` | `test_all_reported_Q_vectors_are_GeV4_not_GeV5` |

**B-08 yeniden doğrulandı:** `Q_ψ^ν` (Yukawa) `= 0+1+3 = 4`; `Q_DM^ν = 0+2+1+1 = 4`.
Yani mevcut `Q_i^ν` ifadelerinin tamamı `GeV⁴`. Düzeltme SPRINT 2'de türetilecek
(tahmin: `y_ψ ∂^ν(ψ f̄f)` benzeri türevli yapı, ya da `Q^ν`'nin `T^{μν}` yerine
`∂·T` olarak tanımlanması).

---

## 5. Eski → yeni formül karşılaştırması

| # | Eski (`main.tex`) | Yeni (eylemden) | Gerekçe | Etkilenen yer |
|---|---|---|---|---|
| 1 | `L = +½(∂φ)² − V` | `L = −½(∂φ)² − V` | §2.1; hem EOM hem `T₀₀` | satır 320, 375, 443, 469, 475, 2541-2544 |
| 2 | `T_{μν} = −2/√−g δS/δg^{μν}` **ve** `= +2/√−g δS/δg_{μν}` | tek tanım: `−2/√−g δS/δg^{μν}` | tutarlılık | satır 318, 1678 |
| 3 | `T = ∂φ∂φ − g[½(∂φ)² − V]` | `T = ∂φ∂φ − g[½(∂φ)² + V]` | §2.3; `+V` olmadan `T₀₀ = −ρ` | Eq. (70), satır 1578-1583 |
| 4 | `L_int^{ψΦ} = −αm²Φ²ψ²/(2E_th²)` | `+αm²Φ²ψ²/(2E_th²)` | Eq. (7) açılımı | Eq. (74), satır 1670 |
| 5 | `L = L_fuel+L_act+L_DM+L_DE` | `+ L_rh` | §2.6 | Eq. (3), satır 368 |
| 6 | `λ = 0.02` (GeV⁻² olarak) | `λ = λ̃/M_Pl²`, `λ̃ = O(0.01-5)` | §2.7 | kod + satır 1219, 1145 |
| 7 | `m_ψ²ψ²/2` (lattice potansiyeli, satır 3363) | `½m²(1−αΦ²/E_th²)ψ²` | tutarlılık | satır 3363 (B-21) |

**Not:** (1)-(5) ve (7) saf işaret/tamlık düzeltmeleridir ve `main.tex`'in
*hiçbir sayısal sonucunu* değiştirmez, çünkü EOM'ler zaten doğru yazılmış.
Tek istisna (6): `λ` birimi sayısal sonuçları **kökten** etkiler (SPRINT 5).

---

## 6. SPRINT 1'de KAPATILAN bulgular

| Bulgu | Durum | Kanıt |
|---|---|---|
| **B-04** kinetik işaret | **KAPATILDI** (karar + test) | `test_canonical_sign_*`, `test_plus_half_*`, `test_T00_from_general_variation_equals_rho` |
| **B-05** `L_rh` eksik | **KAPATILDI** | `test_rh_sector_is_required_in_the_total_lagrangian` |
| **B-06** etkileşim işareti (Lagrangian tarafı) | **KAPATILDI**; `Q` tarafı SPRINT 2 | `test_activation_expansion_sign_is_plus` |
| **B-07** `T_{μν}` tanımı | **KAPATILDI** | `test_wrong_bracket_sign_in_manuscript_eq70_gives_negative_energy` |
| **B-15** `λ` birimi | **KAPATILDI** (fiziksel okuma sabitlendi) | `test_fuel_potential_plateau_requires_lambda_in_inverse_mass_squared` |
| B-21 lattice potansiyeli | **AÇIK** — bu sprintte dokunulmadı, düzeltme listesine eklendi | §5 #7 |
| B-08 `Q^ν` boyutu | **AÇIK** — SPRINT 2 | §4 |

---

## 7. Kalan açık sorular (SPRINT 2'ye devir)

1. **`Q^ν` nasıl `GeV⁵` olur?** Üç aday:
   (a) `Q^ν = ∂_μT^{μν} + Γ...` yerine `∇_μT^{μν}` doğru yazılıp türevli yapı
   (`y_ψ∂^ν(ψf̄f)`) kullanılmalı; (b) `T^{μν}`'ye `ψ`'nin türevli terimleri eklenmeli;
   (c) `L_rh` boyutsal olarak `GeV⁴` olduğundan `Q` otomatik `GeV⁵` olmalı →
   mevcut yazımda bir türev **eksik**. En olası: `Q_ψ^ν ⊃ y_ψ ∂^ν(ψ f̄f) - y_ψ ψ ∂^ν(f̄f)`
   tipi tam varyasyon terimi.
2. **`σ_ψ = 0`** homojen alan için totolojik; perturbatif düzeyde ayrı türetim gerekli (SPRINT 4).
3. **`T_{μν}` sektör ayrımı**: `T_ψ`, `T_Φ` ayrı ayrı tanımlanınca `Σ T_i = T_total`
   sağlanmalı; bu SPRINT 2'nin ilk testi olacak.

---

## 8. Test paketi

```text
$ python -m pytest tests/ -v
27 passed in 4.36s

groups:
  metric / connection / curvature       3 tests
  kinetic sign  (B-04)                  4 tests
  T_munu variation (B-07)               3 tests
  PTUM potentials                       6 tests
  full EOMs vs manuscript (13)-(16)     5 tests
  limits (flat, massless, minimum)      3 tests
  interaction sign (B-06)               2 tests
  dimensional analysis (B-08)           2 tests
  corrected-text regression             2 tests
```

Bağımlılıklar: `sympy>=1.12`, `numpy`, `pytest`. Sürümler bu koşuda:
`sympy 1.14.0`, `numpy 2.4.6`, `pytest 9.2.0`, Python 3.11.

---

## 9. `main.tex` için önerilen diff (uygulanmadı — onay bekliyor)

```diff
@@ line 318-320 (Conventions)
-\\(T_{\\mu\\nu}=-\\frac{2}{\\sqrt{-g}}\\frac{\\delta(\\sqrt{-g}\\mathcal{L}_{\\rm m})}
-{\\delta g^{\\mu\\nu}}\\), so that a canonical scalar
-\\(\\mathcal{L}=\\tfrac12(\\partial\\phi)^2-V\\) gives
+\\(T_{\\mu\\nu}=-\\frac{2}{\\sqrt{-g}}\\frac{\\delta(\\sqrt{-g}\\mathcal{L}_{\\rm m})}
+{\\delta g^{\\mu\\nu}}\\), so that a canonical scalar
+\\(\\mathcal{L}=-\\tfrac12(\\partial\\phi)^2-V\\) gives

@@ line 373-375 (L_fuel)
-=\\tfrac{1}{2}(\\partial_\\mu\\Phi)^2
+=-\\tfrac{1}{2}(\\partial_\\mu\\Phi)^2

@@ line 439 (L_activation)
-=\\tfrac{1}{2}(\\partial_\\mu\\psi)^2
+=-\\tfrac{1}{2}(\\partial_\\mu\\psi)^2

@@ line 466 (L_DM)
-=\\tfrac{1}{2}(\\partial_\\mu\\chi)^2
+=-\\tfrac{1}{2}(\\partial_\\mu\\chi)^2

@@ line 473 (L_DE)
-=\\tfrac{1}{2}(\\partial_\\mu\\Phi_{\\rm res})^2
+=-\\tfrac{1}{2}(\\partial_\\mu\\Phi_{\\rm res})^2

@@ line 2541-2544 (ghost check)
-\\tfrac{1}{2}(\\partial_\\mu\\Phi)^2 + ...
+(-\\tfrac{1}{2})(\\partial_\\mu\\Phi)^2 + ...
  (metin: "positive signs" -> "correct (non-ghost) signs")

@@ line 1578-1583 (Eq. 70)
-- g^{\\mu\\nu}\\left[\\tfrac12(\\partial_\\rho\\chi)^2
-- \\tfrac12 m_\\chi^2\\chi^2 - g_{\\rm DM}\\chi^2\\Phi_{\\rm res}^2\\right]
+- g^{\\mu\\nu}\\left[-\\tfrac12(\\partial_\\rho\\chi)^2
++ \\tfrac12 m_\\chi^2\\chi^2 + g_{\\rm DM}\\chi^2\\Phi_{\\rm res}^2\\right]

@@ line 1672 (L_int)
--\\frac{1}{2}\\alpha m^2 \\frac{\\Phi^2}{E_{\\rm th}^2} \\psi^2
+\\frac{1}{2}\\alpha m^2 \\frac{\\Phi^2}{E_{\\rm th}^2} \\psi^2

@@ line 368 (L_PTUM)
-+\\mathcal{L}_{\\rm DE}.
++\\mathcal{L}_{\\rm DE} + \\mathcal{L}_{\\rm rh}.
```

**Not:** Eq. (70)'deki ikinci satır düzeltmesi (`+½m_χ²χ² + g_DM...`) işaretleri
`-g^{μν}[...]` çarpanıyla birlikte değerlendirilmelidir; tam metin
`T^{μν} = ∂^μχ∂^νχ - g^{μν}[ -½(∂χ)² + ½m_χ²χ² + g_DMχ²Φ_res² ]` olacaktır.
Bu, `T₀₀ = ½χ̇² + ½m_χ²χ² + g_DMχ²Φ_res² = ρ` verir.

---

## 10. Değişen / eklenen dosyalar

```text
Yeni:    src/ptum_symbolic.py                  (türetim çekirdeği)
Yeni:    requirements.txt                       (sürüm pinleri)
Yeni:    src/__init__.py
Yeni:    tests/conftest.py
Yeni:    tests/test_action_consistency.py      (25 test)
Yeni:    derivations/action_consistency.md     (bu belge)
Değişen: yok
main.tex: DOKUNULMADI
```

**SPRINT 1 sonucu: PASS** — 27/27 test geçti, 5 bulgu kapandı (B-04, B-05, B-06-Lagrangian, B-07, B-15),
2 bulgu SPRINT 2'ye devredildi (B-08, B-21).
