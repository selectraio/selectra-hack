#!/bin/bash
# REPO ZEKASI - Termux Kurulum Scripti
# Version: 1.0.0

echo "[*] REPO ZEKASI - Termux Kurulum Scripti"
echo "[*] Baslatiliyor..."

# Paketleri guncelle
echo "[*] Paketler guncelleniyor..."
pkg update -y
pkg upgrade -y

# Gerekli paketleri kur
echo "[*] Gerekli paketler kuruluyor..."
pkg install -y python python-pip git curl wget nano

# Python kutuphanelerini kur
echo "[*] Python kutuphaneleri kuruluyor..."
pip install requests colorama urllib3 beautifulsoup4 lxml dnspython

# Proje dizinini olustur
echo "[*] Proje dizini olusturuluyor..."
PROJECT_DIR="$HOME/repo_zekasi"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Dizin yapisi
mkdir -p modules
mkdir -p reports
mkdir -p wordlists
mkdir -p proxies

echo "[+] Kurulum tamamlandi!"
echo ""
echo "[*] Kullanim:"
echo "  cd $PROJECT_DIR"
echo "  python repo_zekasi.py https://hedef-site.com"
echo ""
echo "[*] Proxy ile:"
echo "  python repo_zekasi.py https://hedef-site.com -p http://127.0.0.1:8080"
echo ""
echo "[*] Thread ayari:"
echo "  python repo_zekasi.py https://hedef-site.com -t 5"
