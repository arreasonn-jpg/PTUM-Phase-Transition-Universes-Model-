# SPRINT 3 — Parametrik Rezonans (Mathieu/Floquet) + Kapatılan Üç Açık Madde

**Proje:** PTUM bilimsel olgunluk denetimi
**Sprint:** 3 / 6
**Tarih:** 2026-11-12
**Revizyon:** 2 — SPRINT 4 öncesi açık kapı taraması (bkz. §12)
**Durum:** ✅ Tamamlandı
**Test:** `pytest tests/` → **104/104 PASS** (S1: 27, S2: 33, S3: 44), 32.7 s
**`main.tex`:** ❌ **değiştirilmedi** (`sha256[:16] = ba1a630914b809ae`)

---

## 0. Yönetici Özeti

SPRINT 3 iki işi birleştirdi:

**(i)** SPRINT 2'de "açıkça sınırlı bıraktığım" üç maddeyi kapatmak.
**(ii)** Mathieu/Floquet analizini sayısal olarak yapmak.

**Beş bulgu:**

| # | Bulgu | Önem |
|---|---|---|
| **M-01** | `μ_max ~ 0.545√q`, **q ile lineer değil** (fit üssü 0.504) | Makalenin `qω/2` iddiası yanlış |
| **M-02** | `a = 2q` yolunda rezonans **q ≈ 0.33**'te başlıyor | Eşik yok, iki rejim var |
| **M-03** | **Benchmark'ta q ~ 10⁻⁵ → rezonans HİÇ yok** | İddia kendi parametrelerinde çürüyor |
| **M-04** | İki `T_rh` yolu arasında **~1400 kat** fark | İç tutarsızlık |
| **M-05** | Makale **kendi kendisiyle çelişiyor**: satır 3121 `0.2ω`'yi reddediyor, satır 4163/4208 onu "doğruluyor" | Denetim izi hatası |

**Kapatılan üç madde:**

- **C — Fermiyonik yarı: TAM KANITLANDI.** `d₀T_f^{00} = +y_ψψ̇f̄f = −Q_ψ` sembolik olarak sıfır kalıntıyla gösterildi. `PARTIAL` etiketi kaldırıldı.
- **D — Γ_ψ: ayrıştırıldı.** `β³` üssü **doğru** (bu, makalenin haklı olduğu bir yer). Ama kuartik kanal 1→2 bozunma vermiyor ve iki `T_rh` yolu tutarsız.
- **E — İz anomalisi: kapsamı netleşti.** `Σ Q_i = 0` **hayatta kalıyor** (difeyomorfizm invaryansı anomalili değil); anomali `T^μ_μ`'de. Ama sektör-bazında ayrım şema bağımlı.

---

## 1. A) Mathieu / Floquet Analizi

### 1.1 Denklem ve normalizasyon

`L = ½(∂χ)² − ½m_χ²χ² − g_DM χ²Φ_res²` ve `Φ_res = A cos(ωt)`:

```
χ'' + [m_χ² + 2g_DM A² cos²(ωt)] χ = 0
χ'' + [m_χ² + g_DM A² + g_DM A² cos(2ωt)] χ = 0
```

`z = ωt` ile standart Mathieu biçimi `χ_zz + [a + 2q cos 2z]χ = 0`:

```
q_std = g_DM A² / (4ω²)          a_std = (m_χ² + g_DM A²/2)/ω²
```

**Makale `q = g_DM A²/ω²` yazıyor — standart normalizasyonun 4 katı.**
`μ(q)` asimptotikleri *standart* `q` için geçerli olduğundan bu, doğrudan bir
sayısal hata kaynağıdır (`test_manuscript_q_normalisation_differs_by_four`).

### 1.2 Yöntem

Floquet üssü **monodromi matrisinden** hesaplandı:

```
d/dz [χ, χ_z] = [[0, 1], [−(a + 2q cos 2z), 0]] [χ, χ_z]
M = monodromi(z: 0 → π),    μ = ln|ρ_max(M)| / π
```

İki **bağımsız** integratör kullanıldı ve karşılaştırıldı:

- sabit adımlı RK4 (adım sayısı parametrik),
- `scipy.solve_ivp`, DOP853, `rtol=1e-11`.

Uyum: **1e-8** mertebesinde. Adım sayısı 100→800 arasında `μ` değişimi `< 1e-6`.
(`test_monodromy_converges_with_the_step_count`, `test_two_independent_integrators_agree`)

### 1.3 BULGU M-01: `μ_max` q ile lineer DEĞİL

