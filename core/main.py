"""
MEGA-STACK v2.5 Installation Wizard — API Gateway (FastAPI)
Kurulum durumunu (current_step) yönetir, log stream sağlar,
Step 02 için DomainType seçim modeli içerir.
FAZ 2: Lisans doğrulama, yedek tarama, DB başlatma endpoint'leri.
"""

import asyncio
import os
from enum import Enum
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.logger import wizard_logger, LOG_FILE
from core.license_hybrid import generate_hwid, verify_license, derive_master_key, load_license_key
from core.db_initializer import initialize_database, scan_backups, check_schema_version
from core.env_manager import fernet_engine
from core.docker_engine import (
    deploy_step, deploy_service, get_all_container_statuses,
    get_service_by_step, get_deployment_order, DEPLOYMENT_ORDER,
    check_tier_authorization, generate_compose_file,
)
from core.dns_generator import (
    generate_cloudflare_json, save_cloudflare_json, save_cloudflare_csv,
    generate_dns_records, detect_server_ip, validate_domain, validate_ipv4,
    save_bind_export, read_dkim_public_key,
)
from core.hardening_tool import run_full_hardening, get_hardening_status
from core.analytics import send_install_event

# ─── Sabitler ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIZARD_VERSION = "2.5.0"
TOTAL_STEPS = 22  # 00 – 21

# ─── FastAPI App ─────────────────────────────────────────────────────────
app = FastAPI(
    title="MEGA-STACK v2.5 Installation Wizard",
    version=WIZARD_VERSION,
    docs_url="/api/docs",
    redoc_url=None,
)


# CORS Ayarları — Domain .env.wizard veya ortam değişkeninden dinamik okunur
_cors_domain = os.environ.get("WIZARD_DOMAIN", "").strip()
if _cors_domain:
    _allowed_origins = [
        f"https://{_cors_domain}",
        f"https://dashboard.{_cors_domain}",
        f"https://www.{_cors_domain}",
    ]
