"""
MEGA-STACK v2.5 Installation Wizard — DNS Generator
Cloudflare uyumlu DNS import dosyaları üretir (JSON + CSV).
Step 02'de girilen domain/IP bilgilerine göre dinamik çıktı sağlar.
"""

import json
import os
import re
import socket
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from core.logger import wizard_logger

MEGA_STACK_DIR = os.environ.get("MEGA_STACK_DIR", "/opt/mega-stack")
DKIM_KEY_DIR = os.path.join(MEGA_STACK_DIR, "iredmail", "custom", "amavisd", "dkim")


def read_dkim_public_key(domain: str) -> Optional[str]:
    """
    iRedMail DKIM PEM dosyasından public key'i okur.
    Step 09 (iRedMail) deploy edildikten sonra gerçek DKIM anahtarını döner.
    Dosya yoksa veya okunamazsa None döner.
    """
    pem_path = os.path.join(DKIM_KEY_DIR, f"{domain}.pem")
    if not os.path.isfile(pem_path):
        return None
    try:
        import subprocess
        result = subprocess.run(
            ["openssl", "rsa", "-in", pem_path, "-pubout", "-outform", "DER"],
            capture_output=True, timeout=5,
        )
        if result.returncode == 0:
            import base64
            pubkey = base64.b64encode(result.stdout).decode("ascii")
            wizard_logger.info(f"[DNS] DKIM public key okundu: {pem_path}", step_id="02")
            return pubkey
    except Exception as exc:
        wizard_logger.warning(f"[DNS] DKIM key okuma hatası: {exc}", step_id="02")
    return None


# ─── Sabitler ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "dns")

# Servis → subdomain eşleşmesi
SUBDOMAIN_MAP = {
    "core-api":   "api",
    "traefik":    "traefik",
    "authelia":   "auth",
    "dashboard":  "dashboard",
    "cloudbeaver": "db",
    "netdata":    "monitor",
    "uptime-kuma": "status",
    "dozzle":     "logs",
    "portainer":  "portainer",
    "mail":       "mail",
}


# ─── Validasyon ──────────────────────────────────────────────────────────
_DOMAIN_RE = re.compile(
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.[A-Za-z]{2,}$"
)
_IPV4_RE = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)


def validate_domain(domain: str) -> bool:
    """Domain adının geçerliliğini kontrol eder."""
    return bool(_DOMAIN_RE.match(domain))


def validate_ipv4(ip: str) -> bool:
    """IPv4 adresinin geçerliliğini kontrol eder."""
    return bool(_IPV4_RE.match(ip))


def detect_server_ip() -> Optional[str]:
    """
    Sunucunun dış IP adresini tespit etmeye çalışır.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


# ─── DNS Kayıt Üreteci ──────────────────────────────────────────────────
def generate_dns_records(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
) -> list[dict]:
    """
    MEGA-STACK için gerekli tüm DNS A/MX/TXT kayıtlarını üretir.
    """
    if not validate_domain(domain):
        raise ValueError(f"Geçersiz domain: {domain}")
    if not validate_ipv4(server_ip):
        raise ValueError(f"Geçersiz IP adresi: {server_ip}")

    records = []

    # Root domain
    records.append({
        "type": "A", "name": domain, "content": server_ip,
        "ttl": 1, "proxied": True, "comment": "MEGA-STACK root domain",
    })

    # www
    records.append({
        "type": "A", "name": "www", "content": server_ip,
        "ttl": 1, "proxied": True, "comment": "www redirect",
    })

    # Servis subdomain'leri
    for service, subdomain in SUBDOMAIN_MAP.items():
        proxied = service != "mail"  # mail proxied=false
        records.append({
            "type": "A", "name": subdomain, "content": server_ip,
            "ttl": 1, "proxied": proxied, "comment": f"{service} subdomain",
        })

    # MX kaydı
    records.append({
        "type": "MX", "name": domain, "content": f"mail.{domain}",
        "priority": 10, "ttl": 1, "proxied": False, "comment": "Mail exchange record",
    })

    # SPF
    records.append({
        "type": "TXT", "name": domain,
        "content": f"v=spf1 mx a ip4:{server_ip} ~all",
        "ttl": 1, "proxied": False, "comment": "SPF record",
    })

    # DMARC
    records.append({
        "type": "TXT", "name": "_dmarc",
        "content": f"v=DMARC1; p=quarantine; rua=mailto:postmaster@{domain}",
        "ttl": 1, "proxied": False, "comment": "DMARC policy",
    })

    # Extra domain'ler
    if extra_domains:
        for extra in extra_domains:
            records.append({
                "type": "A",
                "name": extra.get("subdomain", extra.get("domain", "")),
                "content": server_ip,
                "ttl": 1,
                "proxied": extra.get("proxied", True),
                "comment": extra.get("comment", "Extra domain"),
            })

    return records


# ─── Cloudflare JSON Export ──────────────────────────────────────────────
def generate_cloudflare_json(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
) -> str:
    """
    Jinja2 şablonu kullanarak Cloudflare uyumlu JSON üretir.
    """
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,
    )
    template = env.get_template("dns/cloudflare_import.json.j2")

    rendered = template.render(
        domain=domain,
        server_ip=server_ip,
        domain_type=domain_type,
        extra_domains=extra_domains or [],
    )

    wizard_logger.info(
        f"[DNS] Cloudflare JSON üretildi: {domain} → {server_ip}",
        step_id="02",
    )

    return rendered


def save_cloudflare_json(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
) -> str:
    """
    Cloudflare JSON dosyasını output/dns/ dizinine kaydeder.
    Dosya yolunu döner.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = generate_cloudflare_json(domain, server_ip, domain_type, extra_domains)
    filename = f"cloudflare-import-{domain}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    wizard_logger.info(
        f"[DNS] JSON dosyası kaydedildi: {filepath}",
        step_id="02",
    )

    return filepath


