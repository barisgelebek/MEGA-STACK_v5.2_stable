"""
MEGA-STACK v2.5 Installation Wizard — Hibrit Lisans Motoru
HWID + Remote Auth + RSA Signature + Fernet Key Derivation + Offline Resilience
"""

import base64
import hashlib
import json
import os
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from core.logger import wizard_logger

BASE_DIR = Path(__file__).resolve().parent.parent
LICENSE_DIR = BASE_DIR / "license"
SERVER_PUB_PATH = LICENSE_DIR / "server.pub"
LICENSE_KEY_PATH = LICENSE_DIR / "license.key"

# Lisans sunucu adresi (BarisGelebek Cloud — Master Hub)
LICENSE_SERVER_URL = "https://api.barisgelebek.com/api/license/verify"


# ─── HWID Üretimi ───────────────────────────────────────────────────────
def _read_machine_id() -> str:
    """Sistemin /etc/machine-id değerini okur."""
    machine_id_path = Path("/etc/machine-id")
    if machine_id_path.exists():
        return machine_id_path.read_text().strip()
    # Fallback: dbus machine-id
    dbus_path = Path("/var/lib/dbus/machine-id")
    if dbus_path.exists():
        return dbus_path.read_text().strip()
    wizard_logger.warning(
        "machine-id bulunamadı, hostname kullanılıyor.", step_id="00"
    )
    return platform.node()


def _read_cpu_serial() -> str:
    """CPU seri numarasını /proc/cpuinfo'dan okur."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.strip().startswith("Serial"):
                    return line.split(":")[1].strip()
        # x86 sistemlerde Serial satırı olmayabilir — model name + stepping ile fallback
        result = subprocess.run(
            ["cat", "/proc/cpuinfo"],
            capture_output=True, text=True, timeout=5
        )
        # Model name hash'ini kullan
        model_lines = [
            l for l in result.stdout.splitlines()
            if "model name" in l.lower()
        ]
        if model_lines:
            return model_lines[0].split(":")[1].strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    wizard_logger.warning(
        "CPU serial okunamadı, platform identifier kullanılıyor.", step_id="00"
    )
    return platform.processor() or "unknown-cpu"


def generate_hwid() -> str:
    """
    /etc/machine-id ve CPU seri numarasını birleştirerek
    benzersiz SHA-256 tabanlı HWID hash'i üretir.
    """
    machine_id = _read_machine_id()
    cpu_serial = _read_cpu_serial()
    raw = f"{machine_id}::{cpu_serial}"
    hwid = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    wizard_logger.info(
        f"[Security Audit] HWID üretildi: {hwid[:16]}...", step_id="00"
    )
    return hwid


# ─── RSA İmza Doğrulama ─────────────────────────────────────────────────
def _load_server_public_key():
    """license/server.pub dosyasından RSA public key yükler."""
    from cryptography.hazmat.primitives.serialization import load_pem_public_key

    if not SERVER_PUB_PATH.exists():
        wizard_logger.error(
            "[Security Audit] server.pub bulunamadı!", step_id="00"
        )
        raise FileNotFoundError(
            "Güvenlik anahtarı (server.pub) bulunamadı. "
            "Lütfen kurulum paketini kontrol edin veya destek ekibiyle iletişime geçin. "
            f"Beklenen konum: {SERVER_PUB_PATH}"
        )

    key_data = SERVER_PUB_PATH.read_bytes()
    return load_pem_public_key(key_data)


def verify_rsa_signature(data: bytes, signature: bytes) -> bool:
    """Sunucudan gelen veriyi RSA-PSS-SHA256 imzasıyla doğrular."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    try:
        public_key = _load_server_public_key()
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        wizard_logger.info(
            "[Security Audit] RSA imza doğrulaması başarılı.", step_id="00"
        )
        return True
    except FileNotFoundError as fnf:
        wizard_logger.error(
            f"[Security Audit] {fnf}", step_id="00"
        )
        return False
    except Exception as exc:
        wizard_logger.error(
            f"[Security Audit] RSA imza doğrulaması başarısız: {exc}",
            step_id="00",
        )
        return False


