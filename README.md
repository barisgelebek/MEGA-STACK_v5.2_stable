MEGA-STACK v5.2 - Ultimate Infrastructure Solutions


<p align="center">
  <img src="https://img.shields.io/badge/Version-5.3-blue?style=for-the-badge&logo=docker" alt="Version">
  <img src="https://img.shields.io/badge/Docker-29.3.0-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Async-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-Commercial-orange?style=for-the-badge" alt="License">
</p>

<h1 align="center">🏗️ MEGA-STACK Server</h1>

<p align="center">
  <strong>Kurumsal Düzey Sunucu Yönetim & Dijital Altyapı Platformu</strong>
</p>

<p align="center">
  Tek sunucudan web hosting, e-posta, veritabanı, güvenlik, AI destekli operasyon,<br>
  yedekleme, kripto/kart ödeme ve lisanslama — hepsi tek dashboard'dan.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Containers-18-informational?style=flat-square" alt="">
  <img src="https://img.shields.io/badge/API_Endpoints-330+-success?style=flat-square" alt="">
  <img src="https://img.shields.io/badge/Dashboard_Pages-34-blueviolet?style=flat-square" alt="">
  <img src="https://img.shields.io/badge/DB_Tables-57-yellow?style=flat-square" alt="">
  <img src="https://img.shields.io/badge/Components-89-red?style=flat-square" alt="">
</p>

---

## 📖 İçindekiler

