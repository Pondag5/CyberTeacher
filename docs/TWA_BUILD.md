# CyberTeacher Mobile — TWA (Trusted Web Activity)

## Architektur

Mobile-версия — это **TWA-обёртка над существующей PWA**, а не отдельное React Native приложение.
PWA (`static/manifest.json`, `static/sw.js`, иконки 192/512) уже полностью готова, поэтому
мобильное приложение — это Android-контейнер, который открывает PWA в полноэкранном режиме.

## Структура

```
twa/
  twa_manifest.json          # Манифест TWA (пакет, хост, иконы, ярлыки)
  settings.gradle
  build.gradle
  gradle/wrapper/            # Gradle wrapper конфиг
  app/
    build.gradle             # Модуль приложения (minSdk 23, targetSdk 34)
    src/main/
      AndroidManifest.xml    # LauncherActivity (TWA), intent-фильтры для домена
      java/cyberteacher/launcher/MainActivity.java
      res/values/            # strings, colors, themes
      res/mipmap-*/          # Заглушки иконок (замените на реальные)
static/.well-known/
  assetlinks.json            # Digital Asset Links (нужен SHA-256 отпечаток сертификата)
```

## Сборка

```bash
cd twa
# Сгенерировать wrapper-скрипты (требуется установленный Gradle):
gradle wrapper

# Собрать debug APK:
./gradlew assembleDebug

# Собрать release APK (требуется подписный keystore):
./gradlew assembleRelease
```

## Подготовка к публикации

1. **Создайте keystore** для подписи приложения:
   ```bash
   keytool -genkeypair -v -keystore cyberteacher-upload-keystore.jks \
     -keyalg RSA -keysize 2048 -validity 10000 -alias upload
   ```

2. **Получите SHA-256 отпечаток сертификата** и подставьте в `static/.well-known/assetlinks.json`:
   ```bash
   keytool -list -v -keystore cyberteacher-upload-keystore.jks -alias upload
   ```

3. **Разместите `assetlinks.json`** на домене под `https://cyberteacher.local/.well-known/assetlinks.json`
   (или ваш реальный домен). Это подтверждает, что сайт разрешает приложению обрабатывать его URL.

4. **Замените `cyberteacher.local`** на ваш реальный домен в:
   - `twa/twa_manifest.json` (поле `host`)
   - `twa/app/src/main/AndroidManifest.xml` (`supported_host`, `data android:host`)

5. **Замените заглушки иконок** в `twa/app/src/main/res/mipmap-*` на реальные PNG (48×48 … 192×192).

## Зависимости

- `com.google.androidbrowserhelper:androidbrowserhelper:3.0.0` — TWA LauncherActivity
- `androidx.appcompat:appcompat:1.6.1`
- compileSdk 34, minSdk 23, targetSdk 34

## Примечания

- PWA должна быть доступна по HTTPS (требование TWA/Chrome).
- Service Worker (`static/sw.js`) работает внутри TWA — офлайн-режим и кэширование сохраняются.
- Push-уведомления через FCM можно добавить позже как отдельную задачу.