# ─── Cloudflare CSV Export ───────────────────────────────────────────────
def generate_cloudflare_csv(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
) -> str:
    """
    Cloudflare BIND/CSV formatında DNS kayıtları üretir.
    """
    records = generate_dns_records(domain, server_ip, domain_type, extra_domains)

    lines = []
    for r in records:
        rtype = r["type"]
        name = r["name"]
        content = r["content"]
        proxied = "proxied" if r.get("proxied") else "dns_only"
        comment = r.get("comment", "")

        if rtype == "MX":
            priority = r.get("priority", 10)
            lines.append(f"{name},MX,{content},{priority},{proxied},# {comment}")
        else:
            lines.append(f"{name},{rtype},{content},1,{proxied},# {comment}")

    csv_content = "\n".join(lines)

    wizard_logger.info(
        f"[DNS] Cloudflare CSV üretildi: {domain} → {len(records)} kayıt",
        step_id="02",
    )

    return csv_content


def save_cloudflare_csv(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
) -> str:
    """
    CSV dosyasını output/dns/ dizinine kaydeder.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = generate_cloudflare_csv(domain, server_ip, domain_type, extra_domains)
    filename = f"cloudflare-import-{domain}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    wizard_logger.info(
        f"[DNS] CSV dosyası kaydedildi: {filepath}",
        step_id="02",
    )

    return filepath


# ─── Cloudflare BIND/TXT Export ──────────────────────────────────────────
def generate_bind_export(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
    dkim_public_key: Optional[str] = None,
) -> str:
    """
    Cloudflare uyumlu BIND zone dosyası (.txt) üretir.
    cf_tags=cf-proxied:false etiketleri korunur.
    """
    if not validate_domain(domain):
        raise ValueError(f"Geçersiz domain: {domain}")
    if not validate_ipv4(server_ip):
        raise ValueError(f"Geçersiz IP adresi: {server_ip}")

    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    export_date = now.strftime("%Y-%m-%d %H:%M:%S")
    serial = int(now.timestamp())

    lines = []

    # Header
    lines.append(";;")
    lines.append(f";; Domain:     {domain}.")
    lines.append(f";; Exported:   {export_date}")
    lines.append(";;")
    lines.append(";; This file is intended for use for informational and archival")
    lines.append(";; purposes ONLY and MUST be edited before use on a production")
    lines.append(";; DNS server.  In particular, you must:")
    lines.append(";;   -- update the SOA record with the correct authoritative name server")
    lines.append(";;   -- update the SOA record with the contact e-mail address information")
    lines.append(";;   -- update the NS record(s) with the authoritative name servers for this domain.")
    lines.append(";;")
    lines.append(";; For further information, please consult the BIND documentation")
    lines.append(";; located on the following website:")
    lines.append(";;")
    lines.append(";; http://www.isc.org/")
    lines.append(";;")
    lines.append(";; And RFC 1035:")
    lines.append(";;")
    lines.append(";; http://www.ietf.org/rfc/rfc1035.txt")
    lines.append(";;")
    lines.append(";; Please note that we do NOT offer technical support for any use")
    lines.append(";; of this zone data, the BIND name server, or any other third-party")
    lines.append(";; DNS software.")
    lines.append(";;")
    lines.append(";; Use at your own risk.")

    # SOA
    lines.append(";; SOA Record")
    lines.append(
        f"{domain}\t3600\tIN\tSOA\tchloe.ns.cloudflare.com. dns.cloudflare.com. "
        f"{serial} 10000 2400 604800 3600"
    )
    lines.append("")

    # NS
    lines.append(";; NS Records")
    lines.append(f"{domain}.\t86400\tIN\tNS\tchloe.ns.cloudflare.com.")
    lines.append(f"{domain}.\t86400\tIN\tNS\tcleo.ns.cloudflare.com.")
    lines.append("")

    # A Records — subdomain'ler + root (alfabetik)
    lines.append(";; A Records")
    a_records = []
    for _service, subdomain in sorted(SUBDOMAIN_MAP.items(), key=lambda x: x[1]):
        a_records.append((f"{subdomain}.{domain}.", server_ip))
    # core-api → api (SUBDOMAIN_MAP'te yoksa ekle)
    if "api" not in [s for _, s in SUBDOMAIN_MAP.items()]:
        a_records.append((f"api.{domain}.", server_ip))
    # Extra domains
    if extra_domains:
        for extra in extra_domains:
            sub = extra.get("subdomain", extra.get("domain", ""))
            if sub:
                a_records.append((f"{sub}.{domain}.", server_ip))
    # Root
    a_records.append((f"{domain}.", server_ip))
    # Sort and deduplicate
    seen = set()
    for name, ip in sorted(a_records, key=lambda x: x[0]):
        if name not in seen:
            seen.add(name)
            lines.append(f"{name}\t1\tIN\tA\t{ip} ; cf_tags=cf-proxied:false")
    lines.append("")

    # CNAME
    lines.append(";; CNAME Records")
    lines.append(f"www.{domain}.\t1\tIN\tCNAME\t{domain}. ; cf_tags=cf-proxied:false")
    lines.append("")

    # MX
    lines.append(";; MX Records")
    lines.append(f"{domain}.\t1\tIN\tMX\t10 mail.{domain}.")
    lines.append("")

    # TXT
    lines.append(";; TXT Records")
    lines.append(f'{domain}.\t1\tIN\tTXT\t"v=spf1 ip4:{server_ip} -all"')
    # DKIM: Gerçek anahtar varsa kullan, yoksa placeholder bırak
    dkim_value = dkim_public_key or read_dkim_public_key(domain) or "REPLACE_WITH_DKIM_PUBLIC_KEY_AFTER_IREDMAIL_SETUP"
    lines.append(
        f'dkim._domainkey.{domain}.\t1\tIN\tTXT\t'
        f'"v=DKIM1; p={dkim_value}"'
    )
    lines.append(
        f'_dmarc.{domain}.\t1\tIN\tTXT\t'
        f'"v=DMARC1; p=quarantine; rua=mailto:postmaster@{domain}"'
    )

    content = "\n".join(lines)

    wizard_logger.info(
        f"[DNS] BIND export üretildi: {domain} → {server_ip}",
        step_id="02",
    )

    return content


def save_bind_export(
    domain: str,
    server_ip: str,
    domain_type: str = "static",
    extra_domains: Optional[list[dict]] = None,
    dkim_public_key: Optional[str] = None,
) -> str:
    """BIND .txt dosyasını output/dns/ dizinine kaydeder."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = generate_bind_export(domain, server_ip, domain_type, extra_domains, dkim_public_key)
    filename = f"cloudflare_import_{domain}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    wizard_logger.info(
        f"[DNS] BIND dosyası kaydedildi: {filepath}",
        step_id="02",
    )

    return filepath
