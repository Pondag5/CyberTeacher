#!/bin/bash
# CyberTeacher - Установка Ollama (Linux/Mac)
set -e

echo "============================================"
echo "  CyberTeacher - Установка Ollama"
echo "============================================"
echo

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "[OK] Ollama уже установлен."
    ollama --version
    echo
else
    echo "[1/3] Установка Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    if [ $? -ne 0 ]; then
        echo "[ERROR] Установка не удалась. Попробуйте вручную:"
        echo "  curl -fsSL https://ollama.com/install.sh | sh"
        exit 1
    fi
fi

echo
echo "[2/3] Загрузка модели qwen2.5:7b (~4.7 GB)..."
echo "Это может занять несколько минут."
ollama pull qwen2.5:7b

echo
echo "[3/3] Проверка..."
ollama list

echo
echo "============================================"
echo "  Установка завершена!"
echo "============================================"
echo
echo "Теперь в CyberTeacher выполните:"
echo "  /provider ollama"
echo "  /doctor"
