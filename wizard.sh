#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
#  MEGA-STACK v2.5 Installation Wizard — Bootstrapper (wizard.sh)
#  Görev: Sunucu check, Zombi temizliği, Python Venv, API Boot.
# ══════════════════════════════════════════════════════════════════════════
set -euo pipefail

# ─── Renkler & Semboller ─────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color
CHECK="${GREEN}✔${NC}"
CROSS="${RED}✘${NC}"
WARN="${YELLOW}⚠${NC}"

# ─── Sabitler ────────────────────────────────────────────────────────────
WIZARD_DIR="/opt/mega-stack-product-wizard"
VENV_DIR="${WIZARD_DIR}/.venv"
ENV_FILE="${WIZARD_DIR}/.env.wizard"
LOG_DIR="${WIZARD_DIR}/logs"
LOG_FILE="${LOG_DIR}/install.log"
MEGA_STACK_DIR="/opt/mega-stack"
PYTHON_BIN="python3.12"

# Kaynak limitleri (Standart tier minimumları — sadece bilgi amaçlı)
REC_CPU=2
REC_RAM_GB=4
MIN_DISK_GB=20

# Kontrol edilecek portlar
PORTS=(80 443 1433 25 9999)

# API ayarları
WIZARD_HOST="0.0.0.0"
WIZARD_PORT=9999

# ─── Yardımcı Fonksiyonlar ──────────────────────────────────────────────
log_info()  { echo -e "  ${CHECK}  ${1}"; }
log_warn()  { echo -e "  ${WARN}  ${YELLOW}${1}${NC}"; }
log_fail()  { echo -e "  ${CROSS}  ${RED}${1}${NC}"; }
log_head()  { echo -e "\n${CYAN}${BOLD}═══ ${1} ═══${NC}"; }

# ─── Root Kontrolü ──────────────────────────────────────────────────────
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_fail "Bu script root yetkisi gerektirir. 'sudo bash wizard.sh' ile çalıştırın."
        exit 1
    fi
    log_info "Root yetkisi doğrulandı."
}

# ─── Donanım Kontrolleri (Sadece Bilgilendirme — Lisans Tarafından Zorlanmaz) ──
check_cpu() {
    local cpu_count
    cpu_count=$(nproc 2>/dev/null || grep -c ^processor /proc/cpuinfo 2>/dev/null || echo 0)

    if [[ $cpu_count -lt $REC_CPU ]]; then
        log_warn "vCPU: ${cpu_count} (Tavsiye edilen: ${REC_CPU}+) — Performans düşük olabilir."
    else
        log_info "vCPU: ${cpu_count} ✓"
    fi
}

check_ram() {
    local ram_kb ram_gb
    ram_kb=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}')
    ram_gb=$(( ram_kb / 1024 / 1024 ))

    if [[ $ram_gb -lt $REC_RAM_GB ]]; then
        log_warn "RAM: ${ram_gb}GB (Tavsiye edilen: ${REC_RAM_GB}GB+) — Performans düşük olabilir."
    else
        log_info "RAM: ${ram_gb}GB ✓"
    fi
}

check_disk() {
    local disk_avail_kb disk_avail_gb
    disk_avail_kb=$(df / --output=avail 2>/dev/null | tail -1 | tr -d ' ')
    disk_avail_gb=$(( disk_avail_kb / 1024 / 1024 ))

    if [[ $disk_avail_gb -lt $MIN_DISK_GB ]]; then
        log_warn "Disk (boş): ${disk_avail_gb}GB (Tavsiye edilen: ${MIN_DISK_GB}GB+) — Düşük alan."
    else
        log_info "Disk (boş): ${disk_avail_gb}GB ✓"
    fi
}

prompt_continue() {
    echo ""
    read -rp "  Devam etmek istiyor musunuz? (e/h): " answer
    if [[ "${answer,,}" != "e" && "${answer,,}" != "evet" ]]; then
        log_fail "Kurulum kullanıcı tarafından iptal edildi."
        exit 1
    fi
}

