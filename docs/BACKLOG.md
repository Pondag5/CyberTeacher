# CyberTeacher v4.2 — Backlog (не сейчас)

*Фичи, которые НЕВОЗМОЖНО реализовать без внешних сервисов, облачных ресурсов или значительных новых зависимостей.
Отложены до изменения архитектуры или появления ресурсов.
Последнее обновление: 2026-05-18*

---

## 🏫 Enterprise / LMS

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| M-13 | SCORM / LTI | Для учебных заведений, не для соло | SCORM runtime, LTI provider |
| M-14 | Плагинная архитектура | Избыточно для одного пользователя | Plugin framework, sandboxing |
| M-15 | Курсы от экспертов | Будет через миссии/треки | Content pipeline, review system |
| NEW | Curriculum Builder | Drag-n-drop конструктор | Visual editor, dependency graph UI |
| NEW | Auto-alignment (MITRE ATT&CK) | Нужна external база | MITRE API, mapping engine |
| NEW | Student dashboard | Multi-user analytics | User isolation, admin panel |
| NEW | Predictive dropout | Нужен датасет 1000+ юзеров | ML model, training data |

---

## ☁️ Cloud / DevOps

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| NEW | Docker Swarm/K8s | Overkill для CLI-инструмента | Cluster infrastructure |
| NEW | Blue-green deployments | Нет production сервера | Load balancer, CI/CD pipeline |
| NEW | Automated backups to S3 | Нужен cloud storage | AWS/GCP account, credentials |
| NEW | Health checks + alerting | Нужен monitoring | Prometheus, webhook endpoints |
| NEW | Persona marketplace | Нужен хостинг/ревестр | Registry server, content moderation |
| NEW | File sharing | Нужен storage backend | Cloud storage, access control |
| NEW | Versioning uploads | Нужна VFS | Git-like storage system |

---

## 🌐 External APIs (требуют ключей/подписок)

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| NEW | Real CVE database | Нужен NVD API | API key, rate limit handling |
| NEW | Real Shodan data | Платный API | Shodan API key ($49+/мес) |
| NEW | Real Censys data | Платный API | Censys API key |
| NEW | Real HTB machines | Нужен OAuth | HTB API access token |
| NEW | Real THM rooms | Нужен API key | THM API access |
| NEW | VirusTotal integration | Платный API | VT API key (4 req/min free) |
| NEW | Real threat intel feeds | Нужны подписки | MISP, AlienVault OTX |

---

## 📊 Advanced Analytics (нужны данные)

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| NEW | Predictive dropout | Нужен датасет | 1000+ пользователей, ML pipeline |
| NEW | Auto-generated PDF reports | Нужен PDF engine | ReportLab/WeasyPrint, templates |
| NEW | Learning style detection | Нужен ML model | Training data, classification |
| NEW | Comparative analytics | Нужны другие юзеры | Anonymized data pool |

---

## ♿ Accessibility

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| NEW | High-contrast mode | CLI ограничен | Rich theme system (частично возможно) |
| NEW | Screen reader optimization | CLI не поддерживает ARIA | Terminal accessibility standards |
| NEW | Keyboard-only navigation | Уже работает в CLI | Нечего добавлять |

---

## 📱 Mobile (требует отдельной разработки)

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| NEW | Native iOS app | Отдельная кодовая база | Swift, Xcode, App Store |
| NEW | Native Android app | Отдельная кодовая база | Kotlin, Android Studio, Play Store |
| NEW | Push notifications | Нужен push server | Firebase/APNs, device tokens |

---

## 🔒 Security & Compliance

| ID | Фича | Почему не сейчас | Что нужно |
|----|------|------------------|-----------|
| NEW | GDPR/FERPA compliance | Не актуально для локального CLI | Data anonymization, export/delete |
| NEW | Sandbox escape detection | Нужен kernel-level monitoring | eBPF, seccomp, auditd |
| NEW | Secret scanning | Уже есть в Semgrep | Нечего добавлять |

---

## 📝 Отложено (низкий приоритет)

| ID | Фича | Причина |
|----|------|---------|
| L-07 | Перевод комментариев на английский | Низкий приоритет, не влияет на функциональность |
| T-01 | Integration/E2E тесты | Высокая сложность, низкий ROI для соло-проекта |

---

## 💡 Когда можно вернуться

| Условие | Какие фичи станут возможны |
|---------|---------------------------|
| Появится датасет 1000+ юзеров | Predictive analytics, learning style detection |
| Появится бюджет на API | Real CVE, Shodan, Censys, VirusTotal |
| Появится команда | Native apps, SCORM/LTI, marketplace |
| Появится production deployment | Blue-green, K8s, automated backups |

---

*CyberTeacher v4.4 — 2026-05-18*