Sayısal tarama (`a ∈ [0.01, 6]`, 500 nokta):

| q | μ_max | μ/q | μ/√q |
|---|---|---|---|
| 10 | 1.772 | 0.177 | 0.560 |
| 100 | 5.239 | 0.052 | 0.524 |
| 1000 | 17.25 | 0.017 | 0.545 |
| 2000 | 24.20 | 0.012 | 0.541 |

**Güç yasası fiti: `μ_max ∝ q^0.504`.**

```
μ_max ≈ 0.545 √q          (z birimlerinde)
```

Enerji birimlerinde (`q ≫ 1`): `μ_max ω_res ≈ 0.27 √(g_DM) A_res`.

**Yani büyüme hızı `qω/2` değil, `√q` ile ölçekleniyor.** Makalenin
"`μ_max ≈ qω_res/2`" iddiası `q ~ 10⁶`'da gerçek değerin `~10⁶/√(10⁶) ≈ 10³`
katı fazla tahmin ediyor.

### 1.4 BULGU M-02: Rezonans eşiği `q ≈ 0.33`

PTUM'un `k = 0` modu `m_χ ≪ ω_res` ile **`a = 2q`** eğrisi üzerinde oturur
(`a_std = gA²/2ω² = 2q_std`). Bu eğri üzerinde:

| q | a=2q | μ |
|---|---|---|
| 0.20 | 0.40 | 0 |
| 0.30 | 0.60 | 0 |
| **0.329** | **0.658** | **0⁺ (eşik)** |
| 0.35 | 0.70 | 0.109 |
| 0.50 | 1.00 | 0.243 |
| 1.00 | 2.00 | 0 |
| 2.00 | 4.00 | 0.182 |
| 10.0 | 20.0 | 0.270 |

Bisection: **`q_crit = 0.329`**. Altında büyüme yok; üstünde bant açılıyor.

### 1.5 BULGU M-03: Benchmark rezonans bölgesinin DIŞINDA

`ω_res = 10¹³ GeV`, `A_res = ω_res`, `m_χ ≪ ω_res` için:

| `g_DM` | `q_std` | `a_std` | `μ` | Kararlı? |
|---|---|---|---|---|
| 10⁻⁶ | 2.5×10⁻⁷ | 5×10⁻⁷ | 0 | ✅ kararlı |
| 10⁻³ | 2.5×10⁻⁴ | 5×10⁻⁴ | 0 | ✅ kararlı |
| 10⁻¹ | 2.5×10⁻² | 5×10⁻² | 0 | ✅ kararlı |
| 1 | 0.25 | 0.50 | 0 | ✅ kararlı |
| **2** | 0.50 | 1.00 | **0.243** | ❌ kararsız |

