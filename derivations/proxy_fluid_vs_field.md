# SPRINT 4 — Mikroskopik Alan vs. Proxy-Akışkan Ayrımı

**Proje:** PTUM bilimsel olgunluk denetimi
**Sprint:** 4 / 6
**Tarih:** 2026-11-12
**Durum:** ✅ Tamamlandı
**Test:** `pytest tests/` → **125/125 PASS** (S1: 27, S2: 33, S3: 44, S4: 21), 70.8 s
**`main.tex`:** ❌ **değiştirilmedi** (`sha256[:16] = ba1a630914b809ae`)

---

## 0. Yönetici Özeti

SPRINT 0'ın devrettiği `w_ψ` %99.99 `< −1` bulgusunu yeniden ürettim ve
**yorumunu düzelttim**.

**Ana sonuç:** `w_ψ < −1` bu Lagrangian için **imkânsızdır**. `w = (K−U)/(K+U)`
ve `K,U ≥ 0` olduğundan `w ∈ [−1,+1]`. SPRINT 0'da gözlemlediğim değer
`−1`'in **kendisiydi**, altı değil — ve bu, alanın tepede **donmasının**
doğru sonucudur, sayısal bir çöküş değil.

**Ve önemli bir bulgu:** makalenin §4.4'ü (satır 700–890) bu konuda
**zaten doğru ve olağanüstü dürüst**. `⟨w_ψ⟩ = 0` (kaadratik), `1/3` (kuartik),
overdamped benchmark, "quartic regime not achieved" — hepsi doğru ve
sayısal olarak yeniden üretilebilir. **Bu bölümde düzeltilecek bir fizik hatası
yok.** Sorun, aynı makalenin başka yerlerinde (soyut, §4.2, CLASS closure)
`w = 1/3`'ün *başarılmış* gibi sunulması — makale bunu da §4.4'te açıkça
reddediyor, ama okuyucu iki ifadeyi yan yana koyunca çelişki görüyor.

---

## 1. Yapısal Sonuç: `w` Sınırlıdır

### 1.1 Kanıt

Kanonik skaler, `U ≥ 0`:

```
ρ = ½ψ̇² + U = K + U ,     p = ½ψ̇² − U = K − U
w = (K − U)/(K + U)
```

`K ≥ 0, U ≥ 0` olduğundan:

