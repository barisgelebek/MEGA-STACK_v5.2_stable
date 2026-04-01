#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
#  MEGA-STACK v2.5 — Binaries Bootstrap
#  Sistem binary'lerini binaries/ altına sembolik link veya kopyalama ile
#  bağlayarak Zero-Dependency ilkesini sağlar.
# ══════════════════════════════════════════════════════════════════════════
set -euo pipefail

BINARIES_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "═══ MEGA-STACK Binaries Bootstrap ═══"

# ─── SQLPackage ──────────────────────────────────────────────────────────
if [[ -d /opt/sqlpackage ]]; then
    if [[ ! -L "${BINARIES_DIR}/sqlpackage/sqlpackage" ]]; then
        ln -sf /opt/sqlpackage/sqlpackage "${BINARIES_DIR}/sqlpackage/sqlpackage"
        echo "  ✔ sqlpackage → /opt/sqlpackage/sqlpackage (symlink)"
    else
        echo "  ✔ sqlpackage zaten bağlı"
    fi
else
    echo "  ⚠ /opt/sqlpackage bulunamadı — MSSQL .bak/.dacpac işlemleri devre dışı"
fi

# ─── Docker Compose ─────────────────────────────────────────────────────
COMPOSE_BIN=""
if command -v docker-compose &>/dev/null; then
    COMPOSE_BIN="$(which docker-compose)"
elif docker compose version &>/dev/null; then
    # Docker Compose v2 plugin olarak çalışıyor
    COMPOSE_BIN="docker-compose-plugin"
fi

if [[ -n "${COMPOSE_BIN}" && "${COMPOSE_BIN}" != "docker-compose-plugin" ]]; then
    if [[ ! -L "${BINARIES_DIR}/docker-compose-linux-x86_64" ]]; then
        ln -sf "${COMPOSE_BIN}" "${BINARIES_DIR}/docker-compose-linux-x86_64"
        echo "  ✔ docker-compose → ${COMPOSE_BIN} (symlink)"
    else
        echo "  ✔ docker-compose zaten bağlı"
    fi
else
    echo "  ℹ Docker Compose v2 plugin olarak çalışıyor (docker compose)"
    echo '#!/bin/bash' > "${BINARIES_DIR}/docker-compose-linux-x86_64"
    echo 'exec docker compose "$@"' >> "${BINARIES_DIR}/docker-compose-linux-x86_64"
    chmod +x "${BINARIES_DIR}/docker-compose-linux-x86_64"
    echo "  ✔ docker-compose wrapper oluşturuldu"
fi

# ─── Rclone ──────────────────────────────────────────────────────────────
if command -v rclone &>/dev/null; then
    RCLONE_BIN="$(which rclone)"
    if [[ ! -L "${BINARIES_DIR}/rclone" ]]; then
        ln -sf "${RCLONE_BIN}" "${BINARIES_DIR}/rclone"
        echo "  ✔ rclone → ${RCLONE_BIN} (symlink)"
    else
        echo "  ✔ rclone zaten bağlı"
    fi
else
    echo "  ⚠ rclone bulunamadı — R2/S3 yedekleme devre dışı"
    echo "  ℹ Kurulum: curl https://rclone.org/install.sh | bash"
fi

echo ""
echo "═══ Bootstrap tamamlandı ═══"
