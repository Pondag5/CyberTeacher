# PWA Tab Index — static/js/tabs/
# Source: /workspace/app/static/js/tabs/ + static/js/app.js TAB_SOURCES

## All tabs (app.js TAB_SOURCES, lines 6-48)
modes, chat, progress, quiz, daily, profile, courses, story, tracks, ctf, labs, osint,
scanner, shop, malware, achievements, versus, world, stats, admin, export, leaderboard,
missions, writeups, recon, labs_external, social, phishing, sandbox, network,
mood, summary, dockergen, news, history, threats, offline, skills, equipment, timeloop,
sync, exploit, dashboard, analytics, code_review, walkthroughs, ctf_flags, mermaid,
bug_bounty, media, context, doctor, mistakes, feedback, settings

## Navigation visibility (app.js:123-128)
hiddenTabs = {
  beginner: ['ctf', 'osint', 'scanner', 'malware', 'versus', 'admin', 'leaderboard', 'export'],
  intermediate: ['admin'],
  advanced: [],
  hardcore: [],
}

## Dashboard risk indicators (dashboard.js:43-83)
- Calls /api/noise, /api/trace, /api/debts, /api/history
- Renders inline noise bar, trace bar, debt counter, stealth toggle button
- NOW USES shared component renderRiskIndicators() + updateRiskIndicators() (alpha readiness)

## Shared component (static/js/components/risk_indicators.js)
- renderRiskIndicators(container) — renders noise/trace/debt cards + stealth toggle
- updateRiskIndicators() — polls /api/noise, /api/trace, /api/debts every 10s
- Auto-update: setInterval(updateRiskIndicators, 10000) (line 84)

## App bootstrap (static/js/app.js)
- loadInitialData() (line 214) — loads progress, modes, courses, labs, profile, daily,
  achievements, skills, shop, storyEpisodes, tracks, ctf status
- renderNav() (line 119) — builds sidebar nav from tabs array
- renderCurrentTab() (line 172) — lazy-loads tab script, calls Tab_<id>.render(innerDiv)
- API path mapping (static/js/utils.js API_PATH_MAP) — frontend shorthand -> /api/*

## Key PWA features
- Notifications WS (notifications_ws.js)
- OfflineDB (offline.js) — caching responses
- Themes (themes.js), sounds (sounds.js), glitch effects (glitch.js), particles
- Onboarding (onboarding.js), auto-save /api/save every 30s + beforeunload
