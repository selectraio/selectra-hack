#!/bin/bash
# REPO ZEKASI - Linux Kurulum Scripti
# Version: 1.0.0

echo "[*] REPO ZEKASI - Linux Kurulum Scripti"
echo "[*] Baslatiliyor..."

# Root kontrolu
if [ "$EUID" -ne 0 ]; then 
    echo "[!] Bu script root yetkisi ile calistirilmali"
    echo "[*] sudo bash setup_linux.sh seklinde calistirin"
    exit 1
fi

# Paketleri guncelle
echo "[*] Paketler guncelleniyor..."
apt update -y
apt upgrade -y

# Gerekli paketleri kur
echo "[*] Gerekli paketler kuruluyor..."
apt install -y python3 python3-pip git curl wget nano nmap masscan

# Python kutuphanelerini kur
echo "[*] Python kutuphaneleri kuruluyor..."
pip3 install requests colorama urllib3 beautifulsoup4 lxml dnspython whois

# Proje dizinini olustur
echo "[*] Proje dizini olusturuluyor..."
INSTALL_DIR="/opt/repo_zekasi"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Dizin yapisi
mkdir -p modules
mkdir -p reports
mkdir -p wordlists
mkdir -p proxies

echo "[+] Kurulum tamamlandi!"
echo ""
echo "[*] Kullanim:"
echo "  cd $INSTALL_DIR"
echo "  python3 repo_zekasi.py https://hedef-site.com"
echo ""
echo "[*] Proxy ile:"
echo "  python3 repo_zekasi.py https://hedef-site.com -p http://127.0.0.1:8080"
echo ""
echo "[*] Thread ayari:"
echo "  python3 repo_zekasi.py https://hedef-site.com -t 20"
