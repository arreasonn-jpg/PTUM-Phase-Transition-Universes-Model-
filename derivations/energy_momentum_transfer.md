# SPRINT 2 — Enerji–Momentum Transfer Vektörleri `Q_i^ν`

**Proje:** PTUM (Phase Transition Universes Model) bilimsel olgunluk denetimi
**Sprint:** 2 / 6 — *Tüm `Q_i^ν`'yi tam eylemden türet*
**Tarih:** 2026-11-12
**Durum:** ✅ Tamamlandı (SPRINT 1'in bir ifadesi düzeltildi)
**Test:** `pytest tests/` → **60/60 PASS** (SPRINT 1: 27, SPRINT 2: 33), 13.7 s
**`main.tex`:** ❌ **değiştirilmedi** (`sha256[:16] = ba1a630914b809ae`), öneri §9'da

---

## 0. Yönetici Özeti

SPRINT 2'nin hedefi, makalenin **altı** `Q_i^ν` ifadesini (Eq. 1684–1686) tek bir eylemden
türetmek, hepsinin `GeV⁵` olduğunu göstermek ve `Σ Q_i^ν = 0`'ı **cebirsel olarak**, inşa
yoluyla değil, çıkarmaktı.

**Sonuç üç başlıkta özetlenebilir:**

1. **Türetme tamamlandı.** Kapalı form bulundu:
   `Q_i⁰ = φ̇_i ∂L_int/∂φ_i − λ_i dL_int/dt`. Buradan `Σ Q_i⁰ = 0` **her tahsis
   `{λ_i}` için bir özdeşlik olarak** çıkıyor — iki zıt işaret yazarak değil.

2. **Beklenmedik bulgu (asıl sonuç).** Makalenin basılı dört `Q_i`'sinin **tamamı**,
   türetilen sonucun tam tersi işaretli. Bu sekiz bağımsız hata değil, **tek bir global
   işaret hatası**. Ve makale kendi kendisiyle çelişiyor: 1712. satır (`Q_DM ≈ −Q_DE ≈
   +2g χ² Φ_res Φ̇_res`) benim türetimimle uyuşuyor, 1684. satır ise tersini yazıyor.

3. **B-08 düzeltildi.** SPRINT 0'da "tüm `Q_i` `GeV⁴`" demiştim; bu **fazla geniş** bir
   iddiaydı. Doğrusu: yalnızca **Yukawa terimi** boyut olarak yanlış (`GeV⁴`), diğer üçü
   zaten `GeV⁵`.

**Ve bir özeleştiri:** SPRINT 2 sırasında SPRINT 1'in `T_00` sonucunu yeniden test ettim;
ilk denememde "SPRINT 1 yanlış" sandım. Hata bendeydi: `T_{μν}`'yi `g_{00}` yerine `g^{00}`
üzerinden türetmiştim. SPRINT 1 doğru. Bu, testlerin gerçekten bağımsız bir kontrol
işlevi gördüğünün kanıtı — ayrıntı §7.4'te.

---

## 1. Görev Tanımı ve Kabul Kriterleri

Denetim brifinginin §3'ünde zorunlu tutulan testler:

| # | Zorunlu kontrol | Durum |
|---|---|---|
| 1 | Her `Q_i^ν` boyutu `GeV⁵` | ✅ (Yukawa hariç — bulgu) |
| 2 | `Σ_i Q_i^ν = 0` | ✅ her tahsisde |
| 3 | Etkileşim kapatılınca `Q_i^ν = 0` | ✅ |
| 4 | İki-sektör örneğinde birinin kaybı = diğerinin kazancı | ✅ |
| 5 | FRW zaman bileşeni işaret konvansiyonu açık | ✅ |
| 6 | Çift sayma iddiasının test edilmesi | ✅ (**reddedildi**) |

---

## 2. Türetme

### 2.1 Eylem ve sektörlere ayırma

SPRINT 1'in düzeltilmiş konvansiyonlarıyla (imza `(−+++)`, kanonik skaler
`L = −½(∂φ)² − V`):

```
L = Σ_i L_i^free + L_int ,        L_i^free = ½ φ̇_i² − V_i(φ_i)
```

Etkileşim, iki alan arasında **tahsis** edilir:

```
L_i = L_i^free + λ_i L_int ,      λ_a + λ_b = 1
```