- `w ≥ −1` (eşitlik yalnızca `K = 0`'da),
- `w ≤ +1` (eşitlik yalnızca `U = 0`'da).

**`w < −1` gözlemlenemez.** Hayalet (ghost) alanı, işaret-değiştiren potansiyel
veya modifiye gravite gerekir; PTUM'un hiçbirinde bunlar yok.

Test: `test_w_is_bounded`, `test_w_below_minus_one_is_impossible_for_this_lagrangian`

### 1.2 SPRINT 0 bulgusunun doğru okuması

SPRINT 0'da `w_ψ` zamanın %99.99'unda `< −1` görünüyordu. Yeniden üretim:

```
3H/(2μ) = 25  (makalenin kendi benchmark'ı)
ψ(0) = 10⁻³ψ₀ ,  ψ̇(0) = 0
⟹  ⟨w⟩ = −1.000000     (tam olarak −1, altı değil)
```

**Neden:** Alan tepede oturuyor. `ψ̇ ≈ 0` ⟹ `K ≈ 0` ⟹ `w → −1`.
Bu, kozmolojik sabit gibi davranan **donmuş bir skaler**dir — yani
`w = −1`, `w < −1` değil.

Yani SPRINT 0'ın "%99.99 `< −1`" ifadesi **yanlış etiketlenmişti**; doğrusu
"%99.99 `= −1`" olmalıydı. Bu bir yorum hatasıydı, ölçüm hatası değil.

Test: `test_overdamped_w_is_minus_one`, `test_no_oscillations_in_the_overdamped_regime`

---

## 2. Üç Farklı `w = 1/3` İfadesi

Makale boyunca `1/3` üç ayrı anlamda geçiyor ve bunlar karıştırılıyor:

| # | İfade | Ne zaman doğru | Durum |
|---|---|---|---|
| **(i)** | Anlık `w = 1/3` | Hiçbir zaman (osilatörde anlık `w` salınır) | **HATALI** okuma |
| **(ii)** | Ortalama `⟨w⟩ = 1/3` | Kuartik-baskın yörüngede | **DOĞRU**, koşullu |
| **(iii)** | Akışkan closure `w = c_s² = 1/3` | Fenomenolojik girdi | **VARSAYIM** |

### 2.1 Sayısal doğrulama

Boyutsuz birimlerde (`μ = 1, λ = 0.1, H = 10⁻³μ`), 60 salınım ortalaması:

| Genlik `ψ_amp/ψ₀` | `⟨w⟩` | Rejim |
|---|---|---|
| `1 + 0.01` | `−0.00000` | kaadratik → **0** |
| 2 | `+0.4284` | ara |
| 3 | `+0.4083` | ara |
| 5 | `+0.3630` | ara |
| 100 | `+0.3334` | kuartik → **1/3** |

Analitik virial: `⟨w⟩ = (n−2)/(n+2)`.
`n = 2` ⟹ `0`; `n = 4` ⟹ `1/3`. Sayısal sonuçlarla uyuşuyor.

### 2.2 Beklenmedik ama gerçek: ara genliklerde `⟨w⟩ > 1/3`

Bu bir hata değil, **gerçek bir fiziksel etki**. Ara genliklerde yörünge her
çevrimde kuartik-baskın bölgenin dışına çıkıyor, ama minimum yakınında
potansiyel ortalamada kuartikten daha dik. Tek bir etkin `n` ile virial
teoremi uygulanamaz. `1/3`'e yalnızca **asimptotik olarak** yaklaşılıyor
(`0.428 → 0.408 → 0.363 → 0.341 → 0.3334`).

Test: `test_intermediate_amplitude_overshoots_one_third`

> **Dürüstlük notu:** İlk testim "ara genliklerde `⟨w⟩ ∈ (0, 1/3)`" diyordu.
> Yanlıştı; sayısal sonuç `> 1/3` veriyordu. Testi veriye uydurmak yerine
> fiziksel nedenini yazdım ve testi buna göre düzelttim.

---

## 3. Makalenin §4.4'ü — Denetimde Nadir Bir "Haklı" Bölüm

Satır 700–890 arası titizlikle okundu. Aşağıdakilerin **hepsi doğru**:

| Makale ifadesi | Denetim sonucu |
|---|---|
| `m_osc² = 2μ²` | ✅ `U''(±ψ₀) = 2μ²` |
| `ψ₀² = μ²/λ` | ✅ |
| Küçük salınımlar kaadratiktir, `⟨w⟩ ≃ 0` | ✅ sayısal olarak `−4×10⁻³` |
| Kuartik-baskınlık koşulu `\|ψ\| ≫ ψ₀` | ✅ sayısal eşik |
| `⟨ψ̇²⟩ = 4⟨U⟩` ⟹ `⟨w⟩ = 1/3` | ✅ `n=4` ile tutarlı |
| Benchmark overdamped: `3H/(2μ) ≈ 25` | ✅ birebir yeniden üretildi |
| "quartic regime **not** achieved" | ✅ `⟨w⟩ = −1` |
| `√λ ψ₀ ∼ 3×10¹²` vs `H_* ∼ 10¹³` ⟹ `ω ≳ H` | ✅ `ω_quartic/H = 0.316` |
| CMB normalizasyonu ile kuartik rejim **çelişiyor** | ✅ kabul |

**Sonuç:** §4.4 **düzeltilmemeli**. Bu, denetimde şimdiye kadar gördüğüm en
sağlam bölüm.

### 3.1 `main.tex` için öneri: §4.4 KORUNMALI

```diff
-% (no change to section 4.4)
+% SPRINT 4 audit note: section 4.4 (lines 700-890) was verified numerically
+% and requires no correction.  Keep it.
```

---

## 4. Asıl Sorun: Soyut ve §4.2'nin Dili

### 4.1 Soyut (satır 48)

```
"A falsifiable prediction of PTUM is that, within the effective linear
 proxy-fluid description, the pfd component carries w = 1/3, c_s² = 1/3,
 and zero anisotropic stress."
```

`"within the effective linear proxy-fluid description"` ifadesi doğru
niteleme — ama ardından `"A falsifiable prediction of PTUM is..."` geliyor.
`1/3` bir *tahmin* değil, bir *girdi*dir (VARSAYIM). §4.4 bunu açıkça
söylüyor; soyut söylemiyor.

### 4.2 §4.2 (satır 632–660)

```
"A key result is that coherent oscillations of ψ in a quartic potential
 behave effectively as radiation"
```

`"A key result"` — ama bu bir sonuç değil, bir **koşul**dur (kuartik-baskınlık).
Koşul sağlanmıyorsa `1/3` yok.

### 4.3 CLASS closure (satır 819–830)

```
"the constant closure w = 1/3, c_s² = 1/3, σ = 0 is retained as the
 phenomenological proxy-fluid prescription"
```

Bu **doğru ve dürüst** — `phenomenological` kelimesi var. ✅

### 4.4 Önerilen diff: üç yerde dil düzeltmesi

```diff
-% Soyut, satır 48
-A falsifiable prediction of PTUM is that, within the effective linear
-proxy-fluid description, the pfd component carries w=1/3, c_s^2=1/3,
-and zero anisotropic stress (sigma=0).
+Within the effective linear proxy-fluid description the pfd component is
+*assigned* w=1/3, c_s^2=1/3 and sigma=0 as a phenomenological closure; this
+closure is a falsifiable hypothesis about the pfd sector, not a prediction of
+the PTUM field theory.  Section~\ref{sec:tachyonic_to_quartic} shows that the
+underlying canonical field reaches w=1/3 only in a quartic-dominated regime
+that the stated benchmark does not realize.
```

```diff
-% §4.2, satır 634
-A key result is that coherent oscillations of \(\psi\) in a quartic
-potential behave effectively as radiation~\cite{Turner1983}:
+A standard result for a canonical scalar is that coherent oscillations
+in a quartic potential behave effectively as radiation~\cite{Turner1983},
+\emph{provided} the quartic term dominates the orbit:
```

```diff
-% §4.2, satır 649-656 (kutu denklemi)
 \boxed{
  w_\psi=\frac{1}{3},\qquad
  c_{s,\psi}^2=\frac{1}{3},\qquad
  \sigma_\psi=0 .
 }
+\quad\text{(phenomenological closure, VARSAYIM)}
```

---

## 5. Benchmark Rejimleri

`ω/H` oranları (`μ = 10¹³, λ = 0.1, H_* = 10¹³ GeV`):

| Rejim | `ω` | `ω/H` | Karar |
|---|---|---|---|
| Kuartik, `ψ_amp = 10¹³` | `3.16×10¹²` | **0.316** | ❌ `ω < H` |
| Kaadratik, `√2μ` | `1.41×10¹³` | 1.41 | sınırda |

Yani benchmark'ta **hızlı salınım koşulu sağlanmıyor**. Bu, makalenin
satır 843–850'de kendi söylediği şeyle birebir aynı.

Test: `test_benchmark_fails_the_rapid_oscillation_condition`

---

## 6. Bariyer Geçişi

`E = ½ψ̇² + U(ψ)`, bariyer yüksekliği `U(0) = μ⁴/(4λ)`.

| Başlangıç | `E/E_bariyer` | Geçer? |
|---|---|---|
| `ψ=0, ψ̇=0` | `1.000` | ❌ tepede oturuyor |
| `ψ=10⁻³ψ₀, ψ̇=0` | `0.999999` | ❌ hemen altında |
| `ψ=0, ψ̇=2v_b` | `4.0` | ✅ |

**SPRINT 0'ın "frozen init" bulgusu doğrulandı ve nicelleştirildi:** sıfır
başlangıç hızı, alanı bariyerin *tam üstünde* bırakıyor — geçiş için değil,
donma için doğru başlangıç koşulu.

Test: `test_rest_at_the_top_does_not_cross`,
`test_zero_initial_velocity_is_frozen_at_the_top`,
`test_enough_kinetic_energy_crosses`

> **Düzeltme:** İlk testim `E = E_bariyer` durumunda "geçmez" demek için
> `ratio < 1` bekliyordu; aslında `ratio = 1`. `crosses_barrier` fonksiyonunu
> `E > E_bariyer` (kesin büyük) olacak şekilde düzelttim ve `on_the_barrier`
> alanını ekledim.

---

## 7. Etiket Tablosu

| İddia | Etiket | Gerekçe |
|---|---|---|
| `w ∈ [−1,+1]` | **TÜRETİLDİ** | §1.1 cebiri |
| `w < −1` imkânsız | **TÜRETİLDİ** | aynı |
| Overdamped ⟹ `⟨w⟩ = −1` | **SAYISAL DOĞRULANDI** | §1.2 |
| Kuartik ⟹ `⟨w⟩ = 1/3` | **SAYISAL DOĞRULANDI** | §2.1 |
| Kaadratik ⟹ `⟨w⟩ = 0` | **SAYISAL DOĞRULANDI** | §2.1 |
| `⟨w⟩ = (n−2)/(n+2)` | **ANALİTİK DOĞRULANDI** | virial |
| Ara genlikte `⟨w⟩ > 1/3` | **SAYISAL DOĞRULANDI** | §2.2 |
| Benchmark'ta `1/3` yok | **SAYISAL DOĞRULANDI** | §5 |
| `w = c_s² = 1/3` closure | **VARSAYIM** | fenom. girdi |
| Mikroskopik alan = akışkan | **HATALI** | iki farklı nesne |
| Anlık `w = 1/3` | **HATALI** | salınım var |

---

## 8. Sınırlar

| Konu | Durum |
|---|---|
| Arka plan integrasyonu | Sabit `H` varsayımı (`H ≪ ω` rejiminde geçerli) |
| Uzaysal pertürbasyonlar | ❌ yapılmadı (SPRINT 5) |
| `c_s²` alan teorisinden türetimi | ❌ yapılmadı; makale de yapmıyor |
| Anizotropik stres `σ_ψ` | ❌ doğrudan hesaplanmadı |
| `Φ` ile eşleşmiş evrim | ❌ tek alan yaklaşımı |

Bunlar SPRINT 5'in (sayısal yeniden üretilebilirlik) konusu.

---

## 9. Test Envanteri

`tests/test_sprint4.py` — **21 test**

| Grup | # | Doğrulanan |
|---|---|---|
| Cebirsel sınır | 4 | `w ∈ [−1,1]`, `w = −1` koşulu, virial üsleri |
| Overdamped | 4 | `3H/2μ = 25`, alan donar, `⟨w⟩ = −1`, salınım yok |
| Genlik taraması | 5 | `1/3` (kuartik), `0` (kaadratik), ara aşma, sınırlar |
| Rejim tespiti | 2 | Etkin üs, benchmark `ω/H < 1` |
| Bariyer | 3 | Tepede oturma, donma, yeterli enerji |
| Makale tutarlılığı | 3 | §4.4'ün üç iddiası doğru |

---

## 10. Bulgu Tablosu

| ID | Dosya/denklem | Önceki durum | Yapılan | Test | Sonuç |
|---|---|---|---|---|---|
| P-01 | SPRINT 0 notu | "`w_ψ` %99.99 `< −1`" | Yeniden üretim + yorum | `test_overdamped_w_is_minus_one` | **DÜZELTİLDİ**: değer `−1`, altı değil |
| P-02 | — | — | Cebirsel sınır kanıtı | `test_w_below_minus_one_is_impossible...` | **YENİ — TÜRETİLDİ** |
| P-03 | satır 48 (soyut) | "`1/3` bir tahmin" | Dil analizi | (rapor §4.1) | **HATALI** ifade |
| P-04 | satır 634 (§4.2) | "A key result" | Dil analizi | (rapor §4.2) | **HATALI** ifade |
| P-05 | satır 700–890 (§4.4) | — | Sayısal doğrulama | 3 test | **DOĞRU — korunmalı** |
| P-06 | satır 843 | `ω ≳ H` sınırda | `ω/H` hesabı | `test_benchmark_fails...` | **DOĞRU — makale haklı** |
| P-07 | SPRINT 0 "frozen init" | nitel | `E/E_bariyer` | `test_zero_initial_velocity...` | **NİCELLEŞTİRİLDİ** |

---

## 11. Onay Talebi

SPRINT 4 tamamlandı. **`main.tex` değiştirilmedi.**

1. Bu rapor (§1 sınır kanıtı, §2 üç `1/3` ayrımı, §3 §4.4'ün korunması).
2. §4.4'teki üç maddelik **dil** düzeltmesi — ayrı onay gerektirir.
3. §4.4'ün **değiştirilmemesi** önerisi.
4. SPRINT 0 notundaki `w_ψ` ifadesinin düzeltilmesi.

Onayınızla SPRINT 5'e (sayısal yeniden üretilebilirlik: çift sayma, FRW
kalıntıları, yakınsama, CLASS/Cobaya/lattice artefaktları) geçebilirim.

---

## 12. UYGULANDI — §11 dil düzeltmeleri (onay sonrası)

**Onay:** kullanıcı, "§11'deki dil düzeltmelere ve SPRINT 5'e onay veriyorum."

**Uygulanan:** yalnızca onaylanan **üç** madde. §4.4'e (satır 700–890)
**dokunulmadı** — rapor §3'teki "korunmalı" önerisi geçerli.

| # | Konum | Önce | Sonra |
|---|---|---|---|
| 1 | satır 48 (soyut) | "A falsifiable prediction of PTUM is that … carries w=1/3" | "… is *assigned* … as a phenomenological closure; this closure is a falsifiable hypothesis … not a prediction of the PTUM field theory" |
| 2 | satır 634 (§4.2) | "A key result is that coherent oscillations …" | "A standard result for a canonical scalar is that … *provided* the quartic term dominates the orbit" |
| 3 | satır 649 (kutu) | `\boxed{w=1/3, c_s²=1/3, σ=0}` | aynı kutu + `\quad\text{(phenomenological closure, not a first-principles result)}` |

**Doğrulama:**

- Yanlış eşleşme koruması: her üç hedef için `count == 1` assert edildi.
- Küme parantezi dengesi: `3161 / 3161`, fark **0**.
- `\begin{equation}` / `\end{equation}`: `117 / 117`.
- Satır sayısı: 4460 → 4462 (+2, yalnızca eklenen metin).
- `main.tex` `sha256[:16]`: `ba1a630914b809ae` → **`f708176f286e0972`**.

**Derleme yapılmadı:** sandbox'ta TeX binary'si yok (`pdflatex`, `latexmk`
bulunamadı). Bu bir *derleme doğrulaması değildir*; yalnızca LaTeX yapısal
tutarlılığı (parantez/ortam dengesi) kontrol edildi. Gerçek derleme
kullanıcının kendi ortamında yapılmalı.

**Düzeltme notu:** kutuya ilk yazışta yanlışlıkla İndonezce "bukan" kelimesi
girdi; "not" ile değiştirildi. Yazım hatası, fiziksel içerik etkilenmedi.
