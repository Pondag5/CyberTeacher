# CyberTeacher — 8 Netbuk Lab Plans

*Last updated: 2026-09-20*
*Status: All planned, none implemented yet*

---

## Legend

| Status | Meaning |
|--------|---------|
| 📋 Planned | Documented, not started |
| 🔄 In Progress | Work started |
| ✅ Done | Implemented |
| ❌ Cut | Intentionally excluded |

---

## Available Hardware

| Device | Role | Target Plans |
|--------|------|--------------|
| ASUS 1001PX | Fixed target / lab host | Plan 1, Plan 2, Plan 3 |
| Redmi 9A (Ubuntu Touch) | Portable target | Plan 3 (lightweight) |

---

## Plan 1 — Docker Labs Host (ASUS 1001PX)

**Goal:** noiseless host for vulnerable web apps (DVWA, WebGoat, Juice Shop). Managed via SSH from CyberTeacher.

**Why ASUS:** Atom N550 is enough for one lightweight container at a time. Do not run multiple containers in parallel.

**Steps:**
1. Install Debian 12 32-bit minimal + SSH
2. Install Docker: `sudo apt install docker.io docker-compose-v2`
3. Add user to docker group: `sudo usermod -aG docker $USER`
4. Verify: `docker run hello-world`
5. Prepare `docker-compose.yml` for each lab in `~/labs/<lab_name>/`
6. Enable Docker on boot: `sudo systemctl enable docker`
7. Configure SSH key auth from main PC
8. Test: `ssh user@asus-ip "docker compose -f ~/labs/dvwa/docker-compose.yml up -d"`

**Integration:**
- CyberTeacher sends SSH commands to start/stop labs
- Returns target URL to student

**Status:** 📋 Planned

---

## Plan 2 — LXC Network Sandbox (ASUS 1001PX)

**Goal:** emulate small network: attacker + victim + router, including IPv6.

**Why ASUS:** LXC is lighter than Docker. Can run 1-2 containers simultaneously.

**Steps:**
1. Install LXC: `sudo apt install lxc lxc-templates`
2. Configure lxcbr0 bridge
3. Create attacker and victim containers
4. Set up IPv6 if needed
5. Configure routing between containers

**Status:** 📋 Planned

---

## Plan 3 — Red Team Target (ASUS 1001PX / Redmi 9A)

**Goal:** fixed vulnerable machine for scanning and exploitation practice.

**Why ASUS:** can run vulnerable services natively (FTP, Telnet, Samba, old PHP).
**Why Redmi 9A:** portable target, one lightweight service at a time.

### ASUS Setup:
1. Install vulnerable services:
   - `sudo apt install vsftpd telnetd samba`
   - Install old PHP version if needed
2. Configure each service with weak credentials
3. Set static IP: `192.168.1.100/24`
4. Disable firewall or configure rules
5. Document all services and credentials

### Redmi 9A Setup:
1. Install Ubuntu Touch + OpenSSH
2. Install one lightweight service (e.g., simple HTTP server with old PHP)
3. Use as "pocket target" for demos

**Integration:**
- CyberTeacher references fixed target IP in missions
- Student scans, exploits, captures flags

**Status:** 📋 Planned

---

## Plan 4 — WiFi Range (ASUS 1001PX)

**Goal:** hostapd + aircrack-ng for WiFi security practice.

**Why ASUS:** WiFi adapter may support monitor mode (check with `airmon-ng`).

**Status:** 📋 Planned (hardware-dependent)

---

## Plan 5 — SIEM/Log Collector (ASUS 1001PX)

**Goal:** rsyslog + Loki/Grafana for log analysis practice.

**Why ASUS:** lightweight log collection is feasible, but Grafana UI will be slow on Atom N550. Use GoAccess as alternative.

**Status:** 📋 Planned

---

## Plan 6 — CTFd Platform (ASUS 1001PX)

**Goal:** self-hosted CTFd for challenges.

**Why NOT ASUS:** PHP + MySQL + Redis will be slow on Atom N550 + 1-2GB RAM. Better on main PC or VPS.

**Status:** 📋 Planned (recommended for main PC or VPS)

---

## Plan 7 — Gophish Phishing (ASUS 1001PX)

**Goal:** phishing campaigns for social engineering practice.

**Why NOT ASUS:** SMTP + web UI + templates will be slow. Better on main PC.

**Status:** 📋 Planned (recommended for main PC)

---

## Plan 8 — Anomaly Generator + Honeypot (ASUS 1001PX)

