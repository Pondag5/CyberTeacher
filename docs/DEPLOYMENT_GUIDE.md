# CyberTeacher — Руководство по развёртыванию (L-15)

Это руководство описывает развёртывание CyberTeacher для учебных классов и групп.

---

## 📋 Оглавление

1. [Требования](#требования)
2. [Быстрый старт (Docker Compose)](#быстрый-старт)
3. [Развёртывание для класса](#развёртывание-для-класса)
4. [Настройка сети](#настройка-сети)
5. [Бэкапы](#бэкапы)
6. [Мониторинг](#мониторинг)
7. [Устранение проблем](#устранение-проблем)

---

## Требования

### Минимальные
- **CPU:** 4 ядра
- **RAM:** 8 GB
- **SSD:** 50 GB
- **Docker:** 20.10+
- **Docker Compose:** 2.0+

### Рекомендуемые (с GPU для Ollama)
- **CPU:** 8 ядер
- **RAM:** 16 GB
- **SSD:** 100 GB
- **GPU:** NVIDIA с 8+ GB VRAM
- **NVIDIA Container Toolkit**

---

## Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/your-org/cyberteacher.git
cd cyberteacher
```

### 2. Настроить окружение
```bash
cp .env.example .env
# Отредактировать .env:
# LLM_PROVIDER=ollama
# OLLAMA_MODEL=qwen2.5:7b
# OPENROUTER_API_KEY=your_key
```

### 3. Запустить
```bash
# Полный стек (CyberTeacher + Ollama + лабы)
docker-compose up -d

# Только CyberTeacher + Ollama (без лаб)
docker-compose up -d cyberteacher ollama

# С аналитикой (PostgreSQL)
docker-compose --profile analytics up -d
```

### 4. Проверить
```bash
docker-compose ps
docker-compose logs -f cyberteacher
```

---

## Развёртывание для класса

### Вариант A: Один сервер, несколько студентов

```
┌─────────────────────────────────────┐
│           Сервер (192.168.1.100)     │
│                                     │
│  ┌─────────────┐  ┌──────────────┐  │
│  │ CyberTeacher│  │   Ollama     │  │
│  │   :8501     │  │   :11434     │  │
│  └─────────────┘  └──────────────┘  │
│                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐        │
│  │ DVWA │ │ Juice│ │ Meta │        │
│  │:8080 │ │:3000 │ │:8081 │        │
│  └──────┘ └──────┘ └──────┘        │
└─────────────────────────────────────┘
         ↑         ↑         ↑
    Студент 1  Студент 2  Студент 3
```

**docker-compose.class.yml:**
```yaml
version: "3.8"
services:
  cyberteacher:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./memory:/app/memory
      - ./knowledge_base:/app/knowledge_base
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  dvwa:
    image: vulnerables/web-dvwa
    ports:
      - "8080:80"

volumes:
  ollama_data:
```

### Вариант B: Каждый студент — отдельный контейнер

```bash
# Создать сеть
docker network create class-net

# Для каждого студента
for student in student1 student2 student3; do
  docker run -d \
    --name "ct_$student" \
    --network class-net \
    -v "./data/$student:/app/memory" \
    -p "850${student##*t}:8501" \
    cyberteacher:latest
done
```

---

## Настройка сети

### Изолированная сеть для лаб
```yaml
networks:
  class-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

  internet-isolated:
    driver: bridge
    internal: true  # Без доступа к интернету
```

### Файрвол правила
```bash
# Разрешить только нужные порты
ufw allow 8501/tcp   # Web UI
ufw allow 11434/tcp  # Ollama
ufw allow 22/tcp     # SSH
ufw enable
```

---

## Бэкапы

### Автоматический бэкап (cron)
```bash
# /etc/cron.d/cyberteacher-backup
0 2 * * * root /opt/cyberteacher/scripts/backup.sh
```

**scripts/backup.sh:**
```bash
#!/bin/bash
BACKUP_DIR="/backups/cyberteacher"
DATE=$(date +%Y-%m-%d_%H-%M)

mkdir -p "$BACKUP_DIR"

# Бэкап состояния
tar czf "$BACKUP_DIR/memory_$DATE.tar.gz" ./memory

# Бэкап базы знаний
tar czf "$BACKUP_DIR/knowledge_$DATE.tar.gz" ./knowledge_base

# Бэкап embeddings
tar czf "$BACKUP_DIR/embeddings_$DATE.tar.gz" ./embeddings

# Бэкап Docker volumes
docker run --rm -v ollama_data:/data -v "$BACKUP_DIR:/backup" \
  alpine tar czf "/backup/ollama_$DATE.tar.gz" -C /data .

# Удалить старые бэкапы (>30 дней)
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Восстановление
```bash
# Остановить сервисы
docker-compose down

# Восстановить данные
tar xzf /backups/cyberteacher/memory_2026-05-15.tar.gz -C ./
tar xzf /backups/cyberteacher/knowledge_2026-05-15.tar.gz -C ./

# Запустить
docker-compose up -d
```

---

## Мониторинг

### Health checks
```bash
# Проверить статус
curl http://localhost:8501/health

# Проверить Ollama
curl http://localhost:11434/api/tags

# Проверить лабы
curl -I http://localhost:8080  # DVWA
curl -I http://localhost:3000  # Juice Shop
```

### Логи
```bash
# Все логи
docker-compose logs -f

# Только CyberTeacher
docker-compose logs -f cyberteacher

# Последние 100 строк
docker-compose logs --tail=100 cyberteacher
```

### Ресурсы
```bash
# Использование CPU/RAM
docker stats

# Использование диска
docker system df
docker volume ls
```

---

## Устранение проблем

### Ollama не запускается
```bash
# Проверить GPU
nvidia-smi

# Без GPU (CPU mode)
docker-compose up -d cyberteacher ollama
# Модель будет работать медленнее
```

### Порт уже занят
```bash
# Найти процесс
lsof -i :8501

# Изменить порт в docker-compose.yml
ports:
  - "8502:8501"  # Вместо 8501
```

### Нехватка места
```bash
# Очистить неиспользуемые образы
docker system prune -a

# Уменьшить размер embeddings
rm -rf ./embeddings/*
python main.py  # Переиндексация
```

### Медленная LLM
```bash
# Переключиться на облачный провайдер
# В .env:
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=qwen/qwen-2.5-72b-instruct
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Приложение
COPY . .

# Создать директории
RUN mkdir -p memory knowledge_base embeddings backups

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD curl -f http://localhost:8501/health || exit 1

EXPOSE 8501

CMD ["python", "main.py"]
```

---

*Обновлено: 2026-05-15*
*Версия: CyberTeacher v3.2*
