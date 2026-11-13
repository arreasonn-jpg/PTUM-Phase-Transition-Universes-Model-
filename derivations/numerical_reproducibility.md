# SPRINT 5 — Sayısal Yeniden Üretilebilirlik Denetimi

**Tarih:** 2026-11-12
**Kapsam:** `ptum_task1_simulation.py`, `task1_parameter_scan_results.json`,
`scripts/` dizini, ve `main.tex`'in bu araçlara dayanan iddiaları.
**Yöntem:** kodu çalıştırma + kaynak düzeyi denetim + sayısal ölçüm.
**`main.tex` DURUMU: DEĞİŞTİRİLMEDİ** — `sha256[:16] = f708176f286e0972`,
4462 satır, parantez 3161/3161, `equation` ortamı 117/117.

---

## §0. Yönetici Özeti

Bu sprint tek bir soru sordu: **makalede raporlanan sayılar, depodaki
artefaktlardan yeniden üretilebiliyor mu, ve teşhisler fiziksel olarak
anlamlı mı?**

Cevap: **hayır, sekiz ayrı noktada.** Bunların altısı `main.tex`
değişikliği gerektirir; hiçbiri uygulanmadı.

| # | Bulgu | Etiket |
|---|-------|--------|
| 1 | Arka plan ODE'si ölçeklenmemiş; `ψ_init ≠ 0` noktaları çalışmıyor | HATALI |
| 2 | `ρ_ψ` ile `U(ψ)` **farklı potansiyeller** — sabit kayma değil, `ψ`'ye bağlı fark | HATALI |
| 3 | 18 `w_final` değerinden **16'sı** `[−1,+1]` dışında | HATALI |
| 4 | `energy_conservation` alanı korunum yasası değil (`a⁻⁴` yok) | HATALI |
| 5 | "18 noktalı tarama" homojen kanıt değil (0.004 s vs. >600 s) | EKSİK |
| 6 | `main.tex`'in çağırdığı 4 script **hiç yok** (`scripts/` yok) | EKSİK |
| 7 | "public script ile doğrulandı" iddiaları **desteklenemez** — script'te spektral kod yok | HATALI |
| 8 | `main.tex`'te 21 satırda Türkçe kanıt etiketi sızıntısı | HATALI |

Buna karşılık **yeniden üretilebilen** tek kanıt kümesi, SPRINT 4'te
doğrulanan tek-alanlı arka plan çözümleridir (bkz. §10).

---

## §1. Neden bu sprint gerekliydi

SPRINT 0–4 boyunca `main.tex`'teki iddiaları analitik olarak denetledik.
Her seferinde "sayısal olarak doğrulandı" ibaresine rastladık ve bunu
**etiketli bir kanıt** olarak okuduk. SPRINT 5'in işi, o etiketin
karşılığı olup olmadığını ölçmekti.

Ölçüm üç katmanda yapıldı:

1. **Çalıştırma:** script'i gerçekten koşturmak, ne kadar sürdüğünü ölçmek.
2. **Kaynak denetimi:** hangi fonksiyon var, hangi sembol sadece *tanımlı*.
3. **Fiziksel sağlama:** üretilen sayıların izin verilen aralıkta olup olmadığı.

---

## §2. Bulgu 1 — Arka plan ODE'si ölçeklenmemiş **[HATALI]**

`background_equations` tek bir çağrıda şunu üretiyor:

```
|y|        ≈ 1.0e19      (Φ ≈ 1e19 GeV)
1/|dy/dt|  ≈ 1.3e-39     (karakteristik zaman ölçeği)
oran       ≈ 7.6e57
```

Bu, çözücüden **tek çağrıda 57 on yıl** çözmеsini istemek demek. Pratik
sonucu, `solve_ivp`'in adım boyutunu sürekli küçültmesi ve ilerleyememesi.

**Ölçülen davranış:**

| Başlangıç koşulu | Sonuç |
|---|---|
| `ψ_init = 0` | 0.004 s içinde `success=True` |
| `ψ_init = 0.1 ψ₀` | 20 s bütçede **bitmiyor**, 900 s'de de bitmiyor |

SPRINT 5'in başında denenen 600 s'lik `frw_residual.py` koşusu da bu
duvara çarptı. Bu bir çözücü hatası değil, **boyutsuzlaştırma eksikliğidir**:
denklemler GeV ve GeV⁴ birimlerinde yazılmış, `M_P` ile normalize edilmemiş.

