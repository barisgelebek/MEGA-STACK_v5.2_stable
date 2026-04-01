"""
MEGA-STACK v2.5 Installation Wizard — Database Initializer
SQLite WAL Mode + v2.5 Schema + Restore Intelligence
KIRMIZI ÇİZGİ: WAL Mode aktif edilmeden tablo oluşturulamaz.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from core.logger import wizard_logger

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "wizard.db"
BACKUPS_DIR = Path("/opt/mega-stack/backups")
MEGA_STACK_BACKUPS = Path("/opt/mega-stack-backups")

SCHEMA_VERSION = "2.5.0"


# ─── Veritabanı Bağlantısı ──────────────────────────────────────────────
def get_connection() -> sqlite3.Connection:
    """WAL modunda SQLite bağlantısı oluşturur."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # KIRMIZI ÇİZGİ: İlk satırda WAL modu aktif edilmeli
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")

    return conn


# ─── Tablo Oluşturma (v2.5 Schema) ──────────────────────────────────────
def _create_tables(conn: sqlite3.Connection) -> None:
    """v2.5 şemasına uygun tüm tabloları oluşturur."""

    conn.executescript("""
        -- Şema versiyon takibi
        CREATE TABLE IF NOT EXISTS schema_info (
            id          INTEGER PRIMARY KEY DEFAULT 1,
            version     TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        );

        -- Wizard kurulum durumu
        CREATE TABLE IF NOT EXISTS wizard_state (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            step_id         TEXT NOT NULL,
            step_name       TEXT NOT NULL,
            status          TEXT NOT NULL DEFAULT 'pending',
            started_at      TEXT,
            completed_at    TEXT,
            error_message   TEXT,
            metadata        TEXT
        );

        -- Servis kimlik bilgileri (Fernet ile şifreli)
        CREATE TABLE IF NOT EXISTS service_credentials (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name    TEXT NOT NULL UNIQUE,
            username        TEXT,
            password_enc    TEXT,
            api_key_enc     TEXT,
            extra_enc       TEXT,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        );

        -- Sistem ayarları (key-value)
        CREATE TABLE IF NOT EXISTS system_settings (
            key         TEXT PRIMARY KEY,
            value       TEXT NOT NULL,
            encrypted   INTEGER NOT NULL DEFAULT 0,
            updated_at  TEXT NOT NULL
        );

        -- AI provider token ve konfigürasyonları
        CREATE TABLE IF NOT EXISTS ai_providers (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_name   TEXT NOT NULL UNIQUE,
            api_key_enc     TEXT,
            model           TEXT,
            is_active       INTEGER NOT NULL DEFAULT 1,
            config          TEXT,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        );

        -- Lisans bilgileri
        CREATE TABLE IF NOT EXISTS license_info (
            id              INTEGER PRIMARY KEY DEFAULT 1,
            hwid            TEXT NOT NULL,
            license_key_enc TEXT,
            tier            TEXT,
            verified_at     TEXT,
            salt_enc        TEXT,
            server_response TEXT
        );

        -- Domain yapılandırması
        CREATE TABLE IF NOT EXISTS domain_config (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            domain          TEXT NOT NULL,
            domain_type     TEXT NOT NULL DEFAULT 'static',
            cloudflare_zone TEXT,
            ssl_mode        TEXT NOT NULL DEFAULT 'full_strict',
            is_primary      INTEGER NOT NULL DEFAULT 0,
            created_at      TEXT NOT NULL
        );

        -- Lokal lisans mühür cache (Offline Resilience)
        CREATE TABLE IF NOT EXISTS local_license_cache (
            id                   INTEGER PRIMARY KEY DEFAULT 1,
            license_key          TEXT NOT NULL,
            signed_payload       TEXT NOT NULL,
            signature            TEXT NOT NULL,
            hardware_id          TEXT NOT NULL,
            tier                 TEXT,
            allowed_services     TEXT,
            last_check_timestamp TEXT NOT NULL
        );
    """)