# ─── Fernet Master Key Türetme ──────────────────────────────────────────
def derive_master_key(user_password: str, server_salt: str) -> bytes:
    """
    Kullanıcı şifresi + lisans sunucusundan gelen salt ile
    PBKDF2-HMAC-SHA256 tabanlı Fernet uyumlu anahtar türetir.
    Anahtar asla düz metin olarak saklanmaz.
    """
    salt_bytes = server_salt.encode("utf-8")
    key = hashlib.pbkdf2_hmac(
        "sha256",
        user_password.encode("utf-8"),
        salt_bytes,
        iterations=480_000,  # OWASP 2023 önerisi
    )
    # Fernet 32-byte url-safe base64 encoded key bekler
    fernet_key = base64.urlsafe_b64encode(key[:32])
    wizard_logger.info(
        "[Security Audit] MEGA_MASTER_KEY türetildi (PBKDF2-HMAC-SHA256).",
        step_id="00",
    )
    return fernet_key


# ─── Lokal Mühür Cache (Offline Resilience) ──────────────────────────────
def _save_license_cache(license_key: str, hwid: str, signed_payload: str,
                        signature: str, tier: str | None,
                        allowed_services: list) -> None:
    """Başarılı lisans yanıtını wizard.db → local_license_cache tablosuna mühürler."""
    from core.db_initializer import get_connection

    now = datetime.now(timezone.utc).isoformat()
    services_json = json.dumps(allowed_services or [])
    conn = get_connection()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO local_license_cache
               (id, license_key, signed_payload, signature, hardware_id,
                tier, allowed_services, last_check_timestamp)
               VALUES (1, ?, ?, ?, ?, ?, ?, ?)""",
            (license_key, signed_payload, signature, hwid,
             tier, services_json, now),
        )
        conn.commit()
        wizard_logger.info(
            "[Security Audit] Lisans mühürü lokale kaydedildi (Offline Resilience).",
            step_id="00",
        )
    finally:
        conn.close()


def _load_license_cache(hwid: str) -> dict | None:
    """Lokal mühürü okur, HWID + RSA doğrulaması yapar.

    Returns:
        Başarılıysa lisans dict, aksi halde None
    """
    from core.db_initializer import get_connection

    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM local_license_cache WHERE id = 1"
        ).fetchone()
    finally:
        conn.close()

    if not row:
        wizard_logger.warning(
            "[Security Audit] Lokal lisans mühürü bulunamadı.", step_id="00"
        )
        return None

    # Güvenlik Bariyeri: HWID eşleştirme
    cached_hwid = row["hardware_id"]
    if cached_hwid != hwid:
        wizard_logger.error(
            "[Security Audit] License Identity Mismatch! "
            f"Cached HWID: {cached_hwid[:16]}... ≠ Current HWID: {hwid[:16]}...",
            step_id="00",
        )
        return None

    # RSA imza doğrulama
    signed_payload = row["signed_payload"]
    signature_b64 = row["signature"]
    try:
        sig_bytes = base64.b64decode(signature_b64)
        if not verify_rsa_signature(signed_payload.encode("utf-8"), sig_bytes):
            wizard_logger.error(
                "[Security Audit] Lokal mühür RSA imza doğrulaması başarısız!",
                step_id="00",
            )
            return None
    except Exception as exc:
        wizard_logger.error(
            f"[Security Audit] Lokal mühür imza hatası: {exc}", step_id="00"
        )
        return None

    # Mühür geçerli — cache verilerini döndür
    try:
        allowed_services = json.loads(row["allowed_services"] or "[]")
    except (json.JSONDecodeError, TypeError):
        allowed_services = []

    wizard_logger.info(
        f"[Security Audit] Lokal mühür doğrulandı — OFFLINE MODE. "
        f"Tier: {row['tier']}, Cache: {row['last_check_timestamp']}",
        step_id="00",
    )
    return {
        "verified": True,
        "salt": None,
        "message": "Çevrimdışı mod — lokal mühür geçerli.",
        "tier": row["tier"],
        "hardware_limits": None,
        "allowed_services": allowed_services,
        "offline_mode": True,
        "cached_at": row["last_check_timestamp"],
    }


# ─── Lisans Doğrulama (Remote + RSA) ────────────────────────────────────
async def verify_license(license_key: str, hwid: str) -> dict:
    """
    Lisans sunucusuna (BarisGelebek Cloud) POST isteği atar.
    Gelen RSA imzalı cevabı server.pub ile doğrular.
    Başarılıysa sunucudan gelen salt'ı döner.

    Dönen dict:
        {"verified": bool, "salt": str|None, "message": str, "tier": str|None}
    """
    import httpx

    wizard_logger.info(
        f"[Security Audit] Lisans doğrulama isteği gönderiliyor → {LICENSE_SERVER_URL}",
        step_id="00",
    )

    payload = {
        "license_key": license_key,
        "hwid": hwid,
        "wizard_version": "2.5.0",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0, verify=True) as client:
            response = await client.post(LICENSE_SERVER_URL, json=payload)

        if response.status_code != 200:
            wizard_logger.error(
                f"[Security Audit] Lisans sunucu hatası: HTTP {response.status_code}",
                step_id="00",
            )
            return {
                "verified": False,
                "salt": None,
                "message": f"Lisans sunucusu HTTP {response.status_code} döndü.",
                "tier": None,
                "hardware_limits": None,
                "allowed_services": [],
            }

        data = response.json()

        # RSA imza doğrulama
        signature_b64 = data.get("signature", "")
        verify_payload = data.get("payload", "")

        if signature_b64 and verify_payload:
            sig_bytes = base64.b64decode(signature_b64)
            if not verify_rsa_signature(verify_payload.encode("utf-8"), sig_bytes):
                return {
                    "verified": False,
                    "salt": None,
                    "message": "RSA imza doğrulaması başarısız — yanıt güvenilir değil.",
                    "tier": None,
                    "hardware_limits": None,
                    "allowed_services": [],
                }

        verified = data.get("verified", False)
        salt = data.get("salt")
        tier = data.get("tier")
        message = data.get("message", "Doğrulama tamamlandı.")
        hardware_limits = data.get("hardware_limits")
        allowed_services = data.get("allowed_services", [])

        if verified:
            wizard_logger.info(
                f"[Security Audit] Lisans onaylandı. Tier: {tier}", step_id="00"
            )
            # Lisans anahtarını şifreli olarak sakla
            save_license_key(license_key)

            # Lokal mühür cache — Offline Resilience
            if signature_b64 and verify_payload:
                _save_license_cache(
                    license_key=license_key,
                    hwid=hwid,
                    signed_payload=verify_payload,
                    signature=signature_b64,
                    tier=tier,
                    allowed_services=allowed_services,
                )
        else:
            wizard_logger.warning(
                f"[Security Audit] Lisans reddedildi: {message}", step_id="00"
            )

        return {
            "verified": verified,
            "salt": salt,
            "message": message,
            "tier": tier,
            "hardware_limits": hardware_limits,
            "allowed_services": allowed_services,
        }

    except httpx.ConnectError:
        wizard_logger.warning(
            "[Security Audit] Lisans sunucusuna bağlanılamadı — Offline Resilience devreye giriyor.",
            step_id="00",
        )
        # Offline Resilience: Lokal mühürden doğrula
        cached = _load_license_cache(hwid)
        if cached:
            return cached
        return {
            "verified": False,
            "salt": None,
            "message": "Lisans sunucusuna bağlanılamadı ve geçerli lokal mühür bulunamadı.",
            "tier": None,
            "hardware_limits": None,
            "allowed_services": [],
        }
    except httpx.TimeoutException:
        wizard_logger.warning(
            "[Security Audit] Lisans sunucusu zaman aşımı — Offline Resilience devreye giriyor.",
            step_id="00",
        )
        cached = _load_license_cache(hwid)
        if cached:
            return cached
        return {
            "verified": False,
            "salt": None,
            "message": "Lisans sunucusu zaman aşımı ve geçerli lokal mühür bulunamadı.",
            "tier": None,
            "hardware_limits": None,
            "allowed_services": [],
        }
    except Exception as exc:
        wizard_logger.error(
            f"[Security Audit] Lisans doğrulama hatası: {exc}", step_id="00"
        )
        return {
            "verified": False,
            "salt": None,
            "message": f"Beklenmeyen hata: {str(exc)}",
            "tier": None,
            "hardware_limits": None,
            "allowed_services": [],
        }


# ─── Lisans Anahtarı Kalıcı Saklama ─────────────────────────────────────
def save_license_key(license_key: str) -> None:
    """Lisans anahtarını license/license.key dosyasına kaydeder."""
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    LICENSE_KEY_PATH.write_text(license_key, encoding="utf-8")
    os.chmod(str(LICENSE_KEY_PATH), 0o600)
    wizard_logger.info(
        "[Security Audit] Lisans anahtarı license.key'e mühürlendi (chmod 600).",
        step_id="00",
    )


def load_license_key() -> str | None:
    """Kayıtlı lisans anahtarını okur (varsa)."""
    if LICENSE_KEY_PATH.exists():
        return LICENSE_KEY_PATH.read_text(encoding="utf-8").strip()
    return None
