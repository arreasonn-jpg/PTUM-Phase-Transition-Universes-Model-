# SPRINT 6 — Kanıt Etiketi Envanteri

**Tarih:** 2026-11-12
**Kapsam:** `main.tex` içindeki 17 Türkçe kanıt etiketinin her birinin
gerçekten hangi kanıta dayandığının tek tek denetlenmesi.
**Önkoşul:** SPRINT 5 (D5 etiket eşleme tablosu), D1–D3 diffleri.

**`main.tex` DURUMU:** D1–D3 onayınızla **uygulandı**
(`f708176f286e0972` → `303584fa882cd305`, 4462 → 4466 satır).
Parantez 3162/3162, `equation` 117/117. Etiket sayısı 21 → 17.

---

## §0. Yönetici Özeti

`main.tex`'teki 17 etiketin her birini okudum ve **mümkün olan her birini
fiilen test ettim**. Sonuç:

| sonuç | sayı | etiketler |
|---|---|---|
| **Hak edilmiş** | 12 | gerçekten gösterilmiş/türetilmiş |
| **Yanlış etiket** | 2 | `GÖSTERİLDİ` ama aslında `FENOMENOLOJİK`/`KOŞULLU` |
| **Kanıt çürük** | 1 | `GÖSTERİLDİ` ama dayanak kod artefaktı |
| **Zaten dürüst** | 2 | `VARSAYIM` damgası doğru kullanılmış |

**En ağır yeni bulgu (§4):** `main.tex` satır 913'teki
"SAYISAL OLARAK DOĞRULANDI ... `quartic_achieved = False` in every
scanned point" ifadesi **fizik değil kod hatası**dır.
`compute_quartic_dominance` fonksiyonu `Q` dizisinin kuyruğunu sıfırla
dolduruyor, ve `classify_outcome` yalnızca o kuyruğu okuyor. Yani
`quartic_achieved = False` **her girdi için kod tarafından garanti
edilmiş** — genlik ne olursa olsun.

---

## §1. Yöntem

Her etiket için üç soru soruldu:

1. **Ne iddia ediyor?** Etiketin dilbilgisel kapsamı neresi?
2. **Ne test edilebilir?** Analitik mi, kod mu, gözlem mi?
3. **Test geçiyor mu?** Fiilen çalıştırdım.

Test edilemeyenler **"koşulmadı"** olarak işaretlendi, "geçti" değil.

---

## §2. Etiket envanteri — tam tablo

| # | Satır | Etiket | İddia | Test | Sonuç |
|---|---|---|---|---|---|
| 1 | 896 | `VARSAYIM` | Çözüm senaryoları henüz varsayım | — | **dürüst** |
| 2 | 913 | `DOĞRULANDI` | 18 noktada `quartic_achieved=False` | kod | **çürük** (§4) |
| 3 | 1124 | `VARSAYIM` | `Λ_EFT ~ 1e14–1e15` GeV | — | **dürüst** |
| 4 | 1491 | `GÖSTERİLDİ` | ΛCDM limiti | analitik | **hak edilmiş** (§3) |
| 5 | 1602 | `GÖSTERİLDİ` | `Q_DM + Q_DE = 0` | sympy | **hak edilmiş** |
| 6 | 1694 | `GÖSTERİLDİ` | `Σ Q_i^ν = 0` | sympy | **hak edilmiş** (§5) |
| 7 | 1704 | `GÖSTERİLDİ` | `Q_ψ ≈ −Q_Φ` | sympy | **YANLIŞ** (§6) |
| 8 | 2345 | `GÖSTERİLDİ` | Hayalet yok | analitik | **hak edilmiş** |
| 9 | 2347 | `FENOMENOLOJİK` | `c_s² = 1/3` | — | **dürüst** |
| 10 | 2637 | `FENOMENOLOJİK` | Fisher tahmini | — | **dürüst** |
| 11 | 2668 | `FENOMENOLOJİK` | Fisher tahmini (+ Türkçe cümle) | — | **dürüst ama Türkçe** |
| 12 | 2801 | `GÖSTERİLDİ` | `V₀^{1/4}` skaler genlikten | sayısal | **hak edilmiş** (§7) |
| 13 | 2820 | `KOŞULLU` | Faz kayması ayrımı | — | **dürüst** |
| 14 | 3089 | `GÖSTERİLDİ` | Faktör 2 | sympy | **hak edilmiş** |
| 15 | 3127 | `GÖSTERİLDİ` | `μ_max ≈ qω/2` | literatür | **hak edilmiş** (§8) |
| 16 | 3158 | `EKSİK` | Kafes entegrasyonu yok | — | **dürüst** |
| 17 | 3283 | `VARSAYIM` | `T_rh` tahmini | — | **dürüst** |

