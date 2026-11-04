# CyberTeacher v6.1 — Roadmap

*Last updated: 2026-10-30 | Version: 6.1*

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
| **1** | **Learning Memory Polish** | CLI command `/reindex_knowledge`, category-aware retrieval UI ✅ (API + UI in progress) |
| **2** | **PWA Risk Indicators** | noise bar, trace progress, debt counter ✅ (live updates added) |
| **3** | **Knowledge Base UX** | force reindex, category filters in chat |
| **4** | **Netbuk Lab Plan 1** | Docker Labs SSH management |
| **5** | **Platform Prep** | OAuth2 foundation, 2FA groundwork |
| **6** | **Polish + Release v6.2** | Bug fixes, docs, release tag |

---

## 📋 Prioritized Backlog

### 🔴 P0 — Critical Fixes (from "НОВЫЙ ВЗГЛЯД")

| ID | Task | Effort | Status |
|----|------|--------|--------|
| P0-1 | **Add `lxml` to requirements.txt** (fix XML/RSS parsing) | 5m | ⏳ TODO |
| P0-2 | **Fix news_fetcher.py XML parsing** (use `features="xml"` where needed) | 30m | ⏳ TODO |
| P0-3 | API Keys Rotation (manual `/keys rotate`) | 1-2d | ⏳ TODO |
| P0-4 | JWT_SECRET + ENC_KEY hardening | 1h | ⏳ TODO |
| P0-5 | Rate Limiting token bucket | 1-2d | ⏳ TODO |

### 🟠 P1 — Code Debt

| ID | File:Line | Function | Task | Effort | Status |
|----|-----------|----------|------|--------|--------|
| P1-1 | `handlers/quiz.py` | code review | Interactive input / file read + LLM analysis | 2-3d | ⏳ TODO |
| P1-2 | `handlers/hints.py` | mission hint | Hint for current uncompleted mission step | 1-2d | ⏳ TODO |
| P1-3 | `news_fetcher.py` | XMLParsedAsHTMLWarning | Add `features="xml"` to BeautifulSoup + handle lxml | 1h | ⏳ TODO |
| P1-4 | **NVD CVE API integration** | `news_fetcher.py`/`handlers/cve.py` | Fix 404/403 — use API key or alternative source | 2-3h | ⏳ TODO |
| P1-5 | **LLM auth/log noise** | `config.py`/`resilient_llm.py` | Reduce noisy warnings on provider switch | 1h | ⏳ TODO |

### 🟡 P2 — Infrastructure

| ID | Feature | Effort | Dependencies | Status |
|----|---------|--------|--------------|--------|
| P2-1 | DB Indexes + Connection Pooling | 1-2d | SQLAlchemy | ⏳ TODO |
| P2-2 | WebSocket Pooling + Auto-reconnect | 2-3d | `api_server.py` | ⏳ TODO |
| P2-3 | LLM Response Caching (SQLite TTL + LRU) | 2-3d | `config.py` | ⏳ TODO |
| P2-4 | PWA SW stale-while-revalidate | 2-3d | `static/sw.js` | ⏳ TODO |
| P2-5 | Portable .exe build (PyInstaller) | 1-2d | PyInstaller | ⏳ TODO |

### 🟢 P3 — Long-term / Platform

| ID | Feature | Effort | Dependencies | Status |
|----|---------|--------|--------------|--------|
| P3-1 | Mobile App (React Native / TWA) | 2-4 weeks | PWA ready | ⏳ TODO |
| P3-2 | OAuth2 (Google, GitHub) | 1-2 weeks | auth.py, JWT | ⏳ TODO |
| P3-3 | 2FA (TOTP) | 1 week | auth.py, pyotp | ⏳ TODO |
| P3-4 | Multi-user Auth (Roles) | 1 week | auth.py, JWT | ⏳ TODO |
| P3-5 | Admin Panel | 1 week | JWT, roles | ⏳ TODO |
| P3-6 | GDPR Export/Import | 3 days | | ⏳ TODO |
| P3-7 | SCORM Export | 2 days | `course_manager.py` | ⏳ TODO |

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
