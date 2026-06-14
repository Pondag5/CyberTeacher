static/
├── index.html              # SPA entry point (lazy-load tabs, inline critical CSS)
├── manifest.json           # PWA manifest (standalone, #00B4D8 theme)
├── sw.js                   # Service Worker v4 (cache-first + API LRU)
├── icon-192.png            # PWA icon
├── icon-512.png            # PWA icon (maskable)
├── imsmanifest.xml         # SCORM 1.2 manifest (legacy)
├── css/
│   └── style.css           # All styles (3 themes, responsive)
├── js/
│   ├── app.js              # State, routing, lazy tab loader
│   ├── utils.js            # apiCall, themes, renderUserInfo
│   ├── sounds.js           # Web Audio API effects
│   ├── heatmap.js          # SVG 28-day activity calendar
│   ├── charts.js           # SVG bar/line charts
│   ├── particles.js        # Canvas particle background
│   ├── effects.js          # Glitch text + border glow
│   ├── offline.js          # IndexedDB offline-first
│   ├── notifications.js    # Browser notifications
│   ├── notifications_ws.js # WebSocket real-time notifications
│   ├── onboarding.js       # First-time wizard
│   └── tabs/               # 22 tabs (loaded on demand)
│       ├── modes.js        # Режимы ИИ
│       ├── chat.js         # Чат с ИИ (WebSocket streaming)
│       ├── progress.js     # Прогресс
│       ├── quiz.js         # Квизы + мультиплеер
│       ├── daily.js        # Дейли челлендж
│       ├── profile.js      # Профиль + радар
│       ├── courses.js      # Курсы
│       ├── story.js        # История (эпизоды)
│       ├── tracks.js       # Треки обучения
│       ├── ctf.js          # CTF задания
│       ├── labs.js         # Docker лаборатории
│       ├── osint.js        # OSINT
│       ├── scanner.js      # Сканер кода
│       ├── shop.js         # Магазин
│       ├── malware.js      # Malware анализ
│       ├── achievements.js # Достижения
│       ├── versus.js       # Дуэль
│       ├── world.js        # Мир (инциденты, фракции)
│       ├── stats.js        # Статистика
│       ├── admin.js        # Админ-панель
│       ├── export.js       # Экспорт/импорт данных
│       └── leaderboard.js  # Рекорды