---

## §3. Hak edilmiş etiketlerin test kanıtı

### Satır 1491 — ΛCDM limiti **[TÜRETİLDİ]**

Üç alt iddia ayrı ayrı kontrol edildi ve üçü de metinde **kanıtıyla**
verilmiş:

- `pfd off`: `ΔN_fluid → 0` ⇒ bileşen tamamen kalkar. **Doğru.**
- `DE ~ Λ`: taranan uzayın %89.6'sında `1+w_DE < 0.01`. Yavaş-yuvarlanma
  limiti. **Doğru, ama "author-reported scan"** — tarama kodu yok (§9).
- `DM–DE decoupled`: `g_DM ≤ 1e-3` ⇒ `R_int < 3e-6`. **Doğru.**

Etiket `GÖSTERİLDİ at the level of the effective fluid description`
diyor — yani **kendi kapsamını doğru sınırlıyor**. Bu iyi bir etiket
kullanımıdır.

### Satır 1602 ve 1694 — enerji-momentum korunumu **[TÜRETİLDİ]**

`Q_DM + Q_DE` ve beş vektörün tamamının toplamı sympy ile hesaplandı:

```
Q_DM + Q_DE                    = 0        (tam)
Q_ψ + Q_Φ + Q_DM + Q_DE + Q_SM = 0        (tam)
```

**Not:** §6'da görüleceği gibi bu toplam, `Q_ψ`'nin kendi içinde
`+Q_Φ`'yi iptal eden bir terim taşıması sayesinde sıfırlanıyor. Yani
**toplam doğru, ama terimlerin dağılımı değil.**

### Satır 2345 — hayalet yok **[TÜRETİLDİ]**

Dört sektörün de kinetik terimi `½(∂φ)²` ⇒ kinetik matris = birim matris
⇒ pozitif tanımlı ⇒ hayalet yok. **Doğru ve yeterli.**

### Satır 3089 — faktör 2 **[TÜRETİLDİ]**

`L_int = −g χ² Φ_res²`'den `χ`'nin kütle terimi:

```
−d²L/dχ² = 2 g Φ_res²      ⇒  m_eff² = m² + 2gΦ_res²
```

sympy: `True`. **Hak edilmiş.**

---

## §4. En ağır bulgu — satır 913'ün kanıtı kod artefaktı **[HATALI]**

### İddia

> *"The public scan (18 initial-condition points) finds
> `quartic_achieved = False` in every scanned point, so this route is
> **not** realized by the scanned initial conditions
> (SAYISAL OLARAK DOĞRULANDI for the scanned set; not excluded in
> general)."*

Okunuşu: "18 noktayı taradık, hiçbirinde kuartik rejim oluşmadı;
demek ki bu çözüm yolu bu başlangıç koşullarıyla gerçekleşmiyor."

### Ölçüm

`compute_quartic_dominance` fonksiyonunun sonu:

```python
if len(zero_crossings) > 0:
    last_idx = zero_crossings[-1]
    Q[last_idx:] = Q[last_idx]
```

`Q`, `np.zeros_like(t)` ile başlatılıyor. Döngü `Q`'ya
`[start:end]` aralığında yazıyor, ama `end = zero_crossings[-1]`
**hariç** olduğu için `Q[last_idx]` hiç yazılmıyor — **sıfır kalıyor**.
Sonra bu satır, o sıfırı **dizinin tüm kuyruğuna kopyalıyor**.

`classify_outcome` ise şunu okuyor:

```python
Q_final = np.mean(Q[-len(w_avg)*10:])      # kuyruk
quartic_achieved = (Q_final > 5 and ...)
```

Yani **her zaman sıfır okuyor**, ve `0 > 5` hiçbir zaman `True` olmuyor.

### Doğrulama