# ─── Port Kontrolü ──────────────────────────────────────────────────────
check_ports() {
    local has_conflict=false

    for port in "${PORTS[@]}"; do
        local pid_info
        pid_info=$(ss -tlnp 2>/dev/null | grep ":${port} " || true)

        if [[ -n "$pid_info" ]]; then
            local process_name
            process_name=$(echo "$pid_info" | grep -oP 'users:\(\("\K[^"]+' || echo "bilinmeyen")
            log_warn "Port ${port} meşgul! (Kullanan: ${process_name})"
            has_conflict=true
        else
            log_info "Port ${port} müsait ✓"
        fi
    done

    if [[ "$has_conflict" == "true" ]]; then
        echo ""
        log_warn "Port çakışması tespit edildi. Çakışan servisler durdurulmazsa kurulum başarısız olabilir."
        prompt_continue
    fi
}

# ─── Zombi Konteyner Temizliği ──────────────────────────────────────────
cleanup_zombie_containers() {
    if ! command -v docker &>/dev/null; then
        log_warn "Docker bulunamadı — zombi konteyner kontrolü atlanıyor."
        return
    fi

    # /opt/mega-stack altında tanımlı eski konteynerleri bul
    local zombie_containers
    zombie_containers=$(docker ps -a --filter "status=exited" --filter "label=com.docker.compose.project.working_dir=${MEGA_STACK_DIR}" --format "{{.ID}} {{.Names}} {{.Status}}" 2>/dev/null || true)

    # Ayrıca tüm exited konteynerlerde mega-stack ile ilişkili olanları bul
    if [[ -z "$zombie_containers" ]]; then
        zombie_containers=$(docker ps -a --filter "status=exited" --format "{{.ID}} {{.Names}} {{.Status}}" 2>/dev/null | grep -i "mega\|stack" || true)
    fi

    if [[ -z "$zombie_containers" ]]; then
        log_info "Zombi konteyner bulunamadı — temiz ortam."
        return
    fi

    echo ""
    log_warn "Aşağıdaki 'Exited' durumundaki eski konteynerler tespit edildi:"
    echo "$zombie_containers" | while IFS= read -r line; do
        echo -e "    ${RED}→${NC} $line"
    done

    echo ""
    read -rp "  Bu konteynerler kaldırılsın mı? (e/h): " answer
    if [[ "${answer,,}" == "e" || "${answer,,}" == "evet" ]]; then
        local container_ids
        container_ids=$(echo "$zombie_containers" | awk '{print $1}')
        echo "$container_ids" | xargs docker rm -f 2>/dev/null || true
        log_info "Zombi konteynerler temizlendi."
    else
        log_warn "Zombi konteynerler korunuyor — port çakışması yaşanabilir."
    fi

    # Portları işgal eden çalışan mega-stack konteynerlerini de kontrol et
    local running_containers
    running_containers=$(docker ps --format "{{.ID}} {{.Names}} {{.Ports}}" 2>/dev/null | grep -i "mega\|stack" || true)

    if [[ -n "$running_containers" ]]; then
        echo ""
        log_warn "Çalışan mega-stack konteynerleri tespit edildi:"
        echo "$running_containers" | while IFS= read -r line; do
            echo -e "    ${YELLOW}→${NC} $line"
        done
        echo ""
        read -rp "  Bu konteynerler durdurulsun mu? (e/h): " answer
        if [[ "${answer,,}" == "e" || "${answer,,}" == "evet" ]]; then
            local rids
            rids=$(echo "$running_containers" | awk '{print $1}')
            echo "$rids" | xargs docker stop 2>/dev/null || true
            echo "$rids" | xargs docker rm -f 2>/dev/null || true
            log_info "Çalışan mega-stack konteynerleri durduruldu ve kaldırıldı."
        fi
    fi
}