**Goal:** Cowrie/Dionaea + traffic generator for IDS practice.

**Why NOT ASUS:** CPU and disk will be overloaded. Better on main PC.

**Status:** 📋 Planned (recommended for main PC)

---

## Recommended Order

1. Plan 3 (Red Team Target) — ASUS or Redmi, fastest to deploy
2. Plan 1 (Docker Labs) — after Plan 3, if Docker works on ASUS
3. Plan 2 (LXC Sandbox) — if need network emulation
4. Plan 5 (SIEM) — lightweight log collection
5. Plans 6-8 — deploy on main PC or VPS

---

## Integration with CyberTeacher

- SSH key auth from main PC to ASUS/Redmi
- Commands in CyberTeacher: `/target start|stop|status`
- API endpoints in `api_server.py` for target control
- Missions reference target IP directly

---

*Update this file when starting implementation of each plan.*

2. **Создай шаблон контейнера**  
   - Создай базовый 32-битный Debian контейнер:  
     `sudo lxc-create -n debian-base -t download -- --dist debian --release bookworm --arch i386`  
   - Запусти его, настрой базовые вещи (SSH, обновления), затем останови и скопируй для будущих узлов:  
     `sudo lxc-copy -n debian-base -N attacker`  
     `sudo lxc-copy -n debian-base -N victim1` и т.д.

3. **Создай изолированную сеть для лаборатории**  
   - В `/etc/lxc/lxc.conf` или в конфигах контейнеров пропиши мост, отличный от lxcbr0, например `lxcbr-lab` с подсетью `10.99.0.0/24`.  
   - Или используй виртуальные Ethernet-пары для ручного связывания — но мост проще.

4. **Настрой контейнеры под роли**  
   - **attacker**: установи минимальный Kali-подобный инструментарий (`nmap`, `hydra`, `metasploit` под i386 сложно, но можно `nmap` и скрипты). Или просто Debian + `nmap`, `python3`, `curl`.  
   - **victim1**: уязвимый веб-сервер (apache2 + намеренно старая конфигурация, открытый telnet).  
   - **victim2**: машина с бэкдором (например, netcat слушает порт).  
   - **router**: настрой пересылку пакетов и `radvd` для IPv6.  
     - Включи IPv6 на хосте (нетбуке), выдай контейнерам IPv6 ULA-адреса. В router-контейнере настрой `radvd` для авто-конфигурации других контейнеров.

5. **Запуск всей песочницы**  
   - Напиши скрипт `start-lab.sh`, который последовательно запускает контейнеры и выводит их IP.  
   - Убедись, что с атакующего контейнера видны жертвы (пинг, nmap).

6. **Интеграция с CyberTeacher**  
   - В проекте сделай задание: «Просканируй сеть 10.99.0.0/24, найди уязвимый хост». CyberTeacher через SSH запускает скрипт старта на нетбуке и выдаёт студенту доступ к attacker (или просто IP-адреса, если студент сам запускает атаки со своего ПК, но тогда сеть нетбука должна быть доступна извне — тут лучше пробросить порты или дать доступ к attacker через SSH).

7. **Автоматизация и сброс**  
   - Скрипт `reset-lab.sh`, который удаляет контейнеры и заново копирует из базового образа, чтобы вернуть полигон в исходное состояние.

**Результат:** лёгкая среда для тренировок по сетевой разведке и эксплуатации, которую можно мгновенно пересоздавать.

---

## План 3. «Железная» цель для внешних атак (Red Team)

**Цель:** нетбук выглядит как настоящий плохо настроенный сервер в локальной сети — студенты должны его обнаружить и атаковать.

### Шаги:

1. **Установи уязвимые сервисы прямо на хосте (нетбуке)**  
   - **FTP:** `sudo apt install proftpd`, в конфиге разреши анонимный вход с записью.  
   - **Telnet:** `sudo apt install telnetd`, разреши root-логин (для учебных целей).  
   - **Веб-сервер со старым PHP:** установи Apache + PHP 5.6 из внешних репов (осторожно, 32-bit). Либо просто оставь дефолтную страницу с инъекцией в логах.  
   - **Samba с открытым шаром:** `sudo apt install samba`, расшарь папку `/tmp` без пароля.

2. **Настрой файрвол так, чтобы выглядело реалистично, но с дырами**  
   - Используй `iptables` или `ufw`: открой порты 21, 23, 80, 445, но закрой всё остальное.  
   - Специально оставь неправильное правило, которое позволяет подключиться с определённого IP (или наоборот, забудь закрыть порт 3306).

