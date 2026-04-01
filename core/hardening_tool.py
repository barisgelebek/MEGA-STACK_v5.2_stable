"""
MEGA-STACK v2.5 Installation Wizard — Hardening Tool
Sistem mühürleme: dosya izinleri, acme.json, geçici dosya temizliği, binary pasifleştirme.
KIRMIZI ÇİZGİ: acme.json mutlaka chmod 600 olmalı — Traefik bunu zorunlu tutar.
"""

import os
import stat
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from core.logger import wizard_logger

BASE_DIR = Path(__file__).resolve().parent.parent
MEGA_STACK_DIR = Path("/opt/mega-stack")
SECRETS_DIR = MEGA_STACK_DIR / "secrets"
ACME_JSON = MEGA_STACK_DIR / "traefik" / "acme.json"

# Temizlenecek geçici dosya desenleri
TEMP_PATTERNS = [
    "/tmp/mega-stack-*",
    "/tmp/wizard-*",
    "/tmp/install-*",
]

# İzin korumalı dizinler (güvenlik açısından dokunulmaması gerekenler)
PROTECTED_DIRS = [
    SECRETS_DIR,
    MEGA_STACK_DIR / "traefik" / "certs",
    MEGA_STACK_DIR / "portainer_data" / "certs",
    MEGA_STACK_DIR / "portainer_data" / "tls",
]


class HardeningReport:
    """Mühürleme işleminin raporunu tutar."""

    def __init__(self):
        self.started_at: str = datetime.now(timezone.utc).isoformat()
        self.completed_at: Optional[str] = None
        self.files_chmod: int = 0
        self.dirs_chmod: int = 0
        self.acme_sealed: bool = False
        self.temp_cleaned: int = 0
        self.errors: list[str] = []
        self.actions: list[str] = []

    def add_action(self, action: str) -> None:
        self.actions.append(action)
        wizard_logger.info(f"[Hardening] {action}", step_id="20")

    def add_error(self, error: str) -> None:
        self.errors.append(error)
        wizard_logger.error(f"[Hardening] HATA: {error}", step_id="20")

    def finalize(self) -> None:
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "files_chmod": self.files_chmod,
            "dirs_chmod": self.dirs_chmod,
            "acme_sealed": self.acme_sealed,
            "temp_cleaned": self.temp_cleaned,
            "error_count": len(self.errors),
            "errors": self.errors,
            "action_count": len(self.actions),
            "actions": self.actions,
        }


def seal_permissions(base_dir: Path = MEGA_STACK_DIR, report: Optional[HardeningReport] = None) -> HardeningReport:
    """
    /opt/mega-stack altındaki dosyalara chmod 0600, dizinlere chmod 0700 uygular.
    Sadece secrets/, traefik/certs gibi güvenlik açısından kritik dizinlere dokunur.
    """
    if report is None:
        report = HardeningReport()

    for protected_dir in PROTECTED_DIRS:
        if not protected_dir.exists():
            report.add_action(f"ATLA: {protected_dir} bulunamadı")
            continue

        for root, dirs, files in os.walk(str(protected_dir)):
            root_path = Path(root)

            # Dizinlere 0700
            for d in dirs:
                dir_path = root_path / d
                try:
                    os.chmod(str(dir_path), 0o700)
                    report.dirs_chmod += 1
                except OSError as e:
                    report.add_error(f"chmod 700 başarısız: {dir_path} — {e}")

            # Dosyalara 0600
            for f in files:
                file_path = root_path / f
                try:
                    os.chmod(str(file_path), 0o600)
                    report.files_chmod += 1
                except OSError as e:
                    report.add_error(f"chmod 600 başarısız: {file_path} — {e}")

        report.add_action(f"İzinler mühürlendi: {protected_dir} (files=0600, dirs=0700)")

    return report


def seal_acme_json(report: Optional[HardeningReport] = None) -> HardeningReport:
    """
    KIRMIZI ÇİZGİ: acme.json dosyasına chmod 600 uygular.
    Traefik bu izni zorunlu tutar — aksi halde sertifika alınamaz.
    """
    if report is None:
        report = HardeningReport()

    if ACME_JSON.exists():
        try:
            os.chmod(str(ACME_JSON), 0o600)
            report.acme_sealed = True
            report.add_action(f"acme.json mühürlendi: chmod 600 — {ACME_JSON}")
        except OSError as e:
            report.add_error(f"acme.json mühürleme BAŞARISIZ: {e}")
    else:
        report.add_action(f"acme.json bulunamadı: {ACME_JSON} — atlandı")

    return report