> **Not:** Bu, fiziğin yanlış olduğu anlamına gelmez. Denklemler doğru
> yazılmış olabilir; **çözülemiyor** olması ayrı bir sorundur. Ama
> "sayısal olarak doğrulandı" iddiası, çözülemeyen bir sistem için
> yapılamaz.

---

## §3. Bulgu 2 — `ρ_ψ` ve `U(ψ)` farklı potansiyeller **[HATALI]**

> **Bu bölüm, sprint içinde kendi ilk teşhisimi düzelttiği için önemlidir.
> Öz-eleştiri için §12.1'e bakınız.**

İlk teşhisim şuydu: "`ρ_ψ`, `U(ψ)`'deki `V_min = −μ⁴/4λ` sabit kaymasını
içermiyor; fark sabittir." **Bu yanlıştı.** Ölçüm:

```
ψ/ψ₀     ρ_code          U(ψ)            ρ − U
0.0      0.000000e+00    1.010025e+49   −1.010025e+49
0.1      1.010025e+45    9.899255e+48   −9.898245e+48
0.5      6.312656e+47    5.681391e+48   −5.050125e+48
1.0      1.010025e+49    0.000000e+00   +1.010025e+49
2.0      1.616040e+50    9.090225e+49   +7.070175e+49
```

Fark **sabit değil, işaret bile değiştiriyor**. Sebep kaynak düzeyinde açık:

```python
def shifted_potential_psi(psi, params):
    psi_0 = params.psi_0
    return 0.25*lambda*(psi**2 - psi_0**2)**2      # lam·ψ₀² = |μ²| ölçeği

def rho_psi(Phi, psi, psi_dot, params):
    m_eff_sq = meff_sq_psi(Phi, params)            # m_ψ²(1 − αΦ²/E_th²)
    return 0.5*psi_dot**2 + 0.5*m_eff_sq*psi**2 + 0.25*lambda*psi**4
```

İki fonksiyon **iki farklı kütle ölçeği** kullanıyor:

- `U(ψ)` → `λψ₀² = |μ²| = 2.01e24 GeV²`
- `ρ_ψ` → `m_eff²(Φ)`, ve benchmark noktasında **`m_eff²(Φ_c) = 0` tam olarak**

`Φ_c`'nin tanımı gereği (`1 − αΦ_c²/E_th² = 0`) bu **tam sıfır**. Yani
benchmark noktasında `ρ_ψ` içindeki kütle terimi tamamen yok oluyor ve
`ρ_ψ = ¼λψ⁴` kalıyor — potansiyelin kendisi değil, sadece kuartik parçası.

**Sonuç:** `w_ψ = p_ψ/ρ_ψ`, `U(ψ)`'nin tanımladığı potansiyelin `w`'si
değildir. İkisi arasında seçim yapılmamış; iki farklı nesne aynı isimle
kullanılmış.

`ψ = 0` noktasında ise `ρ_code = 0` olduğu için kod `0.0` korumasına düşüyor:

```
kod:     w = 0.0        (0/0 koruması)
fizik:   w = −1.0       (U(0) > 0, K = 0)
```

Bu, JSON'daki `w_final = 0.0` satırlarının kaynağıdır.

---

## §4. Bulgu 3 — 18 `w` değerinden 16'sı fiziksel aralık dışında **[HATALI]**

SPRINT 4'te türetildi: kanonik bir skaler için `K, U ≥ 0` ise
`w = (K−U)/(K+U) ∈ [−1,+1]`. `w < −1` bu Lagrangian için **imkânsızdır**.

`task1_parameter_scan_results.json` ölçümü:

```
nokta sayısı            18
w < −1                  12
w > +1                   4
aralık dışı             16   (%88.9)
min                  −24.267
max                   +6.286
```

`−24` ve `+6.3` değerleri fiziksel değil, §3'teki potansiyel uyuşmazlığının
doğrudan sonucudur: pay ve payda farklı potansiyellerden geldiğinde oran
`[−1,1]` aralığına kilitlenmez.