3. **Изолируй нетбук в отдельный VLAN или подсеть (опционально)**  
   - Если роутер позволяет, помести нетбук в гостевую сеть, чтобы студенты не поломали домашние устройства.  
   - Или просто дай ему статический IP и предупреди: «цель — 192.168.1.200».

4. **Отключи автообновления и усложни обнаружение**  
   - Смени баннеры сервисов, чтобы не палить версию (например, измени `ServerSignature Off` в Apache, но оставь уязвимость).

5. **Интеграция с CyberTeacher**  
   - Сценарий: «В сети есть неизвестное устройство, получи над ним контроль». CyberTeacher выдаёт только подсеть.  
   - Нетбук постоянно включен, IP фиксирован (можно записать в конфиг урока).  
   - После успешной атаки студент может оставить «флаг» в `/root/flag.txt` — ты можешь проверять его наличие для автоматической оценки.

6. **Сброс к исходному состоянию**  
   - Напиши Ansible playbook или shell-скрипт, который удаляет все изменения и восстанавливает конфиги. Запускай по SSH.

**Результат:** реалистичная цель, которая реагирует как настоящий сервер, без эмуляции.

---

## План 4. Автономный Wi‑Fi‑полигон

**Цель:** нетбук становится учебной точкой доступа и одновременно жертвой/сниффером для отработки атак на Wi-Fi.

### Шаги:

1. **Проверь совместимость Wi-Fi-адаптера**  
   - Встроенный адаптер (скорее всего Broadcom/Atheros) должен поддерживать режим AP (hostapd) и, возможно, monitor mode.  
   - Проверь: `iw list | grep -A 10 "Supported interface modes"` — если есть `AP` и `monitor`, отлично.  
   - Для атак в режиме монитора лучше купить USB-свисток на чипе Ralink RT5370 или Atheros AR9271 (стоят копейки, поддерживаются из коробки).

2. **Настрой точку доступа**  
   - Установи `hostapd` и `dnsmasq`:  
     `sudo apt install hostapd dnsmasq`  
   - Сконфигурируй `hostapd.conf` для открытой/WEP/WPA2 сети. Например, сеть `CyberLab` с WPA2 и простым паролем.  
   - Настрой `dnsmasq` для раздачи IP в подсети (например, 192.168.99.0/24).  
   - Запусти службы.

3. **Подключи второй Wi-Fi-адаптер (для атак)**  
   - USB-свисток вставь, переведи в режим монитора:  
     `sudo ip link set wlan1 down`  
     `sudo iw wlan1 set monitor control`  
     `sudo ip link set wlan1 up`  
   - Установи `aircrack-ng`: `sudo apt install aircrack-ng`.

4. **Сценарии для CyberTeacher**  
   - **Задание 1:** «Взломай WPA2 соседской сети CyberLab». Студент со своего ноутбука (или через attacker-контейнер из Плана 2) выполняет перехват рукопожатия и подбор пароля по словарю.  
   - **Задание 2:** «Проведи атаку деаутентификации на клиента сети CyberLab». Предварительно подключи к точке доступа телефон или второй ноутбук как жертву.  
   - **Задание 3:** «Перехвати трафик открытой сети CyberLab» — настрой AP без шифрования, студент снифает пароли.

5. **Автоматизация**  
   - Скрипт, который переключает нетбук в режим «жертва-AP» или «сниффер».  
   - После окончания упражнения — скрипт сброса, отключающий AP и возвращающий обычный Wi-Fi клиент.

6. **Безопасность**  
   - Сеть должна быть изолирована от домашней (т.е. нетбук не должен маршрутизировать трафик между своим Wi-Fi и домашним роутером). Для этого не включай IP forwarding и не настраивай NAT.

**Результат:** мобильный стенд для пентеста Wi-Fi, управляемый удалённо.

---

## План 5. Хранилище логов и SIEM для учебных стендов

**Цель:** нетбук собирает syslog и другие логи с лабораторных машин, отображает их для анализа.

### Шаги:

1. **Установи центральный syslog-сервер**  
   - `sudo apt install rsyslog` (или syslog-ng). Настрой приём логов по UDP/514.  
   - В конфиге `/etc/rsyslog.conf` раскомментируй модули imudp и разреши приём с сети.

