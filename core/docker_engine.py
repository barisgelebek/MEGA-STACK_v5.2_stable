"""
MEGA-STACK v2.5 Installation Wizard — Docker Orchestration Engine
Şartname: FAZ B — Orkestrasyon & Sıralı Deployment

Deployment Sırası (Sequential & Verified):
  🛡️ Güvenlik  → traefik, authelia, crowdsec, crowdsec-bouncer, cert-dumper
  💾 Veri      → mssql, iredmail
  ⚙️ Uygulama  → nginx-sites, pointvending, domain-api
  📊 İzleme    → netdata, uptime-kuma, dozzle, portainer, cloudbeaver, watchtower

KIRMIZI ÇİZGİ:
  - Her servis healthy olmadan sonraki servis başlatılmaz.
  - iRedMail öncesi amavisd override dosyası garanti edilmeli.
  - Bir servis fail ederse tüm zincir durdurulmalı.
"""

import asyncio
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from typing import Optional

from core.logger import wizard_logger

# ─── Sabitler ────────────────────────────────────────────────────────────
MEGA_STACK_DIR = "/opt/mega-stack"
COMPOSE_FILE = os.path.join(MEGA_STACK_DIR, "docker-compose.yml")
COMPOSE_TEMPLATE = "docker-compose.v2.5.yml.j2"
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
AMAVISD_OVERRIDE_PATH = os.path.join(MEGA_STACK_DIR, "iredmail", "custom", "amavisd", "amavisd.conf")
AMAVISD_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "templates", "iredmail", "custom-amavisd.conf",
)

HEALTH_CHECK_TIMEOUT = 60  # saniye
HEALTH_CHECK_INTERVAL = 3  # saniye


# ─── Deployment Grupları — Şartname Sırası ───────────────────────────────
@dataclass
class ServiceDef:
    """Bir docker-compose servisinin tanımı."""
    name: str                    # docker-compose service adı
    container_name: str          # docker container adı
    step_id: str                 # wizard step numarası (02d)
    group: str                   # güvenlik | veri | uygulama | izleme
    health_timeout: int = HEALTH_CHECK_TIMEOUT
    pre_hooks: list[str] = field(default_factory=list)  # önceden çalışacak hook adları


# 19+ servis — kesin sıra  (AI servisleri tier-koşullu olarak sona eklendi)
DEPLOYMENT_ORDER: list[ServiceDef] = [
    # ── 🛡️ Güvenlik ──
    ServiceDef("traefik",          "traefik",          "03", "güvenlik", health_timeout=90),
    ServiceDef("authelia",         "authelia",         "04", "güvenlik", health_timeout=60),
    ServiceDef("crowdsec",         "crowdsec",         "05", "güvenlik", health_timeout=60),
    ServiceDef("crowdsec-bouncer", "crowdsec-bouncer", "06", "güvenlik", health_timeout=30),
    ServiceDef("cert-dumper",      "cert-dumper",      "07", "güvenlik", health_timeout=90),
    # ── 💾 Veri ──
    ServiceDef("mssql",            "mssql-server",     "08", "veri",     health_timeout=120),
    ServiceDef("iredmail",         "iredmail",         "09", "veri",     health_timeout=180,
               pre_hooks=["ensure_amavisd_override"]),
    # ── ⚙️ Uygulama ──
    ServiceDef("nginx-sites",      "nginx-sites",      "10", "uygulama", health_timeout=30),
    ServiceDef("pointvending",     "pointvending_app", "11", "uygulama", health_timeout=90),
    ServiceDef("domain-api",       "domain-api",       "12", "uygulama", health_timeout=90),
    # ── 📊 İzleme ──
    ServiceDef("netdata",          "netdata",          "13", "izleme",   health_timeout=60),
    ServiceDef("uptime-kuma",      "uptime-kuma",      "14", "izleme",   health_timeout=60),
    ServiceDef("dozzle",           "dozzle",           "15", "izleme",   health_timeout=30),
    ServiceDef("portainer",        "portainer",        "16", "izleme",   health_timeout=30),
    ServiceDef("cloudbeaver",      "cloudbeaver",      "17", "izleme",   health_timeout=60),
    ServiceDef("watchtower",       "watchtower",       "18", "izleme",   health_timeout=30),
    # ── 🧠 AI / Zeka (Tier-koşullu: Professional ve Enterprise) ──
    ServiceDef("mariadb",          "mariadb",          "19", "veri",     health_timeout=60),
    ServiceDef("stack-ai",         "stack-ai",         "20", "ai",       health_timeout=60),
    ServiceDef("masking-engine",   "masking-engine",   "20", "ai",       health_timeout=30),
    ServiceDef("neural-core",      "neural-core",      "20", "ai",       health_timeout=30),
]