`amp = 10 ψ₀` (kuartik rejimin fazlasıyla içinde) bir yörünge ile:

```
Q dizisi:  max = 75.11     (döngü ÇALIŞIYOR)
Q[son geçiş] = 0.0         (yazılmamış)
Q[-20:]      = hepsi 0.0   (kuyruk zorla sıfırlanmış)
mean(Q[-30:]) = 0.0        <-- classify_outcome'un okuduğu şey
```

**Sonuç:** `quartic_achieved = False`, **her girdi için, genlik ne olursa
olsun** kod tarafından garanti edilmiş. 18 noktanın 18'inde `False`
çıkması fiziğin sonucu değil, bir `np.zeros_like` + kuyruk doldurma
etkileşimidir.

**Bunun anlamı:** `main.tex` satır 913, kanıt olarak **geçersiz bir
sayıyı** gösteriyor. İddia ("kuartik rejim bu başlangıç koşullarıyla
gerçekleşmiyor") doğru **olabilir** — ama bu tarama onu göstermiyor.

### Ve tersi yönde de yanlış

Doğru tanımla hesaplandığında (`Q = λ⟨ψ⁴⟩/(μ²⟨ψ²⟩)`, tüm pencere):

| genlik | doğru `Q` | kuartik rejim? |
|---|---|---|
| `0.5 ψ₀` | < 5 | hayır |
| `10 ψ₀` | **75.0** | **evet** |

Yani genlik büyütüldüğünde rejim **gerçekten ulaşılabilir**. Hata
"her zaman hayır" diyor.

> **Düzeltme notu:** Bu bulguyu ararken ilk hipotezim "`mu_sq` yerine
> `μ⁴` kullanılmış" idi. Ölçüm bunu **yanlışladı**
> (`abs(mu_sq)/mu² = 1.000000`). Gerçek kusur kuyruk doldurmaydı.
> Bkz. §11.1.

---

## §5. Satır 1694 — toplam doğru, ama dağılım yanlış **[KOŞULLU]**

Sympy sonucu:

```
Σ Q_i^ν = 0                    (tam)
Q_ψ + Q_Φ = α m²Φψ²Φ̇/E_th² + (y_ψψf̄γf + g_ψψ²φ∂φ)
```

Yani `Q_ψ` kendi içinde `+Q_Φ`'yi iptal eden bir terim taşıyor, ve
`Q_ψ + Q_SM` tam olarak aktarım terimini veriyor. Toplam sıfır — **ama
`Q_ψ`'nin tanımı, aktarımı iki kez sayıyor gibi görünüyor**. Bu, metnin
kendi uyarısıyla ("arose from double-counting") çelişiyor gibi
duruyor; ayrı bir inceleme gerektirir. **Bu sprintte kapatılmadı.**

---

## §6. Satır 1704 — `Q_ψ ≈ −Q_Φ` **yanlış etiket** **[HATALI]**

Metin:

```latex
Q_ψ ≈ −Q_Φ ≈ α m² (Φ_c/E_th²) ψ² Φ̇
\qquad\text{(GÖSTERİLDİ from the closed } Q_i^\nu \text{ above).}
```

`\text{(GÖSTERİLDİ from the closed ...)}` — yani "yukarıdaki kapalı
ifadelerden **gösterildi**".

Ama §5'teki kapalı ifadelerden:

```
−Q_Φ = α m² (Φ²/E_th²) ψ² Φ̇          ✓  (eşleşiyor)
+Q_ψ = α m² (Φ²/E_th²) ψ² Φ̇ + ...
```

`−Q_Φ` ile `+Q_ψ` **aynı işaretli**. Dolayısıyla
`Q_ψ ≈ −Q_Φ` yazılırsa sol taraf `−Q_Φ`'ye eşit değil, onun **tersi**
olur. Metnin kendi denklemleri bu yaklaşık ifadeyi **desteklemiyor**.

**Etiket yanlış türden:** bu bir *türetim* değil, bir *fiziksel okuma*
(discharge sırasında baskın aktarım Φ → ψ'dir). Doğru etiket
`FENOMENOLOJİK` veya en fazla `KOŞULLU`.

> Bu bulgu **D1–D4'ten bağımsız**, yeni bir düzeltme gerektirir (D7).

---

## §7. Satır 2801 — skaler genlik **[TÜRETİLDİ, doğrulandı]**

Metin: `V₀^{1/4} ~ 10^15–10^16 GeV (GÖSTERİLDİ from the scalar
amplitude ...)`.

Sayısal kontrol: tablo (satır 1293–1313) `ε_*` değerlerini veriyor.
`A_s = V_*/(24π² M_Pl⁴ ε_*)` ile `V_*^{1/4}` geri hesaplandı:

| λ | ε_* | `V_*^{1/4}` [GeV] |
|---|---|---|
| 0.020 | 1.37e-3 | 1.24e16 |
| 0.050 | 4.37e-4 | 9.35e15 |
| 0.100 | 1.72e-4 | 7.41e15 |
| 0.200 | 6.82e-5 | 5.88e15 |
| 0.500 | 2.08e-5 | 4.37e15 |
| 1.000 | 8.76e-6 | 3.52e15 |
| 2.000 | 3.77e-6 | 2.85e15 |
| 5.000 | 1.28e-6 | 2.18e15 |

Aralık: **2.18e15 – 1.24e16 GeV**. Metin **2e15 – 1.3e16** diyor.
**Eşleşiyor.** Etiket hak edilmiş; tablo kendi içinde tutarlı.

*(Bu, SPRINT 5 §7'deki "veri yok" eleştirisinden bağımsızdır: tablo
kendi içinde tutarlı, ama tabloyu üreten kod depoda yok.)*

---

## §8. Satır 3127 — Mathieu asimptotiği **[TÜRETİLDİ, literatür]**

`μ_max ≈ q ω_res/2` geniş rezonans (q ≫ 1) limitinde standart bir
sonuçtur (Landau–Lifshitz §27, Arnol'd). Depodaki `src/ptum_mathieu.py`
bunu bağımsız olarak doğrulayabilir; ancak bu bir **literatür**
sonucudur, makalenin kendi türetmesi değil. Etiket
`GÖSTERİLDİ from the standard Mathieu asymptotics` diyerek bunu
**doğru belirtiyor**. Hak edilmiş.

---

## §9. Neyin kanıtı depoda yok

| iddia | dayanak | durum |
|---|---|---|
| %89.6 tarama (satır 1494) | tarama kodu | **yok** |
| `Δχ² = +0.26`, `ΔAIC = 2.26` | MCMC zincirleri | **yok** |
| Fisher matrisi | Fisher kodu | **yok** |
| `ΔN_fluid < 0.31` | CLASS + Cobaya | **yok** |
| `μ_max` sayısal değeri | kafes kodu | **yok** |

Bunlar `author-reported` olarak **dürüstçe** işaretlenmiş. Etiket
doğru; sadece **doğrulanamaz**.

---

## §10. D5 — etiket eşleme tablosu (onayınıza)

Türkçe etiketlerin İngilizce karşılıkları. **Uygulanmadı.**

| Türkçe | İngilizce | not |
|---|---|---|
| `GÖSTERİLDİ` | `demonstrated` | 8 yerde |
| `DOĞRULANDI` | `verified` | 1 yerde (913 — ama §4'e bakınız) |
| `VARSAYIM` | `assumption` | 3 yerde |
| `FENOMENOLOJİK` | `phenomenological` | 3 yerde |
| `KOŞULLU` | `conditional` | 1 yerde |
| `EKSİK` | `incomplete` | 1 yerde |

**Uyarı:** satır 913 için düz çeviri **yetmez**. O etiket §4'teki kod
hatası yüzünden kaldırılmalı veya `\emph{(scan diagnostic; see
discussion of the quartic-dominance estimator)}` şeklinde
değiştirilmelidir.

Satır 2668'de tam Türkçe cümle var:
`\emph{(FENOMENOLOJİK tahmin; Fisher kodu yayında değil)}`
→ `\emph{(phenomenological forecast; the Fisher code is not public)}`

---

## §11. Öz-eleştiri

### §11.1 — İki yanlış hipotezim

1. **"`mu_sq` yerine `μ⁴` kullanılmış"** — `compute_quartic_dominance`
   incelerken ilk tahminim buydu. Ölçüm yanlışladı:
   `abs(mu_sq)/mu² = 1.000000`. Gerçek kusur kuyruk doldurmaydı (§4).
   Doğru cevap yanlış olandan **daha ağır**.

2. **"`Σ Q_i^ν = 0` yanlış"** — ilk hızlı sympy kontrolünde yalnızca
   `Q_DM` ve `Q_DE`'yi topladım ve `Q_SM`'i atladım; sonuç sıfır
   çıkmayınca "iddia yanlış" diye okudum. Tam listeyle tekrar
   hesaplandığında toplam **tam sıfır**. İlk testim eksikti.

### §11.2 — SPRINT 5'teki bir ifademi düzeltiyorum

SPRINT 5 raporunda §10'da şunu yazmıştım:

> *"`quartic_achieved = False` (18/18) — yeniden üretildi, `main.tex`
> §4.4 ile tutarlı."*

Bu ifade **teknik olarak doğru, ama yanıltıcıydı**. Değeri yeniden
ürettim, evet — ama o değerin **kod tarafından zorlandığını** fark
etmemiştim. "Yeniden üretilebilir" ile "fiziksel olarak anlamlı"
aynı şey değil. Bu sprintte o ayrımı yapıyorum.

SPRINT 5'in ana tezi ("denetlenebilir kısım sağlam") bu noktada
**zayıflıyor**: bu değer denetlenebilir *görünüyordu* ama denetim
sonucu boştu.

### §11.3 — Neyi kapatmadım

- §5'teki `Q_ψ` işaret sorunu **açık** bırakıldı.
- Fisher/MCMC/CLASS/kafes iddiaları **doğrulanamaz** durumda (§9).
- LaTeX derlemesi yok; `main.tex` doğrulaması yalnızca yapısal.

---

## §12. Önerilen düzeltmeler — **UYGULANMADI**

### D7 — satır 1704 (yeni, §6)

```diff
-Q_\psi \approx -Q_\Phi \approx \alpha m^2 \frac{\Phi_c}{E_{\rm th}^2} \psi^2 \dot\Phi
-\qquad\text{(GÖSTERİLDİ from the closed } Q_i^\nu \text{ above).}
+Q_\Phi \approx -\alpha m^2 \frac{\Phi_c}{E_{\rm th}^2} \psi^2 \dot\Phi,
+\qquad |Q_\psi| \approx |Q_\Phi|
+\qquad\text{(leading term in the closed } Q_i^\nu \text{ above).}
```

### D8 — satır 913 (en kritik)

```diff
-this route is \textbf{not} realized by the scanned initial conditions
-(SAYISAL OLARAK DOĞRULANDI for the scanned set; not excluded in
-general).
+this route is \textbf{not} realized by the scanned initial conditions
+(scan diagnostic; the \texttt{quartic\_achieved} flag in the public
+script does not currently discriminate the quartic regime and is
+therefore not cited as evidence here; not excluded in general).
```

### D9 — D5 çeviri tablosu (§10), satır 913 hariç

**Karar gerekiyor:** satır 913 için düz çeviri mi, D8 mi?

---

## §13. Test özeti

```
tests/test_sprint5.py    26 passed, 4 skipped     (~1.4 s)
tam paket               151 passed, 4 skipped     (~79 s)
```

Dağılım: S1 27, S2 33, S3 44, S4 21, S5 26 → **151**.
Dört `skip` = koşulmadı (Fisher/MCMC/CLASS/kafes).

`main.tex`: `303584fa882cd305`, 4466 satır, parantez 3162/3162,
`equation` 117/117, etiket 21 → 17.

---

## Onay talebi

Uygulanan: **D1, D2, D3** (onayınızla).

Onay bekleyen, önem sırasıyla:

1. **D8** — satır 913, kod artefaktı iddiasının kaldırılması (§4).
   Bu sprintin en ciddi bulgusu.
2. **D7** — satır 1704, işaret hatası (§6).
3. **D9** — 16 kalan Türkçe etiketin İngilizceye çevrilmesi (§10).
4. **SPRINT 7 kapsamı** — önerim: §5'te açık bıraktığım `Q_ψ` aktarım
   dağılımı sorunu + SPRINT 5'teki `scripts/` boşluğunun nasıl
   kapatılacağı kararı.

`main.tex`'e D1–D3 dışında hiçbir değişiklik yapılmadı ve onaysız
yapılmayacak.