def cleanup_temp_files(report: Optional[HardeningReport] = None) -> HardeningReport:
    """Geçici kurulum dosyalarını temizler."""
    import glob

    if report is None:
        report = HardeningReport()

    for pattern in TEMP_PATTERNS:
        matches = glob.glob(pattern)
        for match in matches:
            match_path = Path(match)
            try:
                if match_path.is_file():
                    match_path.unlink()
                    report.temp_cleaned += 1
                    report.add_action(f"Geçici dosya silindi: {match}")
                elif match_path.is_dir():
                    import shutil
                    shutil.rmtree(str(match_path))
                    report.temp_cleaned += 1
                    report.add_action(f"Geçici dizin silindi: {match}")
            except OSError as e:
                report.add_error(f"Temizlik hatası: {match} — {e}")

    if report.temp_cleaned == 0:
        report.add_action("Temizlenecek geçici dosya bulunamadı.")

    return report


def passivate_wizard(report: Optional[HardeningReport] = None) -> HardeningReport:
    """
    Wizard binary'lerini pasifleştirir.
    .env.wizard korunur (Docker compose buna bağlı).
    """
    if report is None:
        report = HardeningReport()

    env_wizard = BASE_DIR / ".env.wizard"
    wizard_sh = BASE_DIR / "wizard.sh"

    # wizard.sh'ı çalıştırılamaz yap (ancak read kalır)
    if wizard_sh.exists():
        try:
            current_mode = wizard_sh.stat().st_mode
            new_mode = current_mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            os.chmod(str(wizard_sh), new_mode)
            report.add_action("wizard.sh çalıştırma izni kaldırıldı (pasifleştirildi)")
        except OSError as e:
            report.add_error(f"wizard.sh pasifleştirme hatası: {e}")

    # .env.wizard'ı koru
    if env_wizard.exists():
        report.add_action(".env.wizard korundu — Docker compose bağımlılığı aktif")

    # ready moduna geçiş dosyası oluştur
    ready_flag = BASE_DIR / ".ready"
    try:
        ready_flag.write_text(
            datetime.now(timezone.utc).isoformat(),
            encoding="utf-8",
        )
        os.chmod(str(ready_flag), 0o600)
        report.add_action(".ready flag dosyası oluşturuldu — sistem operasyonel")
    except OSError as e:
        report.add_error(f".ready dosyası oluşturma hatası: {e}")

    return report


def run_full_hardening() -> dict:
    """
    Tüm mühürleme adımlarını sırasıyla çalıştırır.
    Her adımın sonucunu toplayarak tek bir rapor döner.
    """
    report = HardeningReport()

    wizard_logger.info("[Hardening] ═══ Sistem mühürleme başlatıldı ═══", step_id="20")

    # 1. Dosya izinleri mühürle
    seal_permissions(report=report)

    # 2. acme.json KIRMIZI ÇİZGİ
    seal_acme_json(report=report)

    # 3. Geçici dosyaları temizle
    cleanup_temp_files(report=report)

    # 4. Wizard'ı pasifleştir
    passivate_wizard(report=report)

    report.finalize()

    wizard_logger.info(
        f"[Hardening] ═══ Mühürleme tamamlandı — "
        f"Dosya: {report.files_chmod}, Dizin: {report.dirs_chmod}, "
        f"Temizlik: {report.temp_cleaned}, Hata: {len(report.errors)} ═══",
        step_id="20",
    )

    return report.to_dict()


def get_hardening_status() -> dict:
    """Mühürleme durumunu kontrol eder (acme.json izni, .ready flag, vb.)."""
    checks = {}

    # acme.json kontrolü
    if ACME_JSON.exists():
        mode = oct(ACME_JSON.stat().st_mode)[-3:]
        checks["acme_json"] = {
            "exists": True,
            "permissions": mode,
            "sealed": mode == "600",
        }
    else:
        checks["acme_json"] = {"exists": False, "sealed": False}

    # .ready flag kontrolü
    ready_flag = BASE_DIR / ".ready"
    checks["ready_flag"] = {
        "exists": ready_flag.exists(),
        "timestamp": ready_flag.read_text().strip() if ready_flag.exists() else None,
    }

    # secrets/ dizini izinleri
    if SECRETS_DIR.exists():
        secret_files = list(SECRETS_DIR.iterdir())
        all_600 = all(
            oct(f.stat().st_mode)[-3:] == "600"
            for f in secret_files if f.is_file()
        )
        checks["secrets_dir"] = {
            "exists": True,
            "file_count": len(secret_files),
            "all_chmod_600": all_600,
        }
    else:
        checks["secrets_dir"] = {"exists": False}

    return checks
