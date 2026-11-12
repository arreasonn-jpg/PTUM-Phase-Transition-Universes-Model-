# AUDIT_00_INVENTORY.md — SPRINT 0: Denetim Envanteri

**Proje:** PTUM (Phase Transition Universes Model)
**Denetlenen depo:** `https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-.git`
**Denetlenen commit:** `6c2d153` ("ilk commit"), dal: `main`
**Denetim dalı:** `arena/172208ee-ptum-phase-transition-universe`
**Denetim tarihi:** 2026-11-12
**Kapsam:** SPRINT 0 — yalnızca envanter ve çelişki matrisi.
**Değişiklik durumu:** **Hiçbir mevcut dosya değiştirilmedi.** Tek yeni dosya bu rapordur.

> **Not:** Bu rapor bir *denetim envanteridir*, doğrulama sertifikası değildir.
> `main.tex` (43 sayfa) sandbox içinde derlenmedi (TeX kurulu değil); derleme
> yalnızca depodaki `main.pdf` / `main.log` üzerinden okundu, yeniden üretilmedi.
> LaTeX'in derlenmesi hiçbir koşulda bilimsel doğrulama sayılmaz.

---

## 0. Yönetici özeti

| Metrik | Değer |
|---|---|
| Toplam dosya (depo kökü) | 60 (25 adet Windows `Zone.Identifier` çöp dosyası dahil) |
| İzlenen dosya | 60 (`.gitignore` yok) |
| `main.tex` boyutu | 208.3 KB / 4460 satır / 147 numaralı denklem |
| Şekil referansı / disk | 18 referans, 18 PDF mevcut (eksik yok), 2 PDF hiç referanslanmamış |
| Python kodu | 1 dosya (`ptum_task1_simulation.py`, 23.8 KB) |
| Test dosyası | **0** |
| CLASS patch / Cobaya YAML / MCMC zinciri / lattice verisi | **0 — kökte yok** |
| `PTUM.zip` | 39 girdi; sadece makale + figürler + log. **Kod, patch, YAML, lattice yok** |
| Kod/veri adresi tutarlılığı | 6 belge başka repoyu (`ErdemEsa/ptum-cosmology`) gösteriyor; **o depo HTTP 404** |
| Tespit edilen kritik hata | **9/9 doğrulandı**, hepsi bağımsız olarak yeniden üretildi |
| Yeni bulgu (bu denetimde) | **11** (aşağıda §5.2) |

**Sonuç:** `PTUM_LIBRARY_FINAL_v1.2_CODE_AVAILABLE_CORRECTED_COMPLETE: PASS`
etiketi (`PTUM_FINAL_AUDIT.md`) **desteklenmiyor**. Kod-adı geçen CLASS patch'i,
Cobaya YAML'ları, MCMC zincirleri ve lattice çıktıları bu depoda dosya düzeyinde
yoktur; işaret edilen ikinci depo da yayında değildir. Durum: **FAIL**.

---

## 1. Dosya ve bağımlılık envanteri

### 1.1 Kaynak / içerik dosyaları

| Dosya | Boyut | Rol | Durum |
|---|---|---|---|
| `main.tex` | 208 KB | Ana makale (147 denklem, 43 sayfa) | Ana kaynak |
| `main.pdf` | 3.70 MB | Derlenmiş makale | `main.log` ile tarih olarak eşleşiyor |
| `svjour.cls`, `svepj.clo` | 42 KB / 10 KB | Springer EPJ sınıfı | Gerekli (yoksa derlenmez) |
| `figures/*.pdf` | 18 PDF | Şekiller | 18/18 mevcut, 2'si kullanılmıyor |
| `ptum_task1_simulation.py` | 23.8 KB | Tek sayısal kod | bkz. §4 |
| `task1_parameter_scan_results.json` | 9.3 KB | 18 noktalı tarama özeti | Yeniden üretildi, birebir aynı |
| `TASK1_FINAL_FINDINGS.md` | 6.4 KB | Taykonik→kuartik bulguları | Ana metinle **çelişiyor** (B-01) |
| `TASK1_FINDINGS_SUMMARY.md` | 7.6 KB | Aynı, erken sürüm | Tekrar |
| `TASK1_TACHYONIC_QUARTIC_RESEARCH_PLAN.md` | 11.9 KB | Araştırma planı | — |
| `PTUM_THEORETICAL_INVENTORY_REPORT.md` | 12.2 KB | Öz-envanter | İçinde "PROVEN" etiketli maddeler var (B-12) |
| `PTUM_CLAIM_BOUNDARY.md` | 3.4 KB | İddia sınırı v1.2 | Adres hatası (B-20) |
| `PTUM_REPRODUCIBILITY_NOTES.md` | 1.2 KB | Yeniden üretilebilirlik | Adres hatası (B-20) |
| `PTUM_FINAL_AUDIT.md` / `.json` | 745 B / 561 B | "PASS" beyanı | **Doğrulanamıyor** (B-02) |
| `PTUM_LIBRARY_MANIFEST.md` | 1.0 KB | Paket manifestosu | `PTUM.zip` içeriğiyle **uyumsuz** (B-03) |
| `PTUM_FILE_LIST.txt` | 987 B | Zip dosya listesi | `compile1.log`, `compile2.log` zip'te var, repoda yok |
| `PTUM_LIBRARY_SUPPLEMENTARY_NOTE.tex/.pdf` | 1.5 KB | Ek not | — |
| `FINAL_SUMMARY.md` | 4.9 KB | Revizyon özeti | "All 11 referee report tasks complete" (doğrulanmamış) |
| `cover_letter.txt`, `highlights.txt`, `page2.txt` | küçük | Yayın evrakı | — |
| `fix_indent.py`, `fix_indent2.py` | 1.9/2.4 KB | Tek seferlik yama scriptleri | Kaynak değil |

### 1.2 Derleme artıkları ve taşınabilirlik kirliliği

