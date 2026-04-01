/**
 * MEGA-STACK v2.5 Installation Wizard — Core Engine
 * Step Management, State Control, Log Stream, UI Orchestration.
 */

const WizardCore = (() => {
    'use strict';

    // ── Step Tanımları ──
    const STEPS = [
        { id: '00', name: 'License Auth',               icon: '🔑', fragment: '00-license-auth.html' },
        { id: '01', name: 'Identity & Branding',        icon: '🏷️', fragment: '01-identity-branding.html' },
        { id: '02', name: 'Global DNS & Domain Config', icon: '🌐', fragment: '02-global-dns-config.html' },
        { id: '03', name: 'Traefik Setup',              icon: '🔀', fragment: '03-traefik-setup.html' },
        { id: '04', name: 'Authelia Setup',             icon: '🛡️', fragment: '04-authelia-setup.html' },
        { id: '05', name: 'CrowdSec Setup',            icon: '🏰', fragment: '05-crowdsec-setup.html' },
        { id: '06', name: 'Bouncer Setup',              icon: '⚔️', fragment: '06-bouncer-setup.html' },
        { id: '07', name: 'CertDumper Setup',           icon: '📜', fragment: '07-certdumper-setup.html' },
        { id: '08', name: 'MSSQL Setup',                icon: '🗄️', fragment: '08-mssql-setup.html' },
        { id: '09', name: 'iRedMail Setup',             icon: '📧', fragment: '09-iredmail-setup.html' },
        { id: '10', name: 'Nginx Setup',                icon: '🌍', fragment: '10-nginx-setup.html' },
        { id: '11', name: 'PointVending Setup',         icon: '💎', fragment: '11-pointvending-setup.html' },
        { id: '12', name: 'Core-API Setup',             icon: '⚡', fragment: '12-core-api-setup.html' },
        { id: '13', name: 'Netdata Setup',              icon: '📊', fragment: '13-netdata-setup.html' },
        { id: '14', name: 'UptimeKuma Setup',           icon: '🟢', fragment: '14-uptimekuma-setup.html' },
        { id: '15', name: 'Dozzle Setup',               icon: '📋', fragment: '15-dozzle-setup.html' },
        { id: '16', name: 'Portainer Setup',            icon: '🐳', fragment: '16-portainer-setup.html' },
        { id: '17', name: 'CloudBeaver Setup',          icon: '🦫', fragment: '17-cloudbeaver-setup.html' },
        { id: '18', name: 'Watchtower Setup',           icon: '🗼', fragment: '18-watchtower-setup.html' },
        { id: '19', name: 'AI & Telegram API',          icon: '🤖', fragment: '19-ai-telegram-api.html' },
        { id: '20', name: 'Hardening & Finalize',       icon: '🔒', fragment: '20-hardening-finalize.html' },
        { id: '21', name: 'Success & Launch',           icon: '🚀', fragment: '21-success-launch.html' },
        { id: '22', name: 'Dashboard Viewer',           icon: '📊', fragment: '22-dashboard-viewer.html', alwaysAccessible: true },
    ];

    // ── Step → Hub Servis Eşlemesi (Tier-Aware Lock) ──
    // Sadece servis-bağımlı adımlar listelenir. Listede olmayan adımlar her zaman açıktır.
    const STEP_SERVICE_MAP = {
        '03': ['traefik'],
        '04': ['authelia'],
        '05': ['crowdsec'],
        '06': ['crowdsec-bouncer'],
        '07': ['cert-dumper'],
        '08': ['mssql'],
        '09': ['iredmail'],
        '10': ['nginx-sites'],
        '12': ['core-api'],
        '13': ['netdata'],
        '14': ['uptime-kuma'],
        '15': ['dozzle'],
        '16': ['portainer'],
        '17': ['cloudbeaver'],
        '18': ['watchtower'],
    };

    // Hangi tier hangi servisleri açar — yükseltme önerisinde kullanılır
    const SERVICE_UNLOCK_TIER = {
        'cert-dumper': 'Standart', 'iredmail': 'Standart', 'uptime-kuma': 'Standart',
        'authelia': 'Professional', 'mssql': 'Professional',
        'cloudbeaver': 'Professional', 'dozzle': 'Professional',
    };

    // ── Tier → Minimum Donanım Gereksinimleri ──
    const TIER_HARDWARE_REQUIREMENTS = {
        'Standart':      { min_ram_gb: 4,  min_vcpu: 2, min_disk_gb: 20, label: 'Standart' },
        'Standard':      { min_ram_gb: 4,  min_vcpu: 2, min_disk_gb: 20, label: 'Standard' },
        'Professional':  { min_ram_gb: 8,  min_vcpu: 4, min_disk_gb: 40, label: 'Professional' },
        'Enterprise':    { min_ram_gb: 16, min_vcpu: 6, min_disk_gb: 80, label: 'Enterprise' },
    };

    // ── State ──
    let state = {
        currentStep: 0,
        steps: {},
        isRunning: false,
        logStream: null,
        tierInfo: { tier: null, allowed_services: [] },
        network: {
            domain: '', server_ip: '', domain_type: 'static',
            ssl_mode: 'full_strict', cf_zone_id: '', dns_confirmed: false,
        },
    };

    // ── Dependency Update System ──
    // Bağımlı adımlar (domain/IP değiştiğinde tetiklenmesi gereken servisler)
    const DEPENDENCY_MAP = {
        'network.domain':    ['03', '04', '09', '10', '12'],  // Traefik, Authelia, iRedMail, Nginx, Core-API
        'network.server_ip': ['02', '03', '10'],               // DNS, Traefik, Nginx
        'tierInfo.tier':     ['00', '08', '19'],               // License, MSSQL, AI
    };
    const _dependencyListeners = [];

    function notifyDependencyUpdate(changedKey) {
        const affectedSteps = DEPENDENCY_MAP[changedKey] || [];
        const payload = { key: changedKey, value: _resolveStateKey(changedKey), affectedSteps };
        _dependencyListeners.forEach(fn => { try { fn(payload); } catch (e) { console.error('[DependencyUpdate]', e); } });
    }

    function _resolveStateKey(key) {
        return key.split('.').reduce((obj, k) => (obj && obj[k] !== undefined ? obj[k] : null), state);
    }

    function onDependencyUpdate(callback) {
        if (typeof callback === 'function') _dependencyListeners.push(callback);
    }

    // ── DOM Cache ──
    const DOM = {};

    function cacheDom() {
        DOM.stepList       = document.getElementById('stepList');
        DOM.stepContent    = document.getElementById('stepContent');
        DOM.progressFill   = document.getElementById('progressFill');
        DOM.progressText   = document.getElementById('progressText');
        DOM.terminalBody   = document.getElementById('terminalBody');
        DOM.terminalClear  = document.getElementById('terminalClearBtn');
        DOM.headerStepInfo = document.getElementById('headerStepInfo');
        DOM.headerBadge    = document.getElementById('headerBadge');
        DOM.toastContainer = document.getElementById('toastContainer');
        DOM.mobileMenuBtn  = document.getElementById('mobileMenuBtn');
        DOM.sidebar        = document.getElementById('sidebar');
        DOM.sidebarOverlay = document.getElementById('sidebarOverlay');
    }

    // ── Sidebar: Step List Render ──
    function renderStepList() {
        DOM.stepList.innerHTML = STEPS.map((step, i) => {
            const statusClass = getStepStatusClass(i);
            const lockCheck = isStepLocked(step.id);
            const lockedClass = lockCheck.locked ? ' locked' : '';
            const alwaysClass = step.alwaysAccessible ? ' always-accessible' : '';
            const num = String(i).padStart(2, '0');
            const icon = lockCheck.locked ? '\ud83d\udd12' : (step.alwaysAccessible ? step.icon : (statusClass === 'completed' ? '' : num));
            return `<div class="step-item ${statusClass}${lockedClass}${alwaysClass}" data-step="${i}">
                <div class="step-icon">${icon}</div>
                <span class="step-name">${step.name}</span>
                ${step.alwaysAccessible ? '<span style="font-size:0.6rem; color:var(--health-yellow); margin-left:auto;">🔒 ReadOnly</span>' : ''}
            </div>`;
        }).join('');
    }

    function getStepStatusClass(index) {
        const info = state.steps[index];
        if (!info) {
            if (index === state.currentStep) return 'active';
            return '';
        }
        switch (info.status) {
            case 'completed': return 'completed';
            case 'running':   return 'active';
            case 'failed':    return 'failed';
            default:          return '';
        }
    }

    function updateStepListUI() {
        const items = DOM.stepList.querySelectorAll('.step-item');
        items.forEach((el, i) => {
            const step = STEPS[i];
            const lockCheck = step ? isStepLocked(step.id) : { locked: false };
            const statusClass = getStepStatusClass(i);
            const lockedClass = lockCheck.locked ? ' locked' : '';
            el.className = `step-item ${statusClass}${lockedClass}`;
            const iconEl = el.querySelector('.step-icon');
            if (lockCheck.locked) {
                iconEl.textContent = '🔒';
            } else if (statusClass === 'completed') {
                iconEl.textContent = '';
            } else {
                iconEl.textContent = String(i).padStart(2, '0');
            }
        });
    }

    // ── Progress Bar ──
    function updateProgress() {
        const completedCount = Object.values(state.steps)
            .filter(s => s.status === 'completed').length;
        const pct = Math.round((completedCount / STEPS.length) * 100);
        DOM.progressFill.style.width = `${pct}%`;
        DOM.progressText.textContent = `${completedCount} / ${STEPS.length}`;
    }

    // ── Header ──
    function updateHeader() {
        const step = STEPS[state.currentStep];
        DOM.headerStepInfo.textContent = `Step ${step.id}: ${step.name}`;

        const badge = DOM.headerBadge;
        if (state.isRunning) {
            badge.className = 'badge badge--running';
            badge.textContent = 'Çalışıyor';
        } else {
            badge.className = 'badge badge--pending';
            badge.textContent = 'Beklemede';
        }
    }

    // ── Tier-Aware: Adım kilitleme kontrolü ──
    function isStepLocked(stepId) {
        const requiredServices = STEP_SERVICE_MAP[stepId];
        if (!requiredServices) return { locked: false, services: [] };
        const allowed = state.tierInfo.allowed_services;
        if (!allowed || allowed.length === 0) return { locked: false, services: [] };
        const missing = requiredServices.filter(s => !allowed.includes(s));
        return { locked: missing.length > 0, services: missing };
    }

    function getUpgradeTierSuggestion(missingServices) {
        for (const svc of missingServices) {
            if (SERVICE_UNLOCK_TIER[svc]) return SERVICE_UNLOCK_TIER[svc];
        }
        return 'Professional';
    }

    function renderLockedStep(step, missingServices) {
        const suggestedTier = getUpgradeTierSuggestion(missingServices);
        const serviceLabels = missingServices.map(s => `<strong>${escapeHtml(s)}</strong>`).join(', ');
        return `
            <div class="card fade-in" style="position:relative; overflow:hidden;">
                <div class="tier-lock-overlay"></div>
                <div class="step-title">
                    <div class="step-number">${step.id}</div>
                    <div>
                        <h2>${escapeHtml(step.name)}</h2>
                        <p style="color:var(--text-muted); font-size:0.85rem;">Servis kurulumu</p>
                    </div>
                </div>
                <div class="tier-lock-content">
                    <div class="tier-lock-icon">🔒</div>
                    <h3 style="margin:12px 0 8px; color:var(--health-yellow);">Paket Y\u00fckseltmesi Gerekli</h3>
                    <p style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6; max-width:520px; margin:0 auto;">
                        \ud83d\udeab Bu servis mevcut paketinizde bulunmamaktad\u0131r.
                        ${serviceLabels} gibi profesyonel \u00f6zellikleri kullanmak i\u00e7in
                        paketinizi <strong style="color:var(--accent-primary);">${escapeHtml(suggestedTier)} Tier</strong>'a y\u00fckseltin.
                    </p>
                    <a href="https://barisgelebek.com/mega-stack#pricing"
                       target="_blank" rel="noopener noreferrer"
                       class="btn btn-primary"
                       style="margin-top:20px; display:inline-flex; align-items:center; gap:6px;">
                        \ud83d\ude80 Paketleri \u0130ncele
                    </a>
                </div>
                <div class="step-actions">
                    <button class="btn btn-primary" disabled style="opacity:0.4; cursor:not-allowed;">
                        \ud83d\udd12 Kilitli \u2014 Kurulum Engellendi
                    </button>
                </div>
            </div>`;
    }

    // ── Step Content Loader ──
    async function loadStepContent(stepIndex) {
        const step = STEPS[stepIndex];
        if (!step) return;

        // ── Tier-Aware Lock Kontrolü ──
        const lockCheck = isStepLocked(step.id);
        if (lockCheck.locked) {
            DOM.stepContent.innerHTML = renderLockedStep(step, lockCheck.services);
            updateStepListUI();
            updateProgress();
            updateHeader();
            return;
        }

        DOM.stepContent.innerHTML = `
            <div class="card" style="text-align:center; padding:48px;">
                <div class="spinner" style="margin:0 auto 16px;"></div>
                <p style="color:var(--text-secondary);">Adım yükleniyor...</p>
            </div>`;

        try {
            const response = await fetch(`steps/${step.fragment}`);
            if (response.ok) {
                const html = await response.text();
                DOM.stepContent.innerHTML = html;
                // Fragment'taki init fonksiyonunu çağır
                const initFn = window[`initStep${step.id}`];
                if (typeof initFn === 'function') {
                    initFn();
                }
            } else {
                DOM.stepContent.innerHTML = `
                    <div class="card">
                        <div class="step-title">
                            <div class="step-number">${step.id}</div>
                            <div>
                                <h2>${step.name}</h2>
                                <p style="color:var(--text-muted); font-size:0.85rem;">
                                    Bu adım henüz implemente edilmedi.
                                </p>
                            </div>
                        </div>
                        <div class="info-box">
                            <span class="info-icon">ℹ️</span>
                            <span>Bu adımın HTML fragment'ı sonraki fazlarda eklenecektir.</span>
                        </div>
                        <div class="step-actions">
                            <button class="btn btn-primary" onclick="WizardCore.nextStep()">
                                Sonraki Adım →
                            </button>
                        </div>
                    </div>`;
            }
        } catch {
            DOM.stepContent.innerHTML = `
                <div class="card">
                    <div class="step-title">
                        <div class="step-number">${step.id}</div>
                        <h2>${step.name}</h2>
                    </div>
                    <p style="color:var(--health-red);">Fragment yüklenemedi.</p>
                </div>`;
        }

        updateStepListUI();
        updateProgress();
        updateHeader();
    }

    // ── Step Geçişi ──
    async function nextStep() {
        const result = await WizardAPI.advanceStep();
        if (result.success) {
            state.currentStep = parseInt(result.data.step_id, 10);
            syncStateFromServer();
            loadStepContent(state.currentStep);
            showToast(`Step ${result.data.step_id} initialized successfully`, 'success');
        } else {
            showToast(result.error || 'Adım geçişi başarısız.', 'error');
        }
    }

    function goToStep(index) {
        // Kilitli adımlara gidilemez
        const step = STEPS[index];
        if (step) {
            const lockCheck = isStepLocked(step.id);
            if (lockCheck.locked) return;
        }
        // alwaysAccessible sayfalar her zaman erişilebilir (Dashboard Viewer gibi)
        if (step && step.alwaysAccessible) {
            loadStepContent(index);
            return;
        }
        // Sadece tamamlanmış veya aktif adımlara gidilebilir
        if (index <= state.currentStep) {
            loadStepContent(index);
        }
    }

    // ── Server State Sync ──
    async function syncStateFromServer() {
        const statusRes = await WizardAPI.getInstallStatus();
        if (statusRes.success) {
            state.currentStep = statusRes.data.current_step;
            state.isRunning = statusRes.data.is_running;
        }

        const stepsRes = await WizardAPI.getAllSteps();
        if (stepsRes.success) {
            state.steps = stepsRes.data.steps;
        }

        updateStepListUI();
        updateProgress();
        updateHeader();
    }

    // ── Log Stream (Terminal) ──
    function startLogStream() {
        if (state.logStream) {
            state.logStream.close();
        }

        state.logStream = WizardAPI.connectLogStream(
            (entry) => appendLog(entry),
            () => {
                // Bağlantı hatası — yeniden deneme otomatik
            }
        );
    }

    function appendLog(entry) {
        const line = document.createElement('div');
        line.className = 'log-line';

        const time = entry.timestamp
            ? new Date(entry.timestamp).toLocaleTimeString('tr-TR')
            : '';
        const level = entry.level || 'INFO';
        const message = entry.message || JSON.stringify(entry);

        line.innerHTML = `
            ${time ? `<span class="log-time">${time}</span>` : ''}
            <span class="log-level ${level}">${level}</span>
            <span class="log-message">${escapeHtml(message)}</span>`;

        DOM.terminalBody.appendChild(line);

        // Auto-scroll
        DOM.terminalBody.scrollTop = DOM.terminalBody.scrollHeight;
    }

    function clearTerminal() {
        DOM.terminalBody.innerHTML = '';
    }

    // ── Toast Notifications ──
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        DOM.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(30px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // ── Mobile Menu ──
    function setupMobileMenu() {
        DOM.mobileMenuBtn.addEventListener('click', () => {
            DOM.sidebar.classList.toggle('open');
            DOM.sidebarOverlay.classList.toggle('active');
        });

        DOM.sidebarOverlay.addEventListener('click', () => {
            DOM.sidebar.classList.remove('open');
            DOM.sidebarOverlay.classList.remove('active');
        });
    }

    // ── Utility ──
    function escapeHtml(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return String(text).replace(/[&<>"']/g, c => map[c]);
    }

    // ── Offline Mode Badge ──
    function updateOfflineBadge(isOffline) {
        let badge = document.getElementById('offlineModeBadge');
        if (isOffline) {
            if (!badge) {
                badge = document.createElement('div');
                badge.id = 'offlineModeBadge';
                badge.style.cssText = 'position:fixed;top:60px;right:16px;z-index:9999;'
                    + 'background:rgba(243,156,18,0.92);color:#fff;padding:6px 14px;'
                    + 'border-radius:8px;font-size:0.82rem;font-weight:600;'
                    + 'box-shadow:0 2px 12px rgba(243,156,18,0.35);'
                    + 'display:flex;align-items:center;gap:6px;backdrop-filter:blur(6px);';
                badge.innerHTML = '⚠️ Çevrimdışı Mod';
                badge.title = 'İnternet bağlantısı yok — lokal mühür ile devam ediliyor.';
                document.body.appendChild(badge);
            }
            badge.style.display = 'flex';
        } else if (badge) {
            badge.style.display = 'none';
        }
    }

    // ── Initialization ──
    async function init() {
        cacheDom();
        renderStepList();
        setupMobileMenu();

        // Terminal clear butonu
        DOM.terminalClear.addEventListener('click', clearTerminal);

        // Step list tıklama
        DOM.stepList.addEventListener('click', (e) => {
            const item = e.target.closest('.step-item');
            if (item) {
                const idx = parseInt(item.dataset.step, 10);
                goToStep(idx);
            }
        });

        // API sağlık kontrolü
        const health = await WizardAPI.healthCheck();
        if (!health.success) {
            showToast('API bağlantısı kurulamadı!', 'error');
            return;
        }

        // State senkronizasyonu
        await syncStateFromServer();

        // Tier bilgisini yükle (lisans daha önce doğrulanmışsa)
        const tierRes = await WizardAPI.getTierInfo();
        if (tierRes.success && tierRes.data.tier) {
            state.tierInfo = tierRes.data;
            renderStepList();
            // Offline Mode göstergesi
            updateOfflineBadge(!!tierRes.data.offline_mode);
        }

        // Log stream başlat
        startLogStream();

        // İlk adımı yükle
        await loadStepContent(state.currentStep);

        showToast('Wizard hazır — kuruluma başlayabilirsiniz.', 'success');

        // ── Online/Offline Event Listeners ──
        window.addEventListener('online', () => {
            updateOfflineBadge(false);
            showToast('İnternet bağlantısı sağlandı.', 'success');
        });
        window.addEventListener('offline', () => {
            updateOfflineBadge(true);
            showToast('İnternet bağlantısı kesildi — çevrimdışı mod aktif.', 'warning');
        });
    }

    // ── StepDeploy — Global deploy fonksiyonu (step HTML fragment'larından çağrılır) ──
    async function stepDeploy(stepId, btnEl) {
        const logEl = document.getElementById(`step${stepId}-log`);
        const healthEl = document.getElementById(`step${stepId}-health`);

        // Butonu devre dışı bırak
        if (btnEl) { btnEl.disabled = true; btnEl.textContent = '⏳ Deploy ediliyor...'; }
        if (logEl) logEl.innerHTML = '<span style="color:var(--health-yellow);">Deploy başlatılıyor...</span>';
        if (healthEl) { healthEl.textContent = '⏳ Çalışıyor'; healthEl.style.color = 'var(--health-yellow)'; }

        try {
            const result = await WizardAPI.request(`/api/install/deploy/${encodeURIComponent(stepId)}`, { method: 'POST' });
            if (result.success) {
                const data = result.data;
                const allOk = data.results ? data.results.every(r => r.success) : true;

                if (logEl) {
                    logEl.innerHTML = (data.results || []).map(r =>
                        `<div style="color:${r.success ? 'var(--health-green)' : 'var(--health-red)'};">` +
                        `${r.success ? '✅' : '❌'} ${escapeHtml(r.service || '')} — ${escapeHtml(r.message || '')}</div>`
                    ).join('') || '<div style="color:var(--health-green);">✅ Deploy tamamlandı.</div>';
                }
                if (healthEl) {
                    healthEl.textContent = allOk ? '✅ Healthy' : '⚠️ Kısmi Hata';
                    healthEl.style.color = allOk ? 'var(--health-green)' : 'var(--health-yellow)';
                }
                if (allOk) {
                    showToast(`Step ${stepId} deploy başarılı.`, 'success');
                    await syncStateFromServer();
                    updateStepListUI();
                    updateProgress();
                } else {
                    showToast(`Step ${stepId} kısmi hata — logları kontrol edin.`, 'warning');
                }
            } else {
                throw new Error(result.error || 'Deploy başarısız');
            }
        } catch (err) {
            if (logEl) logEl.innerHTML = `<span style="color:var(--health-red);">❌ ${escapeHtml(err.message)}</span>`;
            if (healthEl) { healthEl.textContent = '❌ Başarısız'; healthEl.style.color = 'var(--health-red)'; }
            showToast(`Step ${stepId} deploy hatası: ${err.message}`, 'error');
        } finally {
            if (btnEl) { btnEl.disabled = false; btnEl.textContent = '🚀 Yeniden Dene'; }
        }
    }

    // stepDeploy'u global scope'a taşı (HTML fragment'larından onclick ile erişim için)
    window.stepDeploy = stepDeploy;

    // Sayfa yüklendiğinde başlat
    document.addEventListener('DOMContentLoaded', init);

    // ── Public API ──
    return {
        nextStep,
        goToStep,
        showToast,
        syncStateFromServer,
        getState: () => state,
        getSteps: () => STEPS,
        setTierInfo: (info) => {
            const oldTier = state.tierInfo.tier;
            state.tierInfo = info;
            renderStepList();
            if (oldTier !== info.tier) notifyDependencyUpdate('tierInfo.tier');
        },
        setNetworkState: (data) => {
            const prev = { ...state.network };
            Object.assign(state.network, data);
            if (prev.domain !== state.network.domain) notifyDependencyUpdate('network.domain');
            if (prev.server_ip !== state.network.server_ip) notifyDependencyUpdate('network.server_ip');
        },
        onDependencyUpdate,
        updateOfflineBadge,
        escapeHtml,
        stepDeploy,
        TIER_HARDWARE_REQUIREMENTS,
    };
})();