2. **Настрой лабораторные машины (контейнеры или хосты) на отправку логов**  
   - В каждой машине из Плана 2 или 3 добавь запись в `/etc/rsyslog.conf`: `*.* @<ip-нетбука>:514`  
   - Перезапусти rsyslog.

3. **Лёгкая визуализация**  
   - Вместо тяжёлого Elasticsearch используй **Loki + Grafana** (есть 32-битные бинарники?) или простое решение:  
     - Напиши скрипт на Python, который парсит файлы логов и генерирует статический HTML с таблицами.  
     - Либо поставь `lnav` (Log File Navigator) с веб-интерфейсом (запускается на порту).  
   - Как вариант: **GoAccess** для логов веб-сервера — очень лёгкий, выводит красивую статистику в HTML.

4. **Настройка для учебных сценариев**  
   - В CyberTeacher создай модуль «Анализ логов»: после выполнения атаки студент заходит на веб-страницу нетбука (например, http://asus-ip:8888) и видит все попытки входа, ошибки.  
   - Можно заранее инжектировать в логи «следы атак», чтобы студенты искали индикаторы компрометации.

5. **Автоматическая очистка**  
   - Логи могут быстро заполнить SSD. Настрой logrotate для ежедневной архивации и удаления старых данных.

6. **Интеграция через API**  
   - Простой веб-сервер на Python, который отдаёт последние строки логов или количество событий по типам. CyberTeacher дёргает его для отображения в интерфейсе.

**Результат:** централизованный сбор логов без тяжёлой инфраструктуры, наглядно показывающий последствия атак.

---

Конечно, давай придумаем что-то ещё. Я помню, что классические NAS/ретро/Pi‑hole уже не интересуют, а предыдущие пять пунктов (Docker, LXC-сеть, Red Team цель, Wi‑Fi полигон, SIEM) у тебя записаны. Теперь нужен свежий взгляд — что ещё может делать этот слабый, но надёжный нетбук для твоего проекта CyberTeacher. Держи ещё **три идеи**, которые не дублируют предыдущие и заточены именно под обучение кибербезопасности.

---

### **Идея 6. Легковесная CTF‑платформа (CTFd) для проведения мини‑соревнований**

**Суть:** Поднять собственный сервер с CTFd (популярная платформа Capture The Flag) прямо на нетбуке. Студенты заходят на веб‑интерфейс, решают задания, а ты администрируешь соревнования. Atom N450 спокойно тянет CTFd на SQLite для небольшой группы (до 30 человек).

**Почему это круто для CyberTeacher:**
- Можно создавать кастомные задания, привязанные к твоим лабораториям (например, флаг лежит в контейнере из Плана 1).
- Нетбук всегда включен, соревнования доступны 24/7.
- Не требует мощного железа: Python + SQLite + веб‑сервер uWSGI/gunicorn.

#### План реализации (краткий):

1. **Установи зависимости**  
   - `sudo apt install python3 python3-pip python3-venv git nginx`  
   - Для 32-бит могут быть нюансы с pre-built wheels, но CTFd ставится из исходников.

2. **Клонируй CTFd и настрой**  
   - `git clone https://github.com/CTFd/CTFd.git`  
   - `cd CTFd && python3 -m venv venv && source venv/bin/activate`  
   - `pip install -r requirements.txt` (если будут проблемы с пакетами — используй `--no-binary`).

3. **Запусти через gunicorn + nginx**  
   - Сконфигурируй nginx как reverse proxy на порт 8000.  
   - Создай systemd-юнит для автоматического запуска.

4. **Настрой админку**  
   - Зайди по IP, создай первого пользователя-админа, настрой типы заданий (standard, dynamic).  
   - Добавь пару тестовых флагов, проверь работу.

5. **Интеграция с CyberTeacher**  
   - Можно сделать модуль, который через API CTFd автоматически добавляет задания после прохождения урока. Либо просто давать ссылку на CTFd как на «арену» для проверки навыков.

**Результат:** Собственная CTF-песочница без интернета, идеально для практических экзаменов.

---

### **Идея 7. Фишинг‑симулятор (Gophish) для тренировки пользователей**

**Суть:** Нетбук становится сервером для запуска имитационных фишинговых кампаний. Ты создаёшь шаблоны писем, целевые группы (студентов), рассылаешь «вредные» ссылки и отслеживаешь, кто кликнул. Gophish написан на Go, очень лёгкий, есть 32‑битные билды.

**Почему это круто для CyberTeacher:**
- Отличный модуль по социальной инженерии: студенты не только учатся защищаться, но и видят, как работают атаки.
- Нетбук выступает и почтовым сервером (smtp-ретранслятором), и панелью управления.
- Ресурсов ест минимум, работает даже на 512 МБ ОЗУ.

#### План реализации (краткий):

1. **Скачай Gophish под 32‑бит Linux**  
   - С официального GitHub возьми архив `gophish-vX.X-linux-386.tar.gz` (если нет готового — можно собрать из исходников на Go, но бинарник проще).

2. **Распакуй и настрой конфиг**  
   - В `config.json` укажи порты админки (3333) и фишинг-сервера (80/443).  
   - Для отправки писем используй встроенный SMTP-ретранслятор (или внешний, если есть).

3. **Настрой записи DNS**  
   - Чтобы фишинговые ссылки выглядели правдоподобно, пропиши A-запись на IP нетбука (например, `update.cyberteacher.local`). В локальной сети можно просто использовать hosts-файлы или dnsmasq.

4. **Создай кампании и шаблоны**  
   - Через веб-интерфейс (http://asus-ip:3333) залогинься (admin/gophish по умолчанию).  
   - Импортируй реалистичный шаблон письма (например, фальшивое уведомление от деканата) и создай целевую группу из email’ов студентов.

5. **Интеграция с CyberTeacher**  
   - Урок: «Распознай фишинговое письмо». Студенты получают учебную рассылку, результаты кликов показываются преподавателю.  
   - API Gophish позволяет автоматически запускать кампании из твоего проекта.

**Результат:** Реалистичный тренажёр по социальной инженерии, изолированный внутри сети.

---

### **Идея 8. Генератор аномального трафика и honeypot-коллектор**

**Суть:** Нетбук одновременно:
- Генерирует подозрительный сетевой трафик (сканирования, попытки эксплуатации), чтобы студенты учились настраивать IDS/IPS (например, Suricata на другом хосте) и мониторинг.
- Собирает атаки со всего мира (или из локальной сети) на свои приманки (honeypots), давая материал для анализа.

Такой «злобный брат-близнец» предыдущих планов: он не жертва, а имитатор атакующего и наблюдатель за реальными атаками.

**Почему это круто для CyberTeacher:**
- Учебный красный-против-синего: нетбук генерит шум, а студенты должны его задетектировать.
- Honeypot (Cowrie, Dionaea) покажет, какие атаки происходят в реальном времени, если пробросить порт наружу (осторожно!).
- Оба компонента легковесны.

#### План реализации (краткий):

1. **Генератор трафика — DDoS-симуляция и сканирования**  
   - Установи `hping3`, `nmap`, `slowhttptest`.  
   - Напиши простые скрипты bash, которые по расписанию (cron) запускают сканирование портов учебных целей (контейнеров), медленный HTTP-флуд и т.п.  
   - Опционально — используй `scapy` (Python) для крафта кастомных пакетов (IP-спуфинг, аномалии). На 32-бит Debian Scapy работает.

2. **Honeypot-сервер**  
   - Установи **Cowrie** (эмуляция SSH/Telnet) — Python, очень лёгкий.  
     `sudo apt install python3-venv`, затем установка из git.  
   - Настрой проброс порта 22 роутера на порт 2222 нетбука (если хочешь ловить атаки из интернета). Или оставь локально.  
   - Установи **Dionaea** (ловит SMB, HTTP, FTP атаки) — сложнее скомпилировать, но есть Docker-образ для i386? Может быть проще использовать готовый легковесный honeypot вроде **Honeyd** или **T-Pot** не подойдёт по ресурсам, но есть micro-tpot.

3. **Визуализация для студентов**  
   - Логи Cowrie в реальном времени можно транслировать через веб-сокеты или просто отдавать файл логов по HTTP.  
   - Напиши простой Flask-сервер (Python), отображающий последние 20 попыток входа с геолокацией (GeoIP).

4. **Сценарий для CyberTeacher**  
   - Задание: «Настрой Snort/Suricata так, чтобы детектить атаки с этого IP». Генератор на нетбуке начинает посылать аномалии, студент должен написать правило.  
   - Или: «Проанализируй логи Cowrie, найди самые популярные пароли атакующих».

5. **Безопасность**  
   - Если открываешь наружу, обязательно ограничь сетевой доступ файрволом, запускай honeypot в контейнере/песочнице. Но для учебных целей внутри сети — абсолютно безопасно.

**Результат:** Многофункциональный «активный» элемент лаборатории, который и атакует, и подставляется.

---