| Öğe | Adet | Değerlendirme |
|---|---|---|
| `main.aux`, `main.log`, `main.out` | 3 | Derleme artığı; kaynak değil. `main.log` tanık olarak değerli (43 sayfa), ama izlenmemeli. |
| `*Zone.Identifier` (NTFS ADS) | 25 | Windows indirme artığı, sıfır bilgi içeriği. **Silinmeli.** |
| `PTUM.zip` (6.2 MB) | 1 | Git içinde binary arşiv; makale+figürlerin **eski bir kopyası**. `main.tex` SHA256₀₋₁₆: zip `64e8d3d6…`, depo `ba1a6309…` → **farklı sürüm**. Git dışında tutulmalı. |
| `.gitignore` | **yok** | Öneri: `*.aux *.log *.out *.toc *.bbl *.blg *Zone.Identifier *.zip` |

> Silme önerisi (uygulanmadı, onay bekliyor): `*Zone.Identifier` (25 dosya) → `git rm`.
> `main.aux/log/out` → `git rm --cached` + `.gitignore`. `PTUM.zip` → depo dışı arşiv (Zenodo) + SHA256.
> **Not:** `main.log` bu denetimde tek "yeniden üretilebilir derleme kanıtı" olduğu için arşiv kopyası saklanmalı.

### 1.3 Bağımlılıklar

- **LaTeX:** `svjour.cls` (Springer EPJ), `svepj.clo`, `lmodern`, `amsmath/amssymb/mathtools`, `graphicx`, `booktabs`, `array`, `hyperref`, `enumitem`. Log'daki yollar `C:/Users/Gamze/...MiKTeX` → **derleme Windows/MiKTeX'te yapılmış**, sandbox'ta yeniden üretilemedi.
- **Python:** `numpy`, `scipy` (`solve_ivp`, DOP853). Depoda `requirements.txt`, `pyproject.toml`, `Dockerfile` **yok**. Sürüm sabitlemesi yok; JSON'a sürüm/commit/seed yazılmıyor (§4-H).
- **CLASS / Cobaya / PolyChord / CAMB / LATTICEEASY:** beyan ediliyor, **dosya yok**.

---

## 2. `main.tex` denklem envanteri (Lagrangian / EOM / T_μν / Q / Mathieu)

Denklem numaraları `main.aux` → `\newlabel` üzerinden **doğrulandı** (tahmin değil).
"Etiket" sütunu `\label{…}` adıdır; boşsa denklem etiketsizdir.

### 2.1 Konvansiyonlar ve Lagrangian

