#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REPO ZEKASI - Advanced Web Security Scanner
Gelişmiş Web Güvenlik Tarayıcısı
Author: Security Research Team
Version: 1.0.0
"""

import sys
import os
import json
import time
import argparse
import importlib
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class FakeStyle:
        CYAN = GREEN = RED = YELLOW = MAGENTA = ''
        RESET_ALL = ''
    Fore = FakeStyle()
    Style = FakeStyle()

class RepoZekasi:
    """Ana tarayıcı sınıfı"""

    def __init__(self, target_url, proxy=None, threads=10, output_dir="reports"):
        self.target_url = target_url.rstrip('/')
        self.proxy = proxy
        self.threads = threads
        self.output_dir = output_dir
        self.results = []
        self.vulnerabilities = []
        self.modules = []

        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def banner(self):
        """Araç başlığı"""
        banner_text = f"""
{Fore.CYAN}██████╗ ███████╗██████╗  ██████╗      ███████╗███████╗██╗  ██╗ █████╗ ███████╗██╗{Style.RESET_ALL}
{Fore.CYAN}██╔══██╗██╔════╝██╔══██╗██╔═══██╗     ╚══███╔╝██╔════╝██║ ██╔╝██╔══██╗██╔════╝██║{Style.RESET_ALL}
{Fore.CYAN}██████╔╝█████╗  ██████╔╝██║   ██║█████╗  ███╔╝ █████╗  █████╔╝ ███████║███████╗██║{Style.RESET_ALL}
{Fore.CYAN}██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║╚════╝ ███╔╝  ██╔══╝  ██╔═██╗ ██╔══██║╚════██║██║{Style.RESET_ALL}
{Fore.CYAN}██║  ██║███████╗██║     ╚██████╔╝     ███████╗███████╗██║  ██╗██║  ██║███████║██║{Style.RESET_ALL}
{Fore.CYAN}╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝      ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝{Style.RESET_ALL}
{Fore.YELLOW}[*] Advanced Web Security Scanner v1.0.0{Style.RESET_ALL}
{Fore.YELLOW}[*] Target: {self.target_url}{Style.RESET_ALL}
{Fore.YELLOW}[*] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}
"""
        print(banner_text)

    def load_modules(self):
        """Tüm test modüllerini yükle"""
        modules_dir = "modules"
        self.modules = []

        if not os.path.exists(modules_dir):
            print(f"{Fore.RED}[!] Modules directory not found!{Style.RESET_ALL}")
            return False

        for filename in sorted(os.listdir(modules_dir)):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'modules.{module_name}')
                    if hasattr(module, 'Scanner'):
                        self.modules.append({
                            'name': module_name,
                            'module': module,
                            'scanner': module.Scanner
                        })
                except Exception as e:
                    pass

        print(f"{Fore.GREEN}[+] Loaded {len(self.modules)} scan modules{Style.RESET_ALL}")
        return len(self.modules) > 0

    def run_module(self, module_info):
        """Tek bir modül çalıştır"""
        try:
            scanner = module_info['scanner'](self.target_url, self.proxy)
            result = scanner.scan()
            return {
                'module': module_info['name'],
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'module': module_info['name'],
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def run_scan(self):
        """Tüm taramayı çalıştır"""
        self.banner()

        if not self.load_modules():
            return False

        print(f"\n{Fore.CYAN}[*] Starting security scan...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Using {self.threads} threads{Style.RESET_ALL}\n")

        completed = 0
        total = len(self.modules)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_module = {
                executor.submit(self.run_module, mod): mod 
                for mod in self.modules
            }

            for future in concurrent.futures.as_completed(future_to_module):
                module = future_to_module[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    completed += 1

                    status = Fore.GREEN if 'error' not in result else Fore.RED
                    vuln_indicator = ""
                    if 'result' in result and result['result'].get('vulnerable'):
                        self.vulnerabilities.append(result)
                        vuln_indicator = f" {Fore.RED}[VULNERABLE]{Style.RESET_ALL}"

                    print(f"{status}[{completed}/{total}] {module['name']}{vuln_indicator}{Style.RESET_ALL}")

                except Exception as e:
                    print(f"{Fore.RED}[!] Error in {module['name']}: {e}{Style.RESET_ALL}")

        self.generate_report()
        return True

    def generate_report(self):
        """Rapor oluştur"""
        report_file = os.path.join(
            self.output_dir, 
            f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        report = {
            'target': self.target_url,
            'scan_date': datetime.now().isoformat(),
            'total_modules': len(self.modules),
            'vulnerabilities_found': len(self.vulnerabilities),
            'results': self.results,
            'vulnerabilities': self.vulnerabilities
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n{Fore.GREEN}[+] Scan completed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Report saved: {report_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Vulnerabilities found: {len(self.vulnerabilities)}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description='REPO ZEKASI - Advanced Web Security Scanner'
    )
    parser.add_argument(
        'url', 
        help='Target URL to scan (e.g., https://example.com)'
    )
    parser.add_argument(
        '-p', '--proxy',
        help='Proxy URL (e.g., http://127.0.0.1:8080)'
    )
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=10,
        help='Number of threads (default: 10)'
    )
    parser.add_argument(
        '-o', '--output',
        default='reports',
        help='Output directory (default: reports)'
    )

    args = parser.parse_args()

    scanner = RepoZekasi(
        target_url=args.url,
        proxy=args.proxy,
        threads=args.threads,
        output_dir=args.output
    )

    try:
        scanner.run_scan()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main()