def _seed_schema_version(conn: sqlite3.Connection) -> None:
    """Şema versiyon kaydını ekler/günceller."""
    now = datetime.now(timezone.utc).isoformat()
    existing = conn.execute("SELECT version FROM schema_info WHERE id = 1").fetchone()

    if existing is None:
        conn.execute(
            "INSERT INTO schema_info (id, version, created_at, updated_at) VALUES (1, ?, ?, ?)",
            (SCHEMA_VERSION, now, now),
        )
    else:
        conn.execute(
            "UPDATE schema_info SET version = ?, updated_at = ? WHERE id = 1",
            (SCHEMA_VERSION, now),
        )


def _seed_default_settings(conn: sqlite3.Connection) -> None:
    """Varsayılan sistem ayarlarını ekler."""
    now = datetime.now(timezone.utc).isoformat()
    defaults = {
        "wizard_version": SCHEMA_VERSION,
        "install_mode": "fresh",
        "branding_name": "MEGA-STACK",
    }
    for key, value in defaults.items():
        conn.execute(
            """INSERT OR IGNORE INTO system_settings (key, value, encrypted, updated_at)
               VALUES (?, ?, 0, ?)""",
            (key, value, now),
        )


# ─── Ana Başlatma Fonksiyonu ─────────────────────────────────────────────
def initialize_database() -> sqlite3.Connection:
    """
    v2.5 veritabanını başlatır:
    1. WAL Mode aktif edilir (KIRMIZI ÇİZGİ)
    2. Tablolar oluşturulur
    3. Şema versiyonu seed edilir
    """
    wizard_logger.info(
        "[Security Audit] Veritabanı başlatılıyor — WAL Mode zorunlu.",
        step_id="00",
    )

    conn = get_connection()

    # WAL modu doğrula
    result = conn.execute("PRAGMA journal_mode;").fetchone()
    journal_mode = result[0] if result else "unknown"

    if journal_mode.lower() != "wal":
        wizard_logger.critical(
            f"[Security Audit] WAL Mode aktif edilemedi! Mevcut mod: {journal_mode}",
            step_id="00",
        )
        raise RuntimeError(f"KIRMIZI ÇİZGİ İHLALİ: WAL Mode aktif değil ({journal_mode})")

    wizard_logger.info(
        "[Security Audit] WAL Mode doğrulandı ✓", step_id="00"
    )

    _create_tables(conn)
    _seed_schema_version(conn)
    _seed_default_settings(conn)
    conn.commit()

    wizard_logger.info(
        f"[Security Audit] Veritabanı v{SCHEMA_VERSION} şemasıyla hazır: {DB_PATH}",
        step_id="00",
    )
    return conn


# ─── Restore Intelligence ───────────────────────────────────────────────
def scan_backups() -> list[dict]:
    """
    /opt/mega-stack/backups ve /opt/mega-stack-backups dizinlerini
    tarayarak geçerli yedek dosyalarını (.tar.gz, .bak, .db, .sqlite3)
    bulur ve listeler.
    """
    backups = []
    search_dirs = [BACKUPS_DIR, MEGA_STACK_BACKUPS]
    valid_extensions = {".tar.gz", ".bak", ".db", ".sqlite3"}

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        # Dizin içinde doğrudan dosyaları tara
        for item in search_dir.iterdir():
            if item.is_file():
                suffix = item.suffix
                # .tar.gz için çift uzantı kontrolü
                if item.name.endswith(".tar.gz"):
                    suffix = ".tar.gz"
                if suffix in valid_extensions:
                    stat = item.stat()
                    backups.append({
                        "path": str(item),
                        "filename": item.name,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "modified": datetime.fromtimestamp(
                            stat.st_mtime, tz=timezone.utc
                        ).isoformat(),
                        "type": suffix.lstrip("."),
                    })
            elif item.is_dir():
                # Alt dizinlerde de ara (tarih bazlı yedek klasörleri)
                for sub_item in item.rglob("*"):
                    if sub_item.is_file():
                        suffix = sub_item.suffix
                        if sub_item.name.endswith(".tar.gz"):
                            suffix = ".tar.gz"
                        if suffix in valid_extensions:
                            stat = sub_item.stat()
                            backups.append({
                                "path": str(sub_item),
                                "filename": sub_item.name,
                                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                                "modified": datetime.fromtimestamp(
                                    stat.st_mtime, tz=timezone.utc
                                ).isoformat(),
                                "type": suffix.lstrip("."),
                                "parent_dir": item.name,
                            })

    # Tarihe göre sırala (en yeni ilk)
    backups.sort(key=lambda b: b["modified"], reverse=True)

    wizard_logger.info(
        f"[Security Audit] Yedek taraması tamamlandı: {len(backups)} dosya bulundu.",
        step_id="00",
    )
    return backups


