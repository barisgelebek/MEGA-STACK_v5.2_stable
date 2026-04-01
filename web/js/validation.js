/**
 * MEGA-STACK v2.5 Installation Wizard — Validation Logic
 * HWID, Domain, Form doğrulama regex kuralları.
 */

const WizardValidation = (() => {
    'use strict';

    // ── Regex Patterns ──
    const PATTERNS = {
        // Domain: example.com, sub.example.com (xn-- IDN desteği dahil)
        domain: /^(?!:\/\/)([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$/,

        // IPv4
        ipv4: /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/,

        // HWID: 64 hex karakter (SHA-256)
        hwid: /^[a-f0-9]{64}$/i,

        // License key: en az 8 karakter, alfanumerik + tire
        licenseKey: /^[A-Za-z0-9\-]{8,512}$/,

        // Cloudflare Zone ID: 32 hex karakter
        cfZoneId: /^[a-f0-9]{32}$/i,

        // Brand name: 2-64 karakter
        brandName: /^[\p{L}\p{N}\s\-_.]{2,64}$/u,

        // Email
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,

        // R2 Endpoint: https://<account_id>.r2.cloudflarestorage.com
        r2Endpoint: /^https:\/\/[a-f0-9]{32}\.r2\.cloudflarestorage\.com$/i,
    };

    // ── Doğrulama Fonksiyonları ──
    function validateDomain(value) {
        if (!value || !value.trim()) {
            return { valid: false, error: 'Domain adresi boş olamaz.' };
        }
        const trimmed = value.trim().toLowerCase();
        if (PATTERNS.domain.test(trimmed)) {
            return { valid: true, value: trimmed };
        }
        if (PATTERNS.ipv4.test(trimmed)) {
            return { valid: true, value: trimmed };
        }
        return { valid: false, error: 'Geçerli bir domain (örn: example.com) veya IP adresi girin.' };
    }

    function validateLicenseKey(value) {
        if (!value || !value.trim()) {
            return { valid: false, error: 'Lisans anahtarı boş olamaz.' };
        }
        const trimmed = value.trim();
        if (!PATTERNS.licenseKey.test(trimmed)) {
            return { valid: false, error: 'Lisans anahtarı en az 8 karakter olmalı (alfanumerik ve tire).' };
        }
        return { valid: true, value: trimmed };
    }

    function validateHWID(value) {
        if (!value) return { valid: false, error: 'HWID boş.' };
        return PATTERNS.hwid.test(value)
            ? { valid: true, value }
            : { valid: false, error: 'HWID 64 haneli hex olmalı.' };
    }

    function validateBrandName(value) {
        if (!value || !value.trim()) {
            return { valid: false, error: 'Marka adı boş olamaz.' };
        }
        const trimmed = value.trim();
        if (!PATTERNS.brandName.test(trimmed)) {
            return { valid: false, error: 'Marka adı 2-64 karakter olmalı.' };
        }
        return { valid: true, value: trimmed };
    }

    function validateCfZoneId(value) {
        if (!value || !value.trim()) {
            return { valid: true, value: null }; // Opsiyonel
        }
        const trimmed = value.trim();
        if (!PATTERNS.cfZoneId.test(trimmed)) {
            return { valid: false, error: 'Zone ID 32 haneli hex olmalı.' };
        }
        return { valid: true, value: trimmed };
    }

    function validateRequired(value, fieldName) {
        if (!value || (typeof value === 'string' && !value.trim())) {
            return { valid: false, error: `${fieldName} boş olamaz.` };
        }
        return { valid: true, value: typeof value === 'string' ? value.trim() : value };
    }

    // ── Form-Level Doğrulama Helper ──
    function showFieldError(inputEl, message) {
        clearFieldError(inputEl);
        inputEl.style.borderColor = 'var(--health-red)';
        const errorEl = document.createElement('div');
        errorEl.className = 'form-error';
        errorEl.textContent = message;
        inputEl.parentNode.appendChild(errorEl);
    }

    function clearFieldError(inputEl) {
        inputEl.style.borderColor = '';
        const existing = inputEl.parentNode.querySelector('.form-error');
        if (existing) existing.remove();
    }

    function clearAllErrors(containerEl) {
        containerEl.querySelectorAll('.form-error').forEach(el => el.remove());
        containerEl.querySelectorAll('input, select').forEach(el => {
            el.style.borderColor = '';
        });
    }

    // ── Public API ──
    return {
        PATTERNS,
        validateDomain,
        validateLicenseKey,
        validateHWID,
        validateBrandName,
        validateCfZoneId,
        validateRequired,
        showFieldError,
        clearFieldError,
        clearAllErrors,
    };
})();
