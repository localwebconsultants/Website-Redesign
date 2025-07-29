
import requests
from bs4 import BeautifulSoup
import time

def get_html(url):
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except:
        return ""

def has_responsive_meta_tag(html):
    return 'name="viewport"' in html.lower()

def uses_tiny_fonts(html):
    soup = BeautifulSoup(html, "html.parser")
    styles = soup.find_all("style")
    for style in styles:
        if "font-size" in style.text and "px" in style.text:
            sizes = [int(s.strip("px;")) for s in style.text.split() if "px" in s.strip(";")]
            if any(size < 12 for size in sizes):
                return True
    return False

def measure_load_time(url):
    try:
        start = time.time()
        requests.get(url, timeout=10)
        end = time.time()
        return round(end - start, 2)
    except:
        return 999

def analyze_website(url):
    score = 100
    issues = []

    if not url.startswith("https://"):
        issues.append("Site does not use HTTPS.")
        score -= 15

    html = get_html(url)
    if "<title>" not in html.lower():
        issues.append("Missing <title> tag.")
        score -= 10
    if 'meta name="description"' not in html.lower():
        issues.append("Missing meta description.")
        score -= 5

    if not has_responsive_meta_tag(html):
        issues.append("No responsive meta tag for mobile.")
        score -= 20
    if uses_tiny_fonts(html):
        issues.append("Font sizes are too small.")
        score -= 10

    load_time = measure_load_time(url)
    if load_time > 5:
        issues.append(f"Page load time is high ({load_time}s).")
        score -= 15

    return {"url": url, "score": max(score, 0), "issues": issues, "load_time": load_time}
