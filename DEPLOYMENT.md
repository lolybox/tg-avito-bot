# Deployment Guide

## 📦 Free Hosting Options

### 1. **Render.com** (Рекомендуется ⭐)

Бесплатный хостинг с автоматическим деплоем из GitHub

```bash
# После создания бота на GitHub:
1. Зайдите на https://render.com
2. Sign in with GitHub
3. New → Web Service
4. Connect your repository: tg-avito-bot
5. Configuration:
   - Name: avito-bot
   - Environment: Python
   - Build Command: pip install -r requirements.txt
   - Run Command: python bots/main.py
6. Deploy!
```

**Преимущества:**
- ✅ Бесплатно forever
- ✅ Автодеплой при пуше в Git
- ✅ HTTPS включен
- ✅ Переменные окружения через UI

---

### 2. **Railway.app**

Альтернатива Render с похожим подходом

```bash
1. Регистрация через GitHub
2. New Project → Deploy from GitHub
3. Выберите ваш репозиторий
4. Добавить переменные окружения:
   - TELEGRAM_BOT_TOKEN = ваш_токен
5. Deploy!
```

---

### 3. **Fly.io**

Для более продвинутых пользователей

```bash
# Установка CLI
curl -L https://fly.io/install.sh | sh
fly auth login

# Деплой
fly launch --name avito-bot --org personal
fly deploy
```

---

### 4. **HuggingFace Spaces**

Подходит для ML/ботов проектов

```bash
# Создание репозитория на HuggingFace
# Добавление Dockerfile и .flow文件
# Push в репо и автохостинг
```

---

### 5. **Oracle Cloud Free Tier**

Полноценный VPS бесплатно (требуется карта)

```bash
1. Регистрация Oracle Cloud Free Tier
2. Создать Free VM (ARM или AMD)
3. Установить Docker + Docker Compose
4. Запустить бота:
docker-compose up -d
```

---

## 🔧 Подготовка к деплою

### 1. Настройка переменных окружения

Создайте `.env` на сервере:
```bash
TELEGRAM_BOT_TOKEN=your_token_here
CHECK_INTERVAL=300
RESULTS_LIMIT=10
```

### 2. Минимизация зависимостей

Удалите ненужные зависимости из `requirements.txt`:
```txt
aiogram==3.3.0
aiohttp==3.9.1
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

### 3. Добавление health check

В `bots/main.py`:
```python
from aiohttp import web

async def health_check(request):
    return web.json_response({"status": "ok"})

app = web.Application()
app.router.add_get('/health', health_check)

# В main():
web.run_app(app, host='0.0.0.0', port=8000)
```

---

## 📝 CI/CD Pipeline

GitHub Actions для автоматических тестов добавлен в `.github/workflows/python-test.yml`

### Auto-deploy с использованием GitHub Actions

Создайте workflow `.github/workflows/deploy.yml`:

```yaml
name: Deploy Bot

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{"serviceId": "your-service-id"}' \
            https://api.render.com/v1/build
```

---

## 🚀 Быстрый старт с Render

```bash
# 1. Создайте репозиторий на GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/tg-avito-bot.git
git push -u origin main

# 2. Деплой через Render
# - Зайдите на render.com
# - New → Web Service
# - Connect GitHub repo
# - Configure:
#   - Name: avito-telegram-bot
#   - Environment: Python
#   - Build Command: pip install -r requirements.txt
#   - Run Command: python bots/main.py
#   - Add environment variable: TELEGRAM_BOT_TOKEN

# 3. Получите URL: https://avito-telegram-bot.onrender.com
```

---

## 💡 Советы

### Мониторинг uptime

Используйте бесплатные сервисы:
- **UptimeRobot** - проверка каждые 5 минут
- **Pingdom** - мониторинг доступности

### Логи на сервере

```bash
# Просмотр логов (если используете systemd)
sudo journalctl -u avito-bot -f

# Логи через docker
docker-compose logs -f
```

### Резервное копирование

Настройте автоматические бэкапы данных:
```bash
# /etc/cron.d/backup
0 3 * * * root cd /path/to/bot && tar -czf /backups/data-$(date +\%Y\%m\%d).tar.gz data/
```

---

## ❓ Troubleshooting

### Бот не запускается на хостинге

Проверьте:
1. ✅ Версию Python (должна быть ≥ 3.10)
2. ✅ Переменные окружения настроены правильно
3. ✅ Логирование ошибок (`logs/app.log`)
4. ✅ Доступ к интернету из сервера

### Бот работает, но медленный

Решение:
- Используйте Redis для кэширования
- Оптимизируйте запросы к Avito
- Увеличьте интервал между проверками

### Бот падает под нагрузкой

Добавьте:
- Контейнеризацию (Docker)
- Автоскейлинг
- Load balancing

---

🎉 Ваш Telegram Avito Bot готов к работе! Если у вас есть вопросы - создавайте issue в репозитории.
