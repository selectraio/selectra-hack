# modules/xss_scanner.py
"""
XSS Tarama Modülü
Severity: High
"""

import re
import html
import time
from modules.utils import RequestHandler

class Scanner:
    """XSS açıklarını tespit eder"""

    NAME = "Cross-Site Scripting (XSS)"
    DESCRIPTION = "XSS açıklarını tespit eder"
    SEVERITY = "High"

    # XSS Payload'ları
    PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>",
        "<select onfocus=alert('XSS') autofocus>",
        "<textarea onfocus=alert('XSS') autofocus>",
        "<video><source onerror=alert('XSS')>",
        "<audio src=x onerror=alert('XSS')>",
        "<marquee onstart=alert('XSS')>",
        "<details open ontoggle=alert('XSS')>",
        "javascript:alert('XSS')",
        "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
    ]

    def __init__(self, target_url, proxy=None):
        self.target_url = target_url
        self.request_handler = RequestHandler(proxy)

    def scan(self):
        """Taramayı çalıştır"""
        result = {
            'module': self.NAME,
            'vulnerable': False,
            'findings': [],
            'tested_payloads': 0
        }

        test_params = ['q', 'search', 's', 'query', 'keyword', 'name', 'comment']

        for param in test_params:
            for payload in self.PAYLOADS:
                test_url = f"{self.target_url}?{param}={payload}"
                response = self.request_handler.get(test_url)

                if response:
                    result['tested_payloads'] += 1

                    # Payload yansıma kontrolü
                    if payload in response.text:
                        decoded_response = html.unescape(response.text)
                        if payload in decoded_response:
                            finding = {
                                'type': 'Reflected XSS',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': 'Payload reflected without proper encoding',
                                'severity': self.SEVERITY
                            }
                            result['findings'].append(finding)
                            result['vulnerable'] = True

                time.sleep(0.3)

        return result