def check_schema_version(db_path: str) -> dict:
    """
    Verilen yedek veritabanının şema versiyonunu kontrol eder.
    v2.2 veya altıysa migration gerektiğini bildirir.
    """
    result = {
        "path": db_path,
        "version": None,
        "needs_migration": False,
        "migration_type": None,
    }

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        # SQLite mi yoksa JSON tabanlı mı kontrol et
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = [t["name"] for t in tables]

        if "schema_info" in table_names:
            row = conn.execute(
                "SELECT version FROM schema_info WHERE id = 1"
            ).fetchone()
            if row:
                result["version"] = row["version"]

                # Versiyon karşılaştırma
                try:
                    major, minor, _ = result["version"].split(".")
                    ver_num = int(major) * 100 + int(minor) * 10
                    if ver_num < 250:  # v2.5.0 = 250
                        result["needs_migration"] = True
                        result["migration_type"] = "schema_upgrade"
                except ValueError:
                    result["needs_migration"] = True
                    result["migration_type"] = "unknown_version"
        else:
            # schema_info tablosu yok — çok eski versiyon veya JSON tabanlı
            result["version"] = "pre-2.5"
            result["needs_migration"] = True
            result["migration_type"] = "json_to_sqlite"

        conn.close()
    except sqlite3.DatabaseError:
        result["version"] = "invalid"
        result["needs_migration"] = True
        result["migration_type"] = "not_sqlite"
    except Exception as exc:
        wizard_logger.error(
            f"[Security Audit] Yedek şema kontrolü hatası: {exc}", step_id="00"
        )
        result["version"] = "error"
        result["needs_migration"] = True
        result["migration_type"] = "check_failed"

    if result["needs_migration"]:
        wizard_logger.warning(
            f"[Security Audit] Yedek migration gerekli: {db_path} "
            f"(v{result['version']} → v{SCHEMA_VERSION}, tip: {result['migration_type']})",
            step_id="00",
        )

    return result


def migrate_json_to_sqlite(json_dir: str, conn: sqlite3.Connection) -> bool:
    """
    Eski yapıdaki dağınık JSON dosyalarını v2.5 SQLite şemasına migrate eder.
    Bu fonksiyon, v2.2 ve öncesi yedekler için hazır tutulur.
    """
    wizard_logger.info(
        f"[Security Audit] JSON → SQLite migration başlatılıyor: {json_dir}",
        step_id="00",
    )

    json_path = Path(json_dir)
    migrated_count = 0

    # status.json → system_settings
    status_file = json_path / "status.json"
    if status_file.exists():
        try:
            data = json.loads(status_file.read_text(encoding="utf-8"))
            now = datetime.now(timezone.utc).isoformat()
            for key, value in data.items():
                conn.execute(
                    """INSERT OR REPLACE INTO system_settings (key, value, encrypted, updated_at)
                       VALUES (?, ?, 0, ?)""",
                    (f"migrated_{key}", json.dumps(value) if isinstance(value, (dict, list)) else str(value), now),
                )
            migrated_count += 1
        except (json.JSONDecodeError, OSError) as exc:
            wizard_logger.warning(f"status.json migration hatası: {exc}", step_id="00")

    # config.json → system_settings
    config_file = json_path / "config.json"
    if config_file.exists():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
            now = datetime.now(timezone.utc).isoformat()
            for key, value in data.items():
                conn.execute(
                    """INSERT OR REPLACE INTO system_settings (key, value, encrypted, updated_at)
                       VALUES (?, ?, 0, ?)""",
                    (f"migrated_{key}", json.dumps(value) if isinstance(value, (dict, list)) else str(value), now),
                )
            migrated_count += 1
        except (json.JSONDecodeError, OSError) as exc:
            wizard_logger.warning(f"config.json migration hatası: {exc}", step_id="00")

    conn.commit()

    wizard_logger.info(
        f"[Security Audit] JSON → SQLite migration tamamlandı. "
        f"{migrated_count} dosya işlendi.",
        step_id="00",
    )
    return migrated_count > 0
