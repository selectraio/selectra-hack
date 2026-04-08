# REPO ZEKASI - Advanced Web Security Scanner

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Termux%20%7C%20Linux-orange.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-red.svg" alt="License">
</p>

REPO ZEKASI, piyasadaki çeşitli güvenlik testi tekniklerini bir araya getiren kapsamlı bir web güvenlik tarayıcısıdır.

## Özellikler

- **100+ Test Modülü**: SQL Injection, XSS, LFI/RFI, Command Injection ve daha fazlası
- **Çoklu Adım Testi**: Her modülde 10 farklı test adımı
- **Proxy Desteği**: HTTP/HTTPS proxy ve otomatik proxy rotasyonu
- **Çoklu İş Parçacığı**: Ayarlanabilir thread sayısı
- **JSON Raporlama**: Detaylı JSON formatında rapor
- **Modüler Yapı**: Kolayca yeni modül eklenebilir
- **Platform Bağımsız**: Termux ve Linux uyumlu

## Kurulum

### Termux

```bash
curl -O https://raw.githubusercontent.com/repo-zekasi/setup_termux.sh
bash setup_termux.sh
```

### Linux

```bash
sudo bash setup_linux.sh
```

## Kullanım

### Temel Kullanım

```bash
python3 repo_zekasi.py https://hedef-site.com
```

### Proxy ile

```bash
python3 repo_zekasi.py https://hedef-site.com -p http://127.0.0.1:8080
```

### Thread Ayarı

```bash
python3 repo_zekasi.py https://hedef-site.com -t 20
```

## Modüller

| Kategori | Modül Sayısı |
|----------|-------------|
| Bilgi Toplama | 10 |
| SQL Injection | 10 |
| XSS | 10 |
| Komut Enjeksiyonu | 6 |
| Dosya İşlemleri | 8 |
| Kimlik Doğrulama | 10 |
| XXE ve Serileştirme | 8 |
| API Güvenliği | 7 |
| SSL/TLS | 8 |
| CMS/Framework | 8 |
| Bulut ve Konteyner | 8 |
| Gelişmiş Teknikler | 7 |

## Yasal Uyarı

Bu araç yalnızca yetkili sistemlerde kullanılmalıdır. İzinsiz sistem taraması yasalara aykırıdır.

## Lisans

MIT License