**Sonuç:** Rezonans için `g_DM ≳ 5.3` gerekiyor (`A_res = ω_res`'te).
Makale `g_DM = O(10⁻³)`–`O(1)` aralığında çalışıyor — bu bölgede **üstel
büyüme yoktur**. Dolayısıyla parametrik rezonansla `Ω_χh² ~ 0.12` üretme iddiası,
makalenin kendi benchmark parametrelerinde **geçersizdir**.

Bu, SPRINT 0'da "EKSİK: tam sayısal integrasyon gerekli" diye bıraktığım
maddenin **kapandığı** anlamına gelir: eksik olan entegrasyon değil, rezonansın
hiç tetiklenmediği gerçeğiydi.

### 1.6 BULGU M-05: Makale kendi kendisiyle çelişiyor

| Satır | İfade |
|---|---|
| 3121 | `μ_max ≈ q ω_res/2` — "**GÖSTERİLDİ**" |
| 3122–3123 | "the earlier draft's `μ_max ≈ 0.2ω_res` was a narrow-resonance estimate **and is not used here**" |
| 4162–4163 | "lattice … confirming Floquet exponent `μ_max ≈ 0.2ω_res`" |
| 4207–4209 | "lattice `μ_max^lattice = 0.198 ± 0.005 ω_res` **matches** the analytic `μ_max ≈ 0.2ω_res`" |

Yani MD-1 (analitik, `qω/2`) ile MD-2 (lattice, `0.2ω`) birbirini
**doğrulamıyor**; `q ≫ 1`'de iki ifade `q/2 / 0.2 ≈ q/0.4` kadar farklı.
Lattice "doğrulaması" reddedilmiş bir formülü doğruladığını iddia ediyor.

**Gerçek durum:** `0.2ω_res` sabiti `q ~ 0.1–1` aralığında kabaca doğru
(`a=2q` yolunda `μ(0.5, 0.25) ≈ 0.24`), ama `q ≫ 1`'de yanlış — ve o rejimde
doğru olan da `q/2` değil, `0.545√q`.

---

## 2. C) Fermiyonik Yarı — TAM KANIT

### 2.1 Konvansiyonlar

`(−+++)`, `{γ^μ, γ^ν} = 2η^{μν}`, `η = diag(−1,+1,+1,+1)`:

```
γ⁰ = −i diag(1,1,−1,−1)        (γ⁰)² = −1
γⁱ = −i [[0, σⁱ], [−σⁱ, 0]]     (γⁱ)² = +1
```

Clifford cebiri ve Hermitiklik testlerle doğrulandı
(`test_gamma_matrices_satisfy_the_clifford_algebra`,
`test_gamma_hermiticity_matches_the_metric_signature`).

> Not: ilk denememde yanlış γ matrisleri yazdım ve `(γ¹)² = −1` çıktı. Testler
> bunu yakaladı. Bu, testlerin gerçek işlev gördüğünün bir başka kanıtı.

### 2.2 Etkileşen Dirac denklemi

`L_int = −y_ψ ψ f̄f`, homojen ψ:

```
iγ⁰∂₀f − m_f f − y_ψψf = 0
⟹  ∂₀f = i(m_f + y_ψψ) γ⁰ f
```

Yani kondensat **kütle kayması** yapıyor: `m_f → m_f + y_ψψ`. Bu, standart
"skaler kondensat fermiyona kütle verir" ifadesidir; varsayım değil, denklemin
kendisidir. `test_onshell_derivatives_solve_the_dirac_equation` bunu doğrular.

### 2.3 İki korunum yasası

**(a) Vektör akımı korunur:** `∂_μ(f̄γ^μf) = 0`.
Sebep: `f̄γ^μf` fermiyon sayısını sayar, `f̄f` sayı-nötrdür → Yukawa terimi
kaynak olamaz. `test_vector_current_is_conserved`.

**(b) Skaler bilineer korunur:** `∂₀(f̄f) = 0`.
Sebep: `∂₀(f̄f) = (∂₀f̄)f + f̄(∂₀f) = −iM f̄γ⁰f + iM f̄γ⁰f = 0`.
`test_fbar_f_is_conserved`.

> **Özeleştiri:** İlk testim `f̄γ⁰f = 0` varsayıyordu. Bu **yanlıştı** —
> `f̄γ⁰f = n_f`, sayı yoğunluğudur ve sıfır değildir. Test düzeltildi.
> Ama `∂₀(f̄f) = 0` sonucu doğru çıktı, çünkü iki terim birbirini götürüyor.

### 2.4 Stres tensörü ve kapanış

Homojen alan için Belinfante tensörü:

```
T_f^{00} = (m_f + y_ψψ) f̄f
```

Türev:

```
∂₀T_f^{00} = y_ψ ψ̇ f̄f  (çünkü ∂₀(f̄f) = 0)
```

**Ve `−Q_ψ = +y_ψψ̇f̄f`. Dolayısıyla:**

```
∂₀T_f^{00} = −Q_ψ   ⟹   Q_f = +y_ψψ̇f̄f = −Q_ψ
```

Sembolik kalıntı **tam sıfır**. `test_fermionic_half_closes_the_yukawa_transfer`,
`test_Q_f_equals_minus_Q_psi` (SPRINT 2'nin `Q_ψ`'si ile çapraz kontrol).

**`PARTIAL` etiketi kaldırıldı.** Kalan tek sınırlama: düz uzayda ve homojen ψ
için kanıtlandı; FRW düzeltmeleri `H/ω ~ 10⁻³` mertebesinde olduğundan ihmal
edilebilir, ama *tam* FRW ifadesi türetilmedi (`KOŞULLU`).

---

## 3. D) Γ_ψ ve Reheating

### 3.1 `β` üssü — makale HAKLI

Gerçek skaler `ψ` (kanonik `½(∂ψ)² − V`), Dirac çiftine bağlanıyor. Gerçek
skaler için çift **p-dalgasında** olmak zorunda (antisimetri) → `β³`:

```
Γ(ψ → f f̄) = y_ψ² m_ψ β³ / 8π ,    β = √(1 − 4m_f²/m_ψ²)
```

Makale `(1 − 4m_f²/m_ψ²)^{3/2}` yazıyor = `β³`. **Doğru.**
(`test_yukawa_width_power_of_beta`, `test_manuscript_beta_power_is_consistent`)

Bu, denetimde makalenin **haklı çıktığı** nadir yerlerden biri; raporda
belirtilmeli.

### 3.2 Kuartik kanal: 1→2 bozunma YOK

`L = −½g_ψψ²φ_SM²`. `⟨ψ⟩ = 0` iken `∂L/∂ψ = −g_ψψφ_SM² → 0` at `ψ = 0`.

Tek-parçacık matris elemanı `⟨φφ|L|ψ⟩ = 0` çünkü `ψ` **kuadratik** geçiyor.
Önde gelen süreç `ψψ → φφ` yok edilmesi:

```
σ ~ g_ψ²/(16πs)
```

Etkin hıza çevirmek için **sayı yoğunluğu** gerekir:

```
Γ_eff = n_ψ ⟨σv⟩
```

`n_ψ` Lagrangian'da yok — kinetik-teori girdisidir.

**Etiket: `Q_SM ≈ Γ_ψρ_ψ` kuartik kanal için `FENOMENOLOJİK`, Yukawa kanalı
için `KOŞULLU`.**

`test_no_single_particle_decay_from_the_quartic`,
`test_annihilation_requires_a_density`

### 3.3 BULGU M-04: İki `T_rh` yolu tutarsız

Makale iki farklı yerde iki farklı `T_rh` tarifi kullanıyor:

| Yol | Formül | Benchmark değeri |
|---|---|---|
| (a) Bozunma | `T_rh = (90/π²g_*)^{1/4} √(Γ_ψM_Pl)` | `3.0×10¹²` GeV |
| (b) Ani dönüşüm | `T_rh = (30V₀/π²g_*)^{1/4}` | `4.2×10¹⁵` GeV |

**Oran: `(a)/(b) = 7.3×10⁻⁴`** — yaklaşık **1400 kat** fark.

İkisini eşitleyen `Γ`: `2.4×10¹³` GeV, oysa benchmark'ta `Γ_ψ = 1.3×10⁷` GeV.

**Yorum:** (b) yolu "V₀ tamamen ve anında radyasyona dönüşür" varsayımını
içeriyor. Bu, makalenin fiziksel içeriğidir ve **doğrulanmamıştır**. (a) yolu
ise perturbatif bozunmayı varsayıyor. İkisi aynı anda doğru olamaz.

`test_two_T_rh_routes_disagree_at_the_benchmark`

### 3.4 Kondensat uyarısı

Perturbatif genişlik, koherent salınan bir kondensata uygulanamaz; şu üç koşul
gerekir:

1. Hubble zamanı başına çok sayıda salınım (`m_ψ ≫ H`),
2. küçük geri-tepme (backreaction),
3. kuantum modlarına ayrışma.

Aksi halde süreç **parametrik rezonanstır**, bozunma değil.
`test_condensate_caveat_is_stated`

---

## 4. E) İz Anomalisi ve `ΣQ = 0`'ın Kuantum Statüsü

### 4.1 İki farklı ifade

| İfade | Kuantum durumu |
|---|---|
| `∇_μT^{μν}_total = 0` | **Tam** (difeyomorfizm invaryansı anomalili değil) |
| `⟨T^μ_μ⟩ = Σβ_i ∂L/∂g_i` | **Anomalili** |
| `Σ_i Q_i^ν = 0` | **Hayatta kalır** |

**Sonuç:** SPRINT 2'nin `ΣQ=0` sonucu kuantum seviyesinde de geçerli.
Anomali `T^μ_μ`'de, `∇_μT^{μν}`'de değil. `test_anomaly_is_a_trace_statement_only`

### 4.2 Ama sektör ayrımı şema bağımlı

`⟨T_i^{μν}⟩` tek tek şema bağımlıdır. `Φ → (1+ε)Φ`, `ψ → (1−ε)ψ` gibi bir alan
yeniden ölçeklemesi:

- `Q_Φ, Q_ψ` değişir,
- `Q_Φ + Q_ψ = 0` değişmez.

Bu, SPRINT 2'de bulunan **tahsis bağımlılığının kuantum versiyonudur**.
`test_scheme_dependence_of_individual_transfers`

### 4.3 Çalışan düzeltmenin boyutu

`δQ/Q ~ (β_λ/λ)·ln(μ₁/μ₂)`. `λ = 0.1`, bir dekad için:

```
β_λ = 3λ²/16π² = 1.9×10⁻⁴      δQ/Q ≈ 1.9×10⁻²
```

Yani `O(1%)`. SPRINT 2'nin işaret yapısını değiştirmez.
`test_running_correction_is_small`

### 4.4 Açık kalanlar (gizlenmiyor)

`src/ptum_anomaly.py` içinde `OPEN_QUESTIONS` olarak kayıtlı:

1. Tekil "sektör enerjisi" klasik ayrımın ötesinde mevcut değil.
2. Anomalinin sayısal önemi `T_rh`'ye bağlı — o da belirsiz (bkz. M-04).
3. Non-perturbatif etkiler anomali ile yakalanmaz → SPRINT 5.

---

## 5. Birim ve İşaret Analizi (özet)

| Nicelik | Boyut | Kontrol |
|---|---|---|
| `μ` | boyutsuz | ✅ |
| `μ ω_res` | GeV | ✅ |
| `q, a` | boyutsuz | ✅ |
| `Q_f = yψ̇f̄f` | GeV⁵ | ✅ |
| `Γ_ψ` | GeV | ✅ |
| `T_rh` | GeV | ✅ |
| `S_obs` | boyutsuz | ✅ (`∝ g_*^1 T^3`) |

**İşaret analizi:** `Q_f = −Q_ψ` (fermiyon kazanır, skaler kaybeder) —
SPRINT 2'nin işaret konvansiyonuyla tutarlı.

---

## 6. Test Envanteri

`tests/test_sprint3.py` — **35 test**

| Grup | # | Doğrulanan |
|---|---|---|
| Mathieu yakınsama | 3 | Adım bağımsızlığı, iki integratör uyumu, bant dışı sıfır |
| `μ_max` ölçeklenmesi | 2 | Üs ~0.5 (lineer değil), katsayı 0.545 |
| Rezonans eşiği | 2 | `q_crit = 0.329`, benchmark dışında |
| Normalizasyon | 2 | Makale `q`'su 4 kat; e-fold dönüşümü |
| Reheating | 6 | `β³`, kuartik tepe yok, yoğunluk gerekli, iki `T_rh` |
| Fermiyon | 8 | Clifford, Hermitiklik, Dirac, 2 korunum, `T⁰⁰`, kapanış, boyut, limitler |
| Entropi | 3 | Üsler (1 ve 3), normalizasyon, `KOŞULLU` etiketi |
| Anomali | 5 | İz-yalnız, beta katsayıları, küçük düzeltme, şema, açık sorular |

Toplam depo: **95 test**.

---

## 7. Bulgu Tablosu

| ID | Dosya/denklem | Önceki durum | Yapılan | Test | Sonuç |
|---|---|---|---|---|---|
| M-01 | `main.tex` 3121 | "`μ_max ≈ qω/2` (GÖSTERİLDİ)" | Sayısal `μ_max(q)` taraması, güç yasası fiti | `test_mu_max_scales_as_sqrt_q_not_linearly` | **HATALI** — `0.545√q` |
| M-02 | 3095–3110 | "bant `A_k ≈ 1`" | `a = 2q` yolu üzerinde bisection | `test_ptum_locus_instability_onset` | **EKSİK** — eşik `q=0.329` |
| M-03 | 3100–3150 | "rezonans `Ω_χh²~0.12` üretir" | Benchmark taraması | `test_benchmark_is_outside_the_resonance_region` | **HATALI** — rezonans yok |
| M-04 | 1740–1770 | tek `T_rh` gibi sunuluyor | İki yol karşılaştırması | `test_two_T_rh_routes_disagree_at_the_benchmark` | **HATALI** — 1400× fark |
| M-05 | 3121 vs 4163 | çelişki | Satır karşılaştırması | (rapor §1.6) | **HATALI** — iç çelişki |
| M-06 | 3090 `q` tanımı | `q = gA²/ω²` | Standart normalizasyonla karşılaştırma | `test_manuscript_q_normalisation_differs_by_four` | **HATALI** — 4 kat |
| C-01 | S2 §8 "PARTIAL" | Fermiyon yarı eksik | Dirac denklemiyle türetim | `test_fermionic_half_closes_the_yukawa_transfer` | **KAPANDI** |
| D-01 | 1720 `β³` | — | Faz uzayı kontrolü | `test_yukawa_width_power_of_beta` | **DOĞRU** (makale haklı) |
| D-02 | 1726 kuartik | "`Γ_ψ`" | Tepe noktası analizi | `test_no_single_particle_decay_from_the_quartic` | **FENOMENOLOJİK** |
| E-01 | S2 §7.3 | "kuantumda koşullu" | İz anomalisi analizi | `test_anomaly_is_a_trace_statement_only` | **ΣQ=0 HAYATTA** |

---

## 8. `main.tex` için Değişiklik Önerisi (UYGULANMADI)

### 8.1 Satır 3085–3095 — `q` normalizasyonu

```diff
-q \equiv \frac{2g_{\rm DM}\mathcal{A}_{\rm res}^2}{2\omega_{\rm res}^2}
-= \frac{g_{\rm DM}\mathcal{A}_{\rm res}^2}{\omega_{\rm res}^2},
-\qquad
-A_k \equiv \frac{k^2/a^2+m_\chi^2}{\omega_{\rm res}^2}.
+q \equiv \frac{g_{\rm DM}\mathcal{A}_{\rm res}^2}{4\omega_{\rm res}^2},
+\qquad
+a_k \equiv \frac{k^2/a^2+m_\chi^2+g_{\rm DM}\mathcal{A}_{\rm res}^2/2}{\omega_{\rm res}^2},
```
(gerekçe: standart Mathieu normalizasyonu `χ'' + [a + 2q cos 2z]χ = 0`)

### 8.2 Satır 3119–3124 — `μ_max` iddiası

```diff
-For the broad resonance regime ($q \gg 1$),
-the maximum Floquet exponent is $\mu_{\rm max} \approx q\,\omega_{\rm res}/2$
-(GÖSTERİLDİ from the standard Mathieu asymptotics; the earlier draft's
-$\mu_{\rm max}\approx0.2\,\omega_{\rm res}$ was a narrow-resonance
-estimate and is not used here).
+A numerical solution of the monodromy problem (two independent integrators,
+agreeing to $10^{-8}$) gives $\mu_{\rm max}\approx0.545\sqrt{q}$ in units of
+$\omega_{\rm res}$ for $q\gtrsim10$; the growth rate is therefore
+$\sim0.27\sqrt{g_{\rm DM}}\,\mathcal{A}_{\rm res}$, \emph{not} linear in $q$.
+The earlier draft's $\mu_{\rm max}\approx0.2\,\omega_{\rm res}$ is a fair
+approximation only for $q\sim0.1$--$1$ (SAYISAL DOĞRULANDI).
```

### 8.3 Yeni paragraf (satır 3100 sonrası) — rezonans eşiği

```diff
+\noindent\textbf{Threshold for resonance.}  Along the locus
+$a_k=2q$ that the $k=0$ mode follows, the instability band opens only at
+$q_{\rm crit}\simeq0.33$, i.e.\ $g_{\rm DM}\mathcal{A}_{\rm res}^2\gtrsim
+1.3\,\omega_{\rm res}^2$.  For $g_{\rm DM}=10^{-3}$ and
+$\mathcal{A}_{\rm res}=\omega_{\rm res}$ one has $q\simeq2.5\times10^{-4}$,
+so \emph{no} parametric resonance occurs at the stated benchmark
+parameters (SAYISAL DOĞRULANDI).  Either $g_{\rm DM}\gtrsim5$ or a
+different production channel is required.
```

### 8.4 Satır 4160–4210 — lattice "doğrulaması"

```diff
-\item \textbf{Parametric resonance:} The lattice Floquet exponent
-      $\mu_{\rm max}^{\rm lattice} = 0.198 \pm 0.005\,\omega_{\rm res}$
-      matches the analytic $\mu_{\rm max} \approx 0.2\,\omega_{\rm res}$.
+\item \textbf{Parametric resonance:} The quoted lattice value
+      $0.198\,\omega_{\rm res}$ is consistent with the analytic
+      $\mu_{\rm max}\approx0.2\,\omega_{\rm res}$ only in the window
+      $q\sim0.1$--$1$; at the benchmark $q\simeq2.5\times10^{-4}$ no band
+      exists, so this comparison does not validate the production model.
```

### 8.5 Satır 1740–1775 — iki `T_rh` yolu

```diff
+Only one of the two estimates below can hold: the instantaneous-conversion
+route gives $T_{\rm rh}\sim4\times10^{15}\,\mathrm{GeV}$, the perturbative-decay
+route gives $3\times10^{12}\,\mathrm{GeV}$; they differ by a factor $\sim1400$
+at the benchmark point.  The entropy budget $S_{\rm obs}\sim10^{88}$ inherits
+this ambiguity and is a consistency check, not a prediction.
```

### 8.6 Fermiyonik kapanış (SPRINT 2 §8'in kaldırılması)

Satır 1686'daki Yukawa `Q_SM` düzeltmesi (SPRINT 2 §9.1) artık **kanıtlanmıştır**;
"`Q_f` türetilmedi" notu kaldırılabilir.

---

## 9. Sınırlar

| Konu | Durum | Etiket |
|---|---|---|
| `μ_max(q)`, eşik, benchmark | Sayısal, 2 integratör | SAYISAL DOĞRULANDI |
| Fermiyonik kapanış (düz uzay) | Sembolik, kalıntı 0 | TÜRETİLDİ |
| Fermiyonik kapanış (FRW) | Spin bağlantısı dahil, kalıntı 0 | **TÜRETİLDİ** (rev.2) |
| `β³` üssü | Faz uzayı argümanı | ANALİTİK DOĞRULANDI |
| Kuartik kanal `Γ` | Lagrangian vermiyor | FENOMENOLOJİK |
| `S_obs ~ 10⁸⁸` | Ani dönüşüm varsayımı | KOŞULLU |
| İz anomalisi sayısal önemi | `T_rh` belirsizliği | EKSİK |
| Geri-tepme, backreaction | Kapalı-form üst sınır türetildi | **TÜRETİLDİ** (rev.2), sayısal sim. EKSİK |
| Lattice verisi | Kod yok, doğrulanamaz | EKSİK |

---

## 10. SPRINT 4'e Devredilenler

1. **Mikroskopik alan vs. proxy-akışkan ayrımı** — `w_ψ` %99.99 `< −1` bulgusu.
2. **Rezonans yoksa `Ω_χh² = 0.12` nasıl açıklanıyor?** Alternatif üretim kanalı
   (`Φ_res`'in doğrudan bozunması? gravitasyonel üretim?) değerlendirilmeli.
3. **İki `T_rh` yolundan hangisi kullanılıyor** — makale boyunca tutarlı seçim.
4. **`g_DM` değerinin bağımsız gerekçesi** — `O(10⁻³)` nereden geliyor?

---

## 11. Onay Talebi

SPRINT 3 tamamlandı. **`main.tex` değiştirilmedi.**

1. Bu raporun içeriği (M-01…M-06, kapatılan C/D/E).
2. §8'deki altı maddelik diff önerisi — **ayrı onay** gerektirir.
3. SPRINT 2'nin `PARTIAL` etiketinin kaldırılması.

Onayınızla SPRINT 4'e (mikroskopik alan vs. proxy-akışkan) geçebilirim.

---

## 12. Revizyon 2 — SPRINT 4 öncesi açık kapı taraması

SPRINT 4'e geçmeden önce SPRINT 3'ün kendi bıraktığı `KOŞULLU` ve `EKSİK`
etiketlerini tek tek gözden geçirdim. Üçü kapatıldı, biri daraltıldı, ve
**kendi kodumda bir tutarsızlık** buldum.

### 12.1 C2 — Fermiyonik FRW kapanışı: `KOŞULLU` → `TÜRETİLDİ`

SPRINT 3'te "FRW'de `H/ω` mertebesinde, ihmal edilebilir ama türetilmedi"
demiştim. Türettim.

FRW'de homojen bir mod için Dirac denklemi spin bağlantısı terimi taşır:

```
iγ⁰∂₀f + (3i/2)H γ⁰f = (m_f + y_ψψ)f
⟹  ∂₀f = [i(m_f + y_ψψ)γ⁰ − (3/2)H] f
```

Spin bağlantısı terimi **gerçek** ve `f` ile aynı şekilde çarpılıyor; bu yüzden
kütle teriminin aksine bilineerlerde **kalmaz değil, kalır**:

```
∂₀(f̄f) = −3H(f̄f)                              (bilineer kırmızıya kayar)
T_f^{00} = (m_f + y_ψψ)f̄f
∂₀T_f^{00} = [y_ψψ̇ − 3H(m_f + y_ψψ)] f̄f
```

Yani

```
Q_f = y_ψψ̇f̄f − 3Hρ_f = −Q_ψ − 3Hρ_f
```

İkinci terim **sektörler arası transfer değil**, fermiyon enerjisinin
seyrelmesidir — süreklilik denkleminin sol tarafındaki `3Hρ` parçasının ta
kendisi. Onu oraya yazınca:

```
ρ̇_f + 3H(ρ_f + p_f) = Q_f   ⟹   Q_f = −Q_ψ
```

düz uzay sonucu geri geliyor. **`KOŞULLU` etiketi kaldırıldı.**

Testler: `test_frw_bilinear_redshifts`, `test_frw_fermionic_closure`,
`test_frw_reduces_to_flat_space`, `test_redshift_term_is_not_a_transfer`.

### 12.2 Geri-tepme: uydurma simülasyondan kapalı-form sınıra

İlk denemem `dA/dz = −(sabit)·ρ_χ·A/(1+ρ_χ)` gibi **uydurma** bir sönüm terimi
içeren bir ODE sistemiydi. Onu raporlayamam — kuplajı ben seçmiştim, sonuç
fiziğin değil seçimin ürünüydü. Attım.

Yerine **türetilebilir** olan kriteri koydum. Parametrik rezonans analizi `χ`'yi
sabit `Φ_res` içinde bir **test alanı** olarak ele alır. Bu, `Φ_res`
denklemindeki geri-tepme terimi küçük olduğu sürece geçerlidir:

```
Φ_res'' + 3HΦ_res' + W' + 2g_DM χ²Φ_res = 0
⟹   2g_DM⟨χ²⟩ ≪ ω_res²
```

`χ ∝ exp(μωt)` ile `⟨χ²⟩ = χ₀²e^{2μωt}`:

```
┌─────────────────────────────────────────────────────────┐
│   B ≡ 2μω t_br = ln[ ω_res² / (2 g_DM χ₀²) ]            │   (#)
└─────────────────────────────────────────────────────────┘
```

Yani rezonansın kendini kapatmadan önce koşabileceği e-fold sayısı, kuplaja
**yalnızca logaritmik** olarak bağlı. `g_DM` iki katına çıkarmak sadece `ln2`
e-fold maliyetindedir.

**Dürüst sınır:** `B`, `χ₀`'a bağlıdır. 10 dekad `χ₀` farkı `2ln(10¹⁰) ≈ 46`
e-fold demektir. Bu yüzden bunu bir **üst sınır** olarak raporluyorum, tahmin
olarak değil. `χ₀` başlangıç genliği PTUM'da bağımsız olarak sabitlenmiyor —
`EKSİK` kalıyor.

Testler: `test_backreaction_bound_formula`,
`test_backreaction_is_logarithmic_in_the_coupling`,
`test_backreaction_none_without_a_resonance`,
`test_backreaction_depends_on_the_assumed_amplitude`.

### 12.3 Kendi kodumdaki tutarsızlık

`src/ptum_mathieu.py` içinde `mu_broad_resonance_literature(q)` adlı bir
yardımcı vardı ve **`0.2` döndürüyordu** — yani ölçtüğüm `0.545√q` sonucuyla
çelişiyordu. Hiçbir yerde kullanılmıyordu ama modülde "sonuç" gibi duruyordu.

Düzelttim: fonksiyon artık `NotImplementedError` atıyor ve docstring'de
"superseded, use `mu_max_asymptotics()`" diyor.
Test: `test_superseded_placeholder_raises`.

### 12.4 Kapatılmayan (ve neden)

| Konu | Durum | Neden |
|---|---|---|
| `χ₀` başlangıç genliği | `EKSİK` | PTUM'da bağımsız olarak sabitlenmiyor (12.2) |
| Geri-tepme sayısal simülasyonu | `EKSİK` | Güvenilir bir kuplaj türetimi gerektirir; uydurma olur |
| Lattice verisi | `EKSİK` | Kod yok, `PTUM.zip`'te `run_lattice.py` bulunamadı |
| İz anomalisi sayısal önemi | `EKSİK` | `T_rh` belirsizliğine bağlı (M-04) |

**Bunlar SPRINT 5'in konusu** (sayısal yeniden üretilebilirlik). SPRINT 4'ü
engellemiyorlar.

### 12.5 Bu turda bulduğum kendi test hatalarım

Dördü de testlerin işe yaradığını gösteriyor:

1. `t` sembolünü import etmeyi unuttum → `NameError`.
2. Geri-tepme bağımlılığında `2ln(1e40)` yazdım, doğrusu `2ln(5e24)` — `χ₀`
   değerleri 1e-25 ve **0.5**, oranları `1e25` değil.
3. Fonksiyonun `ratio < 1` için 0'a kırptığını hesaba katmadım.
4. **İşareti ters yazdım:** "büyük `χ₀` → çok e-fold" sandım; doğrusu
   **küçük** `χ₀` → çok e-fold (daha geç geri-tepme).

Hiçbiri fiziksel sonucu değiştirmedi; dördü de test/ifade hatasıydı.
