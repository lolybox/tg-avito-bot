# 🚀 Деплой Telegram Avito Bot на Render.com (БЕСПЛАТНО!)

Render.com предоставляет **бесплатный хостинг forever** — ваш бот будет работать 24/7 без затрат!

---

## 📋 Что потребуется

1. Готовый код проекта `tg-avito-bot` ✅
2. Токен бота из @BotFather ✅ (`TELEGRAM_BOT_TOKEN`)
3. Аккаунт GitHub (для репозитория)
4. Аккаунт на [render.com](https://render.com)

---

## 🔧 Этапы деплоя

### Шаг 1: Подготовка репозитория на GitHub

```bash
# Переход в директорию проекта
cd C:/Users/Egorka/Documents/Qoder/2026-09-24/c4b46c5a/tg-avito-bot

# Инициализация git (если еще нет)
git init

# Добавление всех файлов
git add .

# Создание коммита
git commit -m "feat: initial commit of telegram avito bot"

# Настройка ветки main
git branch -M main

# Создание репозитория на GitHub
# Зайдите на https://github.com/new и создайте новый репозиторий
# Или через CLI:
gh repo create tg-avito-bot --public --source=. --remote=origin

# Пуш в репозиторий
git remote add origin https://github.com/YOUR_USERNAME/tg-avito-bot.git
git push -u origin main
```

**Замените:**
- `YOUR_USERNAME` — ваше имя пользователя на GitHub
- `tg-avito-bot` — название репозитория

---

### Шаг 2: Деплой на Render.com

#### 2.1 Регистрация на Render

1. Откройте https://render.com
2. Нажмите **"Sign up"**
3. Выберите **"Continue with GitHub"** (рекомендуется)

#### 2.2 Создание сервиса

1. Нажмите **"New +" → "Web Service"**
2. Подключите ваш GitHub репозиторий `tg-avito-bot`
3. Заполните параметры:

```
┌──────────────────────────────────────────┐
│ Name: avito-telegram-bot                 │
│ Region: Frankfurt (Germany)              │
│ Branch: main                             │
│ Root Directory: [empty]                  │
│ Environment: Python                      │
│ Build Command: pip install -r requirements.txt  
│ Start Command: python bots/main.py       │
└──────────────────────────────────────────┘
```

#### 2.3 Переменные окружения

На вкладке **"Environment"** добавьте переменные:

```
Key                      Value
───────────────────────────────────────
TELEGRAM_BOT_TOKEN       6160274017:AAFHudmtwKA-xRCBi89XcCukB_cTz4zqJV0
CHECK_INTERVAL           300
RESULTS_LIMIT            10
```

⚠️ **ВАЖНО:** Не забудьте сохранить токен вашего бота!

#### 2.4 Бесплатный план

Выберите тариф **"Free"** (бесплатно):
- ✅ 750 часов/month (хватает на 1 сервис)
- ✅ Автодеплой из GitHub
- ✅ HTTPS включен
- ❌ Спящий режим после 15 мин неактивности

#### 2.5 Деплой!

Нажмите **"Create Web Service"** и ждите ~2-3 минуты.

Render автоматически:
1. Клонирует репозиторий
2. Устанавливает зависимости
3. Запускает бота
4. Предоставляет публичный URL

---

### Шаг 3: Проверка работы

#### 3.1 Просмотр логов

В интерфейсе Render перейдите на вкладку **"Logs"**

**Успешный запуск:**
```
INFO - Beginning work...
INFO - Health check server running on port 8080
INFO - Starting polling...
```

**Если ошибка сети:**
```
ClientConnectorError: Cannot connect to host api.telegram.org
```

Это должно исправиться на сервере Render (там нет блокировок как у локально).

#### 3.2 Тестирование бота

1. Откройте Telegram
2. Найдите своего бота по username (@BotFather → /mybots)
3. Напишите `/start`
4. Должно прийти приветствие

---

## 🔍 Диагностика проблем

### Проблема 1: Бот не запускается

**Решение:**
- Проверьте логи в Render Dashboard
- Убедитесь, что `TELEGRAM_BOT_TOKEN` добавлен правильно
- Проверьте синтаксис кода (команда `python bots/main.py` локально)

### Проблема 2: Ошибка подключения к Telegram API

**Причина:** Нет интернета или блокировка
**Решение:** Render имеет стабильный интернет, это проблема должна исчезнуть

### Проблема 3: Бот останавливается через 15 минут

**Это ожидаемо!** Бесплатный план переводит сервис в sleep mode.
Первое сообщение от бота "разбудит" его (~1 минуту).

---

## 💡 Оптимизации для Render

### Увеличение памяти (опционально)

```yaml
# В render.yaml
services:
  - type: web
    name: avito-telegram-bot
    env: python
    plan: starter  # $7/месяц, больше ресурсов
    # ...
```

### Автоматические бэкапы данных

Данные сохраняются в Docker volumes. Добавьте:

```yaml
volumes:
  - name: avito-data
    path: /app/data
```

---

## 📝 Файлы конфигурации для Render

Файл `render.yaml` уже создан и содержит:
```yaml
services:
  - type: web
    name: avito-telegram-bot
    env: python
    region: Frankfurt
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python bots/main.py
    healthCheckPath: /health
```

Этого достаточно для автодеплоя!

---

## 🎯 Итоговая проверка

После деплоя убедитесь:
1. ✅ Сервис статус "Live" (зеленый)
2. ✅ Логи показывают успешный старт
3. ✅ Бот отвечает в Telegram
4. ✅ Поиск работает (/search iPhone 13)

---

## 🔄 Обновление кода

Просто пушите изменения в GitHub:

```bash
# Изменили код?
git add .
git commit -m "fix: improved search functionality"
git push origin main
```

Render автоматически перезапустит бота!

---

## 📞 Поддержка Render

- Документация: https://render.com/docs
- Статус сервиса: https://status.render.com
- Чат поддержки: через dashboard

---

**Готово! Ваш Telegram Avito Bot работает 24/7 бесплатно!** 🎉🚀

Для помощи: проверьте файл `README.md` в проекте.
