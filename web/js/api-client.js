/**
 * MEGA-STACK v2.5 Installation Wizard — API Client
 * FastAPI endpoint'leri ile asenkron haberleşme katmanı.
 */

const WizardAPI = (() => {
    'use strict';

    const BASE_URL = window.location.origin;

    // ── Generic Fetch Wrapper ──
    async function request(endpoint, options = {}) {
        const url = `${BASE_URL}${endpoint}`;
        const config = {
            headers: { 'Content-Type': 'application/json' },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                const errorMsg = data.detail || data.message || `HTTP ${response.status}`;
                throw new Error(errorMsg);
            }

            return { success: true, data };
        } catch (error) {
            console.error(`[API] ${endpoint}:`, error.message);
            return { success: false, error: error.message };
        }
    }

    // ── Health Check ──
    async function healthCheck() {
        return request('/api/health');
    }

    // ── Installation Status ──
    async function getInstallStatus() {
        return request('/api/install/status');
    }

    // ── All Steps ──
    async function getAllSteps() {
        return request('/api/install/steps');
    }

    // ── Advance to Next Step ──
    async function advanceStep() {
        return request('/api/install/next', { method: 'POST' });
    }

    // ── System Resources ──
    async function getSystemResources() {
        return request('/api/system/resources');
    }

    // ── License: Get HWID ──
    async function getHWID() {
        return request('/api/license/hwid');
    }

    // ── License: Verify ──
    async function verifyLicense(licenseKey, userPassword) {
        return request('/api/license/verify', {
            method: 'POST',
            body: JSON.stringify({
                license_key: licenseKey,
                user_password: userPassword || null,
            }),
        });
    }

    // ── License: Tier Info ──
    async function getTierInfo() {
        return request('/api/license/tier-info');
    }

    // ── Domain Config: Set ──
    async function setDomainConfig(config) {
        return request('/api/install/domain-config', {
            method: 'POST',
            body: JSON.stringify(config),
        });
    }

    // ── Domain Config: Get ──
    async function getDomainConfig() {
        return request('/api/install/domain-config');
    }

    // ── Restore Check ──
    async function getRestoreCheck() {
        return request('/api/install/restore-check');
    }

    // ── Log Stream (SSE) ──
    function connectLogStream(onMessage, onError) {
        const evtSource = new EventSource(`${BASE_URL}/api/logs`);

        evtSource.onmessage = (event) => {
            try {
                const logEntry = JSON.parse(event.data);
                if (onMessage) onMessage(logEntry);
            } catch {
                if (onMessage) onMessage({ message: event.data });
            }
        };

        evtSource.onerror = () => {
            if (onError) onError();
            // SSE otomatik yeniden bağlanır
        };

        return evtSource;
    }

    // ── Analytics: Best-Effort Event ──
    async function sendAnalytics() {
        try {
            await request('/api/analytics/send', { method: 'POST' });
        } catch (_) {
            // best-effort — sessizce yut
        }
    }

    // ── DKIM Key Check ──
    async function getDkimKey(domain) {
        const qs = domain ? `?domain=${encodeURIComponent(domain)}` : '';
        return request(`/api/dns/dkim-key${qs}`);
    }

    // ── Public API ──
    return {
        request,
        healthCheck,
        getInstallStatus,
        getAllSteps,
        advanceStep,
        getSystemResources,
        getHWID,
        verifyLicense,
        getTierInfo,
        setDomainConfig,
        getDomainConfig,
        getRestoreCheck,
        connectLogStream,
        sendAnalytics,
        getDkimKey,
    };
})();