| Eq. | Satır | Etiket | İçerik | Durum |
|---|---|---|---|---|
| (1) | 121 | `eq:pfd_signature` | pfd imzası `w=1/3, c_s²=1/3, σ=0` | FENOMENOLOJİK |
| (2) | 312-316 | — | `G_μν = T_μν/M_Pl²`, `T_μν = -2/√-g δ(√-g L_m)/δg^{μν}` | Konvansiyon beyanı |
| (2) | 318-320 | — | `L = ½(∂φ)² - V` → `ρ=½φ̇²+V`, `p=½φ̇²-V` | **HATALI (B-04)** |
| (3) | 368 | — | `L_PTUM = L_fuel + L_act + L_DM + L_DE` | Eksik: `L_rh` yok (B-05) |
| (4) | 375 | — | `L_fuel = ½(∂Φ)² - V_eff(Φ)` | Kinetik işaret B-04 |
| (5) | 387 | `eq:veff` | `V_eff = V₀(1-e^{-λΦ²}) + CW` | Boyut sorunu B-15 |
| (7) | 443 | `eq:lact` | `L_act = ½(∂ψ)² - ½m²(1-αΦ²/E_th²)ψ² - λ_ψψ⁴/4` | Kinetik işaret B-04; açılım işareti B-06 |
| (9) | 457 | `eq:ptum_threshold_box` | `m_eff²<0 ⇔ |Φ|>Φ_c=E_th/√α` | TÜRETİLDİ (tanımdan) |
| (10) | 469 | — | `L_DM = ½(∂χ)² - ½m_χ²χ² - g_DMχ²Φ_res²` | Kinetik işaret B-04 |
| (11) | 475 | — | `L_DE = ½(∂Φ_res)² - W(Φ_res)` | Kinetik işaret B-04 |
| (12) | 486 | `eq:wpot` | `W = W₀e^{-κΦ_res²}(1-e^{-λ_resΦ_res²}) + Λ_NP⁴e^{-S_E}cos(Φ_res/f_res)` | VARSAYIM |
| — | 1668-1690 | — | `L_rh = -y_ψψf̄f - ½g_ψψ²φ_SM²` (yalnızca §5.5.2'de tanıtılıyor) | Toplam Lagranjiyen'de yok (B-05) |

**Konvansiyon çelişkisi:** Metin `(-+++)` ve `T_μν = -2/√-g δS/δg^{μν}` diyor (satır 306-320);
ama §5.5.1'deki DM/DE tensörleri (Eq. 70) `T = ∂χ∂χ - g[½(∂χ)² - …]` yazıyor; bu **ters parantez**
işaretidir ve `T₀₀ = -ρ` verir. Sektör tensörlerinin hiçbiri seçilen tanımdan yeniden türetilmemiş.

### 2.2 Hareket denklemleri

| Eq. | Satır | Etiket | İçerik | Durum |
|---|---|---|---|---|
| (13) | 528 | `eq:frw1` | `Φ̈+3HΦ̇+V_eff,Φ - (αm²/E_th²)Φψ² = 0` | **HATALI** — L ile işaret uyuşmuyor (B-06) |
| (14) | 536 | `eq:frw2` | `ψ̈+3Hψ̇+m²(1-αΦ²/E_th²)ψ+λ_ψψ³ = 0` | +1/2 kinetikle **uyuşmaz** (B-04) |
| (15) | 541 | `eq:frw3` | `χ̈+3Hχ̇+m_χ²χ+2g_DMχΦ_res² = 0` | Doğru (L_DM ile tutarlı) |
| (16) | 556 | `eq:frw4` | `Φ̈_res+3HΦ̇_res+W_,Φ+2g_DMχ²Φ_res = 0` | Doğru |
| (21) | 600 | `eq:Phi_eom` | Eq.(13)'ün "türetimi" | Türetim, hatalı Lagranjiyen'e dayanıyor |
| (34) | 763 | `eq:psi_eom_full` | `ψ̈+3Hψ̇-μ²ψ+λ_ψψ³ = 0` | Doğru (m_eff² sabit varsayımıyla) |

**Not:** §3.4.1 "tüm EOM'ler tutarlı biçimde türetildi" diyor (satır 621-623). Bu, yalnızca
yazılı (hatalı) Lagranjiyen içinde döngüsel olarak doğrudur; **eylemden bağımsız bir türetim yoktur.**

### 2.3 T_μν ve Q_i^ν

| Eq. | Satır | Etiket | İçerik | Durum |
|---|---|---|---|---|
| (62) | 1538 | — | `∇_μT^{μν}_total = 0` | VARSAYIM (kanıt yok) |
| (63) | 1544 | — | `ρ̇_i + 3H(ρ_i+p_i) = Q_i` | Tanım |
| (64) | 1554 | — | `∇_μT^{μν}_i = Q_i^ν`, `Σ Q_i^ν = 0` | Tanım |
| (70) | 1580 | — | `T^{μν}_DM`, `T^{μν}_DE` | **Parantez işareti ters** (B-07) |
| (71) | 1589 | — | `Q_DM^ν = -2g_DMχ²Φ_res ∂^νΦ_res` | TÜRETİLDİ ✓ |
| (72) | 1594 | — | `Q_DE^ν = +2g_DMχ²Φ_res ∂^νΦ_res` | TÜRETİLDİ ✓ |
| (76) | 1670 | — | `Q_ψ^ν = +αm²(Φ/E_th²)ψ²∂^νΦ + y_ψψ f̄γ^νf + g_ψψ²φ_SM∂^νφ_SM` | **HATALI** (B-08: boyut + işaret) |
| (77) | 1672 | — | `Q_Φ^ν = -αm²(Φ/E_th²)ψ²∂^νΦ` | **HATALI** (B-08) |
| (78) | 1679 | — | `Q_DM^ν` (tekrar) | ✓ |
| (79) | 1680 | — | `Q_DE^ν` (tekrar) | ✓ |
| (80) | 1681 | — | `Q_SM^ν = -y_ψψf̄γ^νf - g_ψψ²φ_SM∂^νφ_SM` | **HATALI** (B-08) |
| (69) | 1700 | — | `Q_ψ ≈ αm²(Φ_c/E_th²)ψ²Φ̇` "GÖSTERİLDİ" | Etiket **haksız** (B-09) |

**Boyut testi (bağımsız, `/tmp/audit/dims.py`):** Eq.(76)–(80)'deki **yedi** terimin
tamamı `[GeV]⁴`'tür; `[Q^ν] = [∇_μT^{μν}] = GeV⁵` olmalıdır. Yalnızca arka plan ifadesi
`Q = Γ_ψρ_ψ` doğru boyuttadır. Tablo `main.tex` §B.2'de (satır 3846) `Q_i^ν` için
"`[GeV]⁵`" yazıyor → **makale kendi boyut tablosuyla çelişiyor.**

### 2.4 Mathieu / Floquet

| Eq. | Satır | Etiket | İçerik | Durum |
|---|---|---|---|---|
| (98) | 3087 | — | `m_χ,eff² = m_χ² + 2g_DMΦ_res²` | TÜRETİLDİ ✓ |
| (99) | 3102 | — | `q = g_DM A_res²/ω_res²`, `A_k = (k²/a²+m_χ²)/ω_res²` | **HATALI** (B-10, B-11) |
| (100) | 3112 | — | FRW mod denklemi (H sönümü dahil) | Doğru ama Mathieu'ye indirgerken tutarsız |
| (101) | 3119 | — | `χ_k ∝ e^{μ_k t}` | Tanım |
| (102) | 3128 | — | `n_k ≈ exp(2μ_k N/ω_res)` | Boyut/argüman kontrolü hatalı (B-13) |
| (103) | 3137 | — | `n_χ ~ ω_res³/(2π)³ · exp(2μ_max N/ω_res)` | **HATALI** (B-13) |
| (104) | 3146 | — | `Ω_χh² ~ 0.12 (m_χ/10¹²)(ω_res/10¹³)³ exp(…)` | Çıktı değil, **kalibrasyon** (B-14) |
| — | 3120-3124 | — | `μ_max ≈ q ω_res/2` "GÖSTERİLDİ" | **HATALI** (B-12) |

**Bağımsız Floquet hesabı (monodromi, `/tmp/audit/mathieu2.py`, `mathieu3.py`):**

| q | ν_max (bulundu) | ν_max/√q | makale: q/2 |
|---|---|---|---|
| 0.02 | 0.010000 | — | 0.010000 (dar bant: **makale doğru**) |
| 0.5 | 0.247211 | — | 0.250000 (≈%1 hata) |
| 5 | 3.18004 | 1.422 | 2.5 |
| 20 | 6.31330 | 1.412 | 10 |
| 100 | 14.0724 | 1.407 | 50 |
| 1024 | 44.0082 | 1.375 | 512 |

→ Geniş rezonansta `μ_max → √(2q)·ω_res ≈ 0.45·ω_res`, **`qω_res/2` değil**.
Benchmark `q ≈ 5.9×10⁷` için: makale `2.95×10⁷ ω_res`, monodromi `≈1.08×10⁴ ω_res`
→ **~2700 kat sapma**. İddia `GÖSTERİLDİ` etiketini hak etmiyor: **HATALI**.

**Ayrıca:** `A_k ≈ 1 ⇒ ω_χ ≈ ω_res/2` çıkarımı, `z = ω_res t` değişkeniyle tutarsızdır;
`A_k`'ye `g_DM A_res²/ω_res²` sabit katkısı eksiktir; `x = ω_res t` konunca `A_k` bir **frekans
oranının karesi** olur ve `A_k ≈ 1` demek `ω_χ ≈ ω_res` demektir (faktör-2 hatası).

### 2.5 Diğer kritik nicelikler

| Konu | Satır | Sorun |
|---|---|---|
| `V_eff = V₀(1-e^{-λΦ²})`, `λ = 0.02` | 380, 1219 | Birim: `[λΦ²]` boyutsuz olmalı → `[λ]=GeV⁻²`. Tablo (satır 3823) `[λ]=GeV⁻²` diyor; kodda `λ=0.02` **GeV⁻²** olarak kullanılıyor → `λΦ_c² ≈ 5.9×10³⁶`, üstel tamamen çöküyor (B-15) |
| `Φ_end ~ M_Pl/√λ` | 1145 | Kodla `λ` yorumu çelişiyor; metin `λ~1/M_Pl²` ima ediyor |
| `c_s² = ṗ/ρ̇ = 1/3` | 1903 | `c_a²` ile `c_s²` karıştırılmış; §3.6.1'deki doğru ayrım burada bozuluyor (B-16) |
| `σ_ψ = (ρ-p-2p_⊥)/(ρ+p)` | 1846-1851 | Homojen alan için tanım gereği 0; **kanıt değil, totoloji** |
| `σ_ψ=0` tanımı + "F_ℓ var ama katkı vermez" | 1879-1895 | Birbirini tutmayan iki ifade (B-17) |
| `Φ_res` erken `ω~10¹³ GeV` / geç `m~H₀` | 3175-3194 | Köprü **türetilmemiş** (B-18) |
| "entropy S_obs ~ 10⁸⁸, tutarlı" | 1763-1766, 3309 | Boyut/hesap doğrulanmamış; döngüsel (girdi=çıktı) |
| `Σ_i Ω_i = 1` "<10⁻¹²" | 3697-3699 | Hangi çıktıdan? Dosya yok (B-19) |

---

## 3. §9'daki 14 bulgunun bağımsız doğrulaması

Her satırda "Kanıt" sütunu bu denetimde **yeniden üretilen** kontrolü gösterir.
Yöntem: `/tmp` içinde (depoya yazmadan) bağımsız Python; `scipy`/`numpy` sandbox'a kuruldu.

| # | İddia | Durum | Kanıt |
|---|---|---|---|
| 1 | `(-+++)` + `+½(∂φ)²` + yazılı EOM tutarsız | **DOĞRULANDI** | `+½` → EL kalıntısı `-1.33 ≠ 0`; `T₀₀ = 2.155 ≠ ½φ̇²+V = 3.845`. `−½` → EL `0`, `T₀₀ = 3.845` ✓. Tek kinetik işaret hem EOM'yi hem `ρ`'yi vermez. |
| 2 | `L_act` açılımı ile `L_int^{ψΦ}` zıt işaretli | **DOĞRULANDI** | Eq.(7) açılımı: `+αm²Φ²ψ²/2E_th²`; Eq.(74): `-αm²Φ²ψ²/2E_th²`. Metin satır 565-567 kendi kendine "işaret" tartışması yapıyor. |
| 3 | `Q_ψ^ν` (Yukawa) GeV⁴, olması gereken GeV⁵ | **DOĞRULANDI** | `y ψ f̄γ^νf` = 0+1+3 = 4. Genelleşti: Eq.(76)-(80)'in **tamamı** GeV⁴ (7 terim). |
| 4 | Mathieu `q` faktör-2 | **DOĞRULANDI** | Standart form `A-2q cos2z`; `g A²cos² = (gA²/2)(1+cos2z)` → `q = -gA²/(2ω²)`. Makale `gA²/ω²`. |
| 5 | `A_k`'de `g_DM A_res²` eksik | **DOĞRULANDI** | `m_eff²` sabit kısmı `g_DM A_res²` Eq.(99)'da yok. |
| 6 | `A_k≈1 ⇒ ω_χ≈ω_res/2` tutarsız | **DOĞRULANDI** | `z=ω_res t` ile `A_k = (ω_χ/ω_res)² + …`; `A_k≈1 ⇒ ω_χ≈ω_res`. |
| 7 | `μ_max~qω_res/2` türetilmemiş | **DOĞRULANDI** | Monodromi: geniş q'da `μ_max ≈ 0.45ω_res`, `q`'dan bağımsız. |
| 8 | `rho_phi`/`rho_psi` çift sayım | **KISMEN DOĞRULANDI** | Kod evet: aynı `½m_eff²ψ²` iki yerde. Sayısal etki `H`'de **2×10⁻⁷** (baskın değil). Ama `save_results`'taki `energy_conservation` metriği de aynı çift sayımı kullanıyor. |
| 9 | `rho(t)-rho(0)` enerji korunumu testi değil | **DOĞRULANDI** | FRW'de `ρ_tot` sabit değil. Kod metriği `4.04×10⁻⁷` "küçük" görünüyor; doğru süreklilik kalıntısı ise `|ρ̇+3H(ρ+p)|/(3Hρ)` → `~10⁻¹⁰`. Metrik **yanlış şeyi** ölçüyor. |
| 10 | Q quartic metriği sabit `μ_sq` | **DOĞRULANDI** | `PTUMParameters.mu_sq` `Φ = 1.01Φ_c`'de bir kez hesaplanıyor; `Q` içinde `Phi(t)` yok. |
| 11 | CLASS/Cobaya/MCMC hangi depoda? | **DOĞRULANDI (yok)** | Kökte yok; `PTUM.zip`'te yok; `ErdemEsa/ptum-cosmology` → **HTTP 404**. |
| 12 | Lattice verisi yok, `PTUM.zip` incelenmeli | **DOĞRULANDI** | Zip 39 girdi: 18 figür + makale + loglar. `.py/.patch/.yaml/snapshot` = 0. |
| 13 | Farklı GitHub URL'leri | **DOĞRULANDI** | 6 belge `ErdemEsa/ptum-cosmology`; `git remote` `arreasonn-jpg/PTUM-…`. |
| 14 | "GÖSTERİLDİ" etiketleri çelişkili | **DOĞRULANDI** | 9 adet `GÖSTERİLDİ`; en az 4'ü (§2.3, §2.4) aynı metinde başka yerde "conditional/not independently reproduced". |

---

## 4. `ptum_task1_simulation.py` kod denetimi

Kod `/tmp/audit/` kopyasında `numpy 2.4.6 / scipy 1.17.1` ile **çalıştırıldı**.
`task1_parameter_scan_results.json` **birebir yeniden üretildi** (18/18 nokta,
`n_oscillations` dizisi aynı) → kod-JSON eşleşmesi **PASS**.

| Harf | Sorun | Doğrulama | Durum |
|---|---|---|---|
| A | `rho_phi` ve `rho_psi` aynı `½m_eff²(Φ)ψ²`'yi içeriyor | Etki `H`'de `2.0×10⁻⁷`; baskın değil ama yapısal hata | **DOĞRULANDI** |
| B | `energy_conservation = max|ρ(t)-ρ(0)|` | FRW'de geçersiz; doğru kalıntı `ρ̇+3H(ρ+p)` | **DOĞRULANDI** |
| C | `max(rho,0)` sessiz maskeleme | `hubble_rate()` `np.sqrt(max(rho_tot,0)/…)` | **DOĞRULANDI** |
| D | `mu_sq` sabit referans | bkz. #10 | **DOĞRULANDI** |
| E | `ψ̇` sıfır geçişiyle pencere | 4 testte 70-71 geçiş; ama `n=200` taramada 3-16 → örnekleme bağımlı | **DOĞRULANDI** |
| F | Sınıflandırma: `Q>5 ve |w-1/3|<0.05 ve |virial-1|<0.2` | Test 3/4'te `Q=11.6`, `|virial-1|~10³` → `transitional`; eşik keyfî | **DOĞRULANDI** |
| G | `V0=1e56` (kod) vs `1e64` (makale) | `3H/2μ` = 0.0025 (kod) vs 25.1 (makale). §3.6'daki "overdamped" bulgusu makale benchmark'ına ait, **kodun çalıştırdığı profile değil** | **KRİTİK** |
| H | Solver/tolerans/sürüm/seed kaydı | `DOP853`, `rtol=1e-9`; JSON'a sürüm/commit/seed yazılmıyor | **DOĞRULANDI** |

**Ek bulgular (bu denetimde):**

- **(Yeni) `Phi_dot(t_c) = 0` — donmuş yakıt alanı.** `λ=0.02 GeV⁻²` yorumuyla
  `λΦ_c² ≈ 5.9×10³⁶` → `exp(-λΦ²) = 0` (çift duyarlık altı) → `V = V₀`, `V' = 0` →
  `ε_V = 0` → **`Φ̇(t_c) = 0`**. Yani tarama, yakıt alanı hiç hareket etmeyen bir
  arka planda yapılmış. Doğru birim (`λ ≈ 0.02/M_Pl²`) ile `Φ̇ ≈ -0.212 H M_Pl`.
- **(Yeni) `w_psi` işareti/aralığı fiziksel değil.** Kodun `pressure_psi`'si
  kaydırılmamış `V_act` kullanıyor → örneklerin **%99.99'unda `w < -1`**
  (medyan `-2.49`, min `-334`). Kaydırılmış potansiyel (Eq. 39 standardı) ile
  `w ∈ [-1, 1]`, medyan `-0.285`. Sınıflandırma bu bozuk `w` üzerinden yapılıyor.
- **(Yeni) Metrik/dosya içi çelişki.** `TASK1_FINAL_FINDINGS.md`, `V₀=10⁵⁶`'da
  iki minimum arasında salınım, "periods 0-5 geçici kuartik", `w→-1` gibi ayrıntılı
  bir tablo veriyor. Bu tablo **kod ile üretilemiyor** (kod altı testte
  `quartic_achieved=False`, `n_oscillations=70`, `w=-1.72`). Yani rapor, kodu
  tarafından desteklenmeyen sayılar içeriyor.
- **(Yeni) Tarama `t_max=20/μ` ile `n=200`.** `w_avg` birkaç örnekle hesaplanıyor;
  200 noktalı bir ızgarada 200/μ'yu çözmek için örnek/period ~ 60 gerekirken
  çoğu noktada eksik. Zaman ızgarası yakınsaması yapılmamış.

---

## 5. Çelişki matrisi

### 5.1 Ana metin içi çelişkiler

| ID | Konum A | Konum B | Çelişki | Sınıf |
|---|---|---|---|---|
| B-04 | 316-320 (konvansiyon) | 375, 443, 469, 475, 2541-2544 (kinetik) | `+½` kinetik + `(-+++)` → yazılı EOM/ρ ile uyuşmaz | HATALI |
| B-05 | Eq.(3) toplam L | 1668-1690 (`L_rh`) | `L_rh` toplam Lagranjiyen'de tanımlı değil, ama Q türetiminde kullanılıyor | HATALI |
| B-06 | Eq.(7) `L_act` | Eq.(13)/(21) ve Eq.(74) | `Φ²ψ²` teriminin işareti üç yerde üç farklı | HATALI |
| B-07 | 318 (`T=-2/√-g δS/δg^{μν}`) | 1678 (`T=+2/√-g δS/δg_{μν}`) | İki tanım; ayrıca Eq.(70) parantezi `T₀₀=-ρ` veriyor | HATALI |
| B-08 | Eq.(76)-(80) | §B.2 tablosu (satır 3846) | `Q_i^ν` GeV⁴ yazılmış, tablo GeV⁵ diyor | HATALI |
| B-09 | "GÖSTERİLDİ" (9 yer) | "conditional/not independently reproduced" (7 yer) | Aynı iddia iki statüde | YÜKSEK |
| B-10 | Eq.(99) `q = gA²/ω²` | Mathieu standart formu | Faktör 2 | HATALI |
| B-11 | Eq.(99) `A_k` | `m_eff² = m_χ²+2gΦ_res²` | Sabit `gA²` terimi eksik | HATALI |
| B-12 | `μ_max ≈ qω_res/2` | Monodromi (bu denetim) | Geniş q'da `≈0.45ω_res`; `q` bağımlılığı `√q` | HATALI |
| B-13 | Eq.(102)-(103) `exp(2μN/ω_res)` | boyut analizi | `N/ω_res` **zaman**; `μ` frekans → argüman boyutsuz olmalı; `2μ_max N ω_res^{-1}` ile `n_k` arasında tutarsızlık | HATALI |
| B-14 | Eq.(104) `Ω_χh²=0.12` | 3156-3175 "target benchmark" | Denklem çıktı gibi, metin kalibrasyon diyor | KOŞULLU |
| B-15 | `λ=0.02` + `[λ]=GeV⁻²` | `Φ_end ~ M_Pl/√λ`, `λΦ²~O(1)` | Birim yorumu tutarsız; kod bu yorumla donmuş alan üretiyor | HATALI |
| B-16 | 1900 `c_s²=ṗ/ρ̇=1/3` | 1917-1930 `c_a²` ayrımı | Aynı sembol iki anlamda | YÜKSEK |
| B-17 | 1877 "F_ℓ var" | 1890 "F_ℓ ≥ 2 katkı vermez" | İki ifade uzlaştırılmamış | YÜKSEK |
| B-18 | 3175-3194 `Φ_res` çift rol | — | `ω~10¹³ GeV` → `m~H₀` köprüsü türetilmemiş | VARSAYIM |
| B-19 | 3696 "ΣΩ=1 <10⁻¹²" | 3685 "author-reported" | Sayısal kanıt yok | EKSİK |
| B-20 | 6 belge `ErdemEsa/ptum-cosmology` | `git remote` `arreasonn-jpg/…` | Adres çelişkisi; eski adres 404 | HATALI |
| B-21 | 3363 lattice "potential" | 443 activation | Lattice potansiyelinde `m_ψ²ψ²/2` var, `m_eff²` yok | HATALI |
| B-22 | 3352-3360 lattice "performed" | 3371 "archive does not include" | Aynı sayfada iki statü | YÜKSEK |
| B-23 | `main.tex` iki `\appendix` | `main.aux` B ve D etiketleri | Şekil numaraları 2-18 (1 yok) → LaTeX yapısal artığı | DÜŞÜK |
| B-24 | Şekil `PTUM_F4` | `main.aux` `fig:ptum_cmb_phase_shift_diagnostic` = Şekil 10 | `fig_fluid_vs_freestream` de aynı işi yapıyor (Şekil 15) | DÜŞÜK |

### 5.2 Kod ↔ metin çelişkileri

| ID | Kod | Metin | Çelişki |
|---|---|---|---|
| C-01 | `V0=1e56` (tüm testler) | benchmark `V0~1e64` | §3.6'daki "overdamped, `3H/2μ≈25`" **kodun çalıştırdığı profilde doğru değil** (`0.0025`) |
| C-02 | `Phi_dot=0` (donmuş) | "slow-roll Φ̇" | Başlangıç koşulu fiziksel değil |
| C-03 | `w_psi` sık sık `<-1` | `w_ψ = (½ψ̇²-U)/(½ψ̇²+U)` Eq.(39) | Kod kaydırılmamış potansiyel kullanıyor |
| C-04 | `rho_phi`, `rho_psi` çift sayım | `T₀₀` tek sayım | Yapısal |
| C-05 | `energy_conservation` metriği | "enerji korunumu" | FRW'de yanlış test |
| C-06 | Sınıflandırma eşikleri | "Q>5" evrensel değil | Gerekçesiz |
| C-07 | `compute_quartic_dominance` `Q=λψ⁴/(μ²ψ²)` | Eq.(37) | Boyut: `λψ⁴` GeV⁴, `μ²ψ²` GeV⁴ ✓ ama **tanım** `|ψ|≫ψ₀` koşulunun yeniden yazımı; bağımsız değil |
| C-08 | `TASK1_FINAL_FINDINGS.md` tabloları | kodun kendisi | Kod bu tabloları üretemiyor |

### 5.3 Belge ↔ gerçeklik çelişkileri

| ID | Belge | İddia | Gerçek |
|---|---|---|---|
| D-01 | `PTUM_FINAL_AUDIT.md/.json` | "PASS", "CLASS patch public", "apply check PASS" | Patch **yok**; hedef CLASS commit/tag yok |
| D-02 | `PTUM_REPRODUCIBILITY_NOTES.md` | "CLASS v3.2.0 PTUM patch: public" | Depoda ve zip'te **0** `.patch` |
| D-03 | `PTUM_LIBRARY_MANIFEST.md` | paket içeriğinde `compile logs` | Repoda `compile1.log/2.log` **yok** (zip'te var) |
| D-04 | 6 belge | `ErdemEsa/ptum-cosmology` | HTTP **404** |
| D-05 | `main.tex` 3909 | "upon acceptance … will be made available" | Zaten "public" deniyor; çelişki |
| D-06 | `main.tex` 3685-3712 | CLASS testleri "author-reported" | Kod yok → **NOT RUN** |
| D-07 | `main.tex` 4199-4226 | Lattice `μ=0.198±0.005` | Ham veri/config/seed yok → **BLOCKED** |
| D-08 | `FINAL_SUMMARY.md` | "11/11 tasks complete" | 11 maddenin en az 4'ü (CLASS, MCMC, lattice, profile likelihood) kanıtsız |
| D-09 | `PTUM_THEORETICAL_INVENTORY_REPORT.md` | 26 madde "PROVEN" | En az 5'i (∑Q=0, CLASS doğrulaması, EFT hiyerarşisi, ses hızı uzlaşması, lattice) bu denetimde **FAIL/BLOCKED** |

---

## 6. İddia sınıflandırma tablosu (istenen 8 sınıf)

Makalenin ana iddiaları; her biri için **gerekçe** ve **test durumu**.

| # | İddia | Sınıf | Gerekçe / test |
|---|---|---|---|
| 1 | `m_eff²<0 ⇔ |Φ|>Φ_c` | TÜRETİLDİ | Tanımdan cebir |
| 2 | `χ` ve `Φ_res` EOM'leri (Eq. 15-16) | TÜRETİLDİ + ANALİTİK DOĞRULANDI | Eq.(10)-(11)'den EL; işaretler tutarlı |
| 3 | `Q_DM^ν = -2gχ²Φ_res∂^νΦ_res` | TÜRETİLDİ | Eq.(72) ✓, boyut GeV⁵ ✓ |
| 4 | `Q_ψ^ν` (Eq. 76) | HATALI | boyut GeV⁴; işaret Eq.(7) ile çelişik |
| 5 | `Σ_i Q_i^ν = 0` | **HATALI / kanıtsız** | Terimler yanlış boyutta; "elle zıt işaret" — talimat §8'e aykırı |
| 6 | `L_PTUM` kinetik işaretleri | HATALI | `(-+++)` ile `+½` uyuşmaz |
| 7 | Mathieu indirgemesi (Eq. 99) | HATALI | faktör 2 + eksik `A_k` terimi + zaman değişkeni |
| 8 | `μ_max ≈ qω_res/2` | HATALI | monodromi: `≈0.45ω_res`, `√q` ölçekli |
| 9 | `w_ψ=1/3` kuartik faz | KOŞULLU / FENOMENOLOJİK | Benchmark'ta ulaşılmıyor; metin de kabul ediyor — **dürüst uyarı korunmalı** |
| 10 | `σ_ψ = 0` | FENOMENOLOJİK | Perfect-fluid kapanışı; homojen alan için totolojik tanım |
| 11 | `c_s² = 1/3` | KOŞULLU | `c_a²` ile karışmış; rest-frame türetilmemiş |
| 12 | `Ω_χh² = 0.12` | FENOMENOLOJİK / kalibrasyon | Eq.(104) hedef; çıktı değil |
| 13 | `ΔN_fluid < 0.31` (Planck+BAO+Pantheon+) | EKSİK | Zincir/YAML yok → **NOT RUN** |
| 14 | `Δχ²=+0.26`, `ΔAIC=2.26` | EKSİK | Aynı |
| 15 | `ln Z = -1198.61±0.12` | EKSİK | PolyChord çıktısı yok |
| 16 | CLASS `ΛCDM` recovery, gauge invariance, CAMB <%0.1 | EKSİK | Kod yok |
| 17 | Lattice `μ=0.198±0.005`, `Ω_χh²=0.118±0.015` | EKSİK / BLOCKED | Ham veri yok |
| 18 | `n_s~0.957-0.961`, `r≪0.036` | KOŞULLU | "public script" atfı var, script **yok** |
| 19 | `β_iso ~ 10⁻¹²-10⁻⁶` | VARSAYIM | `ε²` ölçeklemesi türetilmemiş |
| 20 | `Φ_res` erken/geç köprüsü | VARSAYIM | B-18 |
| 21 | `S_obs ~ 10⁸⁸` | HATALI/EKSİK | Döngüsel; bağımsız hesap yok |
| 22 | "no ghosts" | TÜRETİLDİ (koşullu) | Kanonik kinetik işaret **düzeltilirse** geçerli; şu haliyle B-04'e bağlı |
| 23 | `S_8`, `H_0` kayması | EKSİK | Zincir yok |
| 24 | `T_rh ~ 10¹⁴-10¹⁵ GeV` | KOŞULLU | Kendi metni "koşullu tahmin" diyor ✓ |
| 25 | BBN uyumu | KOŞULLU | `ΔN_fluid` bağımsız değil |

---

## 7. Yeniden üretilebilirlik envanteri (dosya düzeyinde)

| Bileşen | Beyan edilen | Dosya düzeyinde bulunan | Durum |
|---|---|---|---|
| Makale kaynağı | `main.tex` | ✓ 208 KB, 147 denklem | **PASS** |
| Figürler | 18 PDF | ✓ 18/18, eksik yok | **PASS** (üretim scripti yok) |
| Şekil üretim scripti | `scripts/reproduce_figures.py` | ✗ | **BLOCKED** |
| Task-1 simülasyonu | `ptum_task1_simulation.py` | ✓ çalışıyor, JSON'u üretiyor | **PARTIAL** (bkz. §4) |
| Testler | — | ✗ 0 dosya | **BLOCKED** |
| CLASS v3.2.0 patch | "public, apply-check PASS" | ✗ | **FAIL** |
| CLASS hedef commit/tag | — | ✗ | **FAIL** |
| CLASS build log | — | ✗ | **FAIL** |
| Cobaya YAML | "pending" | ✗ (tutarlı) | **BLOCKED** |
| MCMC zincirleri | "pending/external" | ✗, DOI/checksum yok | **BLOCKED** |
| PolyChord zincirleri | "pending" | ✗ | **BLOCKED** |
| CAMB patch | "planned" | ✗ | **BLOCKED** |
| Lattice kodu | "LATTICEEASY modified" | ✗ | **BLOCKED** |
| Lattice config/seed/snapshot | — | ✗ | **BLOCKED** |
| Dockerfile | "planned" | ✗ | **BLOCKED** |
| `requirements.txt` / sürüm pinleri | — | ✗ | **FAIL** |
| `.gitignore` | — | ✗ | **FAIL** |
| Lisans | — | ✗ | **FAIL** |
| `PTUM.zip` manifest doğruluğu | "tam paket" | Kod/patch/veri yok | **FAIL** |
| Depo adresi tutarlılığı | 2 farklı URL | biri 404 | **FAIL** |

---

## 8. Bu denetimde çalıştırılan testler (komut + sonuç)

Tümü `/tmp/audit/` altında, **depoya yazılmadan**. Ortam: Python 3, numpy 2.4.6, scipy 1.17.1.

| # | Test | Komut/script | Sonuç |
|---|---|---|---|
| T1 | Kinetik işaret: EL + `T₀₀` | `full_check.py`, `sign_table.py` | `+½` → EL `-1.33`, `T₀₀=2.155`; `−½` → EL `0`, `T₀₀=3.845` → **B-04 DOĞRULANDI** |
| T2 | `Q^ν` boyut analizi | `dims.py` | 7/7 terim GeV⁴ ≠ GeV⁵ → **B-08 DOĞRULANDI** |
| T3 | Mathieu dar bant | `mathieu2.py` | `q=0.02`: `ν=0.010000=q/2` → makale dar bantta **doğru** |
| T4 | Mathieu geniş bant | `mathieu3.py` | `q=1024`: `ν=44.008`, `√(2q)=45.25` → **B-12 DOĞRULANDI** |
| T5 | Kod çalıştırma | `ptum_task1_simulation.py` | Çalışıyor; 4 testte `quartic_achieved=False` |
| T6 | JSON yeniden üretimi | `scan_compare.py` | 18/18 nokta birebir aynı → **PASS** |
| T7 | Çift sayım etkisi | `diag.py` | `H`'de `2×10⁻⁷` → yapısal ama sayısal olarak ikincil |
| T8 | FRW süreklilik kalıntısı | `consistency2.py` | `|ρ̇+3H(ρ+p)|/(3Hρ)` → `1e-10…1e-11` (yakınsıyor) |
| T9 | Kodun enerji metriği | `diag.py` | `4.04×10⁻⁷` — doğru test **değil** |
| T10 | `w_ψ` aralığı | `consistency2.py` | Kod: `[-334.6, -1.0]`, %99.99 `<-1`; kaydırılmış: `[-1, 1]` |
| T11 | `Φ̇(t_c)` | `lambda_check.py` | `0.000e+00` (donmuş) → **C-02** |
| T12 | `λ` birim kontrolü | `lambda_check.py` | `exp(-λΦ_c²) ≈ e^{-5.9×10³⁶}` → alt akış |
| T13 | FIG/ref tutarlılığı | `grep`/`ls` | 18/18 mevcut, 2 kullanılmıyor, eksik 0 |
| T14 | LaTeX log | `grep main.log` | Tanımsız referans **yok**; yalnız `h` float uyarısı; log 'Output written on main.pdf (43 pages)'; depodaki log bir önceki derlemeye ait olabilir (rerun=5) |
| T15 | Zip içerik | `zipfile` | 39 girdi, kod/patch/veri **0** |
| T16 | Depo adresi | GitHub API | `ErdemEsa/ptum-cosmology` → **404**; `arreasonn-jpg/…` → 200 |
| T17 | Zip ↔ depo `main.tex` | SHA256 | **Farklı** (`64e8d3d6…` vs `ba1a6309…`) |
| T18 | LaTeX derleme | — | **NOT RUN** (sandbox'ta TeX yok) |
| T19 | CLASS patch apply/build | — | **BLOCKED** (dosya yok) |
| T20 | MCMC / PolyChord | — | **BLOCKED** (zincir yok) |
| T21 | Lattice | — | **BLOCKED** (kod/veri yok) |

---

## 9. SPRINT 0 kabul kriterleri

| Kriter | Durum |
|---|---|
| Tüm dosya/bağımlılık envanteri çıkarıldı | **PASS** |
| Tüm Lagrangian / EOM / `T_μν` / `Q_i^ν` / Mathieu denklemleri denklem numarası + satırla listelendi | **PASS** (147 denklem, 25 hedef denklem eşlendi) |
| Bölüm/denklem referansları `main.aux` ile doğrulandı | **PASS** |
| Çelişki matrisi üretildi | **PASS** (33 çelişki: 24 metin içi + 8 kod + 9 belge) |
| Hiçbir kaynak dosya değiştirilmedi | **PASS** |
| Veri uydurulmadı | **PASS** |

**SPRINT 0 sonucu: PASS** (envanter tamamlandı).

---

## 10. Sonraki sprintler için öncelik sırası (öneri)

Öncelik, "yeni iddia eklemek" değil, **eylemden başlayan zinciri kapatmak**.

1. **SPRINT 1 (eylem/konvansiyon) — en kritik.** Tek bir konvansiyon seç:
   `(-+++)`, `L = -½(∂φ)² - V`, `T_μν = -2/√-g δS/δg^{μν}`.
   Tüm EOM'leri tam eylemden türet (SymPy); `T₀₀=½φ̇²+V`, `p=½φ̇²-V` testlerini yaz.
   **B-04, B-07 ve B-21 birlikte çözülmeli**, çünkü dördü aynı kök hatadan geliyor.
2. **B-15 (λ birimi)** — SPRINT 1'de netleşmeli; aksi halde tüm sayısal sonuçlar
   yanlış potansiyel şekli üzerinde.
3. **SPRINT 2 (`Q_i^ν`)** — B-06/B-08 aynı anda. Boyut testi `GeV⁵` zorunlu;
   `ΣQ=0` **türetimden** gelmeli, elle değil.
4. **SPRINT 3 (rezonans)** — B-10…B-13. Monodromi çözücüsü + dar/geniş bant
   karşılaştırması; `Ω_χh²` çıktı yapılmalı (kalibrasyon ise etiketlenmeli).
5. **SPRINT 4 (iddia sınırı)** — B-09, B-14, B-16…B-18, B-22. Özellikle
   **`TASK1_FINAL_FINDINGS.md` tabloları kodla uzlaştırılmalı veya geri çekilmeli.**
6. **SPRINT 5 (sayısal)** — C-01…C-08. Çift sayım, FRW kalıntısı, dinamik `m_eff`,
   gerçek periyot tespiti, `V₀=1e64` benchmark'ı, tolerans/çözünürlük yakınsaması.
7. **SPRINT 6 (regresyon)** — D-01…D-09: ya gerçek dosyalar eklenmeli ya da
   "PASS" iddiaları **geri çekilmeli**. CLASS/lattice için DOI + SHA256 şart.

**Onay bekleyen tek soru:** SPRINT 1'e geçmeden önce (a) `(-+++)` + `−½(∂φ)²`
konvansiyonunu mu, yoksa (b) `(+---)` + `+½(∂φ)²` konvansiyonunu mu sabitleyelim?
Her ikisi de tutarlıdır; (a) mevcut metnin çoğuna daha az dokunuşla uyar, (b) ise
yazılı `+½(∂φ)²` kinetik terimlerini korur ama tüm `T₀₀`/`p` işaretlerini değiştirir.
**Önerim: (a)** — çünkü `ρ=½φ̇²+V`, `p=½φ̇²-V` ve `Q_i^ν` yapısı zaten (a) varsayılarak yazılmış.

---

## 11. Değişen dosyalar ve commit

```
Yeni:  AUDIT_00_INVENTORY.md     (bu rapor)
Değişen: yok
Silinen: yok
Kaynak main.tex: DOKUNULMADI
```

Commit: bu rapor tek başına, `SPRINT 0` kapsamında commit edilecek.
`main.tex`, `ptum_task1_simulation.py` ve tüm diğer dosyalar önceki hâlinde bırakıldı.

---

### Ek: sınıflandırma sözlüğü (sonraki sprintlerde kullanılacak)

| Etiket | Anlam |
|---|---|
| **TÜRETİLDİ** | Tam eylemden varyasyonla elde edildi; adımlar yazılı |
| **ANALİTİK DOĞRULANDI** | Bağımsız sembolik/cebirsel kontrol geçti |
| **SAYISAL DOĞRULANDI** | Bağımsız sayısal çözücü ile yeniden üretildi (script + tolerans + sürüm yazılı) |
| **KOŞULLU** | Belirtilen koşullar sağlanırsa geçerli; koşul test edilmedi |
| **FENOMENOLOJİK** | Efektif kapanış/ansatz; mikroskobik türetim değil |
| **VARSAYIM** | Gerekçelendirilmiş ama türetilmemiş varsayım |
| **EKSİK** | Gerekli dosya/veri/hesap yok |
| **HATALI** | Bağımsız kontrol başarısız; düzeltme gerekli |