# ─── Python Venv & Paket Kurulumu ───────────────────────────────────────
setup_python_venv() {
    # Python 3.12 kontrol
    if ! command -v "$PYTHON_BIN" &>/dev/null; then
        log_fail "Python 3.12 bulunamadı. Lütfen 'apt install python3.12 python3.12-venv' ile yükleyin."
        exit 1
    fi

    local python_version
    python_version=$("$PYTHON_BIN" --version 2>&1)
    log_info "Python tespit edildi: ${python_version}"

    # venv yoksa oluştur
    if [[ ! -d "${VENV_DIR}" ]]; then
        log_info "Python venv oluşturuluyor: ${VENV_DIR}"
        "$PYTHON_BIN" -m venv "${VENV_DIR}"
    else
        log_info "Python venv zaten mevcut: ${VENV_DIR}"
    fi

    # pip upgrade & paket kurulumu
    log_info "Gerekli paketler yükleniyor..."
    "${VENV_DIR}/bin/pip" install --upgrade pip --quiet 2>/dev/null
    "${VENV_DIR}/bin/pip" install \
        fastapi \
        "uvicorn[standard]" \
        psutil \
        python-multipart \
        cryptography \
        httpx \
        jinja2 \
        --quiet 2>/dev/null

    log_info "Python paketleri hazır: fastapi, uvicorn, psutil, cryptography, httpx, jinja2 ✓"
}

# ─── .env.wizard Dosyası ────────────────────────────────────────────────
create_env_file() {
    if [[ ! -f "${ENV_FILE}" ]]; then
        cat > "${ENV_FILE}" <<EOF
# MEGA-STACK v2.5 Installation Wizard — Environment Variables
WIZARD_VERSION=2.5.0
WIZARD_HOST=${WIZARD_HOST}
WIZARD_PORT=${WIZARD_PORT}
DEBUG=False
LOG_LEVEL=INFO
MEGA_STACK_DIR=${MEGA_STACK_DIR}
# Domain — Step 02'de ayarlandiktan sonra otomatik guncellenir.
# WIZARD_DOMAIN=
EOF
        chmod 600 "${ENV_FILE}"
        log_info ".env.wizard oluşturuldu ve mühürlendi (chmod 600)."
    else
        log_info ".env.wizard zaten mevcut."
    fi
}

# ─── Dizin & Log Hazırlığı ──────────────────────────────────────────────
prepare_directories() {
    mkdir -p "${LOG_DIR}"
    touch "${LOG_FILE}"
    log_info "Log dizini hazır: ${LOG_DIR}"
}

# ─── Snapshot Uyarısı ────────────────────────────────────────────────────
snapshot_warning() {
    echo ""
    echo -e "  ${WARN}  ${YELLOW}${BOLD}UYARI: Kurulum başlamadan önce sunucu snapshot'ı aldınız mı?${NC}"
    read -rp "  Snapshot alındı mı? (e/h): " answer
    if [[ "${answer,,}" != "e" && "${answer,,}" != "evet" ]]; then
        log_warn "Snapshot alınmadan devam ediliyor — risk kullanıcıya aittir."
    else
        log_info "Snapshot onayı alındı."
    fi
}

# ─── API Başlatma ────────────────────────────────────────────────────────
launch_api() {
    log_info "Wizard API başlatılıyor → http://${WIZARD_HOST}:${WIZARD_PORT}"
    log_info "API Docs → http://$(hostname -I 2>/dev/null | awk '{print $1}' || echo 'localhost'):${WIZARD_PORT}/api/docs"
    echo ""

    cd "${WIZARD_DIR}"
    exec "${VENV_DIR}/bin/uvicorn" core.main:app \
        --host "${WIZARD_HOST}" \
        --port "${WIZARD_PORT}" \
        --log-level info \
        --no-access-log
}

# ─── Wizard Durdurma ────────────────────────────────────────────────────
stop_wizard() {
    log_head "WIZARD DURDURMA"
    local pid
    pid=$(pgrep -f "uvicorn core.main:app" 2>/dev/null || true)
    if [[ -n "${pid}" ]]; then
        kill "${pid}" 2>/dev/null || true
        sleep 2
        kill -9 "${pid}" 2>/dev/null || true
        log_info "Wizard API durduruldu (PID: ${pid})"
    else
        log_warn "Wizard API zaten çalışmıyor."
    fi
}