else:
    # Temiz kurulum: domain henüz ayarlanmamış — localhost + wizard port
    _allowed_origins = ["http://localhost:9999", "http://127.0.0.1:9999"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _update_env_domain(domain: str):
    """Step 02'de domain ayarlanınca .env.wizard'a WIZARD_DOMAIN yazar."""
    env_path = "/opt/mega-stack-product-wizard/.env.wizard"
    if not os.path.isfile(env_path):
        return
    try:
        import re as _re
        content = open(env_path, "r").read()
        if "WIZARD_DOMAIN=" in content:
            content = _re.sub(
                r"^#?\s*WIZARD_DOMAIN=.*$",
                f"WIZARD_DOMAIN={domain}",
                content,
                flags=_re.MULTILINE,
            )
        else:
            content += f"\nWIZARD_DOMAIN={domain}\n"
        with open(env_path, "w") as f:
            f.write(content)
        os.environ["WIZARD_DOMAIN"] = domain
    except Exception:
        pass


# ─── Dashboard Widget Endpoint'leri (Production API) ────────────────────
from fastapi.responses import HTMLResponse, JSONResponse
from core.global_search_utils import search_passhub, search_versions, search_tickets, search_stack_memory


@app.get("/api/global/search")
async def global_search(q: str = ""):
    """Global arama: PassHub, Versions, Tickets, Stack-Memory .md dosyaları"""
    passhub_db = "/opt/mega-stack/core-api/db/passhub.db"
    versions_db = "/opt/mega-stack/core-api/db/versions.db"
    tickets_db = "/opt/mega-stack/core-api/db/tickets.db"
    stack_memory_dir = "/opt/stack-memory/"
    results = {
        "passhub": search_passhub(q, passhub_db),
        "versions": search_versions(q, versions_db),
        "tickets": search_tickets(q, tickets_db),
        "stack_memory": search_stack_memory(q, stack_memory_dir),
    }
    return JSONResponse({"results": results})


@app.get("/api/dashboard/security", response_class=HTMLResponse)
async def dashboard_security_status():
    """Security Status widget'ı için örnek veri."""
    return """
    <div class='widget-sec-status'>
        <div class='sec-row'><span class='sec-label'>Aktif Güvenlik Modülü:</span> <span class='sec-val'>CrowdSec</span></div>
        <div class='sec-row'><span class='sec-label'>Banlı IP:</span> <span class='sec-val sec-val--red'>12</span></div>
        <div class='sec-row'><span class='sec-label'>Yerel Ban:</span> <span class='sec-val sec-val--orange'>3</span></div>
        <div class='sec-row'><span class='sec-label'>Geo-IP Ülke:</span> <span class='sec-val'>7</span></div>
        <div class='sec-row'><span class='sec-label'>Son Olay:</span> <span class='sec-val'>5dk önce</span></div>
    </div>
    """


@app.get("/api/dashboard/pulse", response_class=HTMLResponse)
async def dashboard_system_pulse():
    """System Pulse widget'ı için örnek veri."""
    return """
    <div class='widget-pulse'>
        <div class='pulse-row'><span class='pulse-label'>CPU:</span> <span class='pulse-val'>%23</span></div>
        <div class='pulse-row'><span class='pulse-label'>RAM:</span> <span class='pulse-val'>3.2 GB</span></div>
        <div class='pulse-row'><span class='pulse-label'>Disk:</span> <span class='pulse-val'>120 GB / 500 GB</span></div>
        <div class='pulse-row'><span class='pulse-label'>Load Avg:</span> <span class='pulse-val'>0.42 / 0.38 / 0.35</span></div>
        <div class='pulse-row'><span class='pulse-label'>Container:</span> <span class='pulse-val'>14</span></div>
    </div>
    """


@app.get("/api/dashboard/support", response_class=HTMLResponse)
async def dashboard_support_desk():
    """Support Desk widget'ı için örnek veri."""
    return """
    <div class='widget-support'>
        <div class='support-row'><span class='support-label'>Açık Ticket:</span> <span class='support-val'>2</span></div>
        <div class='support-row'><span class='support-label'>Son Yanıt:</span> <span class='support-val'>3dk önce</span></div>
        <div class='support-row'><span class='support-label'>Destek Seviyesi:</span> <span class='support-val support-val--green'>Normal</span></div>
        <div class='support-row'><span class='support-label'>Acil Durum:</span> <span class='support-val support-val--red'>Yok</span></div>
    </div>
    """


# ─── Pydantic Modeller ──────────────────────────────────────────────────
class DomainType(str, Enum):
    """Step 02 — Domain tipi seçimi."""
    STATIC = "static"   # Type A: Nginx üzerinden statik içerik
    APP = "app"          # Type B: Docker container deployment


class DomainConfig(BaseModel):
    """Step 02 — Domain yapılandırması."""
    domain: str = Field(..., min_length=3, max_length=253, examples=["example.com"])
    domain_type: DomainType
    cloudflare_zone_id: Optional[str] = Field(None, max_length=64)
    ssl_mode: str = Field(default="full_strict", pattern=r"^(full_strict|full|flexible)$")


class StepResult(BaseModel):
    """Her adımın dönüş sonucu."""
    step_id: str
    status: str  # pending | running | completed | failed
    message: str


class LicenseRequest(BaseModel):
    """Step 00 — Lisans doğrulama isteği."""
    license_key: str = Field(..., min_length=8, max_length=512)
    user_password: Optional[str] = Field(None, min_length=6, max_length=128)


class DnsGenerateRequest(BaseModel):
    """Step 02 — DNS import dosyası üretim isteği."""
    domain: str = Field(..., min_length=3, max_length=253)
    server_ip: str = Field(..., min_length=7, max_length=45)
    domain_type: str = Field(default="static", pattern=r"^(static|app)$")
    extra_domains: Optional[list[dict]] = None


class AiTokensRequest(BaseModel):
    """Step 19 — AI ve Telegram API token'ları."""
    gemini_key: Optional[str] = Field(None, min_length=10, max_length=256)
    groq_key: Optional[str] = Field(None, min_length=10, max_length=256)
    telegram_token: Optional[str] = Field(None, min_length=10, max_length=256)
    telegram_chat_id: Optional[str] = Field(None, min_length=1, max_length=64)


# ─── Kurulum Durumu (In-Memory State) ───────────────────────────────────
class InstallationState:
    """Kurulum sürecinin anlık durumunu tutan singleton state."""

    def __init__(self) -> None:
        self.current_step: int = 0
        self.steps: dict[int, dict] = {}
        self.domain_config: Optional[DomainConfig] = None
        self.is_running: bool = False
        self.tier: Optional[str] = None
        self.allowed_services: list[str] = []
        self.offline_mode: bool = False
        self._init_steps()

    def _init_steps(self) -> None:
        step_names = [
            "License Auth", "Identity & Branding", "Global DNS & Domain Config",
            "Traefik Setup", "Authelia Setup", "CrowdSec Setup",
            "Bouncer Setup", "CertDumper Setup", "MSSQL Setup",
            "iRedMail Setup", "Nginx Setup", "PointVending Setup",
            "Core-API Setup", "Netdata Setup", "UptimeKuma Setup",
            "Dozzle Setup", "Portainer Setup", "CloudBeaver Setup",
            "Watchtower Setup", "AI & Telegram API", "Hardening & Finalize",
            "Success & Launch",
        ]
        for i, name in enumerate(step_names):
            self.steps[i] = {
                "step_id": f"{i:02d}",
                "name": name,
                "status": "pending",
            }

    def get_current(self) -> dict:
        return {
            "current_step": self.current_step,
            "total_steps": TOTAL_STEPS,
            "step_info": self.steps.get(self.current_step),
            "is_running": self.is_running,
        }

    def advance(self) -> dict:
        if self.current_step < TOTAL_STEPS - 1:
            self.steps[self.current_step]["status"] = "completed"
            self.current_step += 1
            self.steps[self.current_step]["status"] = "running"
        return self.get_current()

    def mark_failed(self, step: int, message: str) -> None:
        if step in self.steps:
            self.steps[step]["status"] = "failed"
            self.steps[step]["error"] = message
            self.is_running = False


state = InstallationState()


# ─── Endpoints ───────────────────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    """Wizard API sağlık kontrolü."""
    return {"status": "ok", "version": WIZARD_VERSION}


@app.get("/api/install/status")
async def get_install_status():
    """Kurulumun anlık durumunu döner."""
    return state.get_current()


@app.get("/api/install/steps")
async def get_all_steps():
    """Tüm adımların listesini döner."""
    return {"total": TOTAL_STEPS, "steps": state.steps}


@app.post("/api/install/next", response_model=StepResult)
async def advance_step():
    """Bir sonraki kurulum adımına geçer."""
    prev_step = state.current_step
    result = state.advance()
    wizard_logger.info(
        f"Step {prev_step:02d} tamamlandı → Step {result['current_step']:02d} başlatıldı",
        step_id=f"{result['current_step']:02d}",
    )
    step = result["step_info"]
    return StepResult(
        step_id=step["step_id"],
        status=step["status"],
        message=f"{step['name']} adımı aktif.",
    )


@app.post("/api/install/domain-config")
async def set_domain_config(config: DomainConfig):
    """Step 02 — Domain tipi (Static / App) ve domain bilgilerini kaydeder."""
    state.domain_config = config
    wizard_logger.info(
        f"Domain yapılandırması kaydedildi: {config.domain} ({config.domain_type.value})",
        step_id="02",
    )
    return {
        "status": "ok",
        "domain": config.domain,
        "domain_type": config.domain_type.value,
        "ssl_mode": config.ssl_mode,
    }


@app.get("/api/install/domain-config")
async def get_domain_config():
    """Kayıtlı domain yapılandırmasını döner."""
    if state.domain_config is None:
        raise HTTPException(status_code=404, detail="Domain yapılandırması henüz girilmedi.")
    return {
        "domain": state.domain_config.domain,
        "domain_type": state.domain_config.domain_type.value,
        "ssl_mode": state.domain_config.ssl_mode,
        "cloudflare_zone_id": state.domain_config.cloudflare_zone_id,
    }


@app.post("/api/install/generate-compose")
async def api_generate_compose():
    """Lisans tier'ına göre docker-compose.yml dosyasını üretir.

    allowed_services listesi kullanılarak AI servisleri koşullu dahil edilir.
    """
    if state.domain_config is None:
        raise HTTPException(status_code=400, detail="Önce domain yapılandırması girilmelidir.")
    if not state.allowed_services:
        raise HTTPException(status_code=400, detail="Lisans doğrulaması yapılmamış — izinli servis listesi boş.")

    path = generate_compose_file(
        domain=state.domain_config.domain,
        allowed_services=state.allowed_services,
        tier=state.tier or "Standart",
    )
    return {
        "status": "ok",
        "compose_file": path,
        "allowed_services": state.allowed_services,
        "tier": state.tier,
    }


@app.get("/api/logs")
async def stream_logs():
    """
    install.log dosyasını frontend için SSE (Server-Sent Events) olarak stream eder.
    Mevcut satırları gönderir, ardından yeni satırları tail -f mantığıyla canlı yollar.
    """

    async def log_generator():
        if not os.path.exists(LOG_FILE):
            yield "data: {\"message\": \"Log dosyası henüz oluşturulmadı.\"}\n\n"
            return

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            # Mevcut satırları gönder
            for line in f:
                stripped = line.strip()
                if stripped:
                    yield f"data: {stripped}\n\n"

            # Yeni satırları canlı stream et (tail -f)
            while True:
                line = f.readline()
                if line:
                    stripped = line.strip()
                    if stripped:
                        yield f"data: {stripped}\n\n"
                else:
                    await asyncio.sleep(0.5)

    return StreamingResponse(
        log_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/system/resources")
async def get_system_resources():
    """Sunucu kaynaklarını (vCPU, RAM, Disk) raporlar."""
    try:
        import psutil
        import shutil

        disk = shutil.disk_usage("/")
        mem = psutil.virtual_memory()

        return {
            "cpu_count": psutil.cpu_count(logical=True),
            "ram_total_gb": round(mem.total / (1024 ** 3), 1),
            "ram_available_gb": round(mem.available / (1024 ** 3), 1),
            "disk_total_gb": round(disk.total / (1024 ** 3), 1),
            "disk_free_gb": round(disk.free / (1024 ** 3), 1),
        }
    except ImportError:
        raise HTTPException(status_code=500, detail="psutil modülü yüklenemedi.")


# ─── Lisans & Güvenlik Endpoint'leri ────────────────────────────────────
@app.post("/api/license/verify")
async def api_verify_license(req: LicenseRequest):
    """
    Step 00 — Lisans anahtarını HWID ile birlikte doğrular.
    Başarılıysa Fernet master key türetir ve DB'yi başlatır.
    """
    hwid = generate_hwid()
    result = await verify_license(req.license_key, hwid)

    if result["verified"] and result["salt"] and req.user_password:
        # MEGA_MASTER_KEY türet
        master_key = derive_master_key(req.user_password, result["salt"])
        fernet_engine.set_key(master_key)
        wizard_logger.info(
            "[Security Audit] Fernet motoru lisans onayı sonrası aktif.",
            step_id="00",
        )

    # Tier bilgisini state'e kaydet
    if result["verified"]:
        state.tier = result["tier"]
        state.allowed_services = result.get("allowed_services", [])
        state.offline_mode = result.get("offline_mode", False)

    return {
        "hwid": hwid,
        "verified": result["verified"],
        "message": result["message"],
        "tier": result["tier"],
        "hardware_limits": result.get("hardware_limits"),
        "allowed_services": result.get("allowed_services", []),
        "offline_mode": result.get("offline_mode", False),
    }


@app.get("/api/license/tier-info")
async def api_tier_info():
    """Lisans onayı sonrası tier ve izinli servis listesini döner."""
    return {
        "tier": state.tier,
        "offline_mode": state.offline_mode,
        "allowed_services": state.allowed_services,
    }


@app.get("/api/license/hwid")
async def api_get_hwid():
    """Sunucunun HWID hash'ini döner."""
    return {"hwid": generate_hwid()}


@app.get("/api/install/restore-check")
async def api_restore_check():
    """
    /opt/mega-stack/backups ve /opt/mega-stack-backups dizinlerini
    tarayarak mevcut yedekleri listeler. Anayasa Madde 6: Smart Backup Discovery.
    """
    backups = scan_backups()

    # Her SQLite yedek için şema versiyonu kontrol et
    for backup in backups:
        if backup["type"] in ("db", "sqlite3"):
            schema_info = check_schema_version(backup["path"])
            backup["schema_version"] = schema_info["version"]
            backup["needs_migration"] = schema_info["needs_migration"]
            backup["migration_type"] = schema_info["migration_type"]

    return {
        "backup_count": len(backups),
        "backups": backups,
        "restore_available": len(backups) > 0,
    }


# ─── Orkestrasyon Endpoint'leri ──────────────────────────────────────────
@app.post("/api/install/deploy/{step_id}")
async def api_deploy_step(step_id: str):
    """
    Belirli bir adımın konteynerlerini sıralı olarak deploy eder.
    Health check geçene kadar bekler, fail ederse zinciri durdurur.
    """
    services = get_service_by_step(step_id)
    if not services:
        raise HTTPException(
            status_code=404,
            detail=f"Step {step_id} için deploy edilecek servis bulunamadı.",
        )

    # ── Tier Yetki Kontrolü (Backend Guard) ──
    if state.allowed_services:
        authorized, unauthorized = check_tier_authorization(step_id, state.allowed_services)
        if not authorized:
            wizard_logger.warning(
                f"[Tier Guard] Step {step_id} reddedildi — yetkisiz servisler: {unauthorized}",
                step_id=step_id,
            )
            raise HTTPException(
                status_code=403,
                detail=f"Unauthorized Tier — Bu servisler mevcut lisans paketinizde bulunmamaktadır: {', '.join(unauthorized)}",
            )

    wizard_logger.info(
        f"[API] Step {step_id} deploy tetiklendi — {len(services)} servis",
        step_id=step_id,
    )

    results = await deploy_step(step_id)

    all_ok = all(r["success"] for r in results)
    if all_ok:
        state.steps[int(step_id)]["status"] = "completed"
        wizard_logger.info(
            f"Step {step_id} tüm servisler healthy — adım tamamlandı.",
            step_id=step_id,
        )
    else:
        failed = [r["service"] for r in results if not r["success"]]
        state.mark_failed(
            int(step_id),
            f"Başarısız servisler: {', '.join(failed)}",
        )

    return {
        "step_id": step_id,
        "success": all_ok,
        "results": results,
    }


@app.get("/api/install/container-status")
async def api_container_status():
    """
    Tüm servislerin anlık CPU/RAM ve Health durumlarını döner.
    """
    statuses = await asyncio.to_thread(get_all_container_statuses)
    return {
        "total": len(statuses),
        "containers": statuses,
    }


@app.get("/api/install/deployment-order")
async def api_deployment_order():
    """Deployment sırasını döner."""
    return {"order": get_deployment_order()}


# ─── DNS Generator Endpoint'leri ─────────────────────────────────────────
@app.post("/api/dns/generate")
async def api_dns_generate(req: DnsGenerateRequest):
    """
    Step 02 — Cloudflare uyumlu DNS import dosyası üretir.
    JSON ve CSV formatlarını kaydeder.
    """
    if not validate_domain(req.domain):
        raise HTTPException(status_code=400, detail="Geçersiz domain.")
    if not validate_ipv4(req.server_ip):
        raise HTTPException(status_code=400, detail="Geçersiz IP adresi.")

    json_path = save_cloudflare_json(
        req.domain, req.server_ip, req.domain_type, req.extra_domains
    )
    csv_path = save_cloudflare_csv(
        req.domain, req.server_ip, req.domain_type, req.extra_domains
    )
    bind_path = save_bind_export(
        req.domain, req.server_ip, req.domain_type, req.extra_domains
    )

    # WIZARD_DOMAIN'i .env.wizard'a yaz — CORS dinamik olarak güncellensin
    _update_env_domain(req.domain)

    records = generate_dns_records(
        req.domain, req.server_ip, req.domain_type, req.extra_domains
    )

    return {
        "status": "ok",
        "domain": req.domain,
        "server_ip": req.server_ip,
        "record_count": len(records),
        "json_file": json_path,
        "csv_file": csv_path,
        "bind_file": bind_path,
    }


@app.get("/api/dns/server-ip")
async def api_detect_server_ip():
    """Sunucunun dış IP adresini tespit eder."""
    ip = detect_server_ip()
    return {"server_ip": ip, "detected": ip is not None}


@app.get("/api/dns/dkim-key")
async def api_get_dkim_key(domain: str = ""):
    """
    Step 09 sonrası — iRedMail'in ürettiği DKIM public key'i okur.
    Anahtar mevcutsa Step 02 DNS export'unda placeholder yerine kullanılır.
    """
    if not domain:
        # State'ten domain al
        if state.domain_config and state.domain_config.domain:
            domain = state.domain_config.domain
        else:
            return {"available": False, "reason": "Domain henüz yapılandırılmadı."}

    pubkey = read_dkim_public_key(domain)
    return {
        "available": pubkey is not None,
        "domain": domain,
        "dkim_public_key": pubkey,
    }


# ─── FAZ 5: Finalization & Hardening Endpoint'leri ───────────────────────
@app.post("/api/install/save-ai-tokens")
async def api_save_ai_tokens(req: AiTokensRequest):
    """
    Step 19 — Gemini, Groq ve Telegram token'larını DB'ye ve
    fiziksel secrets dosyalarına kaydeder.
    """
    from core.db_initializer import get_connection
    from core.env_manager import save_credential, secrets_manager
    from datetime import datetime, timezone as tz

    saved = []
    conn = get_connection()

    try:
        now = datetime.now(tz.utc).isoformat()

        # Gemini
        if req.gemini_key:
            api_key_enc = fernet_engine.encrypt(req.gemini_key) if fernet_engine.is_ready else req.gemini_key
            conn.execute(
                """INSERT OR REPLACE INTO ai_providers
                   (provider_name, api_key_enc, model, is_active, config, created_at, updated_at)
                   VALUES (?, ?, ?, 1, ?, ?, ?)""",
                ("gemini", api_key_enc, "gemini-2.0-flash",
                 '{"endpoint": "https://generativelanguage.googleapis.com/v1beta"}', now, now),
            )
            saved.append("gemini")

        # Groq
        if req.groq_key:
            api_key_enc = fernet_engine.encrypt(req.groq_key) if fernet_engine.is_ready else req.groq_key
            conn.execute(
                """INSERT OR REPLACE INTO ai_providers
                   (provider_name, api_key_enc, model, is_active, config, created_at, updated_at)
                   VALUES (?, ?, ?, 1, ?, ?, ?)""",
                ("groq", api_key_enc, "llama-3.3-70b-versatile",
                 '{"endpoint": "https://api.groq.com/openai/v1"}', now, now),
            )
            saved.append("groq")

        # Telegram
        if req.telegram_token:
            save_credential(
                conn,
                service_name="telegram",
                username=req.telegram_chat_id,
                api_key=req.telegram_token,
                secret_filename=None,
            )
            saved.append("telegram")

        conn.commit()

        # ai_tokens.env dosyasını güncelle
        ai_env_lines = []
        if req.gemini_key:
            ai_env_lines.append(f"GEMINI_API_KEY={req.gemini_key}")
        if req.groq_key:
            ai_env_lines.append(f"GROQ_API_KEY={req.groq_key}")
        if req.telegram_token:
            ai_env_lines.append(f"TELEGRAM_BOT_TOKEN={req.telegram_token}")
        if req.telegram_chat_id:
            ai_env_lines.append(f"TELEGRAM_CHAT_ID={req.telegram_chat_id}")

        if ai_env_lines:
            secrets_manager.write_secret("ai_tokens.env", "\n".join(ai_env_lines) + "\n")

        wizard_logger.info(
            f"[Step 19] AI token'ları kaydedildi: {', '.join(saved)}",
            step_id="19",
        )

        return {"status": "ok", "saved": saved}

    except Exception as exc:
        wizard_logger.error(f"[Step 19] Token kayıt hatası: {exc}", step_id="19")
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        conn.close()


@app.post("/api/install/finalize")
async def api_finalize():
    """
    Step 20 — Sistem mühürleme (hardening) sürecini tetikler.
    chmod cascade, acme.json mühürleme, temp cleanup ve pasifleştirme.
    """
    wizard_logger.info("[Step 20] Finalize tetiklendi — mühürleme başlıyor...", step_id="20")

    try:
        report = await asyncio.to_thread(run_full_hardening)

        # Container health son kontrol
        container_statuses = await asyncio.to_thread(get_all_container_statuses)
        healthy_count = sum(1 for c in container_statuses if c.get("health") == "healthy")

        # Step 20'yi tamamla
        state.steps[20]["status"] = "completed"
        state.steps[21]["status"] = "running"

        wizard_logger.info(
            f"[Step 20] Mühürleme tamamlandı — Healthy: {healthy_count}/{len(container_statuses)}",
            step_id="20",
        )

        return {
            "status": "ok",
            "hardening": report,
            "containers": {
                "total": len(container_statuses),
                "healthy": healthy_count,
                "details": container_statuses,
            },
        }

    except Exception as exc:
        state.mark_failed(20, str(exc))
        wizard_logger.error(f"[Step 20] Mühürleme hatası: {exc}", step_id="20")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/install/password-matrix")
async def api_password_matrix():
    """
    Step 21 — Tüm servis kimlik bilgilerini ve şifreleri döner.
    Frontend bu veriyi tablo ve PDF/TXT indirme olarak sunar.
    """
    from core.env_manager import secrets_manager

    matrix = []
    secrets_dir = Path("/opt/mega-stack/secrets")

    # Secret dosyalarını oku ve matrise ekle
    secret_mapping = [
        ("mssql_sa_password", "MSSQL", "SA", "Veritabanı yönetici şifresi"),
        ("iredmail_admin_password", "iRedMail", "postmaster", "E-posta yönetici şifresi"),
        ("iredmail_mysql_root_password", "iRedMail MySQL", "root", "MySQL root şifresi"),
        ("iredmail_mlmmjadmin_token", "iRedMail mlmmjadmin", "—", "API token"),
        ("iredmail_iredapd_password", "iRedMail iRedAPD", "—", "Servis şifresi"),
        ("iredmail_dashboard_api_password", "iRedMail Dashboard", "admin", "Dashboard API şifresi"),
        ("authelia_jwt_secret", "Authelia", "—", "JWT secret key"),
        ("authelia_session_secret", "Authelia", "—", "Session secret"),
        ("authelia_storage_encryption_key", "Authelia", "—", "Storage encryption key"),
        ("pointvending_encryption_key", "PointVending", "—", "Şifreleme anahtarı"),
    ]

    for filename, service, username, description in secret_mapping:
        value = secrets_manager.read_secret(filename)
        matrix.append({
            "service": service,
            "username": username,
            "password": value if value else "—",
            "file": filename,
            "description": description,
        })

    # AI token'ları (maskeleme ile)
    ai_tokens_raw = secrets_manager.read_secret("ai_tokens.env")
    if ai_tokens_raw:
        for line in ai_tokens_raw.strip().split("\n"):
            if "=" in line:
                key, val = line.split("=", 1)
                masked = val[:8] + "..." + val[-4:] if len(val) > 12 else "***"
                matrix.append({
                    "service": "AI/Telegram",
                    "username": key,
                    "password": masked,
                    "file": "ai_tokens.env",
                    "description": f"{key} token",
                })

    # Domain bilgisi
    domain = state.domain_config.domain if state.domain_config else "—"

    # Hardening durumu
    hardening_status = get_hardening_status()

    return {
        "status": "ok",
        "domain": domain,
        "credential_count": len(matrix),
        "matrix": matrix,
        "hardening": hardening_status,
        "dashboard_url": f"https://dashboard.{domain}" if domain != "—" else None,
        "webmail_url": f"https://mail.{domain}" if domain != "—" else None,
        "portainer_url": f"https://portainer.{domain}" if domain != "—" else None,
    }


@app.get("/api/install/hardening-status")
async def api_hardening_status():
    """Mühürleme durumunu kontrol eder."""
    return get_hardening_status()


@app.post("/api/analytics/send")
async def api_analytics_send():
    """
    Step 21 — Anonim kurulum analytics'i Master Hub'a best-effort gönderir.
    ASLA kurulumu bloklamaz — tüm hatalar sessizce yutulur.
    """
    await send_install_event("install_complete", state)
    return {"status": "ok", "message": "analytics event queued"}


# ─── Startup Event ───────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    wizard_logger.info("MEGA-STACK v2.5 Installation Wizard API başlatıldı.", step_id="00")

    # Veritabanını başlat (WAL Mode zorunlu)
    try:
        db_conn = initialize_database()
        db_conn.close()
    except Exception as exc:
        wizard_logger.critical(
            f"[Security Audit] DB başlatma hatası: {exc}", step_id="00"
        )

    state.steps[0]["status"] = "running"
    state.is_running = True


# ─── SPA Serving ─────────────────────────────────────────────────────────
WEB_DIR = os.path.join(BASE_DIR, "web")
# ─── Wizard ReadOnly Proxy — Dashboard Viewer (GET-Only) ─────────────
# Bu endpoint'ler Core API'ye (port 8888) sadece GET istekleri proxy eder.
# POST/DELETE gibi yazma istekleri kesinlikle engellenir.
CORE_API_BASE = os.environ.get("CORE_API_URL", "http://127.0.0.1:8888")
# Güvenlik: Hardcoded fallback yerine her başlatmada benzersiz token üretilir.
# Prodüksiyonda WIZARD_READONLY_TOKEN env var ile sabitlenmelidir.
import secrets as _secrets
WIZARD_READONLY_TOKEN = os.environ.get("WIZARD_READONLY_TOKEN") or _secrets.token_hex(32)

# İzin verilen ReadOnly proxy rotaları (sadece GET)
ALLOWED_PROXY_ROUTES = {
    # Versions
    "/api/versions",
    "/api/versions/stats",
    # Components
    "/api/components",
    "/api/components/stats",
    "/api/components/categories",
    "/api/components/graph",
    # Documentation
    "/api/docs",
    "/api/docs/page",
    "/api/docs/stats",
    "/api/docs/search",
    "/api/docs/categories",
    # Release Manager (readonly amaçlı)
    "/api/releases",
    "/api/releases/detail",
}


@app.get("/api/dashboard/proxy/{proxy_path:path}")
async def wizard_readonly_proxy(proxy_path: str, request: Request):
    """
    Wizard ReadOnly Proxy — Core API'ye sadece GET istekleri yönlendirir.
    Güvenlik: X-Wizard-Token header ile tanımlama, ALLOWED_PROXY_ROUTES ile kısıtlama.
    """
    api_path = f"/api/{proxy_path}"

    # Query string'i koru
    query_string = str(request.query_params)
    if query_string:
        target_url = f"{CORE_API_BASE}{api_path}?{query_string}"
    else:
        target_url = f"{CORE_API_BASE}{api_path}"

    # Route whitelist kontrolü
    if api_path not in ALLOWED_PROXY_ROUTES:
        raise HTTPException(
            status_code=403,
            detail=f"Bu API rotasına Wizard üzerinden erişim izni yoktur: {api_path}",
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                target_url,
                headers={"X-Wizard-Token": WIZARD_READONLY_TOKEN},
            )
            return resp.json()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Core API (domain-api) bağlantısı kurulamadı. Servis çalışıyor mu?",
        )
    except Exception as exc:
        wizard_logger.error(f"[Proxy] {api_path} hatası: {exc}")
        raise HTTPException(status_code=502, detail=str(exc))


@app.get("/api/dashboard/viewer-config")
async def wizard_viewer_config():
    """
    Wizard Viewer sayfaları için yapılandırma — hangi sayfalar kullanılabilir,
    hangi aksiyonlar kısıtlı.
    """
    return {
        "readonly_pages": [
            {
                "id": "versions",
                "title": "Versiyon Tarihçesi",
                "icon": "📋",
                "description": "Sistem versiyon geçmişi ve changelog (Salt Okunur)",
                "proxy_base": "/api/dashboard/proxy/versions",
                "permissions": ["view"],
                "restricted_actions": ["create", "update", "delete", "status_change"],
            },
            {
                "id": "components",
                "title": "Bileşen Kataloğu",
                "icon": "🧩",
                "description": "Sistem bileşenleri ve bağımlılık haritası (Salt Okunur)",
                "proxy_base": "/api/dashboard/proxy/components",
                "permissions": ["view"],
                "restricted_actions": ["create", "update", "delete", "status_change"],
            },
            {
                "id": "documentations",
                "title": "Kurumsal Dokümantasyon",
                "icon": "📖",
                "description": "Sistem dokümantasyonu ve rehberler (Salt Okunur)",
                "proxy_base": "/api/dashboard/proxy/docs",
                "permissions": ["view"],
                "restricted_actions": ["create", "update", "delete", "publish"],
            },
        ],
        "release_manager": {
            "proxy_base": "/api/dashboard/proxy/releases",
            "permissions": ["view"],
            "restricted_actions": ["create", "publish", "apply", "rollback"],
        },
    }

@app.get("/")
async def serve_index():
    """SPA index.html döner."""
    return FileResponse(os.path.join(WEB_DIR, "index.html"))


# Static dosyalarını mount et (CSS, JS, step fragment'ları)
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
