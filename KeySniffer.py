import requests
import re
import urllib.parse
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()


banner = """
██╗  ██╗███████╗██╗   ██╗███████╗███╗   ██╗██╗███████╗███████╗███████╗██████╗ 
██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝████╗  ██║██║██╔════╝██╔════╝██╔════╝██╔══██╗
█████╔╝ █████╗   ╚████╔╝ ███████╗██╔██╗ ██║██║█████╗  █████╗  █████╗  ██████╔╝
██╔═██╗ ██╔══╝    ╚██╔╝  ╚════██║██║╚██╗██║██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗
██║  ██╗███████╗   ██║   ███████║██║ ╚████║██║██║     ██║     ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
"""
console.print(banner, style="bold green")

def find_sensitive_info(js_content):
    patterns = {
        "API Key": r'(?i)(api[_-]?key\s*[:=]\s*["\']?([A-Za-z0-9_\-]{10,})["\']?)',
        "Token": r'(?i)(token\s*[:=]\s*["\']?([A-Za-z0-9_\-]{10,})["\']?)',
        "Captcha": r'(?i)(reCAPTCHA|hcaptcha|data-sitekey)'
    }
    
    found = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, js_content)
        if matches:
            found[key] = [match[1] for match in matches]
    
    return found

def extract_js_urls(url):
    response = requests.get(url)
    if response.status_code != 200:
        console.print("[!] Failed to fetch the website.", style="bold red")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tags = soup.find_all('script', src=True)
    
    js_urls = []
    for tag in script_tags:
        js_url = tag['src']
        if js_url.startswith('http'):
            js_urls.append(js_url)
        else:
            js_urls.append(urllib.parse.urljoin(url, js_url))
    
    return js_urls

def scan_website(url):
    js_files = extract_js_urls(url)
    if not js_files:
        console.print("[!] No JavaScript files found.", style="bold red")
        return
    
    found_any = False
    for js_file in js_files:
        try:
            response = requests.get(js_file)
            if response.status_code == 200:
                found_info = find_sensitive_info(response.text)
                if found_info:
                    console.print(f"[+] Found sensitive info in: {js_file}", style="bold green")
                    for key, values in found_info.items():
                        console.print(f"    - {key}:", style="bold yellow", end=" ")
                        for value in values:
                            if key == "API Key":
                                console.print(value, style="bold red")  # Red for API Key
                            elif key == "Token":
                                console.print(value, style="bold cyan")  # Cyan for Token
                            elif key == "Captcha":
                                console.print(value, style="bold magenta")  # Magenta for Captcha
                    found_any = True
        except Exception as e:
            console.print(f"[!] Error processing {js_file}: {e}", style="bold red")
    
    if not found_any:
        console.print("[-] No sensitive information found.", style="bold red")

if __name__ == "__main__":
    target_url = input("Enter website URL: ")
    scan_website(target_url)

# Unit Tests
import pytest

def test_find_sensitive_info():
    test_js = """
        var apiKey = "12345ABCDE";
        var token = "my-secret-token-67890";
        var sitekey = "6Lc_aXQTAAAAANMy5";
    """
    result = find_sensitive_info(test_js)
    assert "API Key" in result
    assert "Token" in result
    assert "Captcha" in result
    assert result["API Key"] == ["12345ABCDE"]
    assert result["Token"] == ["my-secret-token-67890"]
    assert result["Captcha"] == ["6Lc_aXQTAAAAANMy5"]

def test_find_sensitive_info_no_match():
    test_js = "var safeVar = 'nothing here';"
    result = find_sensitive_info(test_js)
    assert result == {}

if __name__ == "__main__":
    pytest.main()
