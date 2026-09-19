from urllib.parse import urlparse
import re


def analyze_url(url):
    score = 0
    reasons = []

    # Add HTTPS if scheme is missing
    test_url = url

    if not test_url.startswith(("http://", "https://")):
        test_url = "https://" + test_url

    parsed = urlparse(test_url)
    hostname = parsed.hostname or ""

    # 1. HTTPS check
    if parsed.scheme != "https":
        score += 20
        reasons.append("URL does not use HTTPS")

    # 2. URL length check
    if len(url) > 75:
        score += 15
        reasons.append("URL is unusually long")

    # 3. IP address check
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, hostname):
        score += 25
        reasons.append("URL uses an IP address instead of a domain name")

    # 4. @ symbol check
    if "@" in url:
        score += 20
        reasons.append("URL contains @ character")

    # 5. Suspicious keywords
    keywords = [
        "login",
        "signin",
        "verify",
        "verification",
        "password",
        "account",
        "update",
        "secure",
        "free",
        "winner",
        "urgent",
        "confirm"
    ]

    found_keywords = []

    for keyword in keywords:
        if keyword in url.lower():
            found_keywords.append(keyword)

    if found_keywords:
        score += 15
        reasons.append(
            "Suspicious keyword detected: "
            + ", ".join(found_keywords)
        )

    # 6. Multiple subdomains
    domain_parts = hostname.split(".")

    if len(domain_parts) > 3:
        score += 15
        reasons.append("URL contains multiple subdomains")

    # 7. Multiple hyphens
    if hostname.count("-") >= 2:
        score += 10
        reasons.append("Domain contains multiple hyphens")

    # 8. URL contains a suspicious port
    if parsed.port is not None and parsed.port not in [80, 443]:
        score += 10
        reasons.append("URL uses a non-standard port")

    # Maximum score
    score = min(score, 100)

    # Risk classification
    if score < 30:
        status = "Low Risk"
    elif score < 60:
        status = "Medium Risk"
    else:
        status = "High Risk"

    # No suspicious indicators
    if not reasons:
        reasons.append(
            "No obvious suspicious patterns detected"
        )

    return {
        "url": url,
        "score": score,
        "status": status,
        "reasons": reasons
    }
