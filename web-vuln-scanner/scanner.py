import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime

visited_urls = set()
vulnerabilities = []

xss_payload = "<script>alert('XSS')</script>"
sql_payloads = ["' OR '1'='1", "';--"]

sql_errors = [
    "sql syntax",
    "mysql",
    "database error",
    "unclosed quotation"
]


def crawl(url):
    to_visit = [url]

    while to_visit:
        current = to_visit.pop()

        if current in visited_urls:
            continue

        visited_urls.add(current)

        try:
            response = requests.get(current, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link['href'])

                if url in full_url:
                    to_visit.append(full_url)

        except:
            pass

    return visited_urls


def get_forms(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except:
        return []


def detect_sql_error(text):
    for error in sql_errors:
        if re.search(error, text, re.IGNORECASE):
            return True
    return False


def log_vulnerability(vuln_type, url, payload, evidence, severity, recommendation):
    vulnerabilities.append({
        "type": vuln_type,
        "url": url,
        "payload": payload,
        "evidence": evidence,
        "severity": severity,
        "recommendation": recommendation
    })


def test_xss(url, form):
    action = form.get("action")
    method = form.get("method", "get").lower()
    target_url = urljoin(url, action)

    inputs = form.find_all("input")
    data = {}

    for input_tag in inputs:
        name = input_tag.get("name")
        if name:
            data[name] = xss_payload

    try:
        if method == "post":
            response = requests.post(target_url, data=data)
        else:
            response = requests.get(target_url, params=data)

        if xss_payload in response.text:
            log_vulnerability(
                "Cross-Site Scripting (XSS)",
                target_url,
                xss_payload,
                "Payload reflected in response",
                "High",
                "Sanitize user inputs & implement output encoding"
            )

    except:
        pass


def test_sqli(url, form):
    action = form.get("action")
    method = form.get("method", "get").lower()
    target_url = urljoin(url, action)

    inputs = form.find_all("input")

    for payload in sql_payloads:
        data = {}

        for input_tag in inputs:
            name = input_tag.get("name")
            if name:
                data[name] = payload

        try:
            if method == "post":
                response = requests.post(target_url, data=data)
            else:
                response = requests.get(target_url, params=data)

            if detect_sql_error(response.text):
                log_vulnerability(
                    "SQL Injection (SQLi)",
                    target_url,
                    payload,
                    "Database error message detected",
                    "High",
                    "Use parameterized queries / prepared statements"
                )

        except:
            pass


def run_scan(target_url):
    visited_urls.clear()
    vulnerabilities.clear()

    start_time = datetime.now()

    pages = crawl(target_url)

    for page in pages:
        forms = get_forms(page)

        for form in forms:
            test_xss(page, form)
            test_sqli(page, form)

    end_time = datetime.now()

    summary = {
        "total_pages": len(pages),
        "total_vulns": len(vulnerabilities),
        "scan_time": str(end_time - start_time)
    }

    return vulnerabilities, summary
