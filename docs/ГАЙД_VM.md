# 🖥️ CyberTeacher - Гайд по лаборатории

## Рекомендуемая система

### VirtualBox (бесплатно)
Скачай: https://www.virtualbox.org/

### Kali Linux (готовый образ)
- Скачать: https://www.kali.org/get-kali/
- образ VMware/VirtualBox

**Уже включено:**
- Nmap, Metasploit, Burp Suite
- SQLmap, John the Ripper
- Wireshark, Hydra
- И 600+ инструментов

## Альтернатива - Ubuntu + установка

### Минимальные требования
- CPU: 4 ядра
- RAM: 8 GB
- SSD: 50 GB

### Установка на Ubuntu/Debian

```bash
# Основные инструменты
sudo apt update
sudo apt install -y nmap wireshark nikto sqlmap

# Для взлома паролей
sudo apt install -y john hydra hashcat

# Веб
sudo apt install -y burpsuite zaproxy

# Скрипты
git clone https://github.com/rebootuser/LinEnum.git
git clone https://github.com/carlospolop/PEASS-ng.git
```

## Облачные лабы (бесплатно)

### TryHackMe
- tryhackme.com
- Лабы для начинающих
- Подсказки внутри

### HackTheBox
- hackthebox.eu
- Более сложные машины
-，需要 VPN

### PortSwigger Web Security Academy
- portswigger.net/web-security/academy
- Бесплатные веб-лабы

## Docker (для изоляции)

```bash
# DVWA - уязвимое веб-приложение
docker run --rm -it -p 8080:80 vulnerables/web-dvwa

# Metasploitable
docker run --rm -it -p 8080:80 tleemcjr/metasploitable2

# OWASP Juice Shop
docker run --rm -it -p 3000:3000 bkimminich/juice-shop
```

## С чего начать новичку

1. **Неделя 1-2:** Kali Linux + basics
   - Изучи терминал
   - Nmap базовые сканы
   
2. **Неделя 3-4:** DVWA + SQLi/XSS
   - Установи DVWA локально
   - Попробуй простые атаки

3. **Неделя 5-6:** TryHackMe
   - Complete Beginner Path
   - 10-15 машин

4. **Неделя 7+:** HTB + CTF
   - Переходи на сложные таски

## Важно

⚠️ **Только на своей машине или с разрешения!**
- Не взламывай чужие системы
- CTF = Legal hacker games
- Используй VPN при лабах

---

*CyberTeacher рекомендует: Начни с TryHackMe - там самые понятные гайды для новичков!*