- [Özellikler](#-özellikler)
- [Mimari Genel Bakış](#-mimari-genel-bakış)
- [Teknoloji Stack](#-teknoloji-stack)
- [Dashboard Sayfaları](#-dashboard-sayfaları)
- [Güvenlik](#-güvenlik)
- [AI & Akıllı Sistemler](#-ai--akıllı-sistemler)
- [Ödeme Sistemi](#-ödeme-sistemi)
- [Yedekleme & Felaket Kurtarma](#-yedekleme--felaket-kurtarma)
- [Mail Altyapısı](#-mail-altyapısı)
- [Lisanslama & Tier Sistemi](#-lisanslama--tier-sistemi)
- [Telegram Bot](#-telegram-bot)
- [Performans](#-performans)
- [Sistem Gereksinimleri](#-sistem-gereksinimleri)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Versiyon Geçmişi](#-versiyon-geçmişi)

---

## ✨ Özellikler

### 🎯 Neden MEGA-STACK?

<table>
<tr>
<td width="50%">

**🖥️ Tek Platform, Tam Kontrol**
- 18 Docker konteyner orkestrasyonu
- 34 yönetim sayfası
- 330+ API endpoint
- Merkezi dashboard

</td>
<td width="50%">

**🛡️ Askeri Düzey Güvenlik**
- 6 katmanlı güvenlik modeli
- Ghost Vault (dosyasız şifreleme)
- Fernet + RSA-4096 + AES-256
- Panic Button (tek tuşla şifre değişikliği)

</td>
</tr>
<tr>
<td>

**🤖 AI Destekli Operasyon**
- 3 katmanlı LLM motoru (Gemini → Groq → Kural)
- Otomatik log analizi & anomali algılama
- KVKK/GDPR uyumlu veri maskeleme
- Proaktif sistem izleme

</td>
<td>

**💳 Kripto + Kart Ödeme**
- 4 gateway SmartRouter (otomatik failover)
- BTC, ETH, USDT, USDC desteği
- PCI-DSS uyumlu kredi kartı
- Web3 Wallet Connect

</td>
</tr>
<tr>
<td>

**💾 Zero-Touch Yedekleme**
- 5-Part system imaging
- AES-256-CBC şifrelemeli cloud backup
- 1-click restore (Time Machine)
- Cloudflare R2 entegrasyonu

</td>
<td>

**📧 Kurumsal Mail**
- 53 mail API endpoint
- Multi-domain yönetimi
- Spam/karantina/DNS sağlık
- BCC arşivleme

</td>
</tr>
</table>

### 📊 Sayılarla Platform

| Metrik | Değer |
|:-------|------:|
| Docker Konteyner | 18 |
| API Endpoint | 330+ |
| Dashboard Sayfası | 34 |
| SQLite Tablo | 57 |
| Kayıtlı Bileşen | 89 |
| Doküman Sayfası | 68 |
| Telegram Komutu | 24 |
| SSL Sertifika | 11 domain |
| Mail Endpoint | 53 |
| Versiyon Geçmişi | 21 release |

---

## 🏗 Mimari Genel Bakış

```
                        ┌──────────────────────┐
                        │     🌐 İnternet       │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  Traefik v2.11       │  ← TLS/SSL + ACME
                        │  (Reverse Proxy)     │  ← Rate Limiting
                        └──────────┬───────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                   │
       ┌────────▼────────┐ ┌──────▼──────┐  ┌────────▼────────┐
       │   CrowdSec      │ │  Authelia   │  │  Nginx 1.29     │
       │   (IPS)         │ │  (SSO/2FA)  │  │  (Dashboard UI) │
       └─────────────────┘ └─────────────┘  └────────┬────────┘
                                                      │
                                            ┌─────────▼─────────┐
                                            │  Core API v12     │
                                            │  FastAPI + Uvicorn│
                                            │  330+ Endpoint    │
                                            └─────────┬─────────┘
                                                      │
                            ┌─────────────────────────┼────────────────┐
                            │                         │                │
                   ┌────────▼────────┐     ┌──────────▼──────┐ ┌──────▼──────┐
                   │  SQLite WAL     │     │  MSSQL 2022     │ │  MariaDB    │
                   │  57 tablo       │     │  İş Verileri    │ │  4 DB (Mail)│
                   └─────────────────┘     └─────────────────┘ └─────────────┘
```

### Konteyner Altyapısı

| # | Servis | Image | Rol | RAM |
|:-:|--------|-------|-----|:---:|
| 1 | **Traefik** | `traefik:v2.11` | Reverse Proxy + TLS | 256M |
| 2 | **Authelia** | `authelia:4.39.15` | SSO / 2FA (TOTP + WebAuthn) | 256M |
| 3 | **CrowdSec** | `crowdsec:v1.6.8` | Intrusion Prevention | 256M |
| 4 | **CrowdSec Bouncer** | `traefik-crowdsec-bouncer:0.5.0` | Traffic filtering | 64M |
| 5 | **Cert Dumper** | `traefik-certs-dumper:v2.8.1` | TLS cert extraction | 64M |
| 6 | **MSSQL Server** | `mssql/server:2022-latest` | İş veritabanı | 2G |
| 7 | **iRedMail** | `iredmail/mariadb:stable` | Mail + MariaDB | 2G |
| 8 | **Nginx** | `nginx:1.29-alpine` | Dashboard + statik siteler | 128M |
| 9 | **NetCore App** | `yourserver/netcoreapp:latest` | ASP.NET Core App | 512M |
| 10 | **Core API** | `mega-stack/core-api:v12` | FastAPI backend | 512M |
| 11 | **Redis** | `redis:7-alpine` | Session store + cache | 128M |
| 12 | **Netdata** | `netdata:v2.9.0` | Sistem izleme | 512M |
| 13 | **Uptime Kuma** | `uptime-kuma:1` | Uptime monitoring | 512M |
| 14 | **Dozzle** | `dozzle:latest` | Container log viewer | 128M |
| 15 | **Portainer** | `portainer-ce:2.39.0` | Docker GUI | 256M |
| 16 | **CloudBeaver** | `cloudbeaver:latest` | DB web client | 1G |
| 17 | **Watchtower** | `watchtower:1.7.1` | Auto-update notify | 64M |

---

## 🔧 Teknoloji Stack

### Backend

| Katman | Teknoloji | Versiyon |
|--------|-----------|:--------:|
| Runtime | Python | 3.12 |
| Framework | FastAPI + Uvicorn | Latest |
| Veritabanı | SQLite WAL | - |
| Veritabanı | MSSQL Server | 2022 CU23 |
| Veritabanı | MariaDB | 10.x |
| Cache | Redis | 7-alpine |
| Şifreleme | Fernet (cryptography) | AES-128-CBC |
| Lisans | RSA-4096 PSS | - |
| Proxy | Traefik | v2.11 |
| Auth | Authelia | 4.39.15 |
| IPS | CrowdSec | v1.6.8 |
| Backup | Rclone | v1.73.2 |
| Container | Docker + Compose | 29.3.0 / v5.1 |

### Frontend

| Teknoloji | Versiyon | Kullanım |
|-----------|:--------:|----------|
| Bootstrap | 5.3.3 | CSS framework |
| Chart.js | 4.x | Grafik ve gauge |
| Monaco Editor | 0.45.0 | Kod editörü |
| xterm.js | Latest | Terminal emülatörü |
| Leaflet.js | 1.9.4 | İnteraktif harita |
| Ace Editor | Latest | SQL editörü |
| Marked.js | Latest | Markdown render |
| Prism.js | 1.29.0 | Syntax highlighting |
| SweetAlert2 | Latest | Dialog sistemi |
| Google Fonts | Inter + Fira Code | Tipografi |
| Vanilla JS | ES6+ | IIFE pattern (framework-free) |

### AI & Machine Learning

| Motor | Model | Rol |
|-------|-------|-----|
| L1 Primary | Google Gemini 2.0 Flash | Ana LLM |
| L2 Fallback | Groq Llama 3.3-70b-versatile | Yedek LLM |
| L3 Offline | Kural Tabanlı Motor | 8 hata kategorisi |
| Masking | Shannon Entropy Engine | Veri anonimleştirme |
| Neural | Custom Observer Engine | Anomali algılama |

---

## 📱 Dashboard Sayfaları

<details>
<summary><strong>🔹 Yönetim (6 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Ana Dashboard** | Hero Stats, CPU/RAM Gauge, GeoMap, Chat Widget, System Tree |
| **Admin Overview** | Launchpad Grid, Container Metrics, Chart.js grafikleri |
| **Domain Yönetimi** | Domain CRUD, istatistik kartları |
| **User Manager** | RBAC, 2FA kurulum, canlı oturum yönetimi, denetim logu |
| **Nav Menu** | Dinamik menü düzenleme |
| **UISetting** | 40+ CSS token, canlı tema önizleme, white-label |

</details>

<details>
<summary><strong>🔹 Güvenlik (5 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Guardian** | Credential dashboard, Atomic Update, Panic Button |
| **Defense Hub** | CrowdSec, GeoIP harita, SSH log analizi |
| **PassHub** | Fernet şifreli parola yönetimi |
| **Cert-Watch** | SSL sertifika izleme + expiry uyarı |
| **Login** | Matrix Rain UI, 2FA, RBAC, device trust |

</details>

<details>
<summary><strong>🔹 Veri & Veritabanı (3 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Data Studio** | Multi-engine SQL, görselleştirme, XLSX/PDF export |
| **SQL Runner** | MSSQL + MariaDB, snippet, object explorer |
| **Migration** | Drag&Drop .bak/.bacpac/.dacpac import |

</details>

<details>
<summary><strong>🔹 AI Sistemleri (2 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **AI Studio** | Ghost Mode, Engine Selector, Maskeleme CRUD, Neural Timeline |
| **STACK-AI** | 3 katmanlı chat, container context, preset scenarios |

</details>

<details>
<summary><strong>🔹 İzleme & Log (4 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Health Check** | Skor (0-100), container pulse, SSL watch |
| **Log Center** | Live tail, audit trail, panic mode, purge |
| **Analytics** | KPI kartları, trend grafikleri, tier dağılımı |
| **Motor Dairesi** | xterm.js terminal, Docker ops, Self-Kill koruması |

</details>

<details>
<summary><strong>🔹 İletişim (1 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Mail Center** | 5 tab, 12 modal, 53 endpoint, DNS sağlık, karantina |

</details>

<details>
<summary><strong>🔹 Yedekleme & Kurtarma (2 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Backup Center** | 5-Part imaging, schedule, cloud sync, progress |
| **Restore Manager** | Time Machine, diff analysis, dry-run simulation |

</details>

<details>
<summary><strong>🔹 Ticaret & Ödeme (4 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **License Hub** | RSA-4096, HWID binding, tier matrix |
| **Payment** | Kripto + kart, SmartRouter, finansal komuta |
| **Product UI** | Servis görünürlük yönetimi |
| **Release Manager** | Release CRUD, signal dağıtımı, changelog |

</details>

<details>
<summary><strong>🔹 Dosya & Bilgi (6 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **File Manager** | Monaco Editor, dual-pane, zip, multi-select |
| **Mega-Editor** | IDE, Python lint, snapshot/rollback |
| **Stack Memory** | Split-view markdown, template, snapshot |
| **Documentations** | Tree-view, markdown render, PDF export |
| **Components** | 89 bileşen kataloğu, kategori filtre |
| **Versions** | 21 versiyon timeline, changelog, component tracker |

</details>

<details>
<summary><strong>🔹 Destek (1 sayfa)</strong></summary>

| Sayfa | Açıklama |
|-------|----------|
| **Tickets** | SLA timer, deflection wizard, chat replies |

</details>

---

## 🛡 Güvenlik

### 6 Katmanlı Güvenlik Modeli

```
Layer 1  ──  Ağ        │  Traefik TLS, CrowdSec IPS, Rate Limit, UFW
Layer 2  ──  Kimlik    │  Authelia 2FA (TOTP+WebAuthn), Redis Session, HttpOnly Cookie
Layer 3  ──  Yetki     │  Auth Middleware Guard, RBAC, Tier Gating
Layer 4  ──  Veri      │  Fernet, RSA-4096, AES-256-CBC, Ghost Vault
Layer 5  ──  Uygulama  │  SQL Blacklist, Path Traversal, XSS Guard, Self-Kill
Layer 6  ──  AI        │  Kervan Kalkanı (5-layer masking), Shannon Entropy
```

### Ghost Vault — "Sunucu Çalınsa Bile Şifreler Güvende"

- Tüm credential'lar **SQLite + RAM cache**'te (Fernet şifreli)
- Disk dosyaları `{{FROM_DB_OR_VAULT}}` placeholder içerir
- Docker container'lara **Ghost Inject** ile diske yazmadan enjeksiyon
- `vault.enc` — felaket kurtarma deposu (AES şifreli)

### Panic Button — 7 Fazlı Acil Durum

```
1. 🔄 Sistem Yedeği
2. 🎲 Tüm Şifre Üretimi
3. 🗄️ MSSQL ALTER LOGIN SA
4. 💾 DB Toplu Güncelleme (Fernet)
5. 🔐 Vault & Ghost Mühürleme
6. 📱 Telegram Bildirim
7. ✅ Tamamlandı
```

---

## 🤖 AI & Akıllı Sistemler

### STACK-AI — LLM Orchestrator

```
Kullanıcı Sorgusu
       │
       ▼
  Kervan Kalkanı ── 5 katmanlı veri maskeleme
       │
       ▼
  L1: Gemini 2.0 Flash ──(hata?)──► L2: Groq Llama 3.3-70b ──(hata?)──► L3: Kural Motoru
       │
       ▼
  NeuralCore ── Sistem bağlamı + anomali algılama
```

- **Blueprint Enjeksiyonu:** SYSTEM_BLUEPRINT.md tüm LLM'lere beslenir
- **8 Preset Senaryo:** Nginx 502, SSL, DB, Mail, OOM, CrowdSec, Docker
- **Ghost Mode:** AI'yı tamamen devre dışı bırakabilme
- **Maskeleme:** IP, e-posta, API key, JWT, şifre otomatik anonimleştirilir

---

## 💳 Ödeme Sistemi

### SmartRouter — 4 Gateway Failover

```
Checkout ──► SmartRouter ──┬──► NOWPayments (öncelikli)
                           ├──► BTCPay Server
                           ├──► MoonPay (KYC fallback)
                           └──► Transak (KYC fallback)
```

| Özellik | Detay |
|---------|-------|
| **Kripto** | BTC, ETH, USDT (TRC20), USDC (ERC20) |
| **Wallet** | Metamask, WalletConnect |
| **Kart** | PCI-DSS uyumlu, 3D Secure |
| **Fiyat** | 15 dakika price lock |
| **Anti-Fraud** | IP blacklist, 5 başarısız → 60dk ban |
| **KVKK** | 30 gün otomatik log silme |

---

## 💾 Yedekleme & Felaket Kurtarma

### 5-Part System Imaging

| Part | İçerik |
|------|--------|
| **Part 1** — Database | MSSQL .bak, SQLite, MariaDB dump |
| **Part 2** — App Core | core-api, docker-compose, web sites |
| **Part 3** — Infrastructure | Configs, secrets, SSL certs |
| **Part 4** — AI & Intelligence | AI modüller, vault.enc, vmail |
| **Part 5** — Orchestration | Bootstrap docker-compose.yml |

| Parametre | Değer |
|-----------|-------|
| **Şifreleme** | AES-256-CBC (PBKDF2 100K iter) |
| **Yerel** | Son 3 gün rotasyon |
| **Bulut** | Cloudflare R2 — son 30 gün |
| **Otomasyon** | Günlük 03:00 cron |
| **Restore** | Time Machine — tam veya kısmi (1-click) |
| **DR Test** | 19.03.2026 — 5/5 Part, 17/17 servis UP |

---

## 📧 Mail Altyapısı

```
Internet ──► Postfix (MTA) ──► Amavisd (Spam Filter) ──► Dovecot (MDA) ──► Mailbox
                                      │
                                      ▼
                                  Karantina
```

| Yetenek | Endpoint Sayısı |
|---------|:---:|
| Domain CRUD | 4 |
| Hesap CRUD | 8 |
| Alias & Yönlendirme | 6 |
| Spam & Greylisting | 4 |
| BCC / Relay / Transport | 11 |
| Karantina & Kuyruk | 9 |
| User WB List | 3 |
| Radar Stats | 5 |
| DNS Sağlık | 1 |
| **Toplam** | **53** |

---

## 🏷 Lisanslama & Tier Sistemi

### 3 Tier — 25 Servis

| Özellik | Standart | Professional | Enterprise |
|---------|:--------:|:------------:|:----------:|
| **Servis Sayısı** | 15 | 23 | 25 |
| Altyapı + Güvenlik | ✅ | ✅ | ✅ |
| Web + Mail + DB | ✅ | ✅ | ✅ |
| İzleme (Uptime, Dozzle) | — | ✅ | ✅ |
| Cloud Backup (R2/S3) | — | ✅ | ✅ |
| AI (STACK-AI) | — | ✅ | ✅ |
| White-Label | — | ✅ | ✅ |
| Masking Engine | — | full | custom |
| Neural Core | — | — | ✅ |
| Ghost Mode | local | full | full |

Detaylı:

## 📊 Tier Sistemi & Servis Matrisi (3 Katman — 25 Servis)

| Kategori | Uygulama & Açıklama | Standart | Professional | Enterprise |
| :--- | :--- | :---: | :---: | :---: |
| **DONANIM** | **Minimum CPU / RAM / Disk** | 2vCPU / 4GB / 40GB | 4vCPU / 8GB / 80GB | 8+vCPU / 16GB / 160GB |
| **CORE** | **Traefik:** Akıllı trafik ve SSL (HTTPS) | ✅ | ✅ | ✅ |
| | **Core API:** Sistemin yönetim beyni | ✅ | ✅ | ✅ |
| | **Portainer:** Görsel konteyner paneli | ✅ | ✅ | ✅ |
| | **Watchtower:** Otomatik güncelleme | ✅ | ✅ | ✅ |
| **GÜVENLİK** | **Authelia:** 2FA (Çift Faktör) koruma | ✅ | ✅ | ✅ |
| | **CrowdSec:** Global saldırgan engelleme | ✅ | ✅ | ✅ |
| | **CS-Bouncer:** Kapıda saldırı durdurma | ✅ | ✅ | ✅ |
| | **Masking Engine:** Veri anonimleştirme motoru | ❌ Basic | ✅ Full | ✅ Custom |
| **APP** | **Nginx-Sites:** Yüksek hızlı web sunumu | ✅ | ✅ | ✅ |
| | **Docker Host:** Node.js, Python, Go, PHP vb. | ✅ | ✅ | ✅ |
| **İLETİŞİM** | **iRedMail:** Sınırsız e-posta trafiği | ✅ | ✅ | ✅ |
| **SQL DB** | **MSSQL 2022:** Kurumsal DB altyapısı | ❌ | ✅ | ✅ |
| | **MariaDB:** Hızlı ve hafif DB motoru | ❌ | ✅ | ✅ |
| | **CloudBeaver:** Tarayıcıdan DB yönetimi | ❌ | ✅ | ✅ |
| **İZLEME** | **Netdata:** Anlık sistem grafikleri | ✅ | ✅ | ✅ |
| | **Uptime-Kuma:** Çökme bildirim sistemi | ✅ | ✅ | ✅ |
| | **Dozzle:** Canlı log izleme ekranı | ❌ | ✅ | ✅ |
| **YEDEKLEME** | **Local Backup:** Sunucu içi günlük yedek | ✅ | ✅ | ✅ |
| | **R2 Cloud Sync:** Cloudflare bulut yedeği | ❌ | ✅ | ✅ |
| | **S3 Disaster:** Kıta dışı felaket yedeği | ❌ | ❌ | ✅ |
| **MARKA** | **White-Label:** Kendi logonuzla satış | ❌ | ❌ | ✅ |
| **AI ZEKÂ** | **STACK-AI:** Yapay zeka analiz motoru | ❌ | ✅ | ✅ |
| | **NeuralCore:** Anomali algılama merkezi | ❌ | ✅ | ✅ |
| | **Ghost Mode:** İzleme anonimleştirme | ✅ Local | ✅ Full | ✅ Full |
| **ÖZET** | **Toplam Aktif Servis Sayısı** | **15** | **23** | **25** |


> **Özgürlük İlkesi:** Donanım (CPU/RAM/Disk) hiçbir zaman lisans tarafından kısıtlanmaz. Satılan şey yazılımdır.

### Lisans Teknolojisi

- **İmza:** RSA-4096 + PSS (MGF1 + SHA256)
- **HWID:** Canvas fingerprint + navigator tabanlı kilitleme
- **Doğrulama:** Online (API) + offline cache
- **Compliance:** 30 dakikada otomatik tarama

---

## 📱 Telegram Bot

**24 komut** — Tier-aware filtreleme (server/customer modu)

| Kategori | Komutlar |
|----------|---------|
| 📊 **İzleme** | `/stats`, `/top`, `/services`, `/health`, `/disk` |
| 🛠 **Yönetim** | `/logs`, `/backup`, `/certs`, `/mail`, `/domains` |
| 🔒 **Güvenlik** | `/security`, `/ban_list`, `/alerts`, `/ssh`, `/geomap` |
| 🤖 **AI** | `/analyze`, `/audit`, `/compliance`, `/updates` |
| ⚙️ **Sunucu** | `/restart` |
| 💬 **Sohbet** | Serbest mesaj → LLM Orchestrator |

**Otomatik Alertler:**
- Container down/up bildirim (60s polling)
- Disk >%85 uyarı
- Log error/critical monitoring (14 container)
- Neural Observer anomali tespiti

---

## ⚡ Performans

| Optimizasyon | Öncesi | Sonrası | İyileşme |
|:------------|:------:|:-------:|:--------:|
| CPU (cgroup v2) | Load 7.39 | Load 1.08 | **>%85** |
| Log gürültüsü | 4304/saat | ~1/saat | **>%99.9** |
| CPU idle | %0 | %93.8 | ∞ |
| Token sızıntısı | 378/saat | 0 | **%100** |

---

## 💻 Sistem Gereksinimleri

### Minimum

| Bileşen | Gereksinim |
|---------|-----------|
| **OS** | Ubuntu 22.04+ LTS |
| **CPU** | 2+ vCPU |
| **RAM** | 4 GB+ |
| **Disk** | 20 GB+ boş alan |
| **Docker** | 24.0+ |
| **Ağ** | Statik IP, domain DNS |

### Önerilen (Production)

| Bileşen | Değer |
|---------|-------|
| **OS** | Ubuntu 24.04 LTS |
| **CPU** | 6+ vCPU |
| **RAM** | 12 GB+ |
| **Disk** | 100 GB+ SSD |
| **Docker** | 29.x |
| **Ağ** | 1 Gbps, DNS A/MX/PTR kayıtları |

---

## 🚀 Hızlı Başlangıç

```bash
# 1. Sunucu kurulumu (sıfırdan)
bash /opt/mega-stack/install.sh install

# 2. Yedekleme altyapısı kurulumu
bash /opt/mega-stack/install-backup.sh

# 3. Durum kontrolü
bash /opt/mega-stack/install.sh status

# 4. Dashboard erişimi
# https://dashboard.mydomain.com
# → Authelia 2FA → PassHub → Dashboard
```

### Temel Komutlar

```bash
# Manuel yedek tetikleme
python3 /opt/backup-center/bin/backup_manager.py

# Core API restart
docker restart domain-api-v12

# Container log görüntüleme
docker logs <container-name> --tail 50

# Sistem sağlık kontrolü
curl -s https://dashboard.mydomain.com/api/health

# MSSQL bağlantı testi
docker exec mssql-server /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -C -Q "SELECT @@VERSION"
```

---

## 📝 Versiyon Geçmişi

| Versiyon | Tarih | Başlık | Öne Çıkan |
|:--------:|:-----:|--------|-----------|
| **v5.3** | 03.04.2026 | Payment System | Kripto + kart ödeme, SmartRouter, 4 gateway |
| **v5.2** | 31.03.2026 | Data Studio v12.0.4 | Full SQL capability, XLSX/PDF export |
| **v5.1** | 31.03.2026 | Veri Senkronizasyonu | DB ↔ MD single source of truth |
| **v5.0** | 27.03.2026 | Data Studio & Backup Rebirth | System Imaging, AI Management, 23 sayfa |
| **v4.9** | 23.03.2026 | Mail Komuta Merkezi v2.8 | The Radar & Interceptor, 53 mail endpoint |
| **v4.8** | 19.03.2026 | IAM & Audit | User attribution, RBAC genişletme |
| **v4.7** | 19.03.2026 | User Manager | DOM Control, UI/UX |
| **v4.5** | 17.03.2026 | AI Security | Kervan Kalkanı + NeuralCore |
| **v4.2** | 16.03.2026 | Redis Identity | Session Manager, Auth Middleware |
| **v4.1** | 15.03.2026 | Motor Dairesi | xterm.js, Self-Kill, PassHub Inject |
| **v4.0** | 15.03.2026 | R2 & Log Dashboard | Cloud backup, log management |
| **v3.5** | 14.03.2026 | Ghost Vault | Dosyasız şifreleme, Hybrid Vault |
| **v3.0** | 14.03.2026 | Mega-Editor & UX | Monaco IDE, UX Overhaul |
| **v2.5** | 13.03.2026 | Product Wizard | Tier sistemi, müşteri kurulum |
| **v2.0** | 10.03.2026 | Modüler Mimari | Monolitik → Core API v2.0 |
| **v1.0** | 01.06.2025 | Monolitik Başlangıç | İlk kurulum — 16 container |

---

## 📁 Proje Yapısı

```
/opt/mega-stack/                    # Ana kök dizin
├── docker-compose.yml              # 18 servis orkestrasyonu
├── install.sh                      # Kurulum + yedek + restore  + status
├── install-backup.sh               # Backup altyapı kurulumu
├── core-api/                       # FastAPI Backend (Python 3.12)
│   ├── main.py                     # Uvicorn entry point
│   ├── routers/                    # 38 router dosyası
│   ├── models/                     # 28 Pydantic model
│   ├── utils/                      # 32 utility modülü
│   ├── core/                       # 11 core modül
│   ├── middleware/                  # Auth + Studio Guard
│   └── db.py                       # DatabaseManager
├── web/mydomain.com/dashboard/ # Frontend (34 sayfa)
│   ├── index.html                  # Ana dashboard
│   ├── static/css/                 # ~10.750+ satır CSS
│   ├── static/js/                  # ~7.230+ satır JS
│   ├── assets/                     # Paylaşılan UI modülleri
│   └── [34 alt dizin]/             # Her biri bir dashboard sayfası
├── data/
│   ├── system_internal.db          # SQLite WAL (57 tablo)
│   └── .master_key                 # Fernet master key
├── security/
│   ├── authelia/                   # SSO konfigürasyonu
│   ├── crowdsec/                   # IPS konfigürasyonu
│   └── vault.enc                   # Hybrid Vault (encrypted)
├── secrets/                        # İskelet dosyalar (placeholder)
├── nginx/vhosts/                   # Nginx virtual hosts
├── traefik/                        # Traefik config + TLS
└── iredmail/                       # iRedMail custom overrides

/opt/backup-center/                 # Yedekleme merkezi
├── bin/backup_manager.py           # Yedekleme motoru
├── config/config.json              # Yedek ayarları
├── local/                          # Yerel yedekler (3 gün)
└── imaging/                        # 5-Part System Imaging

/opt/stack-memory/                  # Sistem hafızası & dokümantasyon
├── SYSTEM_BLUEPRINT.md             # Sistem Anayasası
├── system-core-report.md           # Derinlemesine analiz raporu
└── [20+ .md dosyası]              # Versiyon/rapor/audit belgeleri
```

---

<p align="center">
  <strong>MEGA-STACK Server v5.3</strong> — Tek Sunucu, Sınırsız Kontrol
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made_with-Python_3.12-3776AB?style=flat-square&logo=python" alt="">
  <img src="https://img.shields.io/badge/Powered_by-Docker-2496ED?style=flat-square&logo=docker" alt="">
  <img src="https://img.shields.io/badge/Secured_by-Authelia-1a73e8?style=flat-square" alt="">
  <img src="https://img.shields.io/badge/AI-Gemini_2.0-4285F4?style=flat-square&logo=google" alt="">
</p>

---

*Bu doküman MEGA-STACK v5.3 sistem verileri kullanılarak otomatik oluşturulmuştur.*  
*Son güncelleme: 04 Nisan 2026*
Powered by Barış Gelebek | barisgelebek.com

