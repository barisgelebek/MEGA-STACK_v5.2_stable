# 🛡️ MEGA-STACK v5.2 — Ultimate Infrastructure Wizard

MEGA-STACK v5.2, yüksek performanslı **AI servisleri**, **veri maskeleme motorları**, **veritabanı yönetimi** ve **güvenli ağ altyapılarını** tek bir merkezden kuran profesyonel bir **Deployment Orchestrator** çözümüdür. 

Karmaşık "Bare-Metal" veya "Cloud" sunucu kurulumlarını, hatasız ve paket bazlı kaynak yönetimi ile dakikalar içine indirir.

---

## 🚀 Öne Çıkan Özellikler

* **⚡ Zero-Dependency Bootstrapping:** Sunucuda hiçbir bağımlılık olmasa dahi kendi çalışma ortamını otomatik hazırlar.
* **💎 Tier-Based Resource Control:** Standart, Professional ve Enterprise paketlerine göre Docker kaynak limitlerini (CPU/RAM) dinamik yönetir.
* **🔒 RSA Hybrid Licensing:** Sunucuya özel RSA imzalı anahtarlarla Tuple-proof doğrulama mimarisi.
* **🌐 DNS & Cloud Automation:** Cloudflare entegrasyonu ve DKIM sync süreçlerini merkezi yönetim.
* **🛠️ Self-Healing Core:** Kırık binary linklerini onarır ve sistem portlarını kurulum öncesi denetler.

---

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

---

## 📊 Paket Karşılaştırma Matrisi (Tier Matrix)

| Özellik | Standart | Professional | Enterprise |
| :--- | :--- | :--- | :--- |
| **Masking Engine Mode** | Minimal | Standard | Enterprise |
| **Max Workers** | 2 Workers | 8 Workers | 16 Workers |
| **Data Retention** | 7 Gün | 30 Gün | 365 Gün |
| **Masking RAM/CPU** | 256MB / 0.25 | 512MB / 1.0 | 1GB / 2.0 |
| **Stack AI RAM/CPU** | 512MB / 0.5 | 1GB / 2.0 | 2GB / 4.0 |
| **Neural Core RAM/CPU** | 256MB / 0.25 | 512MB / 0.5 | 1GB / 1.0 |

---

## 💻 Sistem Gereksinimleri

| Paket | CPU (Core) | RAM (GB) | Disk (SSD) | OS (Tavsiye Edilen) |
| :--- | :--- | :--- | :--- | :--- |
| **Standart** | 2 Core | 4 GB | 40 GB | Ubuntu 22.04 LTS |
| **Professional** | 4 Core | 8 GB | 80 GB | Ubuntu 22.04 LTS |
| **Enterprise** | 8 Core | 16 GB+ | 200 GB+ | Ubuntu 24.04 LTS |

---

## 🧩 Teknik Bileşen Envanteri (Component Stack)

Sistem mimarisini oluşturan kritik bileşenlerin teknik detayları ve görev tanımları aşağıda listelenmiştir:

| İkon | Bileşen Adı | Sürüm | Teknoloji | Görev / Açıklama | Bağımlılıklar |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ✨ | **Google Gemini API** | v2.0 | REST | Ana LLM Motoru (Gemini 2.0 Flash) | STACK-AI Engine |
| ⚡ | **Groq API** | v1.0 | REST | İkincil LLM (Llama/Mixtral) - Ultra Düşük Gecikme | STACK-AI Engine |
| 🎭 | **MaskingEngine** | v1.0 | Python | **Kervan Kalkanı:** 5 Katmanlı anonimleştirme | NeuralCore |
| 🧠 | **NeuralCore** | v1.0 | Python | **Merkezi Sinir Sistemi:** 24h+30d Rolling Memory | SQLite WAL |
| 🤖 | **STACK-AI Engine** | v3.0 | Python | 3 Katmanlı LLM Orkestratörü (Fallback Sistemi) | MaskingEngine, NeuralCore |
| 💾 | **Backup Center** | v5.1 | Python/R2 | AES-256-CBC Şifreli, Çift Katmanlı Yedekleme | Rclone 1.73 |
| 🔬 | **Data Studio Engine**| v12.0.4 | FastAPI | 4-Motorlu DB Yönetim (SQLite/MSSQL/MariaDB/Redis) | aiosqlite, pymssql |
| 🎯 | **ASP.NET Core** | v8.0 | C# | PointVending Uygulaması & İş Mantığı | MSSQL Server |
| 🔐 | **Fernet Encryption** | v0.45 | Python | AES-128-CBC + HMAC-SHA256 Vault Güvenliği | cryptography |
| 🏦 | **Vault System** | v1.0 | Python | Hibrit Vault (Seal/Unseal) Mekanizması | Fernet Encryption |
| 🏢 | **MSSQL Server** | 2022 | T-SQL | Ana Kurumsal Veritabanı | Docker |
| 🗄️ | **SQLite WAL** | v3.45 | C/Python | Sistem Konfigürasyon DB (34 Tablo) | Python |
| 🏥 | **Recovery Manager** | v1.0 | Python | DB Sağlık Kontrolü ve Otomatik Onarım | aiosqlite |
| 🪪 | **Identity Snapshot** | v2.0 | SHA256 | Sistem Parmak İzi ve Disaster Recovery Kanıtı | JSON |
| 📸 | **Image Manager** | v1.0 | Docker | Full-System Tar Arşivi ve Restore Scripti | tar |
| 💻 | **xterm.js** | v5.5.0 | JS | Web Tabanlı Canlı Terminal Erişimi | UI |

