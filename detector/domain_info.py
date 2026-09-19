import socket
from urllib.parse import urlparse


def get_domain_info(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    try:
        ip_address = socket.gethostbyname(domain)
        dns_status = "Resolved"
    except socket.gaierror:
        ip_address = "Not Found"
        dns_status = "Failed"

    return {
        "domain": domain,
        "ip": ip_address,
        "protocol": parsed.scheme,
        "dns_status": dns_status
    }