Ayrıca: **18 noktanın hiçbirinde** `quartic_achieved = True` değil. Bu kısım
`main.tex` §4.4 ile **tutarlıdır** (SPRINT 4'te doğrulanmıştı) ve bu sprint
onu doğruluyor.

---

## §5. Bulgu 4 — `energy_conservation` bir korunum yasası değil **[HATALI]**

Alan adı şunu vaat ediyor: enerji korunumu. Kod ise şunu hesaplıyor:

```python
energy_conservation = max|ρ_φ(t) + ρ_ψ(t) − ρ_φ(0) − ρ_ψ(0)|
```

Genişleyen evrende doğru ifade `ρa⁴ = sabit`'tir, yani:

```
d/dt (a⁴ρ) = 0
```

Kodda `a⁴` çarpanı **yok**. Dolayısıyla ölçülen sayı, evrenin genişlemesinden
kaynaklanan fiziksel seyrelmeyi "korunum ihlali" olarak raporluyor.

**Ölçülen değerler:** `4.06e49 … 4.40e51` — yani 50 mertebe. Bu sayı bir
hata payı değil, ölçek hatasıdır. `a⁻⁴` ile düzeltilse bile, §3'teki
potansiyel uyuşmazlığı yüzünden `ρ`'nin kendisi güvenilir değildir.

**Sonuç:** bu alan, tarama çıktısında kanıt olarak kullanılamaz. Ne
korunumu doğrular, ne ihlalini gösterir.

---

## §6. Bulgu 5 — "18 noktalı tarama" homojen kanıt değil **[EKSİK]**

Tarama üç `ψ_init` değeri üzerinde kurulmuş: `0`, `4.483e10`, `4.483e11`.

| `ψ_init` | gerçek çalışma davranışı |
|---|---|
| `0` | 0.004 s — anında döner, çünkü `ψ` ekseni tamamen durgun |
| `≠ 0` | bitmez (§2) |

Yani 18 noktanın yalnızca bir alt kümesi **gerçekten entegre edilmiş**
olabilir; kalanlar ya zaman aşımına düşmüş ya da farklı (gevşetilmiş) ayarlarla
koşturulmuş olmalıdır — depoda bunu gösteren bir kayıt yok.

Bu, taramanın **bilimsel olarak değersiz** olduğu anlamına gelmez; ama
"18 bağımsız nokta" olarak sunulamayacağı anlamına gelir. Kanıtın ağırlığı
18 değil, pratikte 6 noktadır (`ψ_init = 0` satırları).

---

## §7. Bulgu 6 — `scripts/` dizini hiç yok **[EKSİK]**

`main.tex` dört yerde `docker run … scripts/<dosya>.py` çağırıyor:

| `main.tex` satırı | çağrılan dosya | durum |
|---|---|---|
| 3944 | `scripts/reproduce_figures.py` | **yok** |
| 3980 | `scripts/compare_class_camb.py` | **yok** |
| 4189 | `scripts/run_lattice.py` | **yok** |
| 4199 | `scripts/convergence_test.py` | **yok** |

`ls scripts` → dizin mevcut değil. Ayrıca `main.tex`'in bahsettiği
`ptum-cosmology` Docker imajı için depoda **hiçbir Dockerfile yok**.

Bu, okuyucunun makalenin kendi talimatıyla hiçbir figürü üretemeyeceği
anlamına gelir. Yeniden üretilebilirlik açısından bu, en ağır bulgudur:
iddialar yanlış olmasa bile **doğrulanamaz**.

---

## §8. Bulgu 7 — "public script ile doğrulandı" iddiaları desteklenemez **[HATALI]**

`main.tex` üç yerde `ptum_task1_simulation.py`'yi sayısal doğrulamanın
kaynağı olarak gösteriyor:

| satır | iddia |
|---|---|
| 1282 | `Δn_s ≈ 5e-4`, `\|Δr\|/r ≈ 1.5%` — "SAYISAL OLARAK DOĞRULANDI with the public script" |
| 1399 | 200 log-aralıklı `k` modu, `n_s^MS`, `r^MS`, `α_s^MS` — "with the public script" |
| 2795 | "exact-background check SAYISAL OLARAK DOĞRULANDI with the public script" |

**Kaynak düzeyinde ölçüm:** script'in tamamında `k_modes` **bir kez** geçiyor
— sadece `InitialConditions` dataclass'ında tanımlanıyor (satır 100), hiçbir
yerde **okunmuyor**. `power_spectrum`, `mukhanov`, `transfer_function`
sembollerinin hiçbiri dosyada yok.

Script yalnızca **homojen arka plan** çözüyor:
`background_equations` → `Φ̈`, `ψ̈`. Pertürbasyon denklemi, güç spektrumu,
transfer fonksiyonu yok.

**Sonuç:** `n_s`, `r`, `α_s` bu script'ten **hesaplanamaz**. Dolayısıyla
üç atıf da yanlıştır — iddiaların kendisi yanlış olmasa bile, gösterilen
kaynak o iddiayı üretemez. Bu, kanıt etiketinin **yanlış atanmasıdır**.

---

## §9. Bulgu 8 — `main.tex`'te Türkçe etiket sızıntısı **[HATALI, yayın kalitesi]**

`main.tex` İngilizce bir makale, ancak kanıt etiketleri Türkçe bırakılmış:

| etiket | sayı |
|---|---|
| `GÖSTERİLDİ` | 9 |
| `DOĞRULANDI` | 4 |
| `VARSAYIM` | 3 |
| `FENOMENOLOJİK` | 3 |
| `KOŞULLU` | 1 |
| `EKSİK` | 1 |

**Toplam 21 satır** bu etiketlerden en az birini içeriyor.
(Örnekler: satır 913, 1282, 1399, 2795 — "SAYISAL OLARAK DOĞRULANDI".)

Ayrıca satır 2665–2666 civarında **tam bir Türkçe cümle** var
(`tahmin; Fisher kodu yayında değil`).

Bu bulgu fiziğe dokunmaz ama gönderim engelleyicidir: hakem bunu görür.
Düzeltme mekaniktir (etiketleri İngilizceye çevirmek), ancak **her etiketin
hangi İngilizce karşılığa gideceği bir karardır** ve onay gerektirir.

---

## §10. Neyin gerçekten yeniden üretilebildiği **[TÜRETİLDİ]**

Adil olmak gerekirse, pipeline'ın bir parçası sağlam:

| kanıt | durum |
|---|---|
| Tek-alanlı arka plan `⟨w⟩ = −1` (donmuş benchmark) | **yeniden üretildi** (SPRINT 4) |
| Amplitüd tablosu (`2,3,4,5,10,100 ψ₀`) | **yeniden üretildi** (SPRINT 4) |
| `virial: ⟨w⟩ = (n−2)/(n+2)` | **yeniden üretildi** (SPRINT 4) |
| `m_eff²(Φ_c) = 0` | **yeniden üretildi** (bu sprint) |
| `quartic_achieved = False` (18/18) | **yeniden üretildi**, `main.tex` §4.4 ile tutarlı |
| `w ∈ [−1,1]` sınırı | **yeniden üretildi** (SPRINT 4 türetmesi) |

Yani sorun "her şey bozuk" değil. Sorun şu: **denetlenebilir olan kısım
sağlam, denetlenemeyen kısım ise makalenin ana iddialarını taşıyor.**

---

## §11. Önerilen `main.tex` düzeltmeleri — **UYGULANMADI**

Aşağıdakiler inceleme içindir. Hiçbiri uygulanmadı; her biri ayrı onay ister.

### D1 — satır 1282–1283 (en kritik)

```diff
-\(\vert\Delta r\vert/r\simeq1.5\%\). \emph{(SAYISAL OLARAK DOĞRULANDI with the
- public script \texttt{ptum\_task1\_simulation.py}.)}}
+\(\vert\Delta r\vert/r\simeq1.5\%\). \emph{(Analytic slow-roll vs.\ exact
+ background estimate; the public script
+ \texttt{ptum\_task1\_simulation.py} integrates the homogeneous background
+ only and does not compute $n_s$ or $r$.)}}
```

### D2 — satır 1399

```diff
-(SAYISAL OLARAK DOĞRULANDI, with the public script):
+(estimated from the exact background; the 200-mode Mukhanov--Sasaki
+ integration is not contained in the public script):
```

### D3 — satır 2795

```diff
-check SAYISAL OLARAK DOĞRULANDI with the public script)};
+check performed at the exact-background level; the public script
+ integrates the background only)};
```

### D4 — §7 (satır ~3944–4200) — eksik script'ler

Scriptler eklenmeli **veya** metin "these scripts are available from the
authors on request" olarak değiştirilmeli. İkincisi dürüst ama zayıf;
birincisi doğru çözüm. **Karar sizin.**

### D5 — §9 (21 satır) — Türkçe etiketler

Mekanik çeviri mümkün, ama önce bir eşleme tablosu onayınıza sunulmalı:
`GÖSTERİLDİ → demonstrated`, `DOĞRULANDI → verified`,
`VARSAYIM → assumption`, `FENOMENOLOJİK → phenomenological`,
`KOŞULLU → conditional`, `EKSİK → incomplete`.

### D6 — opsiyonel: `energy_conservation` alanının adı

JSON'daki alan adı `energy_conservation` yanıltıcı. `max_drho` gibi nötr bir
ada çevrilmesi veya `a⁴ρ` ile yeniden tanımlanması önerilir. Bu bir kod
değişikliğidir, `main.tex` değil — ayrı onay ister.

---

## §12. Öz-eleştiri

### §12.1 — Bu sprintte kendi teşhisimi düzelttim

Sprint başında şunu yazmıştım: *"`ρ_ψ`, `U(ψ)`'deki sabit `V_min` kaymasını
içermiyor; fark sabittir ve `−μ⁴/(4λ)`'ye eşittir."*

**Bu yanlıştı.** `test_rho_minus_U_is_the_constant_v_min` testi tam da bunu
iddia ediyordu ve **başarısız oldu**. Ölçüm, farkın sabit olmadığını, işaret
değiştirdiğini gösterdi (§3). Gerçek sebep daha ciddi: iki fonksiyon iki
**farklı kütle ölçeği** kullanıyor, ve benchmark noktasında biri tam sıfır.

Doğru teşhis yanlış teşhisten **daha ağır** bir bulguya götürdü. Testin
başarısız olması iyi bir şeydi.

### §12.2 — İki test hatası daha

1. **`claim_is_supported`** — "not public" alt-dizgisine bakıyordu; Docker
   imajı girdisi "not referenced by any Dockerfile" dediği için alt-dizge
   eşleşmedi ve fonksiyon `True` döndürdü. Durum dizgileri artık `present`/
   `absent` ile başlıyor ve mekanik olarak karar veriliyor.

2. **`time_limit`** — `signal.alarm()` tam sayı saniye kabul eder;
   `int(0.5) = 0` alarmı **tamamen kapatıyordu**. `np.ceil` + `max(1, …)` ile
   düzeltildi. Bu bir test altyapısı hatasıydı, fizik bulgusu değil.

### §12.3 — Neyi yapamadım

- **LaTeX derlemesi yok.** `pdflatex`/`latexmk` kurulu değil. `main.tex`
  doğrulaması yalnızca yapısaldır (parantez, ortam sayısı), anlamsal değil.
- **`ψ_init ≠ 0` noktalarını çalıştıramadım.** 900 s'de bitmediler. Yani
  JSON'daki bu satırların *nasıl* üretildiğini bilmiyorum — sadece
  *yeniden üretilemediğini* biliyorum.
- **CLASS/Cobaya/lattice çıktıları yok.** Dört test `skip` olarak işaretli;
  bunlar "geçti" değil, **"koşulmadı"**.

---

## §13. Test özeti

```
tests/test_sprint5.py    21 passed, 4 skipped      (~1.7 s)
tam paket               146 passed, 4 skipped      (~63 s)
```

Dağılım: S1 27, S2 33, S3 44, S4 21, S5 21 → **146**.
Dört `skip`, §12.3'teki bloke kalemlerdir ve raporda **koşulmadı** olarak
kayıtlıdır.

---

## §14. Sonuç ve SPRINT 6 önerisi

SPRINT 5'in sorusu "yeniden üretilebilir mi?" idi. Cevap: **kısmen, ve tam
olarak ana iddialarda değil.**

En önemli üç tespit:

1. `scripts/` yok → makalenin kendi talimatı çalışmıyor (§7).
2. `ρ_ψ` ile `U(ψ)` farklı potansiyeller → tüm `w` değerleri güvenilmez (§3–4).
3. "public script ile doğrulandı" → script'te spektral kod yok (§8).

**SPRINT 6 için öneri (onayınıza):** bu sprintin açtığı ama kapatmadığı
soruyu ele almak — `main.tex`'in genel kanıt etiketi envanteri. 21 Türkçe
etiket, MASTER_AUDIT tablosundaki iddialarla eşleştirilip her birinin
gerçekten hangi kanıta dayandığı tek tek yazılmalı. Bu, D5'in de önkoşulu.

---

## Onay talebi

Bu rapor `main.tex`'e **dokunmadı**. Devam için onayınız gereken üç ayrı şey:

1. **SPRINT 6'nın kapsamı** (§14'teki öneri uygun mu?)
2. **D1–D3 diffleri** — "public script" atıflarının düzeltilmesi
   (en kritik olanlar; ayrı ayrı da onaylayabilirsiniz)
3. **D5 etiket eşleme tablosu** — Türkçe etiketlerin İngilizce karşılıkları

`main.tex`'e yapılacak hiçbir değişiklik bu onay olmadan uygulanmayacaktır.
