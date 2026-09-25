import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Telegram бот
    TELEGRAM_BOT_TOKEN: str
    
    # Настройки мониторинга
    CHECK_INTERVAL: int = 300  # Интервал проверки в секундах (5 минут)
    RESULTS_LIMIT: int = 10    # Максимум объявлений на запрос
    
    # Avito настройки
    AVITO_BASE_URL: str = "https://avito.ru"
    
    # Пути к файлам
    DATA_DIR: str = "data"
    LOGS_DIR: str = "logs"
    CONFIG_FILE: str = "config/config.json"
    
    def __init__(self):
        super().__init__()
        
        # Создание директорий если их нет
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.LOGS_DIR, exist_ok=True)
