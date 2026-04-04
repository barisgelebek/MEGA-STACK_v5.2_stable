# 📖 MEGA-STACK SERVER — SİSTEM İŞLEYİŞ VE KULLANIM KILAVUZU
**Kılavuz Tarihi:** 04 Nisan 2026  
**Sistem Versiyonu:** v5.3  
**Kılavuz Tipi:** Kapsamlı Dashboard İşleyiş & Kullanım Rehberi  
**Hazırlayan:** MEGA-STACK AI Analysis Engine  
**Kapsam:** 34 Dashboard Sayfası · 18 Docker Konteyner · 330+ API Endpoint  

---

## 📑 İÇİNDEKİLER

### A. GİRİŞ
1. [Kılavuz Hakkında](#a1-kılavuz-hakkında)
2. [Sistem Genel Bakış](#a2-sistem-genel-bakış)
3. [Mimari Özet](#a3-mimari-özet)

### B. YÖNETİM PANELLERİ
4. [Ana Dashboard (/)](#b1-ana-dashboard)
5. [Admin Overview (/admin/)](#b2-admin-overview)
6. [Domain Management (/domain-management/)](#b3-domain-management)
7. [User Manager (/user-manager/)](#b4-user-manager)
8. [Nav Menu (/nav-menu/)](#b5-nav-menu)

### C. GÜVENLİK MERKEZLERİ
9. [Guardian (/guardian/)](#c1-guardian)
10. [Defense Hub (/defense/)](#c2-defense-hub)
11. [PassHub (/passhub/)](#c3-passhub)
12. [Certificates Watch (/certificates-watch/)](#c4-certificates-watch)
13. [Login (/login/)](#c5-login)

### D. VERİ & VERİTABANI
14. [Data Studio (/data-studio/)](#d1-data-studio)
15. [SQL Runner (/sql-runner/)](#d2-sql-runner)
16. [Migration Hub (/migration/)](#d3-migration-hub)

### E. AI SİSTEMLERİ
17. [AI Studio (/ai-management/)](#e1-ai-studio)
18. [STACK-AI (/stack-ai/)](#e2-stack-ai)

### F. İZLEME & LOG
19. [Health Check (/healthcheck/)](#f1-health-check)
20. [Log Center (/logs/)](#f2-log-center)
21. [Analytics (/analytics/)](#f3-analytics)
22. [Motor Dairesi — Containers (/containers/)](#f4-motor-dairesi)

### G. İLETİŞİM
23. [Mail Center (/mail/)](#g1-mail-center)

### H. YEDEKLEME & KURTARMA
24. [Backup Center (/backup-center/)](#h1-backup-center)
25. [Restore Manager (/restore-manager/)](#h2-restore-manager)

### I. TİCARET & ÖDEME
26. [License Hub (/license/)](#i1-license-hub)
27. [Payment (/payment/)](#i2-payment)
28. [Product UI (/product-ui/)](#i3-product-ui)
29. [Release Manager (/release-manager/)](#i4-release-manager)

### J. DOSYA & BİLGİ YÖNETİMİ
30. [File Manager (/files/)](#j1-file-manager)
31. [Mega-Editor (/editor/)](#j2-mega-editor)
32. [Stack Memory (/stack-memory/)](#j3-stack-memory)
33. [Documentations (/documentations/)](#j4-documentations)

### K. DESTEK & UI
34. [Tickets (/tickets/)](#k1-tickets)
35. [UISetting (/UISetting/)](#k2-uisetting)
36. [Components (/components/)](#k3-components)
37. [Versions (/versions/)](#k4-versions)

### L. ÖZET & REFERANS
38. [Sayfa-Konteyner Matrisi](#l1-sayfa-konteyner-matrisi)
39. [Teknoloji Referans Tablosu](#l2-teknoloji-referans-tablosu)
40. [API Endpoint Dağılım Özeti](#l3-api-endpoint-dağılım-özeti)

---

## A1. KILAVUZ HAKKINDA

Bu kılavuz, MEGA-STACK Server v5.3 dashboard panelinde yer alan **34 sayfanın** tamamını fiziksel HTML/JS dosya analizi ve karşılık gelen **API router Python** dosyaları üzerinden inceleyerek hazırlanmıştır. Her sayfa için beş temel başlık altında detaylı bilgi sunulmaktadır:

1. **Amaç ve Detaylı Açıklama** — Sayfanın ne işe yaradığı ve teknik yapısı
2. **Kullanım ve Avantajlar** — Kullanıcı deneyimi ve sağladığı faydalar
3. **Sistem İçindeki Rolü** — Platform bütünlüğündeki pozisyonu
4. **Yönettiği Sistem ve Yönetim Mantığı** — Kontrol ettiği altyapı ve iş akışları
5. **Beslendiği Teknoloji ve Servisler** — Kullandığı kütüphaneler, API'ler ve konteynerler

---

## A2. SİSTEM GENEL BAKIŞ

MEGA-STACK Server, **18 Docker konteyner** üzerine inşa edilmiş kurumsal düzeyde bir sunucu yönetim platformudur. Tek bir dashboard üzerinden web hosting, e-posta, veritabanı, güvenlik, izleme, yedekleme, AI destekli analiz ve ödeme gibi kritik iş fonksiyonlarını yönetme imkanı sunar.

| Metrik | Değer |
|--------|-------|
| Docker Konteyner | 18 aktif servis |
| API Endpoint | 330+ (FastAPI) |
| Dashboard Sayfası | 34 alt sayfa |
| SQLite Tablo | 57 tablo |
| Python Router | 38 router dosyası |
| Frontend Paylaşılan JS | 12+ ortak modül |
| Toplam CSS Token | 40+ dinamik değişken |

---

## A3. MİMARİ ÖZET

```
İnternet → Traefik (SSL/TLS) → Nginx (Dashboard UI) / Core API (FastAPI :9998)
                                    │                          │
                              34 HTML/JS sayfa          330+ endpoint
                                    │                          │
                              Bootstrap 5.3.3           SQLite WAL (57 tablo)
                              Chart.js 4.x              MSSQL 2022 CU23
                              Monaco Editor 0.45.0      MariaDB (4 mail DB)
                              xterm.js / Leaflet.js     Redis 7-alpine
```

**Frontend Mimarisi:** Vanilla JS IIFE pattern — herhangi bir framework bağımlılığı yoktur. Tüm sayfalar `mega-stack-ui.js` (MegaAuth, MegaBranding, MegaHealth), `mega-nav-partial.js` (navbar injector), `main-ws-manager.js` (WebSocket singleton), `api-client.js` (merkezi fetch wrapper) ve `security-gate.js` (auth guard) ortak modüllerini kullanır.

**Backend Mimarisi:** FastAPI + Uvicorn, Python 3.12, port 9998. Her sayfa bir veya birden fazla router dosyasıyla eşleşir. Tüm istekler auth middleware'den geçer, denetim günlüğüne kaydedilir.

---


---

# B. YÖNETİM PANELLERİ

---

## B1. ANA DASHBOARD

**URL:** `/` · **HTML:** ~2500 satır · **API:** 20+ endpoint · **Router:** `admin.py`, `health.py`, `monitor.py`, `ai.py`

### 1. Amaç ve Detaylı Açıklama

Ana Dashboard, MEGA-STACK Server'ın **merkezi komuta ve kontrol merkezi**dir. Sunucunun anlık durumunu, performans metriklerini, güvenlik istatistiklerini ve sistem sağlığını tek bir ekranda sunar. Sayfa açıldığında tüm konteynerlerden, veritabanlarından ve güvenlik servislerinden veri toplanarak bütünleşik bir görünüm oluşturulur.

**Sayfa Bileşenleri:**
- **Hero Stats Band:** CPU, RAM, Disk, Uptime — 4 ana metrik kartı, her biri animasyonlu gauge göstergesiyle
- **Container Status Grid:** 18 konteynerin canlı durumu (running/stopped/error) renk kodlu kartlarla
- **GeoIP Harita:** Leaflet.js ile dünya haritası üzerinde aktif bağlantıların coğrafi dağılımı
- **Sağlık Skoru:** 0-100 arası dinamik sağlık puanı, Chart.js gauge göstergesi
- **Son Aktiviteler:** Denetim günlüğünden son 10 işlem listesi
- **Hızlı Erişim FAB (Floating Action Button):** Sık kullanılan işlemlere tek dokunuşla ulaşım
- **STACK-AI Chat Widget:** Sağ alt köşede yapay zeka sohbet balonu — anlık sorgu ve analiz
- **Mini Terminal:** Hızlı komut çalıştırma penceresi
- **Sistem Bildirimleri:** Toast + zil ikonu ile gerçek zamanlı bildirimler

### 2. Kullanım ve Avantajlar

- **Tek Bakışta Tüm Sistem:** Farklı sayfaları dolaşmadan sunucunun genel durumunu anında görme
- **Gerçek Zamanlı Güncelleme:** WebSocket üzerinden container durumu, CPU/RAM metrikleri anlık yenilenir
- **Proaktif Uyarı:** Sağlık skoru düşüşlerinde otomatik bildirim
- **GeoIP İzleme:** Şüpheli coğrafyalardan gelen erişimleri harita üzerinde tespit
- **AI Asistan:** Chat widget ile doğal dilde sunucu analizi isteme imkanı
- **Hızlı Eylem:** FAB menüsü ile backup başlatma, container yeniden başlatma gibi sık işlemlere anında erişim

### 3. Sistem İçindeki Rolü

Ana Dashboard, tüm diğer 33 sayfanın **üst katman özet görünümü**dür. Sistemin nabzını tutar ve anormal durumları yüzeye çıkarır. Tüm kullanıcılar login sonrası ilk bu sayfayla karşılaşır. Admin, wizard ve customer rollerine göre görünen bileşenler tier-aware filtreleme ile dinamik olarak ayarlanır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Container Fleet | Docker Engine API üzerinden canlı durum çekimi |
| Sistem Sağlığı | health_engine.py → 0-100 skor algoritması |
| Güvenlik Durumu | CrowdSec + GeoIP cache + audit_log birleşimi |
| Kaynak Kullanımı | Netdata metrikleri + Docker stats birleşimi |
| AI Chat | STACK-AI WebSocket kanalı üzerinden gerçek zamanlı sorgu |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Chart.js 4.x | Gauge ve bar grafikleri |
| Leaflet.js 1.9.4 | GeoIP dünya haritası |
| WebSocket (main-ws-manager.js) | Canlı veri akışı |
| Bootstrap 5.3.3 | Responsive grid ve kartlar |
| mega-stack-ui.js | MegaAuth, MegaBranding, MegaHealth |
| Core API — admin.py | Container operasyonları |
| Core API — health.py | Sağlık skoru endpoint'leri |
| Core API — monitor.py | Netdata metrik proxy |
| Core API — ai.py | STACK-AI sohbet motoru |
| Docker Engine | 18 konteyner durum bilgisi |
| Netdata v2.9 | CPU, RAM, Disk gerçek zamanlı metrikleri |
| Redis 7 | Session doğrulama |
| SQLite WAL | audit_log, system_state tabloları |

---

## B2. ADMIN OVERVIEW

**URL:** `/admin/` · **HTML:** ~200 satır · **API:** 8+ endpoint · **Router:** `admin.py`, `monitor.py`

### 1. Amaç ve Detaylı Açıklama

Admin Overview, yöneticilere **launchpad tarzı** bir hızlı erişim paneli sunar. Tüm yönetim sayfalarına kartlar halinde organize edilmiş kısayollarla ulaşım sağlar. Aynı zamanda konteyner durumları ve temel sistem metriklerinin özet grafiklerini içerir.

**Sayfa Bileşenleri:**
- **Launchpad Grid:** Her yönetim modülü için ikon + başlık + kısa açıklama içeren kartlar
- **Container Özet Metriği:** Running/Stopped/Error sayıları
- **Chart.js Mini Grafikler:** Günlük kaynak kullanım trendi
- **Hızlı Aksiyon Butonları:** Sık kullanılan admin işlemleri

### 2. Kullanım ve Avantajlar

- **Kolay Navigasyon:** 34 sayfadan herhangi birine tek tıkla erişim
- **Görsel Kategorizasyon:** Sayfalar kategorilere ayrılmış — Güvenlik, Veri, İzleme, vb.
- **Yeni Admin Dostu:** İlk kez kullanan yönetici için öğrenme eğrisini azaltır
- **Özelleştirilebilir:** Tier seviyesine göre görünmeyen modüller otomatik gizlenir

### 3. Sistem İçindeki Rolü

Admin Overview, **navigasyon katmanı** olarak görev yapar. Dashboard'un daha kısa, daha odaklı bir versiyonudur. Özellikle mobil cihazlarda hızlı erişim için tercih edilir. Tier-aware yapısı sayesinde müşterinin lisans seviyesine göre yalnızca erişebildiği sayfalar gösterilir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Sayfa Kataloğu | navigation tablosundan dinamik menü çekimi |
| Konteyner Özeti | Docker stats aggregation |
| Metrik Grafikleri | Netdata verilerinin Chart.js render'ı |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Chart.js 4.x | Mini performans grafikleri |
| Bootstrap 5.3.3 | Launchpad grid kartları |
| Core API — admin.py | Container status özeti |
| Core API — monitor.py | Netdata metrik proxy |
| Core API — navigation.py | Dinamik menü tanımları |
| SQLite WAL | navigation, system_state tabloları |

---

## B3. DOMAIN MANAGEMENT

**URL:** `/domain-management/` · **HTML:** ~180 satır · **API:** 6 endpoint · **Router:** `domains.py`

### 1. Amaç ve Detaylı Açıklama

Domain Management sayfası, sunucu üzerinde barındırılan **tüm domain'lerin merkezi yönetim** noktasıdır. Yeni domain ekleme, mevcut domain yapılandırma, Nginx virtual host ve Traefik routing kurallarını otomatik oluşturma işlemlerini tek panelden gerçekleştirir.

**Sayfa Bileşenleri:**
- **Domain Listesi:** Tablo formatında tüm kayıtlı domain'ler (ad, durum, SSL, oluşturma tarihi)
- **Yeni Domain Ekleme Modal:** Domain adı, hedef port, SSL tercihi
- **Port Discovery:** Sunucuda çalışan servislerin otomatik port taraması
- **Domain Düzenleme:** Mevcut domain yapılandırmasını güncelleme
- **Atomic Provisioning:** Nginx + Traefik konfigürasyonlarının eş zamanlı oluşturulması

### 2. Kullanım ve Avantajlar

- **Tek Tıkla Domain Ekleme:** Nginx conf + Traefik label + SSL otomatik oluşturulur
- **Port Keşfi:** Sunucudaki aktif portları otomatik tarayarak hedef servisi seçme
- **Atomic İşlem:** Nginx ve Traefik yapılandırması ya birlikte başarılı olur ya birlikte geri alınır
- **SSL Otomasyonu:** Let's Encrypt ACME üzerinden otomatik sertifika
- **Durum İzleme:** Her domain'in sağlık durumu (aktif/hata/pending)

### 3. Sistem İçindeki Rolü

Domain Management, **web hosting altyapısının kontrol noktası**dır. Nginx container'ı (statik dosya servisi) ve Traefik container'ı (reverse proxy + SSL) ile doğrudan etkileşir. Eklenen her domain cert-dumper tarafından izlenir ve Certificates Watch sayfasında görünür hale gelir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Nginx Virtual Hosts | Dinamik .conf dosyası oluşturma/güncelleme/silme |
| Traefik Routing | Docker label tabanlı dinamik routing kuralları |
| SSL Sertifikaları | ACME challenge → cert-dumper → Nginx |
| Port Mapping | Sunucu port tarama + servis eşleştirme |
| Domain Veritabanı | SQLite domains tablosunda CRUD |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Tablo ve modal UI |
| Core API — domains.py | Domain CRUD + provisioning |
| Nginx 1.29-alpine | Virtual host oluşturma hedefi |
| Traefik v2.11 | Reverse proxy kural oluşturma hedefi |
| cert-dumper | SSL sertifika export |
| Let's Encrypt | Otomatik ACME sertifika |
| SQLite WAL | domains tablosu |

---

## B4. USER MANAGER

**URL:** `/user-manager/` · **HTML:** ~600 satır · **API:** 16 endpoint · **Router:** `user.py`, `user_admin.py`

### 1. Amaç ve Detaylı Açıklama

User Manager, sistemdeki **kullanıcı hesaplarının tam yaşam döngüsü yönetimi**ni sağlayan kapsamlı bir sayfadır. Kullanıcı oluşturma, rol atama, 2FA ayarlama, aktif oturum izleme ve denetim günlüğü takibi 4 sekme altında organize edilmiştir.

**Sayfa Bileşenleri (4 Sekme):**
- **Kullanıcılar Sekmesi:** Kullanıcı listesi, yeni oluşturma, düzenleme, silme, rol atama (admin/wizard/customer), hesap etkinleştirme/devre dışı bırakma
- **2FA Sekmesi:** TOTP kurulumu, QR kod oluşturma, kurtarma kodları, 2FA zorlama politikası
- **Oturumlar Sekmesi:** Aktif Redis session'larının canlı listesi, IP adresi, tarayıcı bilgisi, "session kick" ile zorla oturum kapatma
- **Denetim Sekmesi:** Kullanıcı bazlı audit log geçmişi, filtreleme, güvenlik challenge kayıtları

### 2. Kullanım ve Avantajlar

- **Rol Tabanlı Erişim (RBAC):** Admin → tam yetki, Wizard → kısıtlı yönetim, Customer → salt okuma
- **2FA Zorlama:** Hassas roller için TOTP zorunlu kılınabilir
- **Canlı Oturum İzleme:** Kimin, nereden, hangi cihazla bağlı olduğu anlık görülür
- **Session Kick:** Şüpheli oturumları anında sonlandırma
- **QR Kod Kurulumu:** 2FA etkinleştirme Google Authenticator uyumlu QR ile tek adımda
- **Güvenlik Sınaması (Security Challenge):** Kritik işlemler öncesi ek doğrulama isteme

### 3. Sistem İçindeki Rolü

User Manager, **kimlik ve erişim yönetimi (IAM)** katmanının merkezidir. Oluşturulan kullanıcılar Redis session store ile oturum yönetir, Authelia ile 2FA doğrulama yapar, tüm işlemleri audit_log tablosuna kaydeder. Tier gating sistemi ile de entegredir — farklı lisans seviyelerindeki müşteriler farklı sayfa ve özelliklere erişir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Kullanıcı CRUD | SQLite users tablosunda oluşturma/güncelleme/silme |
| RBAC Rolleri | 3 rol seviyesi: admin, wizard, customer |
| 2FA/TOTP | pyotp ile TOTP seed oluşturma, QR render, doğrulama |
| Session Yönetimi | Redis key-value: session token → kullanıcı bilgisi |
| Session Kick | Redis'ten hedef session key silme |
| Audit Log | Her kullanıcı işlemi audit_log tablosuna kayıt |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | 4 sekmeli tab arayüzü |
| QR Code JS | 2FA QR kod oluşturma (client-side) |
| Core API — user.py | Kullanıcı self-service endpoint'leri |
| Core API — user_admin.py | Admin kullanıcı yönetim endpoint'leri |
| Core API — session.py | Redis session doğrulama + kick |
| Redis 7-alpine | Aktif oturum depolama |
| Authelia 4.39.15 | 2FA doğrulama katmanı |
| SQLite WAL | users, audit_log tabloları |

---

## B5. NAV MENU

**URL:** `/nav-menu/` · **HTML:** ~900 satır · **API:** 9 endpoint · **Router:** `navigation.py`

### 1. Amaç ve Detaylı Açıklama

Nav Menu, dashboard'un **sol kenar çubuğu navigasyon menüsünü dinamik olarak yöneten** sayfadır. 42 menü öğesinin sıralaması, ikonları, görünürlüğü, gruplama ve yetki seviyelerini görsel bir arayüzle düzenleme imkanı sunar.

**Sayfa Bileşenleri:**
- **Menü Öğesi Listesi:** Sürükle-bırak sıralama destekli tüm menü öğeleri
- **İkon Seçici (Icon Picker):** 500+ Tabler Icons arasından ikon atama
- **Yeni Menü Öğesi Modal:** Başlık, URL, ikon, parent, sıra, yetki seviyesi
- **İzin Seviyeleri:** Her öğe için admin/wizard/customer görünürlük ayarı
- **Grup Yönetimi:** Menü öğelerini kategorilere ayırma ve separator ekleme
- **Drag-Sort:** Sürükle-bırak ile sıra değiştirme, anında kayıt

### 2. Kullanım ve Avantajlar

- **Görsel Düzenleme:** Kod yazmadan menü yapısını değiştirme
- **500+ İkon:** Tabler Icons kütüphanesinden zengin ikon seçimi
- **Yetki Bazlı Görünürlük:** Belirli menü öğelerini sadece admin'e gösterme
- **Sürükle-Bırak:** Menü sıralamasını saniyeler içinde değiştirme
- **Canlı Önizleme:** Değişiklikler anında sol menüye yansır

### 3. Sistem İçindeki Rolü

Nav Menu, dashboard'un **navigasyon altyapısının CRUD yönetim arayüzü**dür. Tüm sayfalar sol kenar çubuğundaki menüyü `mega-nav-partial.js` ile yükler — bu modül arka planda `navigation.py` router'ından menü tanımlarını çeker. Nav Menu sayfası bu tanımları yönetir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Menü Öğeleri | SQLite navigation tablosunda CRUD |
| Sıralama | drag-sort ile order_index güncelleme |
| İkon Ataması | Tabler Icons classname seçimi + kayıt |
| Yetki Filtreleme | min_role alanı: admin=1, wizard=2, customer=3 |
| Parent/Child | parent_id ile hiyerarşik menü yapısı |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Modal ve form UI |
| Tabler Icons | 500+ ikon kütüphanesi |
| Sortable.js (drag-drop) | Sürükle-bırak sıralama |
| Core API — navigation.py | Menü CRUD endpoint'leri (9 endpoint) |
| mega-nav-partial.js | Navbar inject (tüketici) |
| SQLite WAL | navigation tablosu |

---


---

# C. GÜVENLİK MERKEZLERİ

---

## C1. GUARDIAN

**URL:** `/guardian/` · **HTML:** ~450 satır · **API:** 8 endpoint · **Router:** `guardian.py`

### 1. Amaç ve Detaylı Açıklama

Guardian, MEGA-STACK'in **merkezi credential yönetim ve acil durum komuta merkezi**dir. Sunucu üzerindeki tüm hassas bilgilerin (API key, veritabanı şifreleri, servis token'ları) Fernet şifreli olarak depolanması, güncellenmesi ve acil durumlarda toplu değiştirilmesini sağlar.

**Sayfa Bileşenleri:**
- **Credential Hub:** Tüm servis credential'larının şifreli listesi (MSSQL, Authelia, iRedMail, Telegram, CrowdSec, .NetCoreApp, AI Keys, R2 Cloud — 23+ credential)
- **Credential Düzenleme:** Her servis için şifre güncelleme formu
- **Panic Button (Panik Düğmesi):** 7 fazlı acil durum protokolü — tüm şifrelerin tek tuşla toplu değiştirilmesi
- **Dependency Tree:** Credential bağımlılık haritası — hangi şifrenin değişmesinin hangi servisi etkileyeceği
- **Vault Durumu:** vault.enc dosyasının mühürlenme durumu ve son güncelleme zamanı

### 2. Kullanım ve Avantajlar

- **Merkezi Şifre Yönetimi:** Tüm servis credential'ları tek noktadan yönetilir
- **Fernet Şifreleme:** AES-128-CBC + HMAC-SHA256 ile şifreli depolama
- **Atomic Update:** 6 fazlı güncelleme — Backup → DB → Vault Seal → Ghost Inject → Ghost Seal → Tamamlandı; herhangi bir fazda hata → otomatik rollback
- **Panic Button:** Sunucu ele geçirilme şüphesinde tüm şifreler anında değiştirilir
- **Bağımlılık Görselleştirme:** Şifre değişikliğinin cascade etkisini önceden görme
- **Ghost Mode Entegrasyonu:** Şifreler Docker container'lara diske yazmadan enjekte edilir

### 3. Sistem İçindeki Rolü

Guardian, **güvenlik katmanının kalbi**dir. Tüm servisler credential'larını buradan alır. Ghost Vault mekanizması sayesinde disk üzerinde gerçek şifreler bulunmaz — yalnızca `{{FROM_DB_OR_VAULT}}` placeholder'ları vardır. Guardian, boot sırasında vault.enc'yi çözer ve credential'ları RAM'e yükler, ardından Docker container'lara enjekte eder.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Credential DB | service_credentials tablosunda Fernet şifreli CRUD |
| Ghost Vault | vault.enc mühürleme/açma döngüsü |
| Ghost Inject | Docker exec ile container'a credential enjeksiyonu |
| Panic Protocol | 7 faz: validate → backup → regenerate → DB update → vault seal → ghost inject → verify |
| Bağımlılık Ağacı | Credential → servis eşleştirme haritası |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Credential kartları ve modal UI |
| SweetAlert2 | Panic button onay dialogu |
| Core API — guardian.py | Credential CRUD + Panic endpoint'leri |
| Fernet (cryptography) | AES-128-CBC + HMAC-SHA256 şifreleme |
| Docker Engine API | Ghost Inject — container exec |
| vault.py | Hybrid Vault şifreleme motoru |
| SQLite WAL | service_credentials tablosu |
| Tüm 18 konteyner | Credential tüketici olarak bağımlı |

---

## C2. DEFENSE HUB

**URL:** `/defense/` · **HTML:** ~220 satır · **API:** 6 endpoint · **Router:** `defense.py`

### 1. Amaç ve Detaylı Açıklama

Defense Hub, sunucunun **saldırı tespit ve önleme sistemi (IPS)** görselleştirme ve yönetim merkezidir. CrowdSec motorunun topluluk ve yerel istihbarat verilerini, coğrafi saldırı haritasını, SSH brute-force loglarını ve ban listelerini tek panelden sunar.

**Sayfa Bileşenleri:**
- **GeoIP Saldırı Haritası:** Leaflet.js ile dünya haritası üzerinde saldırı kaynaklarının coğrafi dağılımı, ısı haritası katmanı
- **Ban Listesi:** Aktif olarak engellenen IP adresleri tablosu (IP, ülke, sebep, süre)
- **SSH Log Parser:** SSH oturum açma girişimlerinin analizi — başarılı/başarısız giriş dağılımı
- **CrowdSec Metrikleri:** LAPI (Local API) ve CAPI (Central API) bağlantı durumu
- **Tehdit İstihbaratı:** CrowdSec topluluk blocklist'lerinden gelen tehdit senaryoları

### 2. Kullanım ve Avantajlar

- **Görsel Tehdit Haritası:** Saldırıların dünya haritasında gerçek zamanlı görselleştirilmesi
- **Proaktif Koruma:** CrowdSec topluluk istihbaratı ile bilinen saldırgan IP'lerin önceden engellenmesi
- **SSH İzleme:** Brute-force girişimlerinin anında fark edilmesi
- **Manuel Ban/Unban:** Belirli IP'leri elle kara/beyaz listeye ekleme
- **LAPI/CAPI Sağlığı:** CrowdSec motorunun çalışma durumunu izleme

### 3. Sistem İçindeki Rolü

Defense Hub, **ağ güvenliği katmanının gözetim paneli**dir. CrowdSec konteyner'ı ve CrowdSec-Bouncer (Traefik middleware) ile doğrudan iletişir. Tespit edilen tehditleri görselleştirir ve yönetim imkanı sunar. geoip_cache tablosu üzerinden IP → konum çözümlemesi yapar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| CrowdSec LAPI | Lokal decision + alert okuma |
| CrowdSec CAPI | Topluluk blocklist senkronizasyonu |
| Ban Listesi | cscli decisions ile IP ban/unban |
| GeoIP Cache | geoip_cache tablosunda IP → ülke eşleştirmesi |
| SSH Logları | /var/log/auth.log parse → istatistik |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Leaflet.js 1.9.4 | İnteraktif GeoIP saldırı haritası |
| Bootstrap 5.3.3 | Tablo ve kart UI |
| Core API — defense.py | CrowdSec proxy + GeoIP endpoint'leri |
| CrowdSec v1.6.8 | IPS motoru — tehdit algılama |
| CrowdSec-Bouncer | Traefik middleware — IP engelleme |
| SQLite WAL | geoip_cache tablosu |
| Traefik v2.11 | CrowdSec-Bouncer middleware hedefi |

---

## C3. PASSHUB

**URL:** `/passhub/` · **HTML:** ~500 satır · **API:** 1 endpoint (çok aşamalı) · **Router:** `passhub.py`

### 1. Amaç ve Detaylı Açıklama

PassHub, Docker konteyner'ların **çalışma zamanı şifre güncelleme** sistemidir. Motor Dairesi'nden (Containers) container'a bağlanıldığında kullanılan şifrelerin güvenli bir şekilde değiştirilmesini sağlayan 5 fazlı bir güncelleme protokolü sunar.

**Sayfa Bileşenleri:**
- **Servis Seçici:** Şifresi güncellenecek servis seçimi (MSSQL, iRedMail, vb.)
- **5-Faz Güncelleme Wizard'ı:** Doğrulama → Yedekleme → Güncelleme → Test → Onay adımları
- **Master Key Doğrulama:** İşlem öncesi HMAC-SHA256 tabanlı master key kontrolü
- **Şifre Güçlük Ölçer:** Girilen yeni şifrenin entropy ve karmaşıklık analizi
- **İlerleme Çubuğu:** Her fazın durumunu gösteren animasyonlu progress bar

### 2. Kullanım ve Avantajlar

- **Güvenli Güncelleme:** 5 fazlı protokol ile şifre değişikliği — herhangi bir fazda hata → rollback
- **Master Key Koruması:** Yetkisiz şifre değişikliği önlemi
- **Güçlük Analizi:** Zayıf şifre kullanımını önleme
- **Container Enjeksiyonu:** Yeni şifre otomatik olarak ilgili Docker container'a enjekte edilir
- **Guardian Senkron:** Değişiklik Guardian credential DB'ye otomatik yansır

### 3. Sistem İçindeki Rolü

PassHub, Guardian'ın **operasyonel uzantısı**dır. Guardian credential'ları depolarken, PassHub bunları güvenli güncelleme protokolü ile değiştirir. Motor Dairesi'nde terminal açıldığında PassHub'dan gelen credential'lar kullanılır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Şifre Güncelleme | 5-faz: validate → backup → update DB → ghost inject → verify |
| Master Key | SHA-256 hash doğrulama |
| Container Inject | Docker exec ile yeni credential enjeksiyonu |
| Vault Sync | vault.enc güncelleme |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Wizard form adımları |
| Core API — passhub.py | 5-faz şifre güncelleme endpoint'i |
| passhub_engine.py | PassHub iş mantığı motoru |
| Fernet (cryptography) | Credential şifreleme |
| Docker Engine API | Container credential enjeksiyonu |
| guardian.py (router) | Credential DB senkronizasyonu |
| SQLite WAL | service_credentials tablosu |

---

## C4. CERTIFICATES WATCH

**URL:** `/certificates-watch/` · **HTML:** ~270 satır · **API:** 5 endpoint · **Router:** `certs.py`

### 1. Amaç ve Detaylı Açıklama

Certificates Watch, sunucu üzerindeki **tüm SSL/TLS sertifikalarının sağlık durumu izleme ve erken uyarı** sistemidir. Let's Encrypt ACME üzerinden otomatik yenilenen sertifikaların süre dolumu, geçerlilik ve zincir bütünlüğünü takip eder.

**Sayfa Bileşenleri:**
- **SSL Vault Tablosu:** Tüm aktif sertifikaların listesi — domain, veren kuruluş, başlangıç/bitiş tarihi, kalan gün, durum (yeşil/sarı/kırmızı)
- **ACME Parse:** Traefik acme.json dosyasının parse edilmiş görünümü
- **Yenileme Geçmişi:** Son başarılı/başarısız yenileme kayıtları
- **Erken Uyarı:** 30/14/7 gün kala renk kodlu alert
- **2FA Gereksinim:** Bu sayfaya erişim admin rolü + 2FA doğrulama gerektirir

### 2. Kullanım ve Avantajlar

- **Sertifika Envanteri:** 11+ domain'in SSL durumunu tek ekranda görme
- **Süre Dolumu Uyarısı:** Kırmızı/sarı/yeşil renk kodlarıyla erken fark etme
- **Otomatik Yenileme İzleme:** Let's Encrypt ACME sürecinin sağlığını kontrol
- **Zincir Doğrulama:** SSL sertifika zincirinin bütünlüğü kontrolü
- **Audit Trail:** Sertifika değişiklik geçmişi

### 3. Sistem İçindeki Rolü

Certificates Watch, **TLS/SSL altyapısının izleme katmanı**dır. Traefik'in ACME yönetimi ile cert-dumper'ın export ettiği sertifikaları takip eder. Domain Management'tan eklenen yeni domain'lerin sertifika durumu burada izlenir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| SSL Envanteri | acme.json parse + disk sertifika tarama |
| Süre Denetimi | X.509 notBefore/notAfter parse |
| Erken Uyarı | 30/14/7 gün eşik kontrolleri |
| Yenileme İzleme | ACME challenge loglarının analizi |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Tablo ve alert kartları |
| Core API — certs.py | SSL sertifika endpoint'leri |
| ssl_tool.py | X.509 parse ve analiz utility |
| Traefik v2.11 | ACME sertifika yönetimi kaynağı |
| cert-dumper | Sertifika dosya export servisi |
| Let's Encrypt | ACME otomatik sertifika sağlayıcı |

---

## C5. LOGIN

**URL:** `/login/` · **HTML:** ~280 satır · **API:** 4 endpoint · **Router:** `session.py`

### 1. Amaç ve Detaylı Açıklama

Login sayfası, MEGA-STACK dashboard'una **güvenli giriş kapısı**dır. Görsel olarak Matrix tarzı yeşil karakter yağmuru animasyonlu bir arka plan sunar. 3 adımlı kimlik doğrulama süreci ile yüksek güvenlik sağlar.

**Sayfa Bileşenleri:**
- **Matrix Rain Canvas:** Tam ekran canvas animasyon — yeşil karakter yağmuru efekti
- **Login Formu:** Kullanıcı adı + şifre
- **2FA Adımı:** TOTP 6 haneli kod girişi (TOTP etkinse)
- **MasterKey Modu:** Acil durum girişi — master key ile tüm yetkilere erişim
- **RBAC Yönlendirme:** Login sonrası role göre farklı sayfaya yönlendirme
- **Session Cookie:** HttpOnly, Secure, SameSite=Strict cookie oluşturma

### 2. Kullanım ve Avantajlar

- **3 Adımlı Doğrulama:** Kullanıcı/şifre → 2FA TOTP → Session oluşturma
- **Dual Mode:** Normal kullanıcı girişi + MasterKey acil durum girişi
- **Matrix Efekti:** Etkileyici görsel deneyim + güvenlik hissi
- **Session Güvenliği:** HMAC-SHA256 token, HttpOnly cookie, 1800s sliding TTL
- **Otomatik Yönlendirme:** Admin → Dashboard, Wizard → Admin Overview

### 3. Sistem İçindeki Rolü

Login, **kimlik doğrulama zincirinin giriş noktası**dır. Authelia 2FA katmanı, Redis session store ve RBAC yetkilendirme sistemi ile doğrudan çalışır. Başarılı login sonrası oluşturulan session token tüm diğer sayfalarda `security-gate.js` tarafından doğrulanır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Kimlik Doğrulama | Kullanıcı adı + SHA-256 hash şifre kontrolü |
| 2FA | TOTP doğrulama (pyotp entegrasyonu) |
| Session | Redis'te HMAC-SHA256 token oluşturma (1800s TTL) |
| MasterKey | SHA-256 hash eşleştirme — tüm yetki |
| Cookie | HttpOnly, Secure, SameSite=Strict |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Canvas API | Matrix rain animasyon |
| Bootstrap 5.3.3 | Login form UI |
| Core API — session.py | Login/logout/verify endpoint'leri |
| Redis 7-alpine | Session token depolama |
| Authelia 4.39.15 | 2FA doğrulama katmanı |
| SQLite WAL | users tablosu |

---


---

# D. VERİ & VERİTABANI

---

## D1. DATA STUDIO

**URL:** `/data-studio/` · **HTML:** ~200 satır + ~1800 satır inline JS · **API:** 11 endpoint · **Router:** `data_studio.py`

### 1. Amaç ve Detaylı Açıklama

Data Studio, MEGA-STACK'in **profesyonel çoklu veritabanı yönetim ve sorgulama IDE'si**dir. 4 farklı veritabanı motorunu tek arayüzden yönetme, SQL sorgusu yazma ve çalıştırma, sonuçları görselleştirme ve dışa aktarma imkanı sunar. ~2000 satırlık JavaScript ile en kapsamlı frontend modüllerinden biridir.

**Sayfa Bileşenleri:**
- **Ace Editor Paneli:** SQL syntax highlighting, auto-complete, çoklu sekme destekli kod editörü
- **4 Veritabanı Motoru Seçici:** MSSQL, MariaDB vmail, MariaDB iredapd, SQLite arasında geçiş
- **Sonuç Tablosu:** Sorgu sonuçlarının tablo formatında görüntülenmesi
- **Inline Cell Editing:** Tablo hücrelerine tıklayarak doğrudan veri düzenleme
- **Object Explorer:** Sol panelde veritabanı/tablo/kolon ağaç yapısı
- **Export Araçları:** XLSX (SheetJS), PDF (jsPDF), CSV dışa aktarma
- **Sorgu Geçmişi:** Son çalıştırılan sorguların listesi
- **Execution Timer:** Sorgu çalışma süresi göstergesi (120s timeout)

### 2. Kullanım ve Avantajlar

- **Çoklu Motor:** Tek arayüzden MSSQL + MariaDB + SQLite sorgulama
- **Profesyonel Editör:** Ace Editor ile syntax highlighting, auto-indent, bracket matching
- **Inline Düzenleme:** SELECT sonuçlarında hücreye tıklayıp doğrudan UPDATE
- **Zengin Export:** Excel, PDF, CSV formatlarında sonuç indirme
- **Object Explorer:** Veritabanı yapısını görsel ağaç olarak keşfetme
- **Güvenli:** SQL blacklist (DROP/ALTER/TRUNCATE engellemesi) + parameterized query

### 3. Sistem İçindeki Rolü

Data Studio, **veri katmanının birincil etkileşim noktası**dır. MSSQL (iş verileri), MariaDB (mail verileri) ve SQLite (sistem verileri) olmak üzere 3 veritabanı teknolojisinin tamamına erişim sağlar. SQL Runner'dan farklı olarak daha gelişmiş IDE deneyimi sunar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| MSSQL Sorgu | pyodbc → sqlcmd bağlantısı, 120s timeout |
| MariaDB Sorgu | PyMySQL → vmail/iredapd veritabanları |
| SQLite Sorgu | sqlite3 WAL mode → system_internal.db |
| Object Explorer | INFORMATION_SCHEMA / sqlite_master parse |
| Inline Edit | Hücre tıklama → UPDATE statement oluşturma |
| Export | Sunucu taraflı + istemci taraflı dışa aktarma |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Ace Editor 1.36.5 | SQL kod editörü |
| SheetJS (xlsx) | Excel dışa aktarma |
| jsPDF | PDF oluşturma |
| Bootstrap 5.3.3 | Tab ve tablo UI |
| Core API — data_studio.py | Multi-engine SQL endpoint'leri |
| studio_factory.py | Veritabanı bağlantı fabrikası |
| sql_executor.py | Güvenli SQL çalıştırıcı |
| MSSQL 2022 CU23 | İş veritabanı motoru |
| MariaDB (iRedMail) | Mail veritabanı (vmail, iredapd) |
| SQLite WAL | Sistem veritabanı |

---

## D2. SQL RUNNER

**URL:** `/sql-runner/` · **HTML:** ~350 satır · **API:** 6 endpoint · **Router:** `sql.py`

### 1. Amaç ve Detaylı Açıklama

SQL Runner, **hızlı SQL sorgusu çalıştırma ve veritabanı keşfi** için tasarlanmış hafif bir araçtır. Data Studio'nun daha odaklı kardeşidir — MSSQL ve MariaDB üzerinde sorgu çalıştırma, hazır snippet'leri kullanma ve nesne gezgini ile veritabanını keşfetme imkanı sunar.

**Sayfa Bileşenleri:**
- **SQL Editör:** Sözdizimi renklendirmeli metin editörü
- **Motor Seçici:** MSSQL / MariaDB dual-engine geçişi
- **Snippet Kütüphanesi:** Hazır SQL sorgu şablonları (TOP 100, tablo listesi, index bilgisi, vb.)
- **Object Explorer:** Veritabanı → tablo → kolon hiyerarşik gezgin
- **Sonuç Grid:** Sorgu sonuçlarının tablo görünümü
- **Timeout Koruması:** 120 saniye maksimum sorgu süresi

### 2. Kullanım ve Avantajlar

- **Hızlı Erişim:** Basit sorgular için Data Studio'ya göre daha hafif arayüz
- **Snippet Desteği:** Sık kullanılan sorguları tek tıkla yükleme
- **Dual-Engine:** Tek arayüzden MSSQL ve MariaDB'ye erişim
- **Object Explorer:** Tablo ve kolon yapısını görsel keşfetme
- **Güvenli:** SQL blacklist + timeout koruması

### 3. Sistem İçindeki Rolü

SQL Runner, **veri katmanının hızlı erişim aracı**dır. Data Studio tam IDE deneyimi sunarken, SQL Runner operasyonel sorgulamalar için optimize edilmiştir. DBA ve sistem yöneticilerinin günlük sorgu ihtiyaçları için idealdir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| MSSQL Sorgu | pyodbc bağlantısı, 120s timeout |
| MariaDB Sorgu | PyMySQL bağlantısı |
| Snippet | Predefined SQL template set |
| Object Explorer | INFORMATION_SCHEMA parse |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Form ve tablo UI |
| Prism.js 1.29.0 | SQL syntax highlighting |
| Core API — sql.py | Multi-engine SQL endpoint'leri |
| sql_executor.py | Güvenli SQL çalıştırıcı |
| MSSQL 2022 CU23 | Birincil sorgu hedefi |
| MariaDB (iRedMail) | İkincil sorgu hedefi |

---

## D3. MIGRATION HUB

**URL:** `/migration/` · **HTML:** ~650 satır · **API:** 7 endpoint · **Router:** `migration.py`

### 1. Amaç ve Detaylı Açıklama

Migration Hub, **MSSQL veritabanı import ve restore işlemlerinin** yönetim merkezidir. .bak (native backup), .bacpac (data-tier application) ve .dacpac (schema-only) formatlarındaki yedeklerin drag-drop ile yüklenmesi ve canlı terminal çıktısıyla restore edilmesini sağlar.

**Sayfa Bileşenleri:**
- **Drag & Drop Yükleme Alanı:** .bak / .bacpac / .dacpac dosyalarını sürükle-bırak ile yükleme (10 GB limit)
- **Dosya Listesi:** Yüklenmiş dosyaların envanteri — boyut, format, tarih
- **Restore Wizard:** Adım adım restore süreci — dosya seç → hedef DB → onay → başlat
- **Canlı Terminal:** xterm.js tabanlı restore işlemi çıktısını gerçek zamanlı izleme
- **Import Geçmişi:** Tamamlanmış import'ların tarihçesi ve durumu
- **sqlpackage Entegrasyonu:** .bacpac import için Microsoft sqlpackage aracı

### 2. Kullanım ve Avantajlar

- **Drag & Drop:** Karmaşık komut satırı yerine görsel dosya yükleme
- **3 Format Desteği:** .bak (tam backup), .bacpac (veri+şema), .dacpac (sadece şema)
- **Canlı İzleme:** Restore sürecini terminal çıktısıyla adım adım takip
- **10 GB Limit:** Büyük veritabanı dosyaları için geniş kapasite
- **Geçmiş Takibi:** Hangi dosyanın ne zaman import edildiğinin kaydı

### 3. Sistem İçindeki Rolü

Migration Hub, **veri taşıma ve kurtarma altyapısının giriş noktası**dır. MSSQL container ile doğrudan etkileşir. Backup Center'dan farklı olarak dışarıdan gelen veritabanı dosyalarının sisteme aktarılmasına odaklanır. sqlpackage utility'si (/opt/sqlpackage/) ile .bacpac dosyalarını işler.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Dosya Yükleme | multipart upload → /opt/backup-center/imports/ |
| .bak Restore | RESTORE DATABASE T-SQL komutu via pyodbc |
| .bacpac Import | sqlpackage /Action:Import via subprocess |
| .dacpac Deploy | sqlpackage /Action:Publish via subprocess |
| Terminal Stream | xterm.js + WebSocket canlı çıktı |
| Import Geçmişi | import_history tablosu + import_status.json |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| xterm.js | Canlı terminal emülatörü |
| Bootstrap 5.3.3 | Drag-drop ve wizard UI |
| Core API — migration.py | Import/restore endpoint'leri |
| migration_tool.py | MSSQL migrasyon iş mantığı |
| sqlpackage | Microsoft .bacpac/.dacpac aracı |
| MSSQL 2022 CU23 | Restore hedef motoru |
| WebSocket | Terminal çıktı stream |

---


---

# E. AI SİSTEMLERİ

---

## E1. AI STUDIO

**URL:** `/ai-management/` · **HTML:** ~1500 satır · **API:** 18+ endpoint · **Router:** `ai.py`

### 1. Amaç ve Detaylı Açıklama

AI Studio, MEGA-STACK'in **yapay zeka motorlarının merkezi yönetim ve konfigürasyon** sayfasıdır. 3 katmanlı LLM orchestrator'ını, veri maskeleme kurallarını, neural observer'ları, AI denetim günlüğünü ve Ghost Mode kontrolünü tek panelden yönetir. ~1500 HTML satırıyla en kapsamlı sayfalardan biridir.

**Sayfa Bileşenleri:**
- **Motor Durumu Paneli:** L1 (Gemini), L2 (Groq), L3 (Kural) motorlarının çalışma durumu, API key validity, son kullanım istatistikleri
- **Ghost Mode Anahtarı:** AI motorunu tamamen devre dışı bırakan master switch
- **Maskeleme Kuralları (Kervan Kalkanı):** 10 builtin regex + özel maskeleme kuralları CRUD arayüzü — IP, e-posta, API key, JWT, şifre, telefon, kredi kartı, vb.
- **Shannon Entropy Ayarları:** Yüksek entropi eşik değeri konfigürasyonu (varsayılan 4.2)
- **Neural Observer Yönetimi:** Özel anomali algılama kuralları — ad, koşul, aksiyon, tetikleme sıklığı
- **AI Denetim Günlüğü (Audit):** Her AI sorgusunun kaydı — tarih, motor, token sayısı, maskeleme durumu, sonuç
- **Bağlam Enjeksiyonu:** SYSTEM_BLUEPRINT.md dosyasının AI'ye beslenen bağlam olarak yönetimi
- **Motor Konfigürasyonu:** Temperature, max_tokens, timeout gibi LLM parametreleri

### 2. Kullanım ve Avantajlar

- **Motor İzleme:** Her LLM motorunun sağlık durumunu anlık görme
- **Ghost Mode:** Güvenlik endişesinde AI'yi tek tuşla devre dışı bırakma
- **Kervan Kalkanı:** AI'ye gönderilen verilerde otomatik hassas bilgi maskeleme (KVKK/GDPR uyumlu)
- **Özel Maskeleme:** Sektöre özel regex kuralları ekleyebilme
- **Neural Observer:** Proaktif anomali algılama — belirli koşullar sağlandığında otomatik Telegram alert
- **Denetim İzi:** Her AI sorgusunun kaydının tutulması — compliance ve audit için

### 3. Sistem İçindeki Rolü

AI Studio, **yapay zeka katmanının beyin cerrahı**dır. STACK-AI chat widget'ı ve STACK-AI sayfası burada konfigüre edilen motorları kullanır. Maskeleme kuralları tüm AI sorgularına uygulanır. Neural observer'lar arka planda sürekli çalışır ve anomali tespit ettiğinde bildirim gönderir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| LLM Orchestrator | L1→L2→L3 fallback zinciri konfigürasyonu |
| Ghost Mode | system_state tablosunda ai_enabled flag |
| Maskeleme Kuralları | ai_masking_rules tablosunda regex CRUD |
| Shannon Entropy | Eşik değer konfigürasyonu |
| Neural Observer | neural_observers tablosunda kural CRUD |
| AI Audit | audit_log tablosunda AI sorgu kayıtları |
| SYSTEM_BLUEPRINT | AI bağlam dosyası içerik yönetimi |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Çok sekmeli konfigürasyon arayüzü |
| Chart.js 4.x | AI kullanım istatistik grafikleri |
| SweetAlert2 | Ghost Mode onay diyalogu |
| Core API — ai.py | 18+ AI yönetim endpoint'i |
| ai_brain.py | LLM Orchestrator motoru |
| Google Gemini 2.0 Flash | L1 birincil AI motoru |
| Groq Llama 3.3-70b | L2 yedek AI motoru |
| security_engine.py | Maskeleme motoru (Kervan Kalkanı) |
| sentinel.py | Neural observer çalıştırma motoru |
| SQLite WAL | ai_masking_rules, neural_observers, system_neural_memory tabloları |

---

## E2. STACK-AI

**URL:** `/stack-ai/` · **HTML:** ~200 satır · **API:** 6+ endpoint + WebSocket · **Router:** `ai.py`, `ws_hub.py`

### 1. Amaç ve Detaylı Açıklama

STACK-AI, kullanıcıların MEGA-STACK sistemi hakkında **doğal dilde sorgu yapabildikleri yapay zeka sohbet arayüzü**dür. Sunucu durumu analizi, operasyonel tavsiyeler, sorun teşhisi ve yapılandırma önerileri alma imkanı sunar.

**Sayfa Bileşenleri:**
- **Chat Interface:** Mesaj balonu tabanlı sohbet arayüzü (kullanıcı solda, AI sağda)
- **8 Preset Senaryo:** Hazır sorgu şablonları — "Sunucu sağlığını analiz et", "Güvenlik durumunu özetle", "Backup stratejisini değerlendir", vb.
- **Container Context Seçici:** AI'ye hangi container bağlamında sorgu sorulacağının seçimi
- **Ghost Mode Göstergesi:** AI devre dışıysa uyarı banner
- **Markdown Render:** AI yanıtlarında Markdown desteği (kod blokları, tablolar, listeler)
- **WebSocket Stream:** AI yanıtlarının karakter karakter akışı (streaming response)

### 2. Kullanım ve Avantajlar

- **Doğal Dil Sorgu:** Teknik bilgi gerektirmeden "CPU neden yüksek?" gibi sorular sorma
- **Bağlam Farkında:** SYSTEM_BLUEPRINT.md ile sistem durumunun tamamını bilen AI
- **Preset Senaryolar:** Sık sorulan sorular için tek tıkla analiz başlatma
- **Container Bağlamı:** Belirli bir container hakkında odaklı soru sorma
- **Streaming Yanıt:** AI yanıtlarını gerçek zamanlı karakter karakter görme
- **Maskeleme:** Sorgu ve yanıtlarda hassas bilgiler otomatik maskelenir

### 3. Sistem İçindeki Rolü

STACK-AI, **AI katmanının kullanıcı etkileşim noktası**dır. AI Studio'da konfigüre edilen motorları ve maskeleme kurallarını kullanır. Ana Dashboard'daki chat widget'ın tam ekran versiyonudur. WebSocket Hub üzerinden gerçek zamanlı yanıt akışı sağlar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Chat Oturumu | WebSocket bağlantısı + session bazlı geçmiş |
| LLM Sorgu | ai_brain.py → L1/L2/L3 cascade |
| Maskeleme | Giden sorgu + gelen yanıta maskeleme uygulanır |
| Bağlam | SYSTEM_BLUEPRINT.md + container stats enjeksiyonu |
| Preset | 8 predefined sorgu şablonu |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Marked.js | AI yanıtlarında Markdown render |
| Prism.js 1.29.0 | Kod bloğu syntax highlighting |
| Bootstrap 5.3.3 | Chat balonu ve form UI |
| WebSocket (ws_hub.py) | Streaming AI yanıt akışı |
| Core API — ai.py | AI sorgu endpoint'leri |
| ai_brain.py | LLM Orchestrator |
| Google Gemini 2.0 Flash | L1 AI motoru |
| Groq Llama 3.3-70b | L2 yedek AI motoru |
| security_engine.py | Kervan Kalkanı maskeleme |
| SQLite WAL | system_neural_memory |

---

# F. İZLEME & LOG

---

## F1. HEALTH CHECK

**URL:** `/healthcheck/` · **HTML:** ~920 satır · **API:** 8 endpoint + WebSocket · **Router:** `health.py`

### 1. Amaç ve Detaylı Açıklama

Health Check, sunucunun **bütünsel sağlık durumunu 0-100 arası puan** ile ölçen kapsamlı bir izleme sayfasıdır. CPU, RAM, disk, konteyner durumu, SSL sertifikaları, veritabanı bağlantıları ve servis yanıt sürelerini tek bir skor altında birleştirir.

**Sayfa Bileşenleri:**
- **Sağlık Skoru Gauge:** 0-100 arası büyük gauge grafiği (Chart.js) — renk kodlu (kırmızı <50, sarı 50-80, yeşil >80)
- **7 İstatistik Kartı:** CPU %, RAM %, Disk %, Container UP/DOWN, SSL durumu, DB bağlantı, API yanıt ms
- **Chart.js Sparkline'ları:** Her metrik için son 1 saatlik mini trend grafikleri
- **Container Pulse Grid:** 18 konteynerin kalp atışı — son 5 dakikalık durum geçmişi bar chart
- **Netdata Entegrasyonu:** On-demand derinlemesine metrik — istendiğinde Netdata'dan detaylı veri çekimi
- **Aksiyon Butonları:** Sağlık skoru düşükse önerilen aksiyonlar (restart, cleanup, vb.)
- **WebSocket Canlı Güncelleme:** Sağlık skoru ve metrikler gerçek zamanlı yenilenir

### 2. Kullanım ve Avantajlar

- **Tek Skor:** Sunucunun genel durumunu anında anlama
- **Erken Uyarı:** Skor düşüşlerinde proaktif bildirim
- **Derinlemesine Analiz:** Sparkline'lar ile trend değişimlerini izleme
- **Container Pulse:** Hangi container'ın sorunlu olduğunu anında tespit
- **Aksiyon Önerisi:** Düşük skor için otomatik çözüm önerileri
- **On-demand Netdata:** Detaylı metrik gerektiğinde Netdata'ya yönlendirme

### 3. Sistem İçindeki Rolü

Health Check, **izleme katmanının merkezi gösterge tablosu**dur. health_engine.py'deki algoritma tüm metrikleri ağırlıklı olarak birleştirir. Dashboard'daki sağlık göstergesi bu sayfanın özet versiyonudur. Telegram bot'un /health komutu da aynı motoru kullanır. 5 dakikada bir arka planda otomatik çalışır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Sağlık Skoru | health_engine.py → ağırlıklı metrik birleşimi |
| CPU/RAM/Disk | Docker stats + /proc/ dosya sistemi |
| Container Pulse | Docker API → container durumu tarihçesi |
| SSL Durumu | ssl_tool.py → sertifika geçerlilik kontrolü |
| DB Bağlantı | SQLite + MSSQL + MariaDB ping |
| API Yanıt | Core API self-check response time |
| Netdata Proxy | Netdata REST API → metrik çekimi |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Chart.js 4.x | Gauge + sparkline + bar grafikleri |
| Bootstrap 5.3.3 | Stat kartları ve grid |
| WebSocket | Canlı sağlık skoru güncellemesi |
| Core API — health.py | Sağlık metrikleri endpoint'leri |
| health_engine.py | Sağlık skoru hesaplama algoritması |
| Docker Engine API | Container status + stats |
| Netdata v2.9 | Derinlemesine sistem metrikleri |
| SQLite WAL | system_state tablosu |
| MSSQL 2022 | DB bağlantı sağlık kontrolü |
| MariaDB | Mail DB bağlantı kontrolü |
| Redis 7 | Session store sağlık kontrolü |

---

## F2. LOG CENTER

**URL:** `/logs/` · **HTML:** ~800 satır · **API:** 8 endpoint · **Router:** `logs.py`

### 1. Amaç ve Detaylı Açıklama

Log Center, sunucudaki **tüm log kaynaklarının merkezi toplama, filtreleme ve yönetim** sayfasıdır. Docker container logları ve sistem denetim günlüğü olmak üzere 2 ana sekmede organize edilmiştir.

**Sayfa Bileşenleri:**
- **Container Logs Sekmesi:** 18 container'dan herhangi birinin Docker loglarını gerçek zamanlı izleme, satır sayısı filtresi, arama, live tail modu
- **Audit Trail Sekmesi:** Sistem denetim günlüğü — kullanıcı, IP, işlem, tarih, detay (filtrelenebilir tablo)
- **Panic Mode:** Tüm logların acil temizlenmesi (kritik güvenlik olaylarında)
- **Retention Konfigürasyonu:** Log saklama süresi ayarı (varsayılan 14 gün)
- **Purge İşlemi:** Seçili zaman aralığındaki logların güvenli silinmesi
- **Export:** Log kayıtlarının CSV/JSON olarak indirilmesi

### 2. Kullanım ve Avantajlar

- **Merkezi Log:** 18 container'ın loglarını tek ekranda izleme
- **Live Tail:** Gerçek zamanlı log akışı — sorun teşhisinde kritik
- **Audit Trail:** Kim, ne zaman, ne yaptı — compliance ve güvenlik için
- **Panic Mode:** Güvenlik ihlali sonrası log temizleme
- **Retention:** Disk dolmasını önleyen otomatik saklama politikası
- **Filtreleme:** Container, seviye (ERROR/WARN/INFO), tarih aralığı, metin arama

### 3. Sistem İçindeki Rolü

Log Center, **denetim ve sorun giderme katmanının birincil aracı**dır. Docker log driver'dan (json-file, 50MB×3) container loglarını, audit_log tablosundan denetim kayıtlarını toplar. Telegram bot'un /logs komutu da bu altyapıyı kullanır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Container Logları | Docker API → log stream (tail + follow) |
| Audit Trail | audit_log tablosu → filtrelenebilir tablo |
| Retention | Log saklama süresi konfigürasyonu |
| Purge | Zaman aralığına göre log silme |
| Panic | Tüm logların acil temizlenmesi |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | 2 sekmeli tab arayüzü |
| Core API — logs.py | Log okuma, purge, retention endpoint'leri |
| log_reader.py | Docker log okuyucu utility |
| log_streamer.py | Canlı log stream utility |
| Docker Engine API | Container log erişimi |
| SQLite WAL | audit_log tablosu |
| json-file (Docker log driver) | 50MB × 3 per container |

---

## F3. ANALYTICS

**URL:** `/analytics/` · **HTML:** ~600 satır · **API:** 5+ endpoint · **Router:** `analytics.py`

### 1. Amaç ve Detaylı Açıklama

Analytics sayfası, MEGA-STACK'in **kurulum telemetrisi ve iş zekası** gösterge tablosudur. Product Wizard ile yapılan kurulumların istatistiklerini, tier dağılımını, coğrafi dağılımı ve trend grafiklerini sunar.

**Sayfa Bileşenleri:**
- **KPI Kartları:** Toplam kurulum, aktif lisans, son 30 gün kurulum, ortalama tier
- **Trend Grafikleri:** Chart.js ile aylık kurulum trendi (line chart)
- **Tier Dağılımı:** Standart / Professional / Enterprise dağılımı (doughnut chart)
- **Coğrafi Dağılım:** Kurulumların ülke bazında dağılımı
- **Tablo Görünümü:** install_analytics tablosunun detaylı satır listesi

### 2. Kullanım ve Avantajlar

- **Satış Analizi:** Hangi tier'ın en popüler olduğunu görme
- **Trend İzleme:** Kurulum artış/azalış trendinin grafiksel takibi
- **Coğrafi Analiz:** Hangi bölgelerden daha fazla kurulum yapıldığı
- **KPI İzleme:** Önemli metriklerin anlık durumu

### 3. Sistem İçindeki Rolü

Analytics, **ticari operasyonların izleme katmanı**dır. Product Wizard her kurulum yaptığında install_analytics tablosuna veri kaydeder. Analytics bu verileri görselleştirir. License Hub'ın ticari tarafını tamamlar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Kurulum İstatistikleri | install_analytics tablosundan aggregate sorgular |
| Tier Dağılımı | GROUP BY tier → doughnut chart veri |
| Trend Analizi | GROUP BY month → line chart veri |
| Coğrafi Dağılım | GeoIP → ülke bazında gruplama |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Chart.js 4.x | Line, doughnut, bar grafikleri |
| Bootstrap 5.3.3 | KPI kartları ve tablo |
| Core API — analytics.py | Telemetri endpoint'leri |
| SQLite WAL | install_analytics tablosu |

---

## F4. MOTOR DAİRESİ (CONTAINERS)

**URL:** `/containers/` · **HTML:** ~350 satır · **API:** 14+ endpoint · **Router:** `ops.py`, `admin.py`

### 1. Amaç ve Detaylı Açıklama

Motor Dairesi, Docker konteyner'ların **operasyonel yönetim ve terminal erişim** merkezidir. 18 konteynerin başlatma, durdurma, yeniden başlatma işlemleri ile container'a doğrudan terminal bağlantısı sağlar. "Motor Dairesi" ismi gemilerdeki fiziksel motor dairesine atıftır.

**Sayfa Bileşenleri:**
- **Container Grid:** 18 konteynerin durum kartları — isim, image, durum, CPU, RAM, uptime
- **Operasyon Butonları:** Start, Stop, Restart, Remove (her kart üzerinde)
- **Self-Kill Protection:** 6 kritik container (traefik, core-api, nginx, mssql, redis, authelia) durdurma engeli
- **xterm.js Terminal:** Container'a doğrudan shell bağlantısı — tam terminal emülatörü
- **PassHub Inject:** Terminal açıldığında credential'ların otomatik enjeksiyonu
- **Log Önizleme:** Her container'ın son 50 satır log önizlemesi
- **Docker Stats:** Canlı CPU/RAM kullanım metrikleri

### 2. Kullanım ve Avantajlar

- **Görsel Container Yönetimi:** 18 container'ı kart grid ile yönetme
- **Terminal Erişimi:** SSH'a gerek kalmadan container içine shell açma
- **Self-Kill Koruması:** Kritik servislerin yanlışlıkla durdurulmasını önleme
- **Credential Güvenliği:** PassHub entegrasyonu ile şifrelerin otomatik enjeksiyonu
- **Canlı Metrikler:** CPU/RAM kullanımını anlık izleme
- **Operasyonel Kolaylık:** Start/Stop/Restart tek tıkla

### 3. Sistem İçindeki Rolü

Motor Dairesi, **Docker orkestrasyon katmanının birincil kontrolcüsü**dür. Portainer'ın dashboard içi karşılığıdır ancak daha entegre çalışır — PassHub credential enjeksiyonu, self-kill koruması ve Core API üzerinden audit log kaydı gibi özellikler ekler.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Container Ops | Docker Engine API → start/stop/restart/remove |
| Terminal | Docker exec → xterm.js WebSocket bridge |
| Self-Kill | Hardcoded koruma listesi — 6 kritik container |
| PassHub | passhub_engine.py → credential enjeksiyonu at terminal open |
| Stats | Docker stats API → canlı CPU/RAM |
| Loglar | Docker logs → son 50 satır preview |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| xterm.js | Terminal emülatörü |
| Bootstrap 5.3.3 | Container kart grid |
| WebSocket | Terminal + stats stream |
| Core API — ops.py | Container operasyonları |
| Core API — admin.py | Docker management endpoint'leri |
| Docker Engine API | Container lifecycle yönetimi |
| passhub_engine.py | Credential enjeksiyon motoru |
| 18 Docker container | Yönetilen hedef konteynerler |

---


---

# G. İLETİŞİM

---

## G1. MAIL CENTER

**URL:** `/mail/` · **HTML:** ~1000+ satır · **API:** 53 endpoint · **Router:** `mail_pro.py`

### 1. Amaç ve Detaylı Açıklama

Mail Center, MEGA-STACK'in **en kapsamlı sayfası**dır — 53 API endpoint ile kurumsal e-posta altyapısının tüm yönlerini yönetir. iRedMail (Postfix + Dovecot + Amavisd + MariaDB) stack'inin dashboard üzerinden eksiksiz kontrolünü sağlar. 5 ana sekme ve 12+ modal ile organize edilmiştir.

**Sayfa Bileşenleri (5 Sekme):**

**Radar Sekmesi:**
- 24 saatlik mail trafik analizi — gönderilen/alınan/spam/virus/bounce ayrımı
- 5 farklı metrik kartı ile trafik özeti
- Trend grafikleri (Chart.js bar + line)

**Domains Sekmesi:**
- Mail domain yönetimi — ekleme, silme, konfigürasyon
- Her domain için hesap sayısı, alias sayısı, quota kullanımı
- Domain bazlı spam politikası ayarları

**Accounts Sekmesi:**
- Mailbox CRUD — oluşturma, düzenleme, silme, quota ayarı
- Alias yönetimi — e-posta yönlendirme kuralları
- Forwarding — otomatik iletme yapılandırması
- User whitelist/blacklist yönetimi
- Greylisting konfigürasyonu (global/domain/override)

**Security Sekmesi:**
- BCC arşivleme — scope × direction matris (inbound/outbound × domain/user)
- Spam politikaları — Amavisd tag/kill seviyeleri
- Karantina yönetimi — release/delete + 7 content kodu
- Mail kuyruğu (postqueue) — flush/delete/hold
- DNS sağlık kontrolü — SPF/DKIM/DMARC/PTR doğrulama

**Audit Sekmesi:**
- Mail denetim günlüğü — gönderme/alma/spam/bounce kayıtları
- İstatistiksel özet grafikleri

### 2. Kullanım ve Avantajlar

- **Tam Mail Yönetimi:** Domain, hesap, alias, forwarding, quota — tüm mail operasyonları tek ekrandan
- **DNS Sağlık:** SPF/DKIM/DMARC/PTR otomatik doğrulama — mail deliverability için kritik
- **Spam Kontrolü:** Amavisd politika yönetimi — hassas tag/kill eşik ayarları
- **Karantina:** Spam olarak işaretlenen mailleri inceleme ve serbest bırakma
- **BCC Arşiv:** Kurumsal compliance için mail arşivleme
- **Greylisting:** İlk kez gelen gönderenleri geçici reddetme — spam azaltma
- **Mail Kuyruğu:** Takılı mailleri flush etme veya silme
- **Radar:** 24 saat mail trafiğini görselleştirme — anomali tespiti

### 3. Sistem İçindeki Rolü

Mail Center, **iletişim altyapısının tam kontrolcüsü**dür. iRedMail container'ı içindeki Postfix (MTA), Dovecot (MDA), Amavisd (spam filtresi) ve 4 MariaDB veritabanını (vmail, amavisd, iredapd, iredadmin) yönetir. 53 endpoint ile en fazla API'ye sahip modüldür.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Mail Domain | MariaDB vmail.domain tablosu CRUD |
| Mailbox | MariaDB vmail.mailbox tablosu CRUD |
| Alias | MariaDB vmail.alias tablosu CRUD |
| Forwarding | MariaDB vmail.alias + forwardings |
| BCC | MariaDB vmail.sender_bcc_domain/user + recipient_bcc |
| Spam Policy | MariaDB amavisd.policy tablosu |
| Greylisting | MariaDB iredapd.greylisting tablosu |
| Karantina | Amavisd karantina dizini + DB |
| Mail Kuyruğu | postqueue komutu (Docker exec) |
| DNS Sağlık | dig komutu ile SPF/DKIM/DMARC/PTR çözümleme |
| Radar | Mail log parse → istatistik aggregation |
| WB List | MariaDB amavisd.wblist + mailaddr tabloları |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Chart.js 4.x | Radar trafik grafikleri |
| Bootstrap 5.3.3 | 5 sekmeli tab + 12+ modal |
| SweetAlert2 | Onay ve uyarı diyalogları |
| Core API — mail_pro.py | 53 mail yönetim endpoint'i |
| mail_engine.py | Mail iş mantığı motoru |
| mail_db.py | MariaDB bağlantı yöneticisi |
| iRedMail container | Postfix + Dovecot + Amavisd |
| MariaDB — vmail | Mail hesapları ve domainler |
| MariaDB — amavisd | Spam politikaları ve karantina |
| MariaDB — iredapd | Mail politika motoru |
| MariaDB — iredadmin | iRedAdmin yönetim DB |

---

# H. YEDEKLEME & KURTARMA

---

## H1. BACKUP CENTER

**URL:** `/backup-center/` · **HTML:** ~900 satır · **API:** 10+ endpoint · **Router:** `backup.py`

### 1. Amaç ve Detaylı Açıklama

Backup Center, MEGA-STACK'in **5-Part System Imaging teknolojisi ile kapsamlı yedekleme** yönetim merkezidir. Yerel ve bulut yedeklemelerini zamanlama, izleme ve yönetme imkanı sunar.

**Sayfa Bileşenleri:**
- **5-Part Dashboard:** Her part'ın (Database, App Core, Configs, AI, Bootstrap) son yedekleme durumu, boyutu, tarihi
- **İlerleme Çubuğu:** Aktif yedekleme işleminin gerçek zamanlı ilerleme göstergesi
- **Zamanlama (Schedule):** Otomatik yedekleme saati ve sıklık konfigürasyonu (varsayılan: 03:00 günlül)
- **Depolama Durumu:** Yerel (/opt/backup-center/local/) ve bulut (R2) depolama kullanım metrikleri
- **Yedek Geçmişi:** Tamamlanmış yedeklemelerin kronolojik listesi — boyut, süre, durum
- **Cloud Sync:** Cloudflare R2'ye yedek senkronizasyonu durumu ve ayarları
- **Şifreleme Durumu:** AES-256-CBC şifreleme aktif/pasif göstergesi
- **Manuel Yedekleme:** Tek tıkla anlık yedekleme başlatma

### 2. Kullanım ve Avantajlar

- **5-Part Imaging:** Sistem bileşenleri ayrı parçalarda yedeklenir — kısmi restore imkanı
- **AES-256 Şifreleme:** PBKDF2 100K iterasyon ile yedekler şifreli depolanır
- **Dual Depolama:** Yerel (son 3 gün) + Bulut R2 (son 30 gün) — 3-2-1 yaklaşımı
- **Otomatik Zamanlama:** Cron tabanlı günlük otomatik yedekleme
- **İlerleme İzleme:** Yedekleme sürecini gerçek zamanlı takip
- **Bildirm:** Telegram + Dashboard bildirim

### 3. Sistem İçindeki Rolü

Backup Center, **felaket kurtarma stratejisinin birincil aracı**dır. Restore Manager ile birlikte çalışır — Backup oluşturur, Restore geri yükler. 5-Part imaging sistemi sayesinde sadece veritabanını veya sadece konfigürasyonları geri yüklemek mümkündür.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Part 1 — Database | MSSQL .bak + SQLite copy + MariaDB dump |
| Part 2 — App Core | core-api/ + docker-compose.yml + web sites tar |
| Part 3 — Configs | Traefik, Nginx, Authelia, CrowdSec config tar |
| Part 4 — AI & Intelligence | AI modüller + vault.enc + vmail tar |
| Part 5 — Bootstrap | docker-compose.yml (standalone bootstrap) |
| Şifreleme | AES-256-CBC + PBKDF2 100K iterasyon |
| Yerel Depolama | /opt/backup-center/local/ — son 3 gün retention |
| Bulut Depolama | Rclone → Cloudflare R2 — son 30 gün |
| Zamanlama | Cron job — günlük 03:00 |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Part kartları ve progress bar |
| Chart.js 4.x | Depolama kullanım grafikleri |
| Core API — backup.py | Backup CRUD + schedule endpoint'leri |
| backup/ Python modülleri | core.py, db.py, config_backup.py, ai.py, identity.py |
| imaging/ Python modülleri | 5-part imaging motoru |
| AES-256-CBC (cryptography) | Yedek şifreleme |
| Rclone v1.73.2 | R2 cloud sync |
| Cloudflare R2 | Bulut depolama hedefi |
| MSSQL 2022 | .bak backup kaynağı |
| MariaDB | mysqldump kaynağı |
| SQLite WAL | backup_config, backup_history tabloları |
| Docker Engine | Container config backup |

---

## H2. RESTORE MANAGER

**URL:** `/restore-manager/` · **HTML:** ~240 satır · **API:** 5 endpoint + WebSocket · **Router:** `restore.py`

### 1. Amaç ve Detaylı Açıklama

Restore Manager, "The Time Machine" olarak adlandırılan, **yedeklerden sistem geri yükleme** aracıdır. Backup Center'ın oluşturduğu 5-Part imaging yedeklerini analiz ederek güvenli ve kontrollü bir şekilde geri yükleme imkanı sunar.

**Sayfa Bileşenleri:**
- **Zaman Çizelgesi (Timeline):** Yerel, SQL veya R2'deki tüm yedeklerin kronolojik listesi
- **Diff Analizi:** Mevcut sistem ile seçilen yedeğin 4 bölümlük karşılaştırması + 5 severity uyarı seviyesi
- **Dry-Run Simülasyon:** Gerçek restore öncesi "ne olacak?" simülasyonu
- **5-Part Restore Wizard:** Her part'ı ayrı ayrı veya toplu restore etme adımları
- **Yetki Kontrollü:** Master Admin → 5 part koşulsuz, Wizard → Part 1+4 (Recovery Key zorunlu)
- **Canlı İlerleme:** WebSocket ile restore işlemi ilerleme göstergesi

### 2. Kullanım ve Avantajlar

- **Time Machine:** Zaman çizelgesinde herhangi bir tarihe dönme
- **Diff Analysis:** Restore öncesi mevcut sistem ile farkları görme
- **Dry-Run:** Risk almadan "ne olacak?" simülasyonu
- **Kısmi Restore:** Sadece veritabanını veya sadece config'leri geri yükleme
- **Yetki Katmanlı:** Kritik restore işlemleri için Recovery Key zorunluluğu
- **Multi-Source:** Yerel dosya, SQL yedek veya R2 buluttan geri yükleme

### 3. Sistem İçindeki Rolü

Restore Manager, **felaket kurtarma stratejisinin tamamlayıcısı**dır. Backup Center'ın ikiz kardeşi — biri yaratır, diğeri geri yükler. Diff analysis sayesinde bilinçli restore kararı alınır. Dry-run özelliği operasyonel riski minimize eder.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Part 1 Restore | MSSQL RESTORE DATABASE + SQLite copy + MariaDB import |
| Part 2 Restore | core-api/ + web dosyaları tar extract |
| Part 3 Restore | Config dosyaları tar extract + service restart |
| Part 4 Restore | AI modüller + vault.enc restore |
| Part 5 Restore | docker-compose.yml restore + full stack restart |
| Diff Analysis | Dosya hash karşılaştırma + boyut/tarih farkları |
| Dry-Run | Simülasyon modu — gerçek değişiklik yapmadan analiz |
| Yetki | Master Admin: full access, Wizard: Part 1+4 with Recovery Key |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Timeline ve wizard UI |
| WebSocket | Restore ilerleme stream |
| Core API — restore.py | Restore endpoint'leri |
| restore_tool.py | Restore iş mantığı motoru |
| recovery_manager.py | Felaket kurtarma yöneticisi |
| Backup Center dosyaları | /opt/backup-center/local/ kaynak |
| Cloudflare R2 | Bulut yedek kaynağı |
| MSSQL 2022 | DB restore hedefi |
| MariaDB | Mail DB restore hedefi |

---


---

# I. TİCARET & ÖDEME

---

## I1. LICENSE HUB

**URL:** `/license/` · **HTML:** ~560 satır · **API:** 14 endpoint · **Router:** `license.py`

### 1. Amaç ve Detaylı Açıklama

License Hub, MEGA-STACK'in **RSA-4096 tabanlı dijital lisanslama sistemi**nin yönetim merkezidir. Lisans oluşturma, doğrulama, HWID kilitleme, tier yönetimi ve compliance denetimi işlemlerini tek panelden gerçekleştirir.

**Sayfa Bileşenleri:**
- **Aktif Lisanslar Tablosu:** Tüm verilmiş lisansların listesi — müşteri, tier, HWID, başlangıç/bitiş tarihi, durum
- **Lisans Oluşturma Wizard:** Müşteri bilgileri, tier seçimi, süre, HWID kilidi ayarları
- **Tier Matrisi:** Standart (15 servis) / Professional (23) / Enterprise (25) karşılaştırma tablosu
- **HWID Doğrulama:** Canvas fingerprint + navigator tabanlı donanım kimliği eşleştirme (fuzzy match)
- **Compliance Engine:** 30 dakikada bir otomatik lisans ihlali taraması sonuçları
- **RSA İmza Detayı:** Lisans dijital imza bilgileri ve doğrulama durumu

### 2. Kullanım ve Avantajlar

- **RSA-4096 Güvenlik:** Kırılamayan dijital imza ile lisans sahteciliği önleme
- **HWID Kilitleme:** Lisansın yalnızca hedef donanımda çalışmasını sağlama
- **Fuzzy Match:** Küçük donanım değişikliklerinde (RAM ekleme vs.) lisansın geçersizleşmemesi
- **Tier Yönetimi:** 3 kademeli servis erişim kontrolü
- **Compliance Otomasyonu:** İhlalleri otomatik tespit ve bildirim
- **Online + Offline:** api.mydomain.com üzerinden online doğrulama + yerel cache

### 3. Sistem İçindeki Rolü

License Hub, **ticari katmanın temel taşı**dır. Tüm Product Wizard kurulumları burada oluşturulan lisanslarla çalışır. Tier gating sistemi lisans bilgisine göre dashboard sayfalarını ve servisleri etkinleştirir/devre dışı bırakır. Compliance engine sürekli denetim yapar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Lisans CRUD | system_licenses tablosunda RSA-4096 imzalı kayıt |
| Tier Yönetimi | license_tiers, tier_permissions, tier_feature_levels tabloları |
| HWID | Canvas + navigator fingerprint → SHA-256 hash |
| Compliance | 30dk cron → lisans ihlali tarama → compliance_violations |
| İmzalama | RSA-4096 + PSS + MGF1 + SHA-256 |
| Online Doğrulama | public_api.py → /verify endpoint |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Tablo, wizard, modal UI |
| Core API — license.py | 14 lisans yönetim endpoint'i |
| license_tool.py | RSA-4096 imzalama utility |
| Core API — public_api.py | Online doğrulama endpoint |
| cryptography (RSA) | RSA-4096 PSS dijital imza |
| SQLite WAL | system_licenses, license_tiers, tier_permissions, compliance_violations tabloları |

---

## I2. PAYMENT

**URL:** `/payment/` · **HTML:** ~700 satır · **API:** 13 endpoint · **Router:** `payment.py`, `payment_admin.py`

### 1. Amaç ve Detaylı Açıklama

Payment sayfası, MEGA-STACK'in **kripto para ve kredi kartı ödeme sistemi**nin yönetim merkezidir. 4 ödeme gateway'i arasında SmartRouter ile otomatik yönlendirme yapan, anti-fraud korumalı, KVKK uyumlu bir ödeme altyapısı sunar.

**Sayfa Bileşenleri (6 Sekme):**
- **Genel Bakış:** Ödeme istatistikleri — toplam gelir, işlem sayısı, gateway dağılımı
- **İşlem Geçmişi:** Tüm ödeme işlemlerinin detaylı listesi
- **Gateway Yönetimi:** 4 gateway (NOWPayments, BTCPay, MoonPay, Transak) konfigürasyonu ve sağlık durumu
- **Plan Yönetimi:** Standart/Professional/Enterprise fiyatlandırma ve plan detayları
- **Anti-Fraud:** IP blacklist, başarısız deneme sayacı (5 → 60dk ban), şüpheli işlem listesi
- **KVKK Uyumluluk:** IP/browser log 30 gün sonra otomatik silme ayarları

### 2. Kullanım ve Avantajlar

- **SmartRouter:** 4 gateway arasında otomatik yönlendirme ve failover
- **Kripto + Kart:** BTC, ETH, USDT, USDC + kredi kartı desteği
- **Anti-Fraud:** Otomatik saldırı tespiti ve IP engelleme
- **KVKK Uyumlu:** Kişisel veri 30 gün sonra otomatik temizleme
- **PCI-DSS:** Kart bilgisi saklanmaz — gateway'e yönlendirme
- **Price Lock:** Kripto volatilitesi için 15 dakika fiyat sabitleme
- **Web3 Wallet:** WalletConnect ile kripto cüzdan bağlantısı

### 3. Sistem İçindeki Rolü

Payment, **gelir yönetimi ve ticari dönüşüm** katmanıdır. License Hub'da oluşturulan planların satış ve ödeme alma noktasıdır. Başarılı ödeme sonrası ilgili tier lisansı otomatik aktivasyon yapar. Product UI Manager ile entegre çalışır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| SmartRouter | Gateway sağlık kontrolü → öncelik sırasına göre yönlendirme |
| NOWPayments | REST API entegrasyonu — kripto + kart |
| BTCPay Server | Self-hosted kripto ödeme gateway |
| MoonPay / Transak | KYC uyumlu kart ödeme gateway'leri |
| Anti-Fraud | IP blacklist + max 5 fail → 60dk ban |
| KVKK Cleanup | 30 gün retention → otomatik IP/browser log silme |
| Webhook | HMAC + IP whitelist doğrulama |
| Plan Aktivasyon | Ödeme başarılı → tier lisans otomatik aktif |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | 6 sekmeli tab + modal UI |
| Chart.js 4.x | Gelir ve işlem grafikleri |
| Web3.js / WalletConnect | Kripto cüzdan bağlantısı |
| Core API — payment.py | Ödeme işlem endpoint'leri |
| Core API — payment_admin.py | Gateway yönetim endpoint'leri |
| payment_engine.py | SmartRouter + gateway entegrasyonu |
| payment_db.py | Ödeme veritabanı yönetimi |
| payment_config.py | Gateway konfigürasyonu |
| NOWPayments API | Birincil ödeme gateway |
| BTCPay Server API | Yedek kripto gateway |
| SQLite WAL | Ödeme tabloları |

---

## I3. PRODUCT UI

**URL:** `/product-ui/` · **HTML:** ~550 satır · **API:** 3 endpoint · **Router:** `product_ui.py`

### 1. Amaç ve Detaylı Açıklama

Product UI Manager, dashboard'daki **servis ve özelliklerin görünürlük kontrolü**nü sağlayan sayfadır. Lisans tier'ına göre hangi dashboard sayfaları ve servislerin kullanıcıya gösterileceğini yapılandırır.

**Sayfa Bileşenleri:**
- **Feature Toggle Grid:** Tüm servislerin açma/kapama switch'leri ile listesi
- **Core Protection:** Kritik servislerin (traefik, nginx, core-api, redis) kapatılamaz olarak işaretlenmesi
- **Tier-Aware Gösterge:** Her servisin hangi tier'da mevcut olduğu (Standart/Pro/Enterprise)
- **Upgrade Mesajı:** Devre dışı servislere tıklandığında üst tier'a yükseltme önerisi

### 2. Kullanım ve Avantajlar

- **Ticari Kontrol:** Lisans seviyesine göre özellik kısıtlama
- **Core Protection:** Kritik servislerin yanlışlıkla gizlenmesini önleme
- **Upgrade Teşviki:** Devre dışı özellikler için doğal upsell mekanizması
- **Görsel Yönetim:** Switch toggle ile hızlı açma/kapama

### 3. Sistem İçindeki Rolü

Product UI, **ticari katmanın görünürlük kontrol mekanizması**dır. License Hub'dan gelen tier bilgisini alır ve product_feature_configs tablosundaki veriye göre dashboard öğelerini gösterir/gizler. Her sayfa yüklendiğinde mega-stack-ui.js bu bilgiyi kontrol eder.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Feature Visibility | product_feature_configs tablosu CRUD |
| Core Protection | Hardcoded core servis listesi |
| Tier Mapping | tier_feature_levels ile eşleştirme |
| UI Gating | mega-stack-ui.js → verify_license |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Toggle switch grid |
| Core API — product_ui.py | Feature config endpoint'leri |
| License Hub | Tier bilgisi kaynağı |
| mega-stack-ui.js | Client-side gating kontrolü |
| SQLite WAL | product_feature_configs, tier_feature_levels tabloları |

---

## I4. RELEASE MANAGER

**URL:** `/release-manager/` · **HTML:** ~380 satır · **API:** 7 endpoint + WebSocket · **Router:** `release.py`

### 1. Amaç ve Detaylı Açıklama

Release Manager, MEGA-STACK **güncelleme paketlerinin oluşturma, imzalama, dağıtma ve tier promosyon** sistemidir. .v12p formatındaki güncelleme paketlerini RSA dijital imza ile mühürleyerek alpha → beta → stable promosyon zincirinde yönetir.

**Sayfa Bileşenleri:**
- **Release Listesi:** Tüm sürümlerin tablosu — versiyon, kanal (alpha/beta/stable), tarih, boyut, imza durumu
- **Yeni Release Oluşturma:** Paket oluşturma wizard — dosya seçimi, versiyon numarası, changelog
- **RSA İmzalama:** Paketin dijital imza ile mühürlenmesi
- **Tier Promosyon:** Alpha → Beta → Stable promosyon butonları
- **Rollback:** Önceki versiyona geri dönme
- **WebSocket Signals:** Güncelleme sinyallerinin canlı yayını

### 2. Kullanım ve Avantajlar

- **Dijital İmza:** RSA ile güncellemelerin bütünlüğü garanti altında
- **Kanal Sistemi:** Alpha (test) → Beta (sınırlı) → Stable (genel) aşamalı dağıtım
- **Rollback:** Sorunlu güncellemeyi anında geri alma
- **Changelog:** Her sürümün değişiklik notları
- **WebSocket Signal:** Bağlı sistemlere güncelleme bildirimi

### 3. Sistem İçindeki Rolü

Release Manager, **yazılım dağıtım zincirinin kontrolcüsü**dür. Product Wizard ile kurulan müşteri sistemlerine güncelleme dağıtır. Versions sayfası bu release'lerin kaydını tutar. Watchtower container image güncellemelerini, Release Manager ise uygulama seviyesi güncellemeleri yönetir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Release CRUD | releases tablosunda versiyon kayıt |
| RSA İmzalama | RSA-4096 PSS ile paket imzalama |
| Tier Promosyon | channel alanı: alpha → beta → stable geçişi |
| Rollback | Önceki release'e version pin |
| Signal | update_signals tablosuna sinyal yazma + WebSocket broadcast |
| .v12p Paket | Custom paket formatı oluşturma |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Release tablosu ve wizard UI |
| WebSocket | Güncelleme sinyal yayını |
| Core API — release.py | Release yönetim endpoint'leri |
| release_tool.py | Paket oluşturma ve imzalama utility |
| cryptography (RSA) | RSA-4096 dijital imza |
| SQLite WAL | releases, update_history, update_signals tabloları |
| Watchtower 1.7.1 | Docker image güncelleme (tamamlayıcı) |

---


---

# J. DOSYA & BİLGİ YÖNETİMİ

---

## J1. FILE MANAGER

**URL:** `/files/` · **HTML:** ~420 satır · **API:** 8 endpoint · **Router:** `files.py`

### 1. Amaç ve Detaylı Açıklama

File Manager, sunucu dosya sisteminin **web tabanlı görsel yönetim** aracıdır. Nginx web root dizini altındaki dosyaların listelenmesi, düzenlenmesi, yüklenmesi ve silinmesi işlemlerini çift panelli bir arayüzle sunar.

**Sayfa Bileşenleri:**
- **Dual-Pane Layout:** Soldaki dosya gezgini + sağdaki editör/önizleme paneli
- **Monaco Editor Entegrasyonu:** Metin dosyalarını sözdizimi renklendirmeli düzenleme
- **Dosya Yükleme:** 50 MB'a kadar dosya yükleme — drag & drop destekli
- **Resim Önizleme:** jpg/png/gif/svg dosyalarının doğrudan önizlemesi
- **Klasör Navigasyonu:** Ağaç yapısında dizin gezinme
- **Dosya İşlemleri:** Oluşturma, düzenleme, silme, taşıma, kopyalama
- **İndirme:** Tekli dosya indirme

### 2. Kullanım ve Avantajlar

- **SSH'sız Dosya Erişimi:** Terminal bilgisi gerektirmeden dosya yönetimi
- **Profesyonel Editör:** Monaco Editor ile profesyonel kod düzenleme deneyimi
- **Görsel Önizleme:** Resim dosyalarını indirmeden önizleme
- **50MB Yükleme:** Büyük dosyalar için yeterli kapasite
- **Dual-Pane:** Dosya listesi ve editör yan yana — verimli çalışma

### 3. Sistem İçindeki Rolü

File Manager, **web içeriği ve konfigürasyon dosyalarının doğrudan yönetim noktası**dır. Nginx container'ın servis ettiği statik dosyalara erişim sağlar. Mega-Editor'den farklı olarak daha basit, dosya odaklı bir arayüz sunar. Domain Management ile eklenen sitelerin dosyalarını buradan yönetmek mümkündür.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Dosya CRUD | os.path tabanlı dosya sistemi işlemleri |
| Path Koruması | os.path.realpath ile path traversal engelleme |
| Yükleme | multipart upload → 50MB limit |
| Düzenleme | Monaco Editor → API PUT → dosyaya yazma |
| Önizleme | MIME type algılama → inline render |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Monaco Editor 0.45.0 | Dosya düzenleme editörü |
| Bootstrap 5.3.3 | Dual-pane layout |
| Core API — files.py | Dosya CRUD endpoint'leri |
| Nginx 1.29-alpine | Web root dizini kaynak |
| Path traversal koruması | os.path.realpath sandboxing |

---

## J2. MEGA-EDITOR

**URL:** `/editor/` · **HTML:** ~380 satır · **API:** 10 endpoint · **Router:** `files.py` (paylaşımlı)

### 1. Amaç ve Detaylı Açıklama

Mega-Editor, **Monaco Editor 0.45.0 tabanlı tam özellikli web IDE**sidir. File Manager'ın basit editöründen farklı olarak gelişmiş özellikler sunar: Redis file lock, snapshot/diff, çoklu sekme, arama-değiştirme ve sözdizimi desteği.

**Sayfa Bileşenleri:**
- **Monaco Editor 0.45.0:** VS Code editör motoru — IntelliSense, bracket matching, minimap, multi-cursor
- **Redis File Lock:** Eş zamanlı düzenleme önlemi — dosya düzenlenirken kilitlenir
- **Snapshot Kaydetme:** Dosyanın anlık durumunun snapshot olarak saklanması
- **Diff Viewer:** İki snapshot veya mevcut dosya ile snapshot arasında fark görüntüleme
- **Sözdizimi Desteği:** HTML, CSS, JS, Python, JSON, YAML, Markdown, SQL ve daha fazlası
- **Arama-Değiştirme:** Regex destekli arama ve toplu değiştirme
- **Dosya Ağacı:** Sol panelde navigasyon ağacı

### 2. Kullanım ve Avantajlar

- **VS Code Deneyimi:** Web tarayıcısında VS Code kalitesinde kod düzenleme
- **File Lock:** İki kullanıcının aynı dosyayı bozmasını önleme
- **Snapshot:** Deneysel değişiklikler öncesi güvenli kayıt noktası
- **Diff:** Değişiklikleri karşılaştırma — ne değişti görebilme
- **Çok Dil Desteği:** 20+ programlama dili sözdizimi desteği

### 3. Sistem İçindeki Rolü

Mega-Editor, **geliştirme deneyiminin en gelişmiş aracı**dır. File Manager basit dosya işlemleri için, Mega-Editor ise profesyonel kod düzenleme için kullanılır. Redis file lock sayesinde çok kullanıcılı ortamlarda çakışma önlenir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Dosya Düzenleme | Monaco Editor → API → dosya sistemi |
| File Lock | Redis SET NX → kilit al/bırak |
| Snapshot | Dosya içeriğinin zaman damgalı kopyası |
| Diff | İki metin arasında satır satır fark analizi |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Monaco Editor 0.45.0 | Ana editör motoru |
| Bootstrap 5.3.3 | Layout ve toolbar |
| Core API — files.py | Dosya CRUD + snapshot endpoint'leri |
| Redis 7-alpine | File lock mekanizması |
| Nginx 1.29-alpine | Dosya kaynağı dizini |

---

## J3. STACK MEMORY

**URL:** `/stack-memory/` · **HTML:** ~250 satır · **API:** 7 endpoint · **Router:** `memory.py`

### 1. Amaç ve Detaylı Açıklama

Stack Memory, MEGA-STACK'in **bilgi deposu ve sistem dokümantasyon editörü**dür. `/opt/stack-memory/` dizinindeki Markdown dosyalarını split-view editör ile yönetir. Sistem raporları, mimari dokümanlar, versiyon notları ve operational loglar burada tutulur.

**Sayfa Bileşenleri:**
- **Dosya Listesi:** /opt/stack-memory/ altındaki tüm .md dosyalarının listesi
- **Split-View Editör:** Sol taraf raw Markdown, sağ taraf canlı HTML önizleme
- **Prism.js Syntax Highlighting:** Kod bloklarının renkli gösterimi
- **Snapshot Kaydetme:** Dosyanın belirli bir anının korunması
- **3 Sync Modu:** Otomatik kayıt, manuel kayıt, salt okuma
- **Dosya CRUD:** Yeni .md dosya oluşturma, düzenleme, silme

### 2. Kullanım ve Avantajlar

- **Split-View:** Yazarken önizlemeyi anında görme — verimli dokümantasyon
- **Merkezi Bilgi Deposu:** Tüm sistem dokümanları tek yerde
- **Snapshot:** Doküman versiyonlama — önceki haline dönme
- **Markdown:** Zengin metin formatı — tablo, kod, başlık, liste desteği
- **Syntax Highlighting:** Kod örneklerinin okunabilir gösterimi

### 3. Sistem İçindeki Rolü

Stack Memory, sistemin **tek doğruluk kaynağı (Single Source of Truth)** olan `/opt/stack-memory/` dizininin yönetim arayüzüdür. SYSTEM_BLUEPRINT.md (AI bağlam dosyası), system-core-report.md, mimari dokümanlar ve operasyonel loglar burada saklanır ve düzenlenir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| .md Dosya CRUD | /opt/stack-memory/ dizininde oluşturma/okuma/güncelleme/silme |
| Markdown Render | Marked.js ile HTML dönüşümü |
| Snapshot | Dosya içeriğinin zaman damgalı kopyası |
| Sync Modları | auto-save (5s), manual, read-only |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Marked.js | Markdown → HTML render |
| Prism.js 1.29.0 | Kod bloğu syntax highlighting |
| Bootstrap 5.3.3 | Split-view layout |
| Core API — memory.py | Memory dosya CRUD endpoint'leri |
| /opt/stack-memory/ | Dosya depolama dizini |

---

## J4. DOCUMENTATIONS

**URL:** `/documentations/` · **HTML:** ~240 satır · **API:** 8 endpoint · **Router:** `docs.py`

### 1. Amaç ve Detaylı Açıklama

Documentations, MEGA-STACK'in **dahili wiki ve teknik dokümantasyon** sistemidir. Ağaç yapısında organize edilmiş 68+ dokümantasyon sayfasını yönetir. Tree-view navigasyon, Markdown içerik, PDF export ve arama özellikleri sunar.

**Sayfa Bileşenleri:**
- **Tree-View Navigasyon:** Sol panelde hiyerarşik ağaç yapısı — kategori > alt kategori > doküman
- **Doküman Editörü:** Markdown editör ile doküman oluşturma/düzenleme
- **Prism.js Renklendirme:** Kod örneklerinde sözdizimi vurgulaması
- **PDF Export:** html2pdf.js ile dokümanın PDF olarak indirilmesi
- **Arama:** Tüm dokümanlarda tam metin arama
- **Doküman CRUD:** Oluşturma, düzenleme, silme, taşıma

### 2. Kullanım ve Avantajlar

- **Dahili Wiki:** Harici wiki aracına gerek kalmadan sistem içi dokümantasyon
- **Tree-View:** Hiyerarşik navigasyon ile organize doküman erişimi
- **PDF Export:** Dokümanları paylaşılabilir PDF olarak indirme
- **68+ Doküman:** Geniş bilgi tabanı — kurulum, yapılandırma, sorun giderme kılavuzları
- **Tam Metin Arama:** İhtiyaç duyulan bilgiyi hızla bulma

### 3. Sistem İçindeki Rolü

Documentations, **bilgi yönetimi katmanının yapılandırılmış arayüzü**dür. Stack Memory serbest format Markdown dosyaları tutarken, Documentations yapılandırılmış wiki tarzı dokümanları yönetir. system_documentation tablosunda 68+ kayıt ile zengin bir bilgi tabanı oluşturur.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Doküman CRUD | system_documentation tablosunda CRUD |
| Hiyerarşi | parent_id ile ağaç yapısı |
| PDF Export | html2pdf.js ile istemci taraflı PDF oluşturma |
| Arama | LIKE sorgusu ile tam metin arama |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Prism.js 1.29.0 | Kod bloğu syntax highlighting |
| Marked.js | Markdown → HTML render |
| html2pdf.js | PDF export |
| Bootstrap 5.3.3 | Tree-view + editör layout |
| Core API — docs.py | Dokümantasyon CRUD endpoint'leri |
| wiki_engine.py | Wiki iş mantığı motoru |
| SQLite WAL | system_documentation tablosu |

---


---

# K. DESTEK & UI

---

## K1. TICKETS

**URL:** `/tickets/` · **HTML:** ~600 satır · **API:** 11 endpoint · **Router:** (tickets endpoints in admin/system routers)

### 1. Amaç ve Detaylı Açıklama

Tickets, MEGA-STACK'in **müşteri destek bilet sistemi**dir. Bubble chat arayüzü ile sohbet tarzı destek deneyimi, SLA zamanlayıcı, deflection wizard (self-service yönlendirme) ve hazır yanıt şablonları sunar.

**Sayfa Bileşenleri:**
- **Bilet Listesi:** Tüm destek biletlerinin durumuna göre filtrelenebilir tablosu (açık/beklemede/çözüldü/kapatıldı)
- **Bubble Chat Arayüzü:** Messenger tarzı sohbet baloncukları ile bilet yazışmaları
- **SLA Timer:** Bilet önceliğine göre geri sayım sayacı — yanıt süresi hedefi
- **Deflection Wizard:** Bilet açmadan önce self-service çözüm önerileri — ilgili doküman yönlendirmesi
- **Canned Responses:** Hazır yanıt şablonları — sık sorulan sorulara hızlı yanıt
- **Öncelik Seviyeleri:** Düşük / Normal / Yüksek / Acil — renk kodlu
- **Durum Akışı:** Açık → Beklemede → Çözüldü → Kapatıldı

### 2. Kullanım ve Avantajlar

- **Chat UX:** Geleneksel bilet sistemi yerine modern sohbet deneyimi
- **SLA Takibi:** Yanıt süresi hedeflerinin otomatik izlenmesi
- **Deflection:** Bilet hacmini azaltan akıllı self-service yönlendirme
- **Canned Responses:** Tekrarlayan sorulara saniyeler içinde yanıt
- **Öncelik Sistemi:** Acil biletlerin görsel vurgusu

### 3. Sistem İçindeki Rolü

Tickets, **müşteri destek katmanının birincil aracı**dır. Product Wizard ile dağıtılan müşteri sistemlerinden gelen destek taleplerini yönetir. Deflection wizard, Documentations sayfasındaki ilgili dokümanlara yönlendirir. Canned responses admin tarafından özelleştirilebilir.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Bilet CRUD | tickets tablosunda oluşturma/güncelleme/kapatma |
| Yanıtlar | ticket_replies tablosunda sohbet geçmişi |
| Canned Responses | canned_responses tablosunda şablon CRUD |
| SLA Timer | Bilet önceliğine göre hedef süre hesaplama |
| Deflection | Anahtar kelime → doküman eşleştirme |
| Durum Akışı | status enum: open → pending → resolved → closed |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Chat baloncukları ve tablo UI |
| Core API endpoints | Bilet CRUD + yanıt endpoint'leri (11 endpoint) |
| SQLite WAL | tickets, ticket_replies, canned_responses tabloları |
| Documentations | Deflection wizard'ın yönlendirme hedefi |

---

## K2. UISETTING

**URL:** `/UISetting/` · **HTML:** ~1150 satır · **API:** 1 batch PUT endpoint · **Router:** `system.py`

### 1. Amaç ve Detaylı Açıklama

UISetting, MEGA-STACK dashboard'unun **görsel kimlik ve tema yönetim** merkezidir. 40+ CSS token'ını, 13 katmanlı glassmorphism efektlerini, logo, favicon, renk şemaları ve tipografiyi tek sayfadan canlı önizleme ile yönetir. ~1150 HTML satırıyla en büyük sayfalardan biridir.

**Sayfa Bileşenleri:**
- **Renk Paletleri:** Primary, secondary, accent, success, warning, danger renkleri — color picker ile seçim
- **Glassmorphism Kontrolleri:** 13 katmanlı şeffaflık, blur, border, shadow ayarları — slider ile hassas kontrol
- **Logo Yükleme:** Navbar logo + favicon yükleme ve önizleme
- **Tipografi:** Font ailesi, boyut, ağırlık, satır aralığı ayarları
- **Canlı Önizleme:** Tüm değişiklikler kaydedilmeden önce dashboard üzerinde anlık önizleme
- **Tema Kaydetme:** Tüm ayarların tek batch PUT ile kaydedilmesi
- **CSS Token Listesi:** 40+ root CSS değişkeninin yönetimi
- **Brand Settings:** Marka adı, slogan, copyright metni

### 2. Kullanım ve Avantajlar

- **White-Label:** Müşteriye özel marka kimliği oluşturma
- **Canlı Önizleme:** Değişiklikleri kaydetmeden test etme
- **40+ CSS Token:** Detaylı görsel özelleştirme
- **Glassmorphism:** Modern cam efekti arayüz tasarımı
- **Logo + Favicon:** Marka varlıklarının kolay yönetimi
- **Tek Batch Kayıt:** Tüm ayarlar tek seferde kaydedilir — tutarsızlık yok

### 3. Sistem İçindeki Rolü

UISetting, **marka ve görsel kimlik katmanı**dır. Burada ayarlanan CSS token'ları `brand-variables.css` dosyasına yazılır ve tüm 34 sayfada otomatik olarak uygulanır. MegaBranding (mega-stack-ui.js) modülü bu ayarları yükler. Product UI Manager ile entegre çalışır.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| CSS Token'ları | brand_settings tablosu + brand-variables.css |
| Glassmorphism | 13 katmanlı CSS değişken seti |
| Logo/Favicon | brand_assets tablosu + dosya yükleme |
| Tipografi | Font ailesi ve boyut CSS token'ları |
| Tema Kayıt | Tek batch PUT → DB + CSS dosya güncellemesi |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Form kontrolleri ve slider'lar |
| Native Color Picker | Renk seçimi |
| Core API — system.py | Tema batch PUT endpoint |
| brand-variables.css | CSS token çıktı dosyası |
| mega-stack-ui.js | MegaBranding modülü — tema yükleyici |
| SQLite WAL | brand_settings, brand_assets, theme_presets tabloları |

---

## K3. COMPONENTS

**URL:** `/components/` · **HTML:** ~240 satır · **API:** 8 endpoint · **Router:** `components.py`

### 1. Amaç ve Detaylı Açıklama

Components, MEGA-STACK'in **89 kayıtlı bileşeninin katalog ve bağımlılık yönetim** sayfasıdır. Tüm sistem bileşenlerinin envanterini, durumunu, bağımlılık grafiğini ve versiyon bilgilerini sunar.

**Sayfa Bileşenleri:**
- **Bileşen Tablosu:** 89 bileşenin listesi — ad, kategori, versiyon, durum, bağımlılık sayısı
- **Canvas Bağımlılık Grafiği:** Bileşenler arası bağımlılıkların interaktif görselleştirmesi
- **Bileşen Detay Modal:** Seçili bileşenin detayları — açıklama, changelog, bağımlılıklar
- **Kategori Filtresi:** Backend, frontend, infrastructure, security vb. kategorilerde filtreleme
- **Bileşen CRUD:** Yeni bileşen kayıt, güncelleme, silme

### 2. Kullanım ve Avantajlar

- **Sistem Envanteri:** Tüm bileşenlerin tek noktadan görüntülenmesi
- **Bağımlılık Görselleştirme:** Canvas grafik ile hangi bileşenin hangisine bağımlı olduğu
- **Versiyon Takibi:** Her bileşenin versiyon geçmişi
- **Kategorizasyon:** 89 bileşeni mantıksal gruplara ayırma

### 3. Sistem İçindeki Rolü

Components, **sistem mimarisinin envanter katmanı**dır. Versions sayfası ile tamamlayıcı çalışır — Versions zaman bazlı değişiklikleri, Components yapı bazlı envanteri tutar. system_components tablosunda 89 kayıt ile sistemin tüm parçalarının kaydını tutar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Bileşen CRUD | system_components tablosunda CRUD |
| Bağımlılık Grafiği | Canvas API ile force-directed graph çizimi |
| Kategori | category alanı ile gruplama |
| Versiyon | version alanı ile takip |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Canvas API | Bağımlılık grafiği çizimi |
| Bootstrap 5.3.3 | Tablo ve modal UI |
| Core API — components.py | Bileşen CRUD endpoint'leri |
| SQLite WAL | system_components tablosu |

---

## K4. VERSIONS

**URL:** `/versions/` · **HTML:** ~540 satır · **API:** 7 endpoint · **Router:** `components.py` (paylaşımlı)

### 1. Amaç ve Detaylı Açıklama

Versions, MEGA-STACK'in **versiyon geçmişi, changelog yönetimi ve bileşen takip** sayfasıdır. Sistemin v1.0'dan v5.3'e kadar olan evrimini 3 sekmede sunar.

**Sayfa Bileşenleri (3 Sekme):**
- **Timeline Sekmesi:** Versiyon zaman çizelgesi — her major ve minor sürümün tarihi, açıklaması ve değişiklikleri (21 major versiyon)
- **Components Sekmesi:** Bileşen versiyon takibi — her bileşenin hangi versiyonda eklendiği/güncellendiği
- **Docs Sekmesi:** Versiyon dokümantasyonu — her sürümün detaylı changelog'u

### 2. Kullanım ve Avantajlar

- **Sistem Hafızası:** Tüm değişikliklerin kronolojik kaydı
- **Timeline:** Görsel zaman çizelgesi ile evrim takibi
- **Changelog:** Her sürümde ne değiştiğinin detaylı kaydı
- **Bileşen Evrimi:** Hangi bileşenin ne zaman eklendiği/güncellendiği

### 3. Sistem İçindeki Rolü

Versions, **sistem evriminin tarihçe katmanı**dır. Release Manager ile tamamlayıcı çalışır — Release Manager aktif dağıtımı, Versions geçmişi yönetir. system_versions tablosunda 21 major versiyon kaydı ile sistemin tam evrim hikayesini tutar.

### 4. Yönettiği Sistem ve Yönetim Mantığı

| Yönetilen Alan | Yönetim Mantığı |
|----------------|-----------------|
| Versiyon CRUD | system_versions tablosunda değişiklik kaydı |
| Timeline | created_at sıralı versiyon listesi |
| Changelog | Her versiyona ait detaylı değişiklik notu |
| Bileşen Takibi | system_components.version ile eşleştirme |

### 5. Beslendiği Teknoloji ve Servisler

| Teknoloji/Servis | Kullanım |
|------------------|----------|
| Bootstrap 5.3.3 | Timeline ve 3 sekmeli tab UI |
| Core API — components.py | Versiyon ve bileşen endpoint'leri |
| SQLite WAL | system_versions, system_components tabloları |

---


---

# L. ÖZET & REFERANS

---

## L1. SAYFA-KONTEYNER MATRİSİ

Her dashboard sayfasının etkileştiği Docker konteynerler:

| Sayfa | Core API | Nginx | MSSQL | MariaDB | Redis | Traefik | CrowdSec | Authelia | iRedMail | Netdata | Docker Engine | cert-dumper |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Ana Dashboard | ✅ | — | — | — | ✅ | — | — | — | — | ✅ | ✅ | — |
| Admin Overview | ✅ | — | — | — | — | — | — | — | — | ✅ | ✅ | — |
| Domain Management | ✅ | ✅ | — | — | — | ✅ | — | — | — | — | — | ✅ |
| User Manager | ✅ | — | — | — | ✅ | — | — | ✅ | — | — | — | — |
| Nav Menu | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Guardian | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — |
| Defense Hub | ✅ | — | — | — | — | ✅ | ✅ | — | — | — | — | — |
| PassHub | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — |
| Certificates Watch | ✅ | — | — | — | — | ✅ | — | — | — | — | — | ✅ |
| Login | ✅ | — | — | — | ✅ | — | — | ✅ | — | — | — | — |
| Data Studio | ✅ | — | ✅ | ✅ | — | — | — | — | — | — | — | — |
| SQL Runner | ✅ | — | ✅ | ✅ | — | — | — | — | — | — | — | — |
| Migration Hub | ✅ | — | ✅ | — | — | — | — | — | — | — | — | — |
| AI Studio | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| STACK-AI | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Health Check | ✅ | — | ✅ | ✅ | ✅ | — | — | — | — | ✅ | ✅ | — |
| Log Center | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — |
| Analytics | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Motor Dairesi | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — |
| Mail Center | ✅ | — | — | ✅ | — | — | — | — | ✅ | — | ✅ | — |
| Backup Center | ✅ | — | ✅ | ✅ | — | — | — | — | — | — | ✅ | — |
| Restore Manager | ✅ | — | ✅ | ✅ | — | — | — | — | — | — | — | — |
| License Hub | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Payment | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Product UI | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Release Manager | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| File Manager | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — |
| Mega-Editor | ✅ | ✅ | — | — | ✅ | — | — | — | — | — | — | — |
| Stack Memory | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Documentations | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Tickets | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| UISetting | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Components | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Versions | ✅ | — | — | — | — | — | — | — | — | — | — | — |

> **Not:** Tüm sayfalar Core API (domain-api-v12) container'ı üzerinden çalışır. "Docker Engine" sütunu Docker socket üzerinden container yönetimi yapan sayfaları gösterir.

---

## L2. TEKNOLOJİ REFERANS TABLOSU

### Frontend Kütüphaneleri ve Kullanım Dağılımı

| Teknoloji | Versiyon | Kullanan Sayfa Sayısı | Temel Kullanım |
|-----------|----------|:---:|----------------|
| Bootstrap | 5.3.3 | 34 | CSS framework — tüm sayfalar |
| Chart.js | 4.x | 8 | Gauge, bar, line, doughnut grafik |
| Monaco Editor | 0.45.0 | 2 | Kod editörü (Files, Editor) |
| xterm.js | Latest | 2 | Terminal (Containers, Migration) |
| Leaflet.js | 1.9.4 | 2 | Harita (Dashboard, Defense) |
| Ace Editor | 1.36.5 | 1 | SQL editörü (Data Studio) |
| Marked.js | Latest | 3 | Markdown render (STACK-AI, Memory, Docs) |
| Prism.js | 1.29.0 | 3 | Syntax highlighting (Docs, Memory, SQL Runner) |
| SweetAlert2 | Latest | 8+ | Onay diyalogları |
| html2pdf.js | Latest | 1 | PDF export (Docs) |
| SheetJS | Latest | 1 | XLSX export (Data Studio) |
| jsPDF | Latest | 1 | PDF oluşturma (Data Studio) |
| Canvas API | Native | 2 | Login animation, Components graph |
| WebSocket | Native | 7+ | Canlı veri akışı |
| Web3.js / WalletConnect | Latest | 1 | Kripto cüzdan (Payment) |

### Paylaşılan Frontend Modülleri

| Modül | Satır | Kullanım |
|-------|:---:|----------|
| mega-stack-ui.js | 500+ | MegaAuth, MegaBranding, MegaHealth — tüm sayfalar |
| mega-nav-partial.js | 400+ | Navbar injector — tüm sayfalar |
| main-ws-manager.js | 300+ | WebSocket singleton — WS kullanan sayfalar |
| api-client.js | 178 | Merkezi fetch wrapper (`window.API`) — tüm sayfalar |
| mega-stack-notify.js | 451 | Toast + bildirim zili — tüm sayfalar |
| security-gate.js | 200+ | Auth guard — tüm sayfalar (login hariç) |
| ui-manager.js | 200+ | Confirm/modal utils — çoğu sayfa |
| btn-loader.js | 100 | Button loading — form bulunan sayfalar |
| dom-protection.js | 100 | XSS koruma — tüm sayfalar |
| brand-variables.css | 200+ | CSS root variables — tüm sayfalar |
| mega-stack-global.css | 300+ | Global CSS — tüm sayfalar |

---

## L3. API ENDPOINT DAĞILIM ÖZETİ

| Router Dosyası | Sayfa | Endpoint Sayısı | Temel HTTP Metodları |
|----------------|-------|:---:|------|
| mail_pro.py | Mail Center | 53 | GET, POST, PUT, DELETE |
| ai.py | AI Studio + STACK-AI | 18+ | GET, POST, PUT, DELETE |
| user.py + user_admin.py | User Manager | 16 | GET, POST, PUT, DELETE |
| admin.py + ops.py | Motor Dairesi + Admin | 14+ | GET, POST |
| license.py | License Hub | 14 | GET, POST, PUT, DELETE |
| payment.py + payment_admin.py | Payment | 13 | GET, POST, PUT |
| data_studio.py | Data Studio | 11 | GET, POST |
| backup.py | Backup Center | 10+ | GET, POST |
| files.py | File Manager + Editor | 10 | GET, POST, PUT, DELETE |
| navigation.py | Nav Menu | 9 | GET, POST, PUT, DELETE |
| guardian.py | Guardian | 8 | GET, POST, PUT |
| docs.py | Documentations | 8 | GET, POST, PUT, DELETE |
| logs.py | Log Center | 8 | GET, POST, DELETE |
| health.py | Health Check | 8 | GET, POST |
| components.py | Components + Versions | 8+7 | GET, POST, PUT, DELETE |
| migration.py | Migration Hub | 7 | GET, POST |
| release.py | Release Manager | 7 | GET, POST, PUT |
| memory.py | Stack Memory | 7 | GET, POST, PUT, DELETE |
| domains.py | Domain Management | 6 | GET, POST, PUT, DELETE |
| defense.py | Defense Hub | 6 | GET, POST |
| sql.py | SQL Runner | 6 | GET, POST |
| certs.py | Certificates Watch | 5 | GET |
| restore.py | Restore Manager | 5 | GET, POST |
| analytics.py | Analytics | 5 | GET |
| session.py | Login | 4 | POST, DELETE |
| product_ui.py | Product UI | 3 | GET, PUT |
| passhub.py | PassHub | 1 (multi-phase) | POST |
| system.py | UISetting | 1 (batch PUT) | PUT |
| **TOPLAM** | **34 sayfa** | **330+** | |

---

## SONUÇ

Bu kılavuz, MEGA-STACK Server v5.3'ün **34 dashboard sayfasının** tamamını fiziksel HTML/JS ve API router dosya analizleri ile belgelemiştir.

### Sistem Özet Metrikleri

| Metrik | Değer |
|--------|-------|
| Toplam Dashboard Sayfası | 34 |
| Toplam API Endpoint | 330+ |
| Docker Konteyner | 18 |
| SQLite Tablo | 57 |
| Frontend HTML Toplam | ~15.000+ satır |
| Paylaşılan JS Modül | 12+ |
| CSS Token | 40+ |
| Python Router | 38 |
| Python Utility | 32 |
| AI Motor | 3 (L1 Gemini, L2 Groq, L3 Kural) |
| Ödeme Gateway | 4 (NOWPayments, BTCPay, MoonPay, Transak) |
| Mail Endpoint | 53 |
| Veritabanı Motoru | 4 (SQLite, MSSQL, MariaDB, Redis) |

### Sayfa Kategori Dağılımı

| Kategori | Sayfa Sayısı | Sayfalar |
|----------|:---:|----------|
| Yönetim | 5 | Dashboard, Admin, Domain, User Manager, Nav Menu |
| Güvenlik | 5 | Guardian, Defense, PassHub, Cert-Watch, Login |
| Veri & DB | 3 | Data Studio, SQL Runner, Migration |
| AI | 2 | AI Studio, STACK-AI |
| İzleme & Log | 4 | Health Check, Log Center, Analytics, Motor Dairesi |
| İletişim | 1 | Mail Center |
| Yedekleme | 2 | Backup Center, Restore Manager |
| Ticaret | 4 | License Hub, Payment, Product UI, Release Manager |
| Dosya & Bilgi | 4 | File Manager, Mega-Editor, Stack Memory, Docs |
| Destek & UI | 4 | Tickets, UISetting, Components, Versions |
| **TOPLAM** | **34** | |

---

*Bu kılavuz MEGA-STACK v5.3 dashboard HTML/JS dosyaları ve API router Python dosyalarının fiziksel analizi ile oluşturulmuştur.*  
*Single Source of Truth: `/opt/stack-memory/` + `system_internal.db`*  
*Kılavuz Tarihi: 04 Nisan 2026*