`λ_i` bir *konvansiyon*dur, fizik değil: yalnızca `T_total` tekildir, `T_i` değil.

### 2.2 Sektör enerji yoğunluğu ve basıncı

```
ρ_i = ½ φ̇_i² + V_i − λ_i L_int
p_i = ½ φ̇_i² − V_i + λ_i L_int
ρ_i + p_i = φ̇_i²
```

`½ φ̇²`'nin işareti SPRINT 1'de sabitlendi (`T_00 = ρ` şartı).

### 2.3 Diverjans

```
∇_μ T_i^{μ0} = ρ̇_i + 3H(ρ_i + p_i)
             = φ̇_i (φ̈_i + 3H φ̇_i + V_i') − λ_i dL_int/dt
```

Ara adım: `ρ̇_i = φ̇_iφ̈_i + V_i'φ̇_i − λ_i dL_int/dt` ve `3H(ρ_i+p_i) = 3Hφ̇_i²`.

### 2.4 Tam hareket denklemi

`S = ∫√−g (…)` eyleminden, `i` alanının **tam** EOM'i:

```
φ̈_i + 3H φ̇_i + V_i' = ∂L_int/∂φ_i
```

### 2.5 Transfer vektörü (**ana formül**)

(2.3) ve (2.4) birleştirilir:

```
┌─────────────────────────────────────────────┐
│  Q_i⁰ = φ̇_i ∂L_int/∂φ_i − λ_i dL_int/dt      │   (**)
└─────────────────────────────────────────────┘
```

Kovaryant biçimde `Q_i^ν = ∂^νφ_i ∂L_int/∂φ_i − λ_i ∂^νL_int`.

### 2.6 `Σ Q_i = 0` — cebirsel kanıt

```
Σ_i Q_i⁰ = Σ_i φ̇_i ∂L_int/∂φ_i − (Σ_i λ_i) dL_int/dt
         = dL_int/dt − 1 · dL_int/dt
         = 0                                                     ∎
```

Burada kullanılan tek şey zincir kuralı ve `Σλ_i = 1`'dir. **Hiçbir EOM kullanılmadı** —
yani kapanma on-shell bile değil, *off-shell* bir özdeşliktir. Bu, makalenin "double
counting" açıklamasından çok daha güçlü bir ifadedir.

### 2.7 Tahsisten bağımsızlık

`Q_i` **λ'ya bağlıdır**, `Σ Q_i` değildir. Fiziksel olarak gözlenebilir olan, bir sektörün
`ρ_i + 3H(ρ_i+p_i)` sol tarafı ile `Q_i` arasındaki *bölüşüm*dür; bu bölüşüm λ değişince
değişir ama toplam evrim değişmez. Test:
`test_allocation_dependence`, `test_sum_Q_vanishes_identically` (4 farklı λ kombinationu).

---

## 3. Dört Etkileşim, Türetilmiş Sonuçlar

### 3.1 `L_int^{ψΦ} = +α m² Φ²ψ²/(2E_th²)`

`lam_Phi = 0` (etkileşim `ψ` tarafında, çünkü eylemde `m_eff²(Φ)ψ²/2` içinden geliyor):

```
Q_Φ⁰ = +α m² (Φ/E_th²) ψ² Φ̇
Q_ψ⁰ = −α m² (Φ/E_th²) ψ² Φ̇
```

### 3.2 `L_int = −g_DM χ²Φ_res²`, `λ_χ = 1`

```
Q_DM⁰ = +2 g_DM χ² Φ_res Φ̇_res
Q_DE⁰ = −2 g_DM χ² Φ_res Φ̇_res
```

### 3.3 `L_int = −y_ψ ψ f̄f`, `λ_ψ = 0`

```
Q_ψ⁰ = −y_ψ (f̄f) ψ̇
Q_f⁰ = +y_ψ (f̄f) ψ̇
```

Boyut: `0 + 3 + 2 = 5` ✔. Makalenin `y_ψ ψ f̄γ^ν f` biçimi: `0+1+3 = 4` ✘ —
hem boyut hem yapı yanlış (vektör akım, bilineerin türevi değil).

### 3.4 `L_int = −½ g_ψ ψ²φ_SM²`, `λ_ψ = 0`

