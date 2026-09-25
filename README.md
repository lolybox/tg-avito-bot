# 🤖 Telegram Avito Bot

Telegram бот для мониторинга свежих объявлений на Avito.ru

## ✨ Особенности

- 🔍 **Поиск по ключевым словам** - находите товары по названию
- 🏙️ **Выбор города** - ищите в нужном регионе
- 💰 **Фильтр по цене** - настройте максимальную стоимость
- ⚡ **Мониторинг свежих** - уведомления о объявлениях до 2 часов назад
- 📊 **История поисков** - сохраняйте последние запросы
- 🔔 **Уведомления** - мгновенные оповещения в Telegram

## 🛠 Установка

### Требования

- Python 3.10+
- Token от @BotFather в Telegram

### Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/tg-avito-bot.git
cd tg-avito-bot

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate
# Или (Linux/Mac)
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание конфигурации
cp config/config.json.example config/config.json
```

### Настройка бота

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен
3. Отредактируйте `config/config.json`:

```json
{
    "bot": {
        "token": "ВАШ_ТОКЕН_ОТ_BOTFATHER"
    },
    "monitoring": {
        "check_interval_seconds": 300,
        "results_limit": 10
    }
}
```

## 🚀 Запуск

```bash
python bots/main.py
```

## 💬 Команды

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и инструкция |
| `/search` | Начать поиск товара |
| `/stop` | Остановить текущий поиск |
| `/help` | Показать справку |
| `/history` | История последних поисков |
| `/settings` | Настроить параметры поиска |

## 📁 Структура проекта

```
tg-avito-bot/
├── bots/                 # Основной код бота
│   ├── main.py          # Точка входа
│   └── __init__.py
├── config/              # Конфигурация
│   ├── settings.py      # Настройки приложения
│   └── config.json      # Основные настройки
├── handlers/            # Обработчики сообщений
│   ├── start.py         # Команда /start
│   └── search.py        # Логика поиска
├── keyboards/           # Клавиатуры бота
│   └── inline.py        # Inline-кнопки
├── services/            # Сервисы
│   └── avito_monitor.py # Мониторинг Avito
├── data/                # Данные (история)
├── logs/                # Логи работы
├── requirements.txt     # Зависимости
└── README.md            # Документация
```

## 🔧 Дополнительные возможности

### Docker

```bash
# Сборка образа
docker build -t avito-bot .

# Запуск контейнера
docker run -it --env-file .env avito-bot
```

### Деплой на сервер

```bash
# Использование systemd
sudo nano /etc/systemd/system/avito-bot.service

# Файл сервиса:
# [Unit]
# Description=Avito Monitor Bot
# After=network.target

# [Service]
# User=www-data
# WorkingDirectory=/path/to/bot
# ExecStart=/path/to/venv/bin/python bots/main.py
# Restart=always

# [Install]
# WantedBy=multi-user.target

# Запуск
sudo systemctl enable avito-bot
sudo systemctl start avito-bot
```

## ⚠️ Важные примечания

- Бот использует публичный API Avito, возможны изменения в структуре
- Частые запросы могут привести к временной блокировке IP
- Рекомендуется использовать прокси при частом мониторинге

## 📝 Лицензия

MIT License

## 🤝 Contributing

Pull requests welcome!

## 📞 Поддержка

При возникновении вопросов обращайтесь или создавайте issue.