# ─── Finalize & Pasifleştirme ────────────────────────────────────────────
finalize_wizard() {
    log_head "WIZARD FİNALİZASYON"

    # .ready flag kontrolü — zaten finalize edilmiş mi?
    if [[ -f "${WIZARD_DIR}/.ready" ]]; then
        log_info "Sistem zaten operasyonel modda (.ready flag mevcut)."
        return 0
    fi

    # Wizard API'yi durdur
    stop_wizard

    # wizard.sh çalıştırma iznini kaldır (pasifleştir)
    chmod -x "${WIZARD_DIR}/wizard.sh" 2>/dev/null || true
    log_info "wizard.sh pasifleştirildi (chmod -x)"

    # .env.wizard korunur — Docker compose bağımlılığı
    if [[ -f "${ENV_FILE}" ]]; then
        log_info ".env.wizard korundu — Docker compose bağımlılığı aktif"
    fi

    # .ready flag oluştur
    date -u +"%Y-%m-%dT%H:%M:%SZ" > "${WIZARD_DIR}/.ready"
    chmod 600 "${WIZARD_DIR}/.ready"
    log_info ".ready flag oluşturuldu — sistem operasyonel moda geçti"

    echo ""
    echo -e "  ${CHECK}  ${GREEN}${BOLD}MEGA-STACK v2.5 kurulumu tamamlandı ve mühürlendi.${NC}"
    echo -e "  ${CHECK}  ${GREEN}Wizard artık pasif durumda.${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  ANA AKIŞ
# ═══════════════════════════════════════════════════════════════════════════
main() {
    # Ready mode kontrolü — kurulum zaten tamamlanmışsa
    if [[ -f "${WIZARD_DIR}/.ready" ]]; then
        echo ""
        echo -e "  ${CHECK}  ${GREEN}${BOLD}MEGA-STACK v2.5 zaten operasyonel modda.${NC}"
        echo -e "  ${WARN}  Kurulum tamamlanmış ve mühürlenmiş. Wizard pasif durumda."
        echo ""
        exit 0
    fi

    clear
    echo ""
    echo -e "${CYAN}${BOLD}"
    echo "  ╔══════════════════════════════════════════════════════════════╗"
    echo "  ║    🛡️  MEGA-STACK v2.5 — Installation Wizard              ║"
    echo "  ║    Zero Dependency, Total Security, One-Click Deployment   ║"
    echo "  ╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    # 1. Root kontrol
    log_head "YETKI KONTROLÜ"
    check_root

    # 2. Donanım kontrolleri (sadece bilgilendirme — lisans tarafından zorlanmaz)
    log_head "DONANIM KONTROLÜ (Bilgilendirme — Zorlanmaz)"
    check_cpu
    check_ram
    check_disk

    # 3. Port kontrolü
    log_head "PORT KONTROLÜ"
    check_ports

    # 4. Zombi konteyner temizliği
    log_head "PRE-INSTALLATION CLEANUP"
    cleanup_zombie_containers

    # 5. Snapshot uyarısı
    log_head "SNAPSHOT ONAY"
    snapshot_warning

    # 6. Dizin hazırlığı
    log_head "DİZİN HAZIRLIĞI"
    prepare_directories

    # 7. .env.wizard oluştur
    create_env_file

    # 8. Binary bootstrap (symlink onarımı: rclone, sqlpackage, docker-compose)
    log_head "BINARY BOOTSTRAP"
    local bootstrap_script="${WIZARD_DIR}/binaries/bootstrap.sh"
    if [[ -f "${bootstrap_script}" ]]; then
        bash "${bootstrap_script}"
        log_info "Binary bootstrap tamamlandı."
    else
        log_warn "binaries/bootstrap.sh bulunamadı — symlink onarımı atlandı."
    fi

    # 9. Python venv & paketler
    log_head "PYTHON ORTAMI"
    setup_python_venv

    # 10. API başlat
    log_head "API BAŞLATMA"
    launch_api
}

main "$@"