```
Q_ψ⁰ = −g_ψ ψ φ_SM² ψ̇
Q_SM⁰ = +g_ψ ψ φ_SM² ψ̇
```

---

## 4. Birim Analizi

Doğal birimler, `[φ]=1`, `[f]=3/2`, `[∂_μ]=1`:

| Terim | Hesap | Sonuç | |
|---|---|---|---|
| `α m²(Φ/E_th²)ψ²∂Φ` | 0+2+1−2+2+1+1 | **5** | ✅ |
| `y_ψ ψ f̄γ^ν f` (basılı) | 0+1+3 | **4** | ❌ |
| `y_ψ(f̄f)∂ψ` (türetilen) | 0+3+1+1 | **5** | ✅ |
| `2g_DM χ²Φ_res∂Φ_res` | 0+2+1+1+1 | **5** | ✅ |
| `g_ψ ψ²φ_SM∂φ_SM` | 0+2+1+1+1 | **5** | ✅ |

**Düzeltme (B-08):** SPRINT 0'da "tüm `Q_i` `GeV⁴`" yazmıştım. Bu **yanlıştı** —
yalnızca Yukawa terimi `GeV⁴`. Diğer üçü zaten doğru boyutta. Bu, denetimin kendi
hatasının düzeltilmesidir ve raporda açıkça belirtilmelidir.

---

## 5. İşaret Analizi — Asıl Bulgu

### 5.1 Karşılaştırma tablosu

| `Q_i` | Makale (1684–1686) | Türetilen | İlişki |
|---|---|---|---|
| `Q_Φ^ν` | `−αm²(Φ/E_th²)ψ²∂^νΦ` | `+αm²(Φ/E_th²)ψ²Φ̇` | **ters** |
| `Q_ψ^ν` (Φψ kısmı) | `+αm²(Φ/E_th²)ψ²∂^νΦ` | `−αm²(Φ/E_th²)ψ²Φ̇` | **ters** |
| `Q_DM^ν` | `−2g_DMχ²Φ_res∂^νΦ_res` | `+2g_DMχ²Φ_resΦ̇_res` | **ters** |
| `Q_DE^ν` | `+2g_DMχ²Φ_res∂^νΦ_res` | `−2g_DMχ²Φ_resΦ̇_res` | **ters** |
| `Q_ψ^ν` (Yukawa) | `+y_ψψf̄γ^νf` | `−y_ψ(f̄f)ψ̇` | **yapı farklı** |
| `Q_SM^ν` (Yukawa) | `−y_ψψf̄γ^νf` | `+y_ψ(f̄f)ψ̇` | **yapı farklı** |
| `Q_ψ^ν` (kuartik) | `+g_ψψ²φ_SM∂^νφ_SM` | `−g_ψψφ_SM²ψ̇` | **yapı farklı** |
| `Q_SM^ν` (kuartik) | `−g_ψψ²φ_SM∂^νφ_SM` | `+g_ψψφ_SM²ψ̇` | **yapı farklı** |

### 5.2 Yorum

