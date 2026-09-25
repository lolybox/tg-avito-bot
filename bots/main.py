#!/usr/bin/env python3
"""Telegram Avito Bot - основной файл запуска

⚠️ Важно для пользователей Windows:
Если вы видите ошибку "WinError 121" при запуске, это связано с антивирусом.

Срочные решения:
1. Откройте QUICK_FIX_WINDOWS.md в корне проекта
2. Отключите SSL-сканирование в вашем антивирусе
3. Или используйте Docker: docker-compose up

Подробнее в TROUBLESHOOTING.md
"""
import asyncio
import logging
import ssl
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from datetime import datetime
import os
from aiohttp import web, TCPConnector, ClientTimeout, ClientSession
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

# Добавим путь к родительским модулям для импорта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in __import__('sys').path:
    __import__('sys').path.insert(0, project_root)

from config.settings import Settings
from services.avito_monitor import AvitoMonitor
from keyboards.inline import create_search_keyboard
from handlers.search import router as search_router
from handlers.start import router as start_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def health_check(request):
    """Health check endpoint для Render"""
    return web.json_response({"status": "ok", "service": "avito-telegram-bot"})


async def run_health_server(port: int = 8080):
    """Запуск HTTP сервера для health check
        
        Args:
            port: Порт для health check (по умолчанию 8080 для Render)
    """
    try:
        app = web.Application()
        app.router.add_get('/health', health_check)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        logger.info(f"Health check server running on port {port}")
        return runner
    except Exception as e:
        logger.warning(f"Could not start health check server on port {port}: {e}")
        return None


async def create_bot_session(bot: Bot):
    """Создание асинхронного сессии для бота с улучшенной обработкой SSL"""
    
    # Создаем надежный SSL контекст
    ssl_context = ssl.create_default_context()
    
    # Улучшаем работу с соединениями (актуально для Windows)
    connector = TCPConnector(
        limit=0,  # Без ограничений на количество соединений
        ttl_dns_cache=300,  # Кэширование DNS
        use_dns_cache=True,
        ssl=ssl_context,
        enable_cleanup_closed=True,
    )
    
    timeout = ClientTimeout(
        total=30,  # Общий таймаут запроса
        connect=10,  # Таймаут соединения
        sock_read=30,  # Таймаут чтения
        sock_connect=10,  # Таймаут подключения
    )
    
    # Настраиваем сессию с лучшими настройками для Windows
    session = aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={
            'User-Agent': 'AvitoMonitorBot/1.0',
        }
    )
    
    # Передаем сессию боту
    bot._session = session


async def send_avito_notification(bot: Bot, user_id: int, item_info: str):
    """Отправка уведомления о новом товаре в Telegram"""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=item_info,
            parse_mode="HTML"
        )
        logger.info(f"Notification sent to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send notification to {user_id}: {e}")


async def monitoring_loop(bot: Bot, settings: Settings):
    """Фоновый цикл мониторинга новых объявлений"""
    while True:
        try:
            await asyncio.sleep(settings.CHECK_INTERVAL)
            
            # Здесь будет логика проверки активных поисков
            # Пока заглушка - можно добавить уведомления
            
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")


async def main():
    """Основная функция запуска бота"""
    
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        logger.info("Начало работы Telegram Avito Bot...")
        
        # Инициализация настроек
        settings = Settings()
        
        # Инициализация бота
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()
        
        # Регистрация роутеров
        dp.include_router(start_router)
        dp.include_router(search_router)
        
        # Создание монитора
        monitor = AvitoMonitor(settings)
        
        # Запуск health check сервера параллельно с polling (испытываем несколько портов)
        health_runner = None
        for port in [8080, 8081, 8082]:
            try:
                health_runner = await run_health_server(port)
                if health_runner:
                    break
            except Exception as e:
                logger.warning(f"Could not start on port {port}: {e}")
                continue
        
        # Запуск фонового мониторинга
        asyncio.create_task(monitoring_loop(bot, settings))
        
        # Запуск polling (блокирует до остановки)
        await dp.start_polling(bot)
        
    except ClientConnectorError as e:
        logger.error(f"Network connection error: {e}")
        logger.error("\nSSL/TLS connection failed!")
        logger.error("\nPossible causes:")
        logger.error("  • Antivirus/Firewall blocking HTTPS connections")
        logger.error("  • SSL certificate validation issues")
        logger.error("  • Network proxy configuration needed")
        logger.error("\nSolutions:")
        logger.error("  1. Check your antivirus settings (especially Kaspersky, ESET, Dr.Web)")
        logger.error("  2. Try disabling SSL inspection in your antivirus")
        logger.error("  3. Add exception for api.telegram.org in firewall")
        logger.error("  4. Run from command line with: python -u bots/main.py")
        raise
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
    finally:
        await bot.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
