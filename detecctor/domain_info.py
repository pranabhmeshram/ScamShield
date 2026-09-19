from urllib.parse import urlparse
import socket


def get_domain_info(url):
    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname

    if not domain:
        return {
            "domain": "Invalid",
            "ip_address": "Not available",
            "protocol": parsed.scheme,
            "status": "Invalid domain"
        }

    try:
        ip_address = socket.gethostbyname(domain)
        dns_status = "DNS resolution successful"
    except socket.gaierror:
        ip_address = "Not found"
        dns_status = "DNS resolution failed"

    return {
        "domain": domain,
        "ip_address": ip_address,
        "protocol": parsed.scheme.upper(),
        "status": dns_status
    }
