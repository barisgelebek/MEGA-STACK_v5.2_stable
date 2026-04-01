"""
MEGA-STACK v2.5 Installation Wizard — Analytics Collector (Ticari İstihbarat)
══════════════════════════════════════════════════════════════════════════════
Best-effort, anonim kurulum analytics'i Master Hub'a gönderir.
ASLA kurulum akışını bloklayamaz — tüm hatalar sessizce yutulur.

Kullanım:
    from core.analytics import send_install_event

    await send_install_event("install_complete", state)
    await send_install_event("install_error", state, failed_step_id="07", failed_step_name="CertDumper Setup")
"""

import asyncio
import logging
import os
import platform

log = logging.getLogger("analytics")

# Master Hub analytics endpoint
HUB_ANALYTICS_URL = "https://api.barisgelebek.com/api/analytics/collect"
WIZARD_VERSION = "2.5.0"
TIMEOUT_SEC = 5


def _collect_system_info() -> dict:
    """Anonim donanım bilgisi topla — PII yok."""
    info = {}
    try:
        info["cpu_cores"] = os.cpu_count()
    except Exception:
        pass

    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    info["total_ram_gb"] = round(kb / 1048576, 1)
                    break
    except Exception:
        pass

    try:
        st = os.statvfs("/")
        info["total_disk_gb"] = round(st.f_blocks * st.f_frsize / (1024 ** 3), 1)
    except Exception:
        pass

    try:
        info["os_name"] = f"{platform.system()} {platform.release()}"[:64]
    except Exception:
        pass

    return info


async def send_install_event(
    event_type: str,
    state,
    failed_step_id: str = None,
    failed_step_name: str = None,
    install_duration_sec: int = None,
) -> None:
    """Best-effort analytics event gönder — ASLA exception fırlatmaz."""
    try:
        import urllib.request
        import json

        sys_info = _collect_system_info()

        payload = {
            "event_type": event_type,
            "tier": getattr(state, "tier", None),
            "wizard_version": WIZARD_VERSION,
            "install_duration_sec": install_duration_sec,
            "failed_step_id": failed_step_id,
            "failed_step_name": failed_step_name,
            "service_count": len(getattr(state, "allowed_services", [])),
            **sys_info,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            HUB_ANALYTICS_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        # Non-blocking: thread'e delege et, timeout ile sınırla
        await asyncio.wait_for(
            asyncio.to_thread(urllib.request.urlopen, req, timeout=TIMEOUT_SEC),
            timeout=TIMEOUT_SEC + 2,
        )
        log.info("Analytics event gönderildi: %s", event_type)

    except Exception:
        # Best-effort — asla bloklamaz, asla exception fırlatmaz
        log.debug("Analytics event gönderilemedi (best-effort, normal): %s", event_type)
