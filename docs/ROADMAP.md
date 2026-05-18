# CyberTeacher v5.0 — Roadmap возможных улучшений

*Фичи, которые можно реализовать БЕЗ внешних сервисов, мульти-пользовательской инфраструктуры,
облачных ресурсов или значительных новых зависимостей.
Последнее обновление: 2026-05-18*

---

## ✅ Выполнено (Спринты 1-5)

### Спринт 1: Quick Wins (10/10 ✅)
| ID | Фича | Статус |
|----|------|--------|
| ACH-01 | Streak Achievements | ✅ Done |
| SHOP-01 | Расширить магазин | ✅ Done |
| CNT-01 | Hybrid Persona | ✅ Done |
| CLI-02 | Статистика при старте | ✅ Done |
| CLI-04 | "Прошлая сессия" | ✅ Done |
| DATA-02 | Синхронизация ачивок | ✅ Done |
| SKL-01 | Decay навыков | ✅ Done |
| SR-01 | Статистика повторений | ✅ Done |
| ANA-01 | Длительность сессии | ✅ Done |
| CQ-03 | Fix `/genassignment` | ✅ Done |

### Спринт 2: Analytics (6/6 ✅)
| ID | Фича | Статус |
|----|------|--------|
| ANA-02 | Command Heatmap | ✅ Done |
| ANA-04 | Writeup Browser | ✅ Done |
| ANA-05 | Exploit Log | ✅ Done |
| SHOP-02 | История покупок | ✅ Done |
| SHOP-03 | Динамические цены | ✅ Done |
| ANA-03 | Learning Velocity | ✅ Done |

### Спринт 3: Skills + SR + CLI (6/6 ✅)
| ID | Фича | Статус |
|----|------|--------|
| SKL-02 | Рекомендации по навыкам | ✅ Done |
| SKL-03 | Сертификаты навыков | ✅ Done |
| SR-02 | Календарь повторений | ✅ Done |
| SR-03 | Session Mode | ✅ Done |
| CLI-03 | Алиасы команд | ✅ Done |
| CLI-05 | Export/Import State | ✅ Done |

### Спринт 4: Content (6/6 ✅)
| ID | Фича | Статус |
|----|------|--------|
| CNT-02 | Prerequisites Graph | ✅ Done |
| CNT-03 | Topic Explorer | ✅ Done |
| CNT-04 | Flashcards | ✅ Done |
| CNT-05 | Glossary | ✅ Done |
| CQ-04 | Улучшить hints | ✅ Done |
| CQ-05 | Code review в квизе | ✅ Done |

### Спринт 5: PWA + Design System (15/15 ✅)
| ID | Фича | Статус |
|----|------|--------|
| PWA-01 | Daily Challenge tab | ✅ Done |
| PWA-02 | Skills tab | ✅ Done |
| PWA-03 | Spaced Repetition tab | ✅ Done |
| PWA-04 | Tracks tab | ✅ Done |
| PWA-05 | Shop tab | ✅ Done |
| NEW | Modes tab | ✅ Done |
| NEW | Profile tab | ✅ Done |
| NEW | Story tab | ✅ Done |
| NEW | CTF tab | ✅ Done |
| NEW | OSINT tab | ✅ Done |
| NEW | Scanner tab | ✅ Done |
| NEW | Malware tab | ✅ Done |
| NEW | 3 Visual Themes (Ocean/Sunset/Matrix) | ✅ Done |
| NEW | Rick Sanchez Persona | ✅ Done |
| NEW | Launcher GUI | ✅ Done |

### Спринт 6: Infrastructure (4/4 ✅)
| ID | Фича | Статус |
|----|------|--------|
| INF-01 | SQLAlchemy abstraction layer | ✅ Done |
| INF-02 | PostgreSQL support | ✅ Done |
| INF-03 | Alembic migrations | ✅ Done |
| INF-04 | Docker Compose (PostgreSQL + pgAdmin) | ✅ Done |

### Спринт 7: Code Polish (4/4 ✅)
| ID | Фича | Статус |
|----|------|--------|
| POL-01 | Ruff linting (0 errors) | ✅ Done |
| POL-02 | Lambda bug fix (F821) | ✅ Done |
| POL-03 | Subprocess safety (PLW1510) | ✅ Done |
| POL-04 | Import sorting + whitespace | ✅ Done |

### Спринт 8: File Organization (5/5 ✅)
| ID | Фича | Статус |
|----|------|--------|
| DATA-03 | Delete 25 junk/temp files | ✅ Done |
| DATA-03 | Delete 6 cache directories | ✅ Done |
| DATA-03 | Move 14 state files → models/ | ✅ Done |
| DATA-03 | Clean backups (keep 3 newest) | ✅ Done |
| DATA-03 | Update .gitignore + imports | ✅ Done |

---

## 📈 Осталось (3 задачи)

### DATA (1 задача)
| ID | Фича | Время | Сложность |
|----|------|-------|-----------|
| DATA-01 | State Migration | 3ч | Medium |

### Code Quality (2 задачи)
| ID | Фича | Время | Сложность |
|----|------|-------|-----------|
| CQ-01 | Type hints 100% | 6ч+ | High |
| CQ-02 | Integration tests | 6ч+ | High |

---

## 📊 Сводка

| Категория | Всего | Выполнено | Осталось |
|-----------|-------|-----------|----------|
| Quick Wins | 10 | 10 | 0 |
| Analytics | 6 | 6 | 0 |
| Skills + SR | 6 | 6 | 0 |
| Content | 6 | 6 | 0 |
| PWA | 14 | 10 | 4 |
| Infrastructure | 4 | 4 | 0 |
| Data | 2 | 1 | 1 |
| Code Quality | 2 | 0 | 2 |
| Code Polish | 4 | 4 | 0 |
| File Organization | 5 | 5 | 0 |
| **ИТОГО** | **59** | **52** | **7** |

**Прогресс: 88% (52/59 задач)**

---

## 🎯 Рекомендуемый порядок

1. ~~**Спринт 7 (PWA Polish):** PWA-06, PWA-07, PWA-08, PWA-09~~ ✅ Done
2. ~~**Спринт 8 (Data + Quality):** DATA-01, DATA-03, CQ-01, CQ-02~~ DATA-03 ✅ Done
3. **Спринт 9 (Remaining):** DATA-01, CQ-01, CQ-02

---

*CyberTeacher v5.0 — 2026-05-18*
