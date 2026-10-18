# CyberTeacher — Planned Features (v6.1+)

*Last updated: 2026-09-18*

---

## 📋 Overview

All features from **STORY_IMPLEMENTATION_PLAN.md** are complete (15/15). This document tracks truly pending ideas from vision docs that are **not yet implemented**.

---

## 🟡 P3 — Long-term / Platform

| ID | Feature | Description | Effort | Dependencies |
|------|---------|-------------|--------|--------------|
| ECO-01 | **Mobile App (TWA)** | ✅ Done — TWA wrapper над PWA. Keystore + fingerprint + assetlinks.json готовы. GitHub Actions workflow для автосборки APK. Осталось: 4 секрета в GitHub Settings + тег v1.0.0. | `twa/`, `app/src/main/`, `.github/workflows/build-twa-apk.yml`, `static/manifest.json` |
| ECO-02 | **OAuth2 (Google, GitHub)** | 🔄 In Progress — `auth.py` + `api_server.py` implemented: provider configs, authorize URL, code exchange, userinfo, account linking, JWT issuance. Endpoints: `/api/auth/oauth/{provider}`, `/api/auth/oauth/{provider}/callback`, `/api/auth/oauth/providers`, `/api/auth/oauth/links`, `/api/auth/oauth/unlink`. Needs GOOGLE_OAUTH_CLIENT_ID/SECRET and GITHUB_OAUTH_CLIENT_ID/SECRET env vars. | 1-2 weeks | auth.py, python-jose, oauthlib, requests-oauthlib |
| ECO-03 | **2FA (TOTP)** | 🔄 In Progress — `auth.py` extended with TOTP secret/backup codes, `api_server.py` endpoints: `/api/2fa/enable`, `/api/2fa/verify`, `/api/2fa/disable`, `/api/2fa/status`, `/api/2fa/backup-codes`. Login flow supports `totp_code` and returns `2fa_required`. | 1 week | auth.py, pyotp, qrcode |
| ECO-08 | **Mobile App (React Native)** | ❌ Отменено в пользу TWA (ECO-01). RN требует переписывания всех 58+ вкладок, дублирует работу. | — | ECO-01 |

---

## 📦 Netbuk Lab Plans

| ID | Feature | Description | Effort | Priority |
|----|---------|-------------|--------|----------|
| MF-08 | **Netbuk Plan 1 (Docker Labs)** | Docker host on netbuk, SSH management, docker-compose templates | 1-2 weeks | Medium |
| MF-09 | **Netbuk Plan 6 (CTFd)** | CTFd on netbuk, API integration | 1-2 weeks | Medium |
| MF-10 | **Netbuk Plan 8 (Honeypot + Generator)** | Cowrie/Dionaea + traffic generator | 1-2 weeks | Low |

---

## 📊 RICE Prioritization

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| Mobile App (TWA) | 500 | 3 | 0.5 | 20 | 37 | P3 |
| OAuth2 | 300 | 3 | 0.7 | 10 | 63 | P3 |
| 2FA (TOTP) | 200 | 3 | 0.8 | 5 | 48 | P3 |
| Netbuk Plan 1 (Docker Labs) | 200 | 4 | 0.6 | 10 | 48 | P2 |
| Netbuk Plan 6 (CTFd) | 300 | 4 | 0.7 | 14 | 60 | P2 |
| Netbuk Plan 8 (Honeypot) | 100 | 3 | 0.5 | 14 | 15 | P3 |

---

## 📅 Suggested 6-Week Sprint Plan

| Week | Focus | Deliverables |
|------|-------|--------------|
| **1** | **Learning Memory Polish** | CLI command `/reindex_knowledge`, category-aware retrieval UI |
| **2** | **PWA Risk Indicators** | noise bar, trace progress, debt counter |
| **3** | **Knowledge Base UX** | force reindex, category filters in chat |
| **4** | **Netbuk Lab Plan 1** | Docker Labs SSH management |
| **5** | **Platform Prep** | OAuth2 foundation, 2FA groundwork |
| **6** | **Polish + Release v6.2** | Bug fixes, docs, release tag |

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

*Last updated: 2026-06-10 | CyberTeacher v6.0*