---
---

## 🏗️ Katmanlı Mimari Yapısı (Layered Architecture)

Sistem, modülerlik ve yüksek ölçeklenebilirlik prensiplerine dayalı 5 ana katman üzerinde yükselmektedir:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND KATMANI                               │
│  • 25+ Dashboard Paneli (Vanilla JS, Chart.js, xterm.js)                │
│  • Glassmorphism UI Tasarımı & WebSocket Real-time Veri Akışı           │
├─────────────────────────────────────────────────────────────────────────┤
│                            API KATMANI                                  │
│  • 219+ REST Endpoint (FastAPI / GET-POST-DELETE)                       │
│  • 4 WebSocket Hub (Live Dashboard / Logs / Metrics / AI Chat)          │
│  • Güvenlik: Redis HMAC-SHA256 Session Yönetimi (1800s TTL)             │
├─────────────────────────────────────────────────────────────────────────┤
│                         İŞ MANTIĞI KATMANI                              │
│  • 28+ Kritik Python Modülü (NeuralCore, Guardian, MaskingEngine)       │
│  • Stack-AI Orkestrasyonu & Hibrit Vault (Fernet/RSA) Sistemi           │
├─────────────────────────────────────────────────────────────────────────┤
│                         VERİTABANI KATMANI                              │
│  • SQLite WAL (27+ Tablo, ACID Uyumluluğu, Sistem Konfigürasyonu)       │
│  • MSSQL 2022 (Kurumsal İş Uygulamaları & PointVending Verisi)          │
│  • MariaDB (iRedMail & İletişim Veritabanı)                             │
│  • Redis 7 (Hızlı Session Katmanı & Performans Cache)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                         ALTYAPI KATMANI                                 │
│  • Docker Compose Orkestrasyonu (17+ İzole Konteyner)                   │
│  • Traefik v2.11 (Otomatik SSL/ACME & Reverse Proxy)                    │
│  • Mega-Stack_webnet Bridge Network (İzole Ağ Güvenliği)                │
└─────────────────────────────────────────────────────────────────────────┘

```
## 📂 Proje Mimarisi

```text
mega-stack-product-wizard/
├── wizard.sh           # Ana giriş noktası (Bootstrap + Runner)
├── core/               # FastAPI Backend & Business Logic
├── binaries/           # Sistem araçları ve onarım scriptleri
├── templates/          # Jinja2 tabanlı dinamik Docker şablonları
├── web/                # 22 adımlık Kurulum UI (React/JS)
└── license/            # RSA Public key (Güvenlik anahtarı)
```
🛠️ Kurulum Kılavuzu (Hızlı Başlangıç)
1. Depoyu Klonlayın
```text

git clone [https://github.com/barisgelebek/MEGA-STACK_v5.2_stable.git](https://github.com/barisgelebek/MEGA-STACK_v5.2_stable.git)
cd mega-stack-product-wizard

```
2. İzinleri Düzenleyin ve Başlatın
```text

chmod +x wizard.sh binaries/bootstrap.sh
sudo ./wizard.sh

```
3. Kurulum Arayüzüne Erişin
Sihirbaz başladıktan sonra tarayıcınızdan şu adrese gidin:
```text

http://SUNUCU_IP_ADRESI:9999

```
🖥️ Kurulum Aşamaları
*  🔍 Donanım Tarama: CPU/RAM ve port durumu kontrolü.
*  🔑 Lisans Doğrulama: RSA anahtarı ile yetkilendirme (Step 00).
*  🏆 Tier Seçimi: Satın alınan paketin (Standart/Pro/Enterprise) seçimi.
*  ⚙️ Servis Ayarları: DNS, Mail, AI ve DB yapılandırması.
*  🚀 Finalize: Konteynerların seçilen limitlerle ayağa kaldırılması.
------------------------------------------------------------------------------------------
🔍 Hata Giderme (Troubleshooting)
Kurulum sırasında canlı logları izlemek için:
```text

tail -f logs/wizard.log

```
MEGA-STACK v5.2 - Ultimate Infrastructure Solutions
