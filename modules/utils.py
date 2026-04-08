# modules/utils.py
"""
Yardımcı fonksiyonlar ve sınıflar
"""

import requests
import random
import time
import urllib3
from urllib.parse import urljoin, urlparse

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RequestHandler:
    """HTTP isteklerini yöneten sınıf"""

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

    def __init__(self, proxy=None, timeout=30):
        self.proxy = proxy
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def get(self, url, **kwargs):
        """GET isteği gönder"""
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
        try:
            return self.session.get(
                url, 
                proxies=proxies, 
                timeout=self.timeout,
                verify=False,
                allow_redirects=True,
                **kwargs
            )
        except Exception as e:
            return None

    def post(self, url, **kwargs):
        """POST isteği gönder"""
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
        try:
            return self.session.post(
                url, 
                proxies=proxies, 
                timeout=self.timeout,
                verify=False,
                allow_redirects=True,
                **kwargs
            )
        except Exception as e:
            return None

class ProxyRotator:
    """Proxy rotasyon sınıfı"""

    def __init__(self, proxy_list):
        self.proxies = proxy_list
        self.current_index = 0

    def get_next_proxy(self):
        """Sıradaki proxy'yi al"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
