import requests
from bs4 import BeautifulSoup
import re
import socket
import ssl

FAKE_KEYWORDS = [
    "earn money fast", "work from home", "miracle", "investment opportunity",
    "limited time offer", "100% guaranteed", "act now", "get rich quick",
    "binary options", "no experience", "only today", "exclusive deal"
]

def get_text_from_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"Error fetching website: {e}"

def check_https(url):
    if not url.startswith("https://"):
        return False
    try:
        hostname = url.replace("https://", "").split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname):
                return True
    except Exception:
        return False

def detect_fake_website(url):
    result = {
        "url": url,
        "status": "Likely Genuine",
        "reason": [],
        "uses_https": check_https(url)
    }

    website_text = get_text_from_url(url)

    if website_text.startswith("Error"):
        result["status"] = "Likely Fake"
        result["reason"].append("Website not accessible or timed out")
        return result

    lower_text = website_text.lower()
    keyword_hits = [kw for kw in FAKE_KEYWORDS if kw in lower_text]
    if keyword_hits:
        result["status"] = "Suspicious"
        result["reason"].append(f"Contains suspicious keywords: {', '.join(keyword_hits)}")

    if not re.search(r"@|contact|email|phone|linkedin", lower_text):
        result["status"] = "Suspicious"
        result["reason"].append("No contact info or LinkedIn/email found")

    if len(website_text) < 500:
        result["status"] = "Likely Fake"
        result["reason"].append("Very little content on the site")

    return result
