# CyberTeacher — TWA (Trusted Web Activity) Setup

Полная инструкция по сборке Android-приложения через Trusted Web Activity.

## Что нужно для TWA

1. **PWA** — уже готово (manifest.json, sw.js, icons)
2. **assetlinks.json** — создан в `static/.well-known/assetlinks.json`
3. **SHA256 fingerprint** — от keystore для подписи приложения
4. **Bubblewrap** — утилита Google для сборки TWA

---

## Быстрый старт (Development)

### 1. Генерация debug keystore (если нет)
```bash
keytool -genkey -v \
  -keystore debug.keystore \
  -alias androiddebugkey \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass android -keypass android \
  -dname "CN=Android Debug,O=Android,C=US"
```

### 2. Получить SHA256 fingerprint
```bash
# Из keystore
python scripts/generate_assetlinks.py --keystore debug.keystore --alias androiddebugkey

# Или из уже собранного APK
python scripts/generate_assetlinks.py --apk app-release.apk
```

### 3. Обновить assetlinks.json
Заменить `PLACEHOLDER:REPLACE_WITH_YOUR_SHA256_FINGERPRINT` в `static/.well-known/assetlinks.json` на реальный fingerprint.

### 4. Запустить локально (HTTPS обязательно для TWA)
```bash
# Вариант 1: mkcert для локального HTTPS
mkcert -install
mkcert localhost 127.0.0.1 ::1

# Запуск с сертификатами
uvicorn api_server:app --host 0.0.0.0 --port 8000 --ssl-keyfile localhost+2-key.pem --ssl-certfile localhost+2.pem
```

### 5. Собрать TWA через Bubblewrap
```bash
# Установка
npm install -g @bubblewrap/cli

# Инициализация (создаст twa.json если нет)
bubblewrap init --manifest=https://localhost:8000/manifest.json

# Сборка
bubblewrap build

# Результат: app-release-signed.apk / app-release.aab
```

---

## Production Checklist

- [ ] Реальный домен с HTTPS (Let's Encrypt или другой CA)
- [ ] assetlinks.json раздается с `https://your-domain/.well-known/assetlinks.json`
- [ ] Production keystore (не debug!)
- [ ] SHA256 fingerprint от production keystore в assetlinks.json
- [ ] Подписанный AAB для Google Play Console
- [ ] Проверка в Chrome: `chrome://flags/#enable-trusted-web-activity`

---

## Структура файлов

```
static/
├── manifest.json              # PWA manifest + TWA related_application
├── sw.js                      # Service Worker
├── icon-192.png               # Иконка 192x192
├── icon-512.png               # Иконка 512x512 (maskable)
├── .well-known/
│   └── assetlinks.json        # Верификация домена для TWA
├── scripts/
│   └── generate_assetlinks.py # Генерация fingerprint
└── twa.json                   # Bubblewrap конфигурация
```

---

## Полезные команды

```bash
# Проверить assetlinks.json доступен
curl https://your-domain/.well-known/assetlinks.json

# Проверить manifest
curl https://your-domain/manifest.json

# Подписать APK вручную (если нужно)
apksigner sign --ks android.keystore --out app-signed.apk app-unsigned.apk

# Проверить подпись APK
apksigner verify --print-certs app-signed.apk
```

---

## Troubleshooting

| Проблема | Решение |
|----------|---------|
| "Digital Asset Links verification failed" | Проверьте assetlinks.json доступен по HTTPS, fingerprint верный |
| "ERR_CERT_AUTHORITY_INVALID" | Используйте валидный SSL сертификат (не самоподписанный для продакшна) |
| Приложение не открывает PWA | Проверьте scope в manifest.json, start_url должен быть в scope |
| Bubblewrap ошибки | Обновите Node.js, npm, @bubblewrap/cli |

---

## Ссылки

- [Trusted Web Activity Guide](https://developer.chrome.com/docs/android/trusted-web-activity/)
- [Bubblewrap Documentation](https://github.com/GoogleChromeLabs/bubblewrap)
- [Digital Asset Links](https://developers.google.com/digital-asset-links)
- [PWA Criteria](https://web.dev/pwa-checklist/)