# ─── Pre-Hook'lar ───────────────────────────────────────────────────────
def ensure_amavisd_override() -> bool:
    """
    KIRMIZI ÇİZGİ: iRedMail başlatılmadan önce amavisd override dosyası
    kontrol edilir. Yoksa şablondan oluşturulur.
    """
    if os.path.isfile(AMAVISD_OVERRIDE_PATH):
        wizard_logger.info(
            f"Amavisd override dosyası mevcut: {AMAVISD_OVERRIDE_PATH}",
            step_id="09",
        )
        return True

    # Dizin yoksa oluştur
    override_dir = os.path.dirname(AMAVISD_OVERRIDE_PATH)
    os.makedirs(override_dir, exist_ok=True)

    # Şablondan kopyala veya boş oluştur
    if os.path.isfile(AMAVISD_TEMPLATE_PATH):
        shutil.copy2(AMAVISD_TEMPLATE_PATH, AMAVISD_OVERRIDE_PATH)
        wizard_logger.info(
            f"Amavisd override şablondan oluşturuldu: {AMAVISD_TEMPLATE_PATH} → {AMAVISD_OVERRIDE_PATH}",
            step_id="09",
        )
    else:
        # Şablon da yoksa minimal boş dosya oluştur
        with open(AMAVISD_OVERRIDE_PATH, "w", encoding="utf-8") as f:
            f.write("# MEGA-STACK v2.5 — Amavisd Custom Override\n")
        wizard_logger.warning(
            f"Amavisd şablon bulunamadı, boş override oluşturuldu: {AMAVISD_OVERRIDE_PATH}",
            step_id="09",
        )

    return True


# Hook registry
_PRE_HOOKS = {
    "ensure_amavisd_override": ensure_amavisd_override,
}


