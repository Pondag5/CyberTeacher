# CyberTeacher v6.1 — Roadmap

*Last updated: 2026-09-18 | Version: 6.1*

---

## 🎯 Vision

> **CyberTeacher** → *A living, atmospheric AI cybersecurity mentor that feels present, remembers you, and evolves with you.*

**Core Philosophy**: *Atmosphere > Raw Intelligence* — A smaller model with continuity, memory, and personality beats a stateless giant model.

---

## 📊 Current State (v6.1)

| Metric | Value |
|--------|-------|
| **Tests** | 105+ passed in key modules (85 test files) |
| **Handlers** | 79 |
| **PWA Tabs** | 58 |
| **Story Mechanics** | 15/15 ✅ |
| **Risk Mechanics** | Noise/Trace/Debt/Stealth ✅ |
| **Factions** | Rick/Ghost/Archive ✅ |
| **Cyberpsychosis** | 4 levels, PWA glitches ✅ |
| **Learning Memory** | SQLite + semantic retrieval + personality drift ✅ |
| **Knowledge Base** | FAISS + BM25 full-corpus + RRF + query expansion ✅ |

---

## 🚀 Sprint Plan (Next 6 Weeks)

| Week | Focus | Deliverables |
|------|-------|--------------|
| **1** | **Learning Memory Polish** | CLI command `/reindex_knowledge`, category-aware retrieval UI |
| **2** | **PWA Risk Indicators** | noise bar, trace progress, debt counter |
| **3** | **Knowledge Base UX** | force reindex, category filters in chat |
| **4** | **Netbuk Lab Plan 1** | Docker Labs SSH management |
| **5** | **Platform Prep** | OAuth2 foundation, 2FA groundwork |
| **6** | **Polish + Release v6.2** | Bug fixes, docs, release tag |

---

## 📋 Prioritized Backlog

### 🟢 P3 — Long-term / Platform

| ID | Feature | Effort | Dependencies |
|----|---------|--------|--------------|
| P3-1 | Mobile App (React Native / TWA) | 2-4 weeks | PWA ready |
| P3-2 | OAuth2 (Google, GitHub) | 1-2 weeks | auth.py, JWT |
| P3-3 | 2FA (TOTP) | 1 week | auth.py, pyotp |
| P3-4 | Multi-user Auth (Roles) | 1 week | auth.py, JWT |
| P3-5 | Admin Panel | 1 week | JWT, roles |
| P3-6 | GDPR Export/Import | 3 days | |
| P3-7 | SCORM Export | 2 days | `course_manager.py` |

### 🟡 P2 — Infrastructure

| ID | Feature | Effort | Dependencies |
|----|---------|--------|--------------|
| P2-1 | DB Indexes + Connection Pooling | 1-2d | SQLAlchemy |
| P2-2 | WebSocket Pooling + Auto-reconnect | 2-3d | `api_server.py` |
| P2-3 | LLM Response Caching (SQLite TTL + LRU) | 2-3d | `config.py` |
| P2-4 | PWA SW stale-while-revalidate | 2-3d | `static/sw.js` |
| P2-5 | Portable .exe build (PyInstaller) | 1-2d | PyInstaller |

### 🟠 P1 — Code Debt

| ID | File:Line | Function | Task | Effort |
|----|-----------|----------|------|--------|
| P1-1 | `handlers/quiz.py` | code review | Interactive input / file read + LLM analysis | 2-3d |
| P1-2 | `handlers/hints.py` | mission hint | Hint for current uncompleted mission step | 1-2d |
| P1-3 | `news_fetcher.py` | XMLParsedAsHTMLWarning | Add `features="xml"` to BeautifulSoup | 1h |

### 🔴 P0 — Manual Actions

| ID | Task | Effort |
|----|------|--------|
| P0-1 | API Keys Rotation (manual `/keys rotate`) | 1-2d |
| P0-2 | JWT_SECRET + ENC_KEY hardening | 1h |
| P0-3 | Rate Limiting token bucket | 1-2d |

---

## 📦 Netbuk Lab Plans (8 Ideas)

| Plan | Title | Effort | Priority |
|------|-------|--------|----------|
| NB-1 | Docker Labs Host | 1-2 wks | Medium |
| NB-2 | LXC Network Sandbox | 1-2 wks | Medium |
| NB-3 | Red Team Target | 1-2 wks | Medium |
| NB-4 | WiFi Range (hostapd + aircrack-ng) | 1-2 wks | Low |
| NB-5 | SIEM/Log Collector | 1-2 wks | Medium |
| NB-6 | CTFd Platform | 1-2 wks | Medium |
| NB-7 | Gophish Phishing | 1-2 wks | Low |
| NB-8 | Anomaly Generator + Honeypot | 1-2 wks | Low |

---

## 📊 RICE Prioritization (Top 10)

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| Mobile App (TWA) | 500 | 3 | 0.5 | 20 | 37 | P3 |
| OAuth2 | 300 | 3 | 0.7 | 10 | 63 | P3 |
| 2FA (TOTP) | 200 | 3 | 0.8 | 5 | 48 | P3 |
| Netbuk Plan 1 (Docker Labs) | 200 | 4 | 0.6 | 10 | 48 | P2 |
| Netbuk Plan 6 (CTFd) | 300 | 4 | 0.7 | 14 | 60 | P2 |
| Netbuk Plan 8 (Honeypot) | 100 | 3 | 0.5 | 14 | 15 | P3 |

---

## 🏷️ Definition of Done (Per Feature)

- [ ] Implementation complete
- [ ] Unit tests added (≥3 cases)
- [ ] Integration test passes
- [ ] Documentation updated (README + relevant .md)
- [ ] Code review passed (ruff, mypy clean)
- [ ] Manual QA passed (CLI + PWA)
- [ ] CHANGELOG.md updated

---

*Roadmap is a living document. Review every Monday. Adjust based on learning.*

---

*Last updated: 2026-09-18 | CyberTeacher v6.1*
