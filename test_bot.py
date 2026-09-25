"""Тестовый файл для проверки токена и настройки"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Проверка токена
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    print("Ошибка: TELEGRAM_BOT_TOKEN не найден в .env файле!")
    exit(1)

print("OK Токен найден:", token[:15], "...")
print("OK Длина токена:", len(token), "символов")
print("\nНастраиваем бот готов к запуску!")
print("\nДля запуска выполните:")
print("   python bots/main.py")
print("\nИли для теста напишите /start в Telegram вашему боту!")
