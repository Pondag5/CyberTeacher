@echo off
echo ============================================
echo   CyberTeacher - Установка Ollama
echo ============================================
echo.

REM Check if Ollama is already installed
where ollama >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] Ollama уже установлен.
    ollama --version
    echo.
    goto :pull_model
)

echo [1/3] Скачивание Ollama...
echo Используйте: https://ollama.com/download
echo Или выполните вручную:
echo   winget install Ollama.Ollama
echo.
echo После установки вернитесь к этому скрипту.
pause
goto :pull_model

:pull_model
echo.
echo [2/3] Загрузка модели qwen2.5:7b (~4.7 GB)...
echo Это может занять несколько минут.
echo.
ollama pull qwen2.5:7b
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Не удалось загрузить модель.
    echo Проверьте подключение к интернету и повторите: ollama pull qwen2.5:7b
    pause
    exit /b 1
)

echo.
echo [3/3] Проверка...
ollama list
echo.
echo ============================================
echo   Установка завершена!
echo ============================================
echo.
echo Теперь в CyberTeacher выполните:
echo   /provider ollama
echo   /doctor
echo.
pause