# ─── Docker Komut Çalıştırıcı ───────────────────────────────────────────
def _run_cmd(args: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """
    Alt süreçte komut çalıştırır, (returncode, stdout, stderr) döner.
    """
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=MEGA_STACK_DIR,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Komut zaman aşımına uğradı ({timeout}s): {' '.join(args)}"
    except FileNotFoundError:
        return -1, "", f"Komut bulunamadı: {args[0]}"


def _docker_compose_up(service_name: str) -> tuple[bool, str]:
    """
    Tek bir servisi docker-compose up -d ile başlatır.
    """
    rc, stdout, stderr = _run_cmd(
        ["docker", "compose", "-f", COMPOSE_FILE, "up", "-d", "--no-deps", service_name],
        timeout=120,
    )
    if rc != 0:
        return False, stderr or stdout
    return True, stdout


def _get_container_health(container_name: str) -> str:
    """
    Docker container'ın health status'unu döner:
    healthy | unhealthy | starting | none | not_found
    """
    rc, stdout, _ = _run_cmd(
        ["docker", "inspect", "--format", "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}", container_name],
        timeout=10,
    )
    if rc != 0:
        return "not_found"
    return stdout.strip() if stdout.strip() else "not_found"


def _is_container_running(container_name: str) -> bool:
    """Container'ın running state'de olup olmadığını kontrol eder."""
    rc, stdout, _ = _run_cmd(
        ["docker", "inspect", "--format", "{{.State.Running}}", container_name],
        timeout=10,
    )
    return rc == 0 and stdout.strip().lower() == "true"


def get_container_stats(container_name: str) -> dict:
    """
    Container'ın CPU%, Memory kullanımı ve health durumunu döner.
    """
    info = {
        "container": container_name,
        "running": False,
        "health": "not_found",
        "cpu_percent": "0.00%",
        "memory_usage": "0B / 0B",
        "memory_percent": "0.00%",
    }

    if not _is_container_running(container_name):
        return info

    info["running"] = True
    info["health"] = _get_container_health(container_name)

    # docker stats --no-stream
    rc, stdout, _ = _run_cmd(
        ["docker", "stats", "--no-stream", "--format",
         "{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}", container_name],
        timeout=15,
    )
    if rc == 0 and stdout:
        parts = stdout.split("|")
        if len(parts) == 3:
            info["cpu_percent"] = parts[0].strip()
            info["memory_usage"] = parts[1].strip()
            info["memory_percent"] = parts[2].strip()

    return info


# ─── Ana Orkestrasyon Fonksiyonları ──────────────────────────────────────
async def deploy_service(svc: ServiceDef) -> dict:
    """
    Tek bir servisi deploy eder:
    1. Pre-hook'ları çalıştır
    2. docker-compose up -d
    3. Health check bekle (max timeout)
    """
    result = {
        "service": svc.name,
        "container": svc.container_name,
        "step_id": svc.step_id,
        "group": svc.group,
        "success": False,
        "health": "unknown",
        "message": "",
        "duration_seconds": 0,
    }

    start_time = time.time()

    # ── 1. Pre-Hooks ──
    for hook_name in svc.pre_hooks:
        hook_fn = _PRE_HOOKS.get(hook_name)
        if hook_fn:
            wizard_logger.info(
                f"[Pre-Hook] {hook_name} çalıştırılıyor → {svc.name}",
                step_id=svc.step_id,
            )
            try:
                hook_fn()
            except Exception as exc:
                msg = f"[Pre-Hook HATA] {hook_name}: {exc}"
                wizard_logger.error(msg, step_id=svc.step_id)
                result["message"] = msg
                result["duration_seconds"] = round(time.time() - start_time, 1)
                return result

    # ── 2. Docker Compose Up ──
    wizard_logger.info(
        f"[Deploy] {svc.name} başlatılıyor (docker compose up -d)...",
        step_id=svc.step_id,
    )

    success, output = await asyncio.to_thread(_docker_compose_up, svc.name)
    if not success:
        msg = f"[Deploy HATA] {svc.name} başlatılamadı: {output}"
        wizard_logger.error(msg, step_id=svc.step_id)
        result["message"] = msg
        result["duration_seconds"] = round(time.time() - start_time, 1)
        return result

    # ── 3. Health Check Bekleme (max timeout saniye) ──
    wizard_logger.info(
        f"[HealthCheck] {svc.name} → healthy bekleniyor (max {svc.health_timeout}s)...",
        step_id=svc.step_id,
    )

    elapsed = 0
    while elapsed < svc.health_timeout:
        await asyncio.sleep(HEALTH_CHECK_INTERVAL)
        elapsed += HEALTH_CHECK_INTERVAL

        health = await asyncio.to_thread(_get_container_health, svc.container_name)
        running = await asyncio.to_thread(_is_container_running, svc.container_name)

        if health == "healthy":
            result["success"] = True
            result["health"] = "healthy"
            result["message"] = f"{svc.name} başarıyla deploy edildi ve healthy."
            result["duration_seconds"] = round(time.time() - start_time, 1)
            wizard_logger.info(
                f"[HealthCheck ✓] {svc.name} → healthy ({result['duration_seconds']}s)",
                step_id=svc.step_id,
            )
            return result

        if health == "unhealthy":
            msg = f"[HealthCheck ✗] {svc.name} → unhealthy (container çöktü)"
            wizard_logger.error(msg, step_id=svc.step_id)
            result["health"] = "unhealthy"
            result["message"] = msg
            result["duration_seconds"] = round(time.time() - start_time, 1)
            return result

        if not running:
            msg = f"[HealthCheck ✗] {svc.name} → container çalışmıyor (exited)"
            wizard_logger.error(msg, step_id=svc.step_id)
            result["health"] = "exited"
            result["message"] = msg
            result["duration_seconds"] = round(time.time() - start_time, 1)
            return result

        # health = "none" (healthcheck tanımsız) → running ise başarılı say
        if health == "none" and running:
            result["success"] = True
            result["health"] = "running"
            result["message"] = f"{svc.name} çalışıyor (healthcheck tanımsız, running kabul edildi)."
            result["duration_seconds"] = round(time.time() - start_time, 1)
            wizard_logger.info(
                f"[HealthCheck ~] {svc.name} → running (no healthcheck, accepted) ({result['duration_seconds']}s)",
                step_id=svc.step_id,
            )
            return result

    # Timeout
    msg = f"[HealthCheck ✗] {svc.name} → zaman aşımı ({svc.health_timeout}s)"
    wizard_logger.error(msg, step_id=svc.step_id)
    result["health"] = "timeout"
    result["message"] = msg
    result["duration_seconds"] = round(time.time() - start_time, 1)
    return result


async def deploy_step(step_id: str) -> list[dict]:
    """
    Belirli bir wizard step_id'sine ait tüm servisleri sırasıyla deploy eder.
    Bir servis fail ederse sonraki servislere geçmez.
    """
    services = [s for s in DEPLOYMENT_ORDER if s.step_id == step_id]
    if not services:
        wizard_logger.warning(
            f"Step {step_id} için deploy edilecek servis bulunamadı.",
            step_id=step_id,
        )
        return []

    results = []
    for svc in services:
        result = await deploy_service(svc)
        results.append(result)

        if not result["success"]:
            wizard_logger.error(
                f"[Orkestrasyon DURDURULDU] {svc.name} başarısız → sonraki servisler engellendi.",
                step_id=step_id,
            )
            break

    return results


async def deploy_all() -> list[dict]:
    """
    Tüm 16 servisi şartname sırasıyla deploy eder.
    Bir servis fail ederse zincir kırılır.
    """
    wizard_logger.info(
        "[Orkestrasyon] Tam deployment başlatılıyor — sıralı modda.",
        step_id="03",
    )

    all_results = []
    for svc in DEPLOYMENT_ORDER:
        result = await deploy_service(svc)
        all_results.append(result)

        if not result["success"]:
            wizard_logger.error(
                f"[Orkestrasyon DURDURULDU] {svc.name} (grup: {svc.group}) başarısız. "
                f"Kalan servisler engellendi.",
                step_id=svc.step_id,
            )
            break

    successful = sum(1 for r in all_results if r["success"])
    total = len(all_results)
    wizard_logger.info(
        f"[Orkestrasyon Özet] {successful}/{total} servis başarılı.",
        step_id="18",
    )

    return all_results


def get_all_container_statuses() -> list[dict]:
    """
    Tüm servislerin anlık CPU/RAM ve health durumunu döner.
    """
    statuses = []
    for svc in DEPLOYMENT_ORDER:
        stats = get_container_stats(svc.container_name)
        stats["service"] = svc.name
        stats["step_id"] = svc.step_id
        stats["group"] = svc.group
        statuses.append(stats)
    return statuses


# ─── Step → Hub Servis Adı Eşlemesi ──────────────────────────────────────
# Hub'daki services.service_name ile docker-compose servis adları
# farklı olabilir (Ör: domain-api → core-api). Bu harita farkları köprüler.
_DOCKER_TO_HUB_SERVICE: dict[str, str] = {
    "domain-api": "core-api",
}


def check_tier_authorization(step_id: str, allowed_services: list[str]) -> tuple[bool, list[str]]:
    """
    Verilen step_id'nin allowed_services listesiyle uyumunu kontrol eder.
    Döner: (authorized, unauthorized_service_names)
    """
    services = [s for s in DEPLOYMENT_ORDER if s.step_id == step_id]
    if not services:
        return True, []  # Servis-olmayan adımlar her zaman izinli

    unauthorized = []
    for svc in services:
        hub_name = _DOCKER_TO_HUB_SERVICE.get(svc.name, svc.name)
        if hub_name not in allowed_services:
            unauthorized.append(hub_name)

    return len(unauthorized) == 0, unauthorized


def get_service_by_step(step_id: str) -> list[ServiceDef]:
    """Belirli bir step_id'ye ait servisleri döner."""
    return [s for s in DEPLOYMENT_ORDER if s.step_id == step_id]


def get_deployment_order() -> list[dict]:
    """Deployment sırasını JSON-serializable formda döner."""
    return [
        {
            "name": s.name,
            "container": s.container_name,
            "step_id": s.step_id,
            "group": s.group,
            "health_timeout": s.health_timeout,
        }
        for s in DEPLOYMENT_ORDER
    ]


# ─── Tier → Kaynak Eşleme ─────────────────────────────────────────────────
TIER_RESOURCE_MAP = {
    "Standart": {
        "masking_engine_mode": "minimal",
        "max_workers": 2,
        "data_retention": "7d",
    },
    "Professional": {
        "masking_engine_mode": "standard",
        "max_workers": 8,
        "data_retention": "30d",
    },
    "Enterprise": {
        "masking_engine_mode": "enterprise",
        "max_workers": 16,
        "data_retention": "365d",
    },
}


# ─── Docker Compose Render (Jinja2 Template → docker-compose.yml) ────────
def render_compose(context: dict) -> str:
    """
    Jinja2 template'ini allowed_services ve diğer değişkenlerle render eder.
    context: {"domain": "...", "allowed_services": [...], "tier": "...", ...}
    """
    from jinja2 import Environment, FileSystemLoader

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(COMPOSE_TEMPLATE)
    return template.render(**context)


def generate_compose_file(domain: str, allowed_services: list[str],
                          tier: str = "Standart",
                          extra_context: dict = None) -> str:
    """
    Tier'a göre docker-compose.yml dosyasını üretir ve /opt/mega-stack/'e yazar.
    allowed_services listesine göre AI servisleri koşullu olarak dahil edilir.
    tier parametresi kaynak limitlerini (CPU/RAM) ve MaskingEngine modunu belirler.
    """
    context = {
        "domain": domain,
        "allowed_services": allowed_services,
        "tier": tier,
    }
    # Tier kaynak haritasını context'e ekle
    tier_resources = TIER_RESOURCE_MAP.get(tier, TIER_RESOURCE_MAP["Standart"])
    context.update(tier_resources)

    if extra_context:
        context.update(extra_context)

    rendered = render_compose(context)

    with open(COMPOSE_FILE, "w", encoding="utf-8") as f:
        f.write(rendered)

    wizard_logger.info(
        f"[Compose] docker-compose.yml üretildi — Tier: {tier}, "
        f"{len(allowed_services)} izinli servis, domain: {domain}",
        step_id="02",
    )
    return COMPOSE_FILE
