def detect_platform(url):
    url = url.lower()
    if "wixsite.com" in url or "wix" in url:
        return "Wix", "High"
    elif "godaddysites.com" in url or "godaddy" in url:
        return "GoDaddy", "Medium"
    elif "squarespace" in url:
        return "Squarespace", "High"
    else:
        return "Unknown", "Low"
