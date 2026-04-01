/**
 * MEGA-STACK UI Master Script v1.0
 * Dashboard'un "Görsel Beyni" — 7 ana sayfa için merkezi UI yönetimi.
 *
 * Modüller:
 *   1. MegaAuth     — Güvenli fetch wrapper (401/403 → /login/ redirect)
 *   2. MegaBranding  — Global branding & identity (/api/uisettings)
 *   3. MegaHealth    — Live Health Badges (60s polling)
 *   4. MegaAuditLog  — Audit Log UI renderer (renk kodlu tablo)
 *
 * Usage:  <script src="/assets/mega-stack-ui.js"></script>  (before </body>)
 * Deps:   Vanilla JS (ES6+), sıfır kütüphane bağımlılığı
 */
(function () {
    'use strict';

    // ═════════════════════════════════════════════════
    //  0. YAPILANDIRMA
    // ═════════════════════════════════════════════════

    const CONFIG = {
        API_UISETTINGS: '/api/uisettings',
        API_HEALTH: '/api/health',
        API_AUDIT_LOGS: '/api/system/audit-logs',
        CACHE_KEY: 'mega_ui_settings',
        CACHE_TTL: 5 * 60 * 1000,          // 5 dakika
        HEALTH_INTERVAL: 60 * 1000,         // 60 saniye
        LOGIN_PATH: '/login/',
        HEALTH_MODULES: [
            { key: 'database', label: 'Database', icon: '🗄️' },
            { key: 'services', label: 'Services', icon: '⚙️' },
            { key: 'telegram', label: 'Telegram', icon: '📨' },
            { key: 'monitor', label: 'Monitor', icon: '📊' }
        ],
        AUDIT_METHOD_COLORS: {
            post: '#A31621',    // Bordo
            get: '#003366',     // Lacivert
            system: '#6f42c1'   // Mor
        }
    };

    // ═════════════════════════════════════════════════
    //  1. MegaAuth — Güvenli Fetch Wrapper
    // ═════════════════════════════════════════════════

    const MegaAuth = {
        /**
         * Güvenli fetch — 401/403 yanıtlarında /login/'e yönlendirir.
         * @param {string} url
         * @param {RequestInit} [opts]
         * @returns {Promise<Response>}
         */
        async fetch(url, opts = {}) {
            const response = await fetch(url, opts);
            if (response.status === 401 || response.status === 403) {
                console.warn('[MegaAuth] Yetkisiz erişim (' + response.status + '), login sayfasına yönlendiriliyor.');
                window.location.href = CONFIG.LOGIN_PATH;
                // Promise'i askıda bırak — redirect gerçekleşecek
                return new Promise(() => {});
            }
            return response;
        },

        /**
         * JSON dönen güvenli fetch.
         * @param {string} url
         * @param {RequestInit} [opts]
         * @returns {Promise<any>}
         */
        async fetchJSON(url, opts = {}) {
            const response = await this.fetch(url, opts);
            if (!response.ok) {
                throw new Error('HTTP ' + response.status + ' — ' + url);
            }
            return response.json();
        }
    };

    // ═════════════════════════════════════════════════
    //  2. MegaBranding — Global Branding & Identity
    // ═════════════════════════════════════════════════

    const MegaBranding = {
        _settings: null,

        // ── Renk yardımcıları ──
        _hexToRgb(hex) {
            const h = hex.replace('#', '');
            return {
                r: parseInt(h.substring(0, 2), 16),
                g: parseInt(h.substring(2, 4), 16),
                b: parseInt(h.substring(4, 6), 16)
            };
        },

        _lighten(hex, amount) {
            const { r, g, b } = this._hexToRgb(hex);
            const lr = Math.min(255, r + Math.round((255 - r) * amount));
            const lg = Math.min(255, g + Math.round((255 - g) * amount));
            const lb = Math.min(255, b + Math.round((255 - b) * amount));
            return '#' + [lr, lg, lb].map(c => c.toString(16).padStart(2, '0')).join('');
        },

        _darken(hex, amount) {
            const { r, g, b } = this._hexToRgb(hex);
            return '#' + [r, g, b]
                .map(c => Math.max(0, Math.round(c * (1 - amount))).toString(16).padStart(2, '0'))
                .join('');
        },

        _rgba(hex, alpha) {
            const { r, g, b } = this._hexToRgb(hex);
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        },

        _escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        },

        // ── Önbellek ──
        _getCached() {
            try {
                const raw = sessionStorage.getItem(CONFIG.CACHE_KEY);
                if (!raw) return null;
                const cached = JSON.parse(raw);
                if (Date.now() - cached._ts > CONFIG.CACHE_TTL) {
                    sessionStorage.removeItem(CONFIG.CACHE_KEY);
                    return null;
                }
                return cached;
            } catch {
                return null;
            }
        },

        _setCache(settings) {
            try {
                const copy = Object.assign({}, settings, { _ts: Date.now() });
                sessionStorage.setItem(CONFIG.CACHE_KEY, JSON.stringify(copy));
            } catch { /* sessizce devam */ }
        },

        // ── CSS Değişkenlerini Uygula ──
        _applyColors(s) {
            const root = document.documentElement;
            const { primary_color: p, secondary_color: sec, accent_color: acc } = s;

            if (p) {
                root.style.setProperty('--brand-navy', p);
                root.style.setProperty('--brand-navy-light', this._lighten(p, 0.3));
                root.style.setProperty('--brand-navy-dark', this._darken(p, 0.5));
                root.style.setProperty('--surface', this._rgba(p, 0.25));
                root.style.setProperty('--surface2', this._rgba(p, 0.35));
                root.style.setProperty('--glass-bg', this._rgba(p, 0.15));
                root.style.setProperty('--glass-border', this._rgba(p, 0.3));

                const bgDark = this._darken(p, 0.85);
                root.style.setProperty('--bg', bgDark);
                root.style.setProperty('--bg-gradient',
                    `linear-gradient(135deg, ${bgDark} 0%, ${this._darken(p, 0.78)} 25%, ${this._darken(p, 0.7)} 50%, ${this._darken(p, 0.78)} 75%, ${bgDark} 100%)`
                );
            }

            if (sec) {
                root.style.setProperty('--brand-burgundy', sec);
                root.style.setProperty('--brand-burgundy-light', this._lighten(sec, 0.2));
                root.style.setProperty('--brand-burgundy-dark', this._darken(sec, 0.25));
                root.style.setProperty('--accent-brand', sec);
            }

            if (acc) {
                root.style.setProperty('--accent', acc);
            }
        },

        // ── DOM Branding ──
        _applyDOM(s) {
            const esc = this._escapeHtml.bind(this);

            // Title: "Brand Name | Page Name"
            if (s.brand_name) {
                const pageName = document.documentElement.getAttribute('data-page-name');
                if (pageName) {
                    document.title = s.brand_name + ' | ' + pageName;
                } else {
                    const orig = document.title;
                    for (const sep of [' — ', ' | ', ' - ']) {
                        const idx = orig.indexOf(sep);
                        if (idx > 0) {
                            document.title = s.brand_name + ' | ' + orig.substring(idx + sep.length);
                            break;
                        }
                    }
                }
            }

            // Favicon
            const faviconSrc = s.logo_icon_url || s.favicon_url;
            if (faviconSrc) {
                let fav = document.querySelector('link[rel*="icon"]');
                if (fav) {
                    fav.href = faviconSrc;
                } else {
                    fav = document.createElement('link');
                    fav.rel = 'icon';
                    fav.href = faviconSrc;
                    document.head.appendChild(fav);
                }
            }

            // Logo images
            if (s.logo_full_url) {
                document.querySelectorAll('.brand-logo, [data-brand="logo-full"]').forEach(img => {
                    img.src = s.logo_full_url;
                    if (s.brand_name) img.alt = s.brand_name;
                });
            }
            if (s.logo_icon_url) {
                document.querySelectorAll('.brand-icon, [data-brand="logo-icon"]').forEach(img => {
                    img.src = s.logo_icon_url;
                    if (s.brand_name) img.alt = s.brand_name;
                });
            }

            // Brand name
            if (s.brand_name) {
                document.querySelectorAll('[data-brand="name"]').forEach(el => {
                    el.textContent = s.brand_name;
                });
            }

            // System name
            if (s.system_name) {
                document.querySelectorAll('[data-brand="system-name"]').forEach(el => {
                    el.textContent = s.system_name;
                });
                document.querySelectorAll('[data-brand="powered-by"]').forEach(el => {
                    el.innerHTML = 'Powered by <strong>' + esc(s.system_name) + '</strong>';
                });
            }

            // Domain
            if (s.domain) {
                document.querySelectorAll('[data-brand="domain"]').forEach(el => {
                    el.textContent = s.domain;
                    if (el.tagName === 'A') el.href = 'https://' + s.domain;
                });

                // Subdomain linkleri
                document.querySelectorAll('[data-brand-subdomain]').forEach(el => {
                    const sub = el.getAttribute('data-brand-subdomain');
                    const full = sub ? sub + '.' + s.domain : s.domain;
                    if (el.tagName === 'A') el.href = 'https://' + full;
                });
                document.querySelectorAll('[data-brand-subdomain-text]').forEach(el => {
                    const sub = el.getAttribute('data-brand-subdomain-text');
                    const suffix = el.getAttribute('data-brand-url-suffix') || '';
                    el.textContent = (sub ? sub + '.' + s.domain : s.domain) + suffix;
                });
            }

            // Header title
            if (s.brand_name) {
                document.querySelectorAll('[data-brand="header-title"]').forEach(el => {
                    const pageLabel = el.getAttribute('data-page-label') || '';
                    el.innerHTML = '&#9881; <span>' + esc(s.brand_name) + ' </span>' + esc(pageLabel);
                });
            }

            // Header subtitle
            if (s.domain) {
                document.querySelectorAll('[data-brand="header-subtitle"]').forEach(el => {
                    const prefix = el.getAttribute('data-prefix') || '';
                    el.innerHTML = esc(prefix) + esc(s.domain);
                });
            }
        },

        // ── Tam uygulama ──
        apply(settings) {
            this._settings = settings;
            this._applyColors(settings);
            this._applyDOM(settings);
        },

        // ── Init ──
        async init() {
            // Önce cache'den uygula (hızlı render, FOUC önleme)
            const cached = this._getCached();
            if (cached) this.apply(cached);

            try {
                const settings = await MegaAuth.fetchJSON(CONFIG.API_UISETTINGS);
                this._setCache(settings);
                this.apply(settings);
            } catch (err) {
                console.warn('[MegaBranding] Ayarlar yüklenemedi:', err.message);
            }
        },

        getSettings() {
            return this._settings;
        }
    };

    // ═════════════════════════════════════════════════
    //  3. MegaHealth — Live Health Badges
    // ═════════════════════════════════════════════════

    const MegaHealth = {
        _intervalId: null,

        _render(container, modules, status) {
            container.innerHTML = modules.map(m => {
                let isUp = false;
                if (status) {
                    // API sağlıklıysa tüm modüller ayakta kabul edilir
                    isUp = status.status === 'healthy' || status.status === 'ok' ||
                        status[m.key] === 'up' || status[m.key + '_status'] === 'up';
                }
                const cls = isUp ? 'up' : 'down';
                const glowCls = isUp ? 'bg-success glow' : 'bg-danger pulse';
                return `<span class="health-badge ${cls}" data-glow="${glowCls}">` +
                    `<span class="health-dot ${cls}"></span> ${m.icon} ${m.label}</span>`;
            }).join('');
        },

        async _load() {
            const container = document.getElementById('healthBadges');
            if (!container) return;

            try {
                const data = await MegaAuth.fetchJSON(CONFIG.API_HEALTH);
                this._render(container, CONFIG.HEALTH_MODULES, data);
            } catch {
                // API erişilemez → tüm badge'leri DOWN yap
                container.querySelectorAll('.health-badge').forEach(b => {
                    b.className = 'health-badge down';
                    const dot = b.querySelector('.health-dot');
                    if (dot) dot.className = 'health-dot down';
                });
            }
        },

        init() {
            this._load();
            this._intervalId = setInterval(() => this._load(), CONFIG.HEALTH_INTERVAL);
        },

        stop() {
            if (this._intervalId) {
                clearInterval(this._intervalId);
                this._intervalId = null;
            }
        },

        refresh() {
            this._load();
        }
    };

    // ═════════════════════════════════════════════════
    //  4. MegaAuditLog — Audit Log UI Renderer
    // ═════════════════════════════════════════════════

    const MegaAuditLog = {

        _page: 1,
        _pageSize: 20,
        _totalRecords: 0,
        _totalPages: 1,
        _searchTerm: '',

        _escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        },

        /**
         * Action string'inden method tipi çıkar.
         * POST → bordo, GET → lacivert, System → mor
         */
        _getMethodType(action) {
            if (!action) return 'system';
            const a = action.toLowerCase();
            if (a.includes('update') || a.includes('upload') || a.includes('add') ||
                a.includes('remove') || a.includes('unban') || a.includes('action') ||
                a.includes('preset') || a.includes('change') || a.includes('delete') ||
                a.includes('create') || a.includes('import') || a.includes('run') ||
                a.includes('restart') || a.includes('prune')) {
                return 'post';
            }
            if (a.includes('check') || a.includes('view') || a.includes('list') ||
                a.includes('health') || a.includes('status') || a.includes('get') ||
                a.includes('read') || a.includes('fetch')) {
                return 'get';
            }
            return 'system';
        },

        _formatTime(ts) {
            if (!ts) return '-';
            try {
                const iso = ts.includes('T') ? ts : ts.replace(' ', 'T');
                const d = new Date(iso);
                if (isNaN(d.getTime())) return ts;
                return d.toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric' }) + ' ' +
                    d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            } catch {
                return ts;
            }
        },

        _buildRow(log) {
            const esc = this._escapeHtml;
            const method = this._getMethodType(log.action);
            let userBadge = '';
            if (log.user_context) {
                try {
                    const uc = typeof log.user_context === 'string' ? JSON.parse(log.user_context) : log.user_context;
                    userBadge = '<span class="audit-user-badge" title="IP: ' + esc(uc.ip || '') + ' | HWID: ' + esc(uc.hwid || '') + '">' +
                        '👤 ' + esc(uc.user || 'admin') + ' <span class="audit-role-tag">' + esc(uc.role || '') + '</span></span>';
                } catch(_) {}
            }
            return '<tr>' +
                '<td class="audit-time">' + this._formatTime(log.timestamp) + '</td>' +
                '<td><span class="audit-method-badge ' + method + '">' + method.toUpperCase() + '</span></td>' +
                '<td><span class="audit-module">' + esc(log.module) + '</span></td>' +
                '<td>' + esc(log.action) + '</td>' +
                '<td class="audit-user-col">' + (userBadge || '<span class="audit-user-system">⚙ system</span>') + '</td>' +
                '<td style="max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" ' +
                'title="' + esc(log.details || '') + '">' + esc(log.details || '-') + '</td>' +
                '</tr>';
        },

        changePageSize(val) {
            this._pageSize = parseInt(val, 10) || 20;
            this._page = 1;
            this.load();
        },

        goToPage(p) {
            p = parseInt(p, 10);
            if (isNaN(p) || p < 1) p = 1;
            if (p > this._totalPages) p = this._totalPages;
            this._page = p;
            this.load();
        },

        search(term) {
            this._searchTerm = (term || '').trim();
            this._page = 1;
            this.load();
        },

        _renderPagination(logs) {
            const tbody = document.getElementById('auditTableBody');
            const pagination = document.getElementById('auditPagination');
            if (!tbody) return;

            if (logs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="audit-empty">' +
                    (this._searchTerm ? 'Arama sonucu bulunamadı' : 'Henüz audit kaydı yok') + '</td></tr>';
                if (pagination) pagination.style.display = 'none';
                return;
            }

            tbody.innerHTML = logs.map(log => this._buildRow(log)).join('');

            if (pagination) {
                if (this._totalPages <= 1) {
                    pagination.style.display = 'none';
                    return;
                }
                pagination.style.display = 'flex';

                const start = (this._page - 1) * this._pageSize + 1;
                const end = Math.min(start + logs.length - 1, this._totalRecords);

                const infoEl = document.getElementById('auditPaginationInfo');
                if (infoEl) {
                    infoEl.textContent = start + '-' + end + ' / ' + this._totalRecords + ' kayıt';
                }

                const ctrlEl = document.getElementById('auditPaginationControls');
                if (ctrlEl) {
                    let btns = '';
                    btns += '<button class="audit-page-btn" onclick="MegaStackUI.auditGoToPage(1)" ' + (this._page === 1 ? 'disabled' : '') + '>&laquo;</button>';
                    btns += '<button class="audit-page-btn" onclick="MegaStackUI.auditGoToPage(' + (this._page - 1) + ')" ' + (this._page === 1 ? 'disabled' : '') + '>&lsaquo;</button>';

                    let startP = Math.max(1, this._page - 2);
                    let endP = Math.min(this._totalPages, startP + 4);
                    if (endP - startP < 4) startP = Math.max(1, endP - 4);

                    for (let i = startP; i <= endP; i++) {
                        btns += '<button class="audit-page-btn' + (i === this._page ? ' active' : '') + '" onclick="MegaStackUI.auditGoToPage(' + i + ')">' + i + '</button>';
                    }

                    btns += '<button class="audit-page-btn" onclick="MegaStackUI.auditGoToPage(' + (this._page + 1) + ')" ' + (this._page === this._totalPages ? 'disabled' : '') + '>&rsaquo;</button>';
                    btns += '<button class="audit-page-btn" onclick="MegaStackUI.auditGoToPage(' + this._totalPages + ')" ' + (this._page === this._totalPages ? 'disabled' : '') + '>&raquo;</button>';
                    ctrlEl.innerHTML = btns;
                }
            }
        },

        async load() {
            const tbody = document.getElementById('auditTableBody');
            if (!tbody) return;

            tbody.innerHTML = '<tr><td colspan="5" class="audit-empty">Yükleniyor...</td></tr>';
            const pagination = document.getElementById('auditPagination');
            if (pagination) pagination.style.display = 'none';

            // Dropdown'dan mevcut seçimi al
            const sel = document.getElementById('auditPageSize');
            if (sel) this._pageSize = parseInt(sel.value, 10) || 20;

            try {
                let url = CONFIG.API_AUDIT_LOGS + '?page=' + this._page + '&page_size=' + this._pageSize;
                if (this._searchTerm) {
                    url += '&search=' + encodeURIComponent(this._searchTerm);
                }
                const data = await MegaAuth.fetchJSON(url);
                this._totalRecords = data.total_records || 0;
                this._totalPages = data.total_pages || 1;
                this._page = data.page || 1;
                this._renderPagination(data.logs || []);
            } catch (err) {
                tbody.innerHTML = '<tr><td colspan="5" class="audit-empty">Audit loglar yüklenemedi: ' +
                    this._escapeHtml(err.message) + '</td></tr>';
            }
        },

        init() {
            if (document.getElementById('auditTableBody')) {
                this.load();
                this._bindRefresh();
                this._bindPageSize();
            }
        },

        _bindRefresh() {
            const btn = document.querySelector('.audit-refresh');
            if (btn) {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.load();
                });
            }
        },

        _bindPageSize() {
            const sel = document.getElementById('auditPageSize');
            if (sel) {
                sel.addEventListener('change', () => {
                    this.changePageSize(sel.value);
                });
            }
        }
    };

    // ═════════════════════════════════════════════════
    //  5. ORCHESTRATOR — Başlatma Sırası
    // ═════════════════════════════════════════════════

    async function init() {
        try {
            // Phase 1: Branding (en yüksek öncelik — görsel tutarlılık)
            await MegaBranding.init();
        } catch (err) {
            console.warn('[MegaUI] Branding init hatası:', err.message);
        }

        // Phase 2: Health Badges (arka plan polling)
        MegaHealth.init();

        // Phase 3: Audit Log (varsa render et)
        MegaAuditLog.init();
    }

    // DOM hazır olunca başlat
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ═════════════════════════════════════════════════
    //  6. GLOBAL API — Dış erişim
    // ═════════════════════════════════════════════════

    window.MegaStackUI = {
        /** Branding ayarlarını yeniden yükle */
        reloadBranding: () => MegaBranding.init(),

        /** Ayarları manuel uygula (admin panelden anında yansıma) */
        applySettings: (settings) => {
            MegaBranding._setCache(settings);
            MegaBranding.apply(settings);
        },

        /** Mevcut branding ayarlarını döndür */
        getSettings: () => MegaBranding.getSettings(),

        /** Health badge'leri anında yenile */
        refreshHealth: () => MegaHealth.refresh(),

        /** Health polling'i durdur */
        stopHealth: () => MegaHealth.stop(),

        /** Audit logları yeniden yükle */
        refreshAuditLogs: () => MegaAuditLog.load(),

        /** Audit sayfa değiştir */
        auditGoToPage: (p) => MegaAuditLog.goToPage(p),

        /** Audit sayfa boyutu değiştir */
        auditChangePageSize: (val) => MegaAuditLog.changePageSize(val),

        /** Audit log arama */
        auditSearch: (term) => MegaAuditLog.search(term),

        /** Güvenli fetch wrapper */
        fetch: (url, opts) => MegaAuth.fetch(url, opts),
        fetchJSON: (url, opts) => MegaAuth.fetchJSON(url, opts)
    };

    // Geriye uyumluluk — eski brand-manager.js API'si
    window.MegaBrandManager = {
        reload: () => MegaBranding.init(),
        applySettings: (s) => {
            MegaBranding._setCache(s);
            MegaBranding.apply(s);
        }
    };

})();
