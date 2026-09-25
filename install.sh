#!/bin/bash

# Скрипт быстрой установки Telegram Avito Bot

set -e

echo "🚀 Установка Telegram Avito Bot..."

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.10+."
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация окружения
echo "⚙️ Активация окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание директорий
echo "📁 Создание папок данных..."
mkdir -p data logs

# Копирование примера env файла если его нет
if [ ! -f .env ]; then
    echo "🔧 Настройка переменных окружения..."
    cp .env.example .env
    echo "⚠️ Не забудьте настроить TELEGRAM_BOT_TOKEN в .env файле!"
fi

echo "✅ Установка завершена!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Отредактируйте .env файл и добавьте токен вашего бота"
echo "2. Запустите: python bots/main.py"
echo ""