Dört potansiyel-kaynaklı `Q_i`'nin **dördü de** tam ters işaretli. Sekiz bağımsız hata
olamaz — bu, tek bir **global işaret konvansiyonu** hatasıdır. Kökeni, makalenin
`T_i^{μν} = +2/√−g δS/δg_{μν}` tanımıdır (B-07'nin tekrarı): `g_{μν}` yerine `g^{μν}`
türevi alınırsa `T` işaret değiştirir, dolayısıyla `∇_μT_i = Q_i` de ters çıkar.

### 5.3 Fiziksel tutarlılık kontrolü (bağımsız doğrulama)

Deşarj sırasında `Φ̇ < 0` ve yakıt **enerji kaybetmelidir**. İşaret konvansiyonu
`Q_i > 0` = *giriş* olduğuna göre `Q_Φ < 0` olmalı:

- Türetilen: `Q_Φ = +αm²(Φ/E_th²)ψ²·Φ̇ < 0` ✔
- Basılı: `Q_Φ = −αm²(Φ/E_th²)ψ²·Φ̇ > 0` ✘ — yakıt, deşarjı sürerken **enerji kazanıyor**

Test: `test_manuscript_states_nabla_T_equals_Q_but_uses_the_opposite_sign`.

### 5.4 Makalenin kendi iç çelişkisi

Satır 1712: `Q_DM ≈ −Q_DE ≈ 2g_DMχ²Φ_resΦ̇_res` — bu **benim türetimim**.
Satır 1684 (iki satır yukarıda): `Q_DM = −2g_DMχ²Φ_res∂^νΦ_res` — tersi.

Yani makale kendi kendisiyle çelişiyor ve 1712. satır doğru olan. Bu, onarımın
**tek bir global işaret düzeltmesi** olması gerektiğini kanıtlıyor; sekiz yerel yama değil.
Test: `test_manuscript_line_1712_contradicts_its_own_equation_1684`.

---

## 6. "Çift Sayma" İddiasının Testi

Makale (satır 1694–1702) şunu iddia ediyor:

> "The terms `αm²(Φ²/E_th²)ψ∂^νψ` and `g_DM χΦ_res²∂^νχ` that appeared in an earlier
> draft arose from **double-counting** the symmetric interaction variation; they cancel
> once each interaction is assigned exactly once to each of the two exchanging sectors."

**Bu iddia test edildi ve reddedildi.** Formül (**) bu iki terimin nereden geldiğini
tam olarak gösteriyor:

```
ψ için:  Q_ψ⁰ = ψ̇ · ∂L_int/∂ψ − λ_ψ dL_int/dt
```

`∂L_int^{ψΦ}/∂ψ ≠ 0` olduğundan `ψ̇ ∂L_int/∂ψ` terimi **kaçınılmazdır** — bu
`αm²(Φ²/E_th²)ψψ̇`'dir, yani makalenin "çift sayma artığı" dediği terimin ta kendisi.
Bu bir hata değil, **ψ sektörünün kendi EOM'inin zorunlu sonucudur**.

Dolayısıyla:

- Bu terimler "çift sayma" değildir; **eksik bırakılmıştır**.
- Terimleri atıp yerine `Q_ψ = −Q_Φ` yazmak, `Σ Q = 0`'ı **inşa ederek** sağlamaktır —
  brifingin açıkça yasakladığı hamle.
- Doğru okuma: `Q_ψ` hem `Φ̇` hem `ψ̇` içerir; ikisi birlikte kapanmayı sağlar.

Test: `test_sum_Q_is_not_a_term_by_term_sign_flip` (yapısal tanımı doğrular),
`test_psi_sector_residual_is_exactly_the_other_two_interactions` (ψ'nin üç etkileşimde
yer aldığını, tek etkileşimle kapatınca kalanın **tam olarak** diğer iki transfer olduğunu
gösterir — güçlü bir bağımsız kontrol).

---

## 7. `Σ Q_i = 0` Kanıtının Yapısı

### 7.1 İnşa yoluyla değil, cebirle

`Σ Q_i = 0` üç bağımsız düzeyde gösterildi:

1. **Sembolik özdeşlik** (§2.6): `Σ` ifadesi `dL_int/dt − dL_int/dt`'ye indirgeniyor.
   4 farklı λ kombinasyonunda test edildi.
2. **Bağımsız diverjans karşılaştırması**: `closure_residual()` fonksiyonu, `ρ_i, p_i`'den
   **doğrudan** `∇_μT_i^{μ0}` hesaplayıp EOM'i yerine koyuyor ve (**) ile
   karşılaştırıyor. Kalıntı **tam sıfır** (5 farklı λ için).
3. **Kalan-terim testi**: ψ sektörünü tek etkileşimle kapatınca kalan, tam olarak diğer
   iki etkileşimin transferi çıkıyor.

### 7.2 "İki zıt işaret" neden yetersiz

Makalenin yöntemi `Q_ψ = −Q_Φ` yazmaktır. Bu, `Σ Q = 0`'ı **tanım gereği** doğru yapar
ama:

- her bir `Q_i`'nin *doğru* olup olmadığını söylemez;
- ψ'nin `ψ̇` terimini kaybeder;
- tahsis bağımlılığını gizler.

Bizim yöntem her `Q_i`'yi ayrı ayrı türetiyor ve kapanmayı **sonuç** olarak elde ediyor.

### 7.3 Kuantum düzeltmeleri (kapsam dışı, açıkça)

Bu türetme **ağaç seviyesindedir**. `⟨T^{μν}⟩`'nin kuantum beklenti değeri, iz anomalisi
(`⟨T^μ_μ⟩ ≠ 0`) nedeniyle klasik diverjansı korumaz. PTUM bu rejimde çalışıyorsa
`Σ Q_i = 0` kuantum seviyesinde **koşulludur**. Raporda açıkça belirtilmelidir.

### 7.4 Bir özeleştiri (SPRINT 1'in yeniden testi)

SPRINT 2 sırasında `T_00` sonucunu bağımsız olarak yeniden test ettim. İlk denememde
"SPRINT 1 yanlış" sonucuna vardım. **Hata bendeydi:** `T_{μν}`'yi `g^{00}` yerine `g_{00}`
üzerinden türetmiştim, bu fazladan bir işaret veriyor. Doğru hesap:

```
L = ½(∂φ)² − V  →  T_00 = ½φ̇² + V = ρ   ✔
```

Yani SPRINT 1'in `−½` düzeltmesi doğru. Bu bölümü raporda tutuyorum çünkü:

- denetim sürecinin kendi hatalarını da raporlaması gerekir;
- bu, testlerin gerçekten bağımsız kontrol işlevi gördüğünü kanıtlıyor;
- `g_{μν}` vs `g^{μν}` tuzağı, makalenin B-07 hatasının da kökeni.

**Ancak:** bu yeniden test, B-04'ün *gerekçesini* keskinleştirdi. Makalenin yazdığı
`L = +½φ̇² − ½m²(1−αΦ²/E_th²)ψ²` çifti, makalenin **kendi EOM'lerini (13)–(14) tam olarak
üretir**. Yani EOM tarafında bir tutarsızlık yok. Tutarsızlık **`T_00`'da**: `+½` kinetikle
`T_00 = −ρ`, makalenin kendi `ρ = ½φ̇² + V` tanımıyla çelişiyor. B-04 düzeltmesi geçerli,
ama gerekçesi "EOM tutmuyor" değil, "**enerji yoğunluğu tutmuyor**" olmalıdır.

---

## 8. Kapsam ve Sınırlar

| Konu | Durum | Etiket |
|---|---|---|
| Φψ, DM-DE, kuartik transferleri | Tam türetildi | TÜRETİLDİ |
| `Σ Q_i = 0` (klasik, ağaç) | Cebirsel özdeşlik | TÜRETİLDİ |
| Yukawa `Q_ψ`, `Q_f` | Bilineer yaklaşımında türetildi | KOŞULLU |
| Yukawa'nın **fermiyonik yarısı** | Dirac denklemi açılmadı | EKSİK |
| `Q_SM ≈ Γ_ψρ_ψ` | Bu Lagrangian'dan çıkmaz (1→2 yok) | FENOMENOLOJİK |
| Kuantum/iz anomalisi | İncelenmedi | EKSİK |
| Ayrıklaştırma / lattice tutarlılığı | SPRINT 5 | — |

**Yukawa hakkında dürüst ifade:** `Q_f⁰`'yi yalnızca `⟨f̄f⟩` bilineeri üzerinden
türettim, tam Dirac spinörü üzerinden değil. Kapanma bu düzeyde doğru çıkıyor, ancak
**tam** kapanma `iγ^μ∇_μf − m_ff = y_ψψf` denkleminin bileşen bileşen açılmasını
gerektirir. Bunu yapmadım ve "ispatlandı" demiyorum.

**Kuartik sektör hakkında:** `⟨ψ⟩ = 0` iken `−½g_ψψ²φ_SM²` operatörü `ψψ → φ_SMφ_SM`
yok edilmesini (annihilation) tanımlar, tek parçacık `ψ → φ_SMφ_SM` bozunmasını **değil**.
`Γ_ψ` bozunma genişliği bu Lagrangian'dan okunamaz; `Q_SM ≈ Γ_ψρ_ψ` bir **etkin
kinetik-teori girdisi**dir, türetilmiş bir sonuç değil.

---

## 9. `main.tex` için Değişiklik Önerisi (UYGULANMADI)

Aşağıdaki diff onayınıza sunulur. **Hiçbiri uygulanmadı.**

### 9.1 Satır 1684–1686 — global işaret

```diff
 \begin{align}
-Q_{\rm DM}^\nu &= -2g_{\rm DM}\chi^2\Phi_{\rm res}\partial^\nu\Phi_{\rm res}, \\
-Q_{\rm DE}^\nu &= +2g_{\rm DM}\chi^2\Phi_{\rm res}\partial^\nu\Phi_{\rm res}, \\
-Q_{\rm SM}^\nu &= -y_\psi \psi \bar{f}\gamma^\nu f - g_\psi \psi^2 \phi_{\rm SM} \partial^\nu\phi_{\rm SM}.
+Q_{\rm DM}^\nu &= +2g_{\rm DM}\chi^2\Phi_{\rm res}\partial^\nu\Phi_{\rm res}, \\
+Q_{\rm DE}^\nu &= -2g_{\rm DM}\chi^2\Phi_{\rm res}\partial^\nu\Phi_{\rm res}, \\
+Q_{\rm SM}^\nu &= +y_\psi (\bar{f}f)\,\partial^\nu\psi
+                  + g_\psi \psi\phi_{\rm SM}^2\,\partial^\nu\psi .
 \end{align}
```

### 9.2 Satır 1678–1682 — `Q_ψ, Q_Φ` ve Yukawa yapısı

```diff
-Q_\psi^\nu &= +\alpha m^2 \frac{\Phi}{E_{\rm th}^2} \psi^2 \partial^\nu\Phi
- + y_\psi \psi \bar{f}\gamma^\nu f
- + g_\psi \psi^2 \phi_{\rm SM} \partial^\nu\phi_{\rm SM}, \\
-Q_\Phi^\nu &= -\alpha m^2 \frac{\Phi}{E_{\rm th}^2} \psi^2 \partial^\nu\Phi, \\
+Q_\psi^\nu &= -\alpha m^2 \frac{\Phi}{E_{\rm th}^2} \psi^2 \partial^\nu\Phi
+ - y_\psi (\bar{f}f)\,\partial^\nu\psi
+ - g_\psi \psi\phi_{\rm SM}^2\,\partial^\nu\psi, \\
+Q_\Phi^\nu &= +\alpha m^2 \frac{\Phi}{E_{\rm th}^2} \psi^2 \partial^\nu\Phi, \\
```

### 9.3 Satır 1694–1702 — "çift sayma" paragrafı

```diff
-Direct summation now gives $\sum_i Q_i^\nu = 0$ identically, as required
-by $\nabla_\mu T^{\mu\nu}_{\rm total}=0$ (GÖSTERİLDİ). The terms
-$\alpha m^2(\Phi^2/E_{\rm th}^2)\psi\partial^\nu\psi$ and
-$g_{\rm DM}\chi\Phi_{\rm res}^2\partial^\nu\chi$ that appeared in an
-earlier draft arose from double-counting the symmetric interaction
-variation; they cancel once each interaction is assigned exactly once
-to each of the two exchanging sectors.
+Direct summation gives $\sum_i Q_i^\nu = 0$ identically, as required
+by $\nabla_\mu T^{\mu\nu}_{\rm total}=0$ (GÖSTERİLDİ). Writing the
+transfer of each sector as
+$Q_i^0=\dot\phi_i\,\partial\mathcal{L}_{\rm int}/\partial\phi_i
+-\lambda_i\,d\mathcal{L}_{\rm int}/dt$ with $\sum_i\lambda_i=1$
+makes the closure algebraic, for any allocation $\{\lambda_i\}$.
+The $\psi\dot\psi$ terms are therefore not a double-counting artefact
+but the mandatory contribution of the proxy sector's own equation of
+motion; dropping them and setting $Q_\psi=-Q_\Phi$ by hand would
+enforce the sum by construction rather than derive it.
```

### 9.4 Satır 1678 — `T_i^{μν}` tanımı (B-07 tekrarı)

```diff
-The energy-momentum tensor for each sector is
-$T_i^{\mu\nu} = \frac{2}{\sqrt{-g}}\frac{\delta(\sqrt{-g}\mathcal{L}_i)}{\delta g_{\mu\nu}}$.
+The energy-momentum tensor for each sector is
+$T_i^{\mu\nu} = -\frac{2}{\sqrt{-g}}\frac{\delta(\sqrt{-g}\mathcal{L}_i)}{\delta g_{\mu\nu}}$,
+consistently with the $g^{\mu\nu}$ variation defined in \S\ref{sec:conventions}.
```

### 9.5 Satır 1712 — değişiklik gerekmiyor

`Q_DM ≈ −Q_DE ≈ 2g_DMχ²Φ_resΦ̇_res` zaten doğru. 9.1 uygulanınca makale kendi
içinde tutarlı hale gelir.

---

## 10. Test Envanteri

`tests/test_transfer_vectors.py` — **33 test, tümü PASS**

| Grup | Test sayısı | Ne doğruluyor |
|---|---|---|
| Boyut analizi | 2 | `GeV⁵`; yalnızca Yukawa'nın başarısız olduğu |
| FRW diverjansı | 2 | `∇_μT^{μ0} = φ̇·EOM`; işaret konvansiyonu |
| Türetme ↔ doğrudan diverjans | 3 | (**) ≠ ansatz; ψ kalıntısı = diğer iki transfer |
| Global kapanma | 2 | `ΣQ=0` 4 farklı λ'da; yapısal (işaret taklidi değil) |
| Φψ sektörü | 3 | Kapalı form; makaleye ters; kapatma |
| DM-DE sektörü | 4 | Kapalı form; iki-sektör enerji korunumu; kapatma |
| Yukawa | 5 | Boyut; yapı; kapatma; `PARTIAL` etiketi |
| Kuartik | 5 | Kapalı form; yapı farkı; kapatma; annihilation |
| Toplu | 2 | Tüm kuponlar kapalıyken `Q=0` |
| **İşaret bulgusu** | 3 | 8/8 ters; fiziksel tutarlılık; iç çelişki |

Çalıştırma: `/tmp/venv/bin/python -m pytest tests/ -v`

---

## 11. Bulgu Durumu

| ID | Açıklama | Önceki | Şimdi |
|---|---|---|---|
| B-07 | `T^{μν}` tanımında `+` yerine `−` | Açık | **Tekrar doğrulandı**, §9.4 |
| B-08 | `Q_i^ν` boyutları | "hepsi `GeV⁴`" | **Düzeltildi**: yalnızca Yukawa, `GeV⁴` |
| **Y-01** | **Tüm `Q_i` global işaret hatası** | *Bilinmiyordu* | **YENİ — HATALI** |
| **Y-02** | **"Çift sayma" açıklaması** | "GÖSTERİLDİ" iddiası | **YENİ — HATALI (reddedildi)** |
| **Y-03** | **Yukawa yapısı** (`f̄γ^νf` vs `(f̄f)∂^νψ`) | Boyut notu | **YENİ — HATALI** |
| B-04 | Kinetik işaret | Açık | Kapalı; **gerekçe keskinleşti** (§7.4) |

---

## 12. SPRINT 3'e Devredilenler

1. **Parametrik rezonans (Mathieu/Floquet)** — `Q_DM` işareti düzeltildikten sonra
   yeniden hesaplanmalı; `w_ψ` %99.99 `< −1` bulgusu hâlâ açık.
2. **`Γ_ψ` türetimi** — kuartik sektör tek başına 1→2 bozunma vermiyor; üçlü kuplaj
   veya termal ortam varsayımı gerekiyor. Hangi varsayımın kullanıldığı yazılmalı.
3. **Kuantum iz anomalisi** — `ΣQ=0`'ın kuantum düzeyindeki statüsü.
4. **Yukawa'nın tam Dirac analizi** — bu sprintte `PARTIAL` bırakıldı.
5. **Sayısal doğrulama** — türetilen `Q_i` ile `ptum_task1_simulation.py` çıktısının
   karşılaştırılması; arka plan çözümünde enerji korunumunun sayısal kalıntısı.

---

## 13. Onay Talebi

SPRINT 2 tamamlandı. **`main.tex` değiştirilmedi.** Onayınıza sunulanlar:

1. Bu raporun bilimsel içeriği (türetme, işaret tablosu, §6 reddi).
2. §9'daki beş maddelik diff önerisi — **ayrı bir onay** gerektirir.
3. B-08'in düzeltilmiş ifadesi (yalnızca Yukawa boyut hatası).
4. §7.4'teki özeleştiri: B-04'ün gerekçesi "EOM" değil "enerji yoğunluğu" olmalı.

Onayınızla SPRINT 3'e (parametrik rezonans / Floquet) geçebilirim.
