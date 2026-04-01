"""
MEGA-STACK v2.5 Installation Wizard — Environment & Secrets Manager
Fernet şifreleme motoru + fiziksel secrets/ dosya yönetimi.
KIRMIZI ÇİZGİ: Fiziksel secrets/ dosyaları DB senkronizasyonunda silinmez,
Docker mount'ları için her zaman güncel tutulur.
"""

import os
import secrets
import string
from datetime import datetime, timezone
from pathlib import Path

from cryptography.fernet import Fernet

from core.logger import wizard_logger

BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_DIR = Path("/opt/mega-stack/secrets")


# ─── Fernet Şifreleme Motoru ────────────────────────────────────────────
class FernetEngine:
    """
    Fernet tabanlı simetrik şifreleme motoru.
    MEGA_MASTER_KEY ile çalışır — key yoksa işlem reddedilir.
    """

    def __init__(self, master_key: bytes | None = None):
        self._fernet = None
        if master_key:
            self.set_key(master_key)

    def set_key(self, master_key: bytes) -> None:
        """Fernet anahtarını ayarlar."""
        self._fernet = Fernet(master_key)
        wizard_logger.info(
            "[Security Audit] Fernet motoru aktif.", step_id="00"
        )

    @property
    def is_ready(self) -> bool:
        return self._fernet is not None

    def _ensure_ready(self) -> None:
        if not self.is_ready:
            raise RuntimeError(
                "Fernet motoru hazır değil — MEGA_MASTER_KEY henüz türetilmedi."
            )

    def encrypt(self, plaintext: str) -> str:
        """Düz metni şifreler, base64 encoded string döner."""
        self._ensure_ready()
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        """Şifreli metni çözer, düz metin döner."""
        self._ensure_ready()
        return self._fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")


# Singleton instance — tüm modüller tarafından paylaşılır
fernet_engine = FernetEngine()


# ─── Güvenli Şifre Üretici ──────────────────────────────────────────────
def generate_secure_password(length: int = 32) -> str:
    """Kriptografik olarak güvenli rastgele şifre üretir."""
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


# ─── Fiziksel Secrets Dosya Yönetimi ────────────────────────────────────
class SecretsManager:
    """
    /opt/mega-stack/secrets/ altındaki fiziksel dosyaları yönetir.
    Docker mount'ları canlı dosya beklediği için bu dosyalar silinmez,
    sadece güncellenir.
    """

    def __init__(self, secrets_dir: Path = SECRETS_DIR):
        self.secrets_dir = secrets_dir

    def _ensure_dir(self) -> None:
        self.secrets_dir.mkdir(parents=True, exist_ok=True)

    def write_secret(self, filename: str, value: str) -> Path:
        """
        Fiziksel secret dosyası oluşturur/günceller.
        Dosya izni her zaman 0600 olarak set edilir.
        """
        self._ensure_dir()
        file_path = self.secrets_dir / filename
        file_path.write_text(value, encoding="utf-8")
        os.chmod(str(file_path), 0o600)
        wizard_logger.info(
            f"[Security Audit] Secret dosyası güncellendi: {filename} (chmod 600)",
            step_id="00",
        )
        return file_path

    def read_secret(self, filename: str) -> str | None:
        """Fiziksel secret dosyasını okur (varsa)."""
        file_path = self.secrets_dir / filename
        if file_path.exists():
            return file_path.read_text(encoding="utf-8").strip()
        return None

    def exists(self, filename: str) -> bool:
        """Secret dosyasının var olup olmadığını kontrol eder."""
        return (self.secrets_dir / filename).exists()

    def list_secrets(self) -> list[dict]:
        """Mevcut secret dosyalarını listeler (içerik gösterilmez)."""
        self._ensure_dir()
        result = []
        for item in self.secrets_dir.iterdir():
            if item.is_file():
                stat = item.stat()
                result.append({
                    "filename": item.name,
                    "size_bytes": stat.st_size,
                    "permissions": oct(stat.st_mode)[-3:],
                    "modified": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                })
        return result


# Singleton instance
secrets_manager = SecretsManager()


# ─── DB + Fiziksel Dosya Senkronizasyonu ─────────────────────────────────
def save_credential(
    conn,
    service_name: str,
    username: str | None = None,
    password: str | None = None,
    api_key: str | None = None,
    extra: str | None = None,
    secret_filename: str | None = None,
) -> None:
    """
    Servis kimlik bilgisini hem DB'ye (şifreli) hem de fiziksel dosyaya yazar.
    KIRMIZI ÇİZGİ: Fiziksel dosyalar silinmez, sadece güncellenir.
    """
    now = datetime.now(timezone.utc).isoformat()

    # Şifreleme (Fernet hazırsa)
    password_enc = fernet_engine.encrypt(password) if password and fernet_engine.is_ready else password
    api_key_enc = fernet_engine.encrypt(api_key) if api_key and fernet_engine.is_ready else api_key
    extra_enc = fernet_engine.encrypt(extra) if extra and fernet_engine.is_ready else extra

    # DB'ye yaz
    conn.execute(
        """INSERT OR REPLACE INTO service_credentials
           (service_name, username, password_enc, api_key_enc, extra_enc, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (service_name, username, password_enc, api_key_enc, extra_enc, now, now),
    )
    conn.commit()

    # Fiziksel dosyaya yaz (Docker mount'ları için)
    if secret_filename and password:
        secrets_manager.write_secret(secret_filename, password)

    wizard_logger.info(
        f"[Security Audit] Credential kaydedildi: {service_name} "
        f"(DB + {'fiziksel dosya' if secret_filename else 'yalnızca DB'})",
        step_id="00",
    )


def get_credential(conn, service_name: str) -> dict | None:
    """Servis kimlik bilgisini DB'den okur ve şifresini çözer."""
    row = conn.execute(
        "SELECT * FROM service_credentials WHERE service_name = ?",
        (service_name,),
    ).fetchone()

    if row is None:
        return None

    result = dict(row)

    # Şifre çözme (Fernet hazırsa)
    if fernet_engine.is_ready:
        for field in ("password_enc", "api_key_enc", "extra_enc"):
            if result.get(field):
                try:
                    result[f"{field}_decrypted"] = fernet_engine.decrypt(result[field])
                except Exception:
                    result[f"{field}_decrypted"] = None

    return result


def save_system_setting(
    conn,
    key: str,
    value: str,
    encrypted: bool = False,
) -> None:
    """Sistem ayarını DB'ye kaydeder."""
    now = datetime.now(timezone.utc).isoformat()
    actual_value = fernet_engine.encrypt(value) if encrypted and fernet_engine.is_ready else value
    conn.execute(
        """INSERT OR REPLACE INTO system_settings (key, value, encrypted, updated_at)
           VALUES (?, ?, ?, ?)""",
        (key, actual_value, 1 if encrypted else 0, now),
    )
    conn.commit()


def get_system_setting(conn, key: str) -> str | None:
    """Sistem ayarını DB'den okur."""
    row = conn.execute(
        "SELECT value, encrypted FROM system_settings WHERE key = ?",
        (key,),
    ).fetchone()
    if row is None:
        return None
    value, is_encrypted = row["value"], row["encrypted"]
    if is_encrypted and fernet_engine.is_ready:
        try:
            return fernet_engine.decrypt(value)
        except Exception:
            return None
    return value
