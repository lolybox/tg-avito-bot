import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from datetime import datetime
import os
from aiohttp import web

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


async def run_health_server():
    """Запуск HTTP сервера для health check на порту 8080 (требование Render)"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    
    # Render требует порт 8080
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("Health check server running on port 8080")


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
    
    # Запуск health check сервера параллельно с polling
    asyncio.create_task(run_health_server())
    
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
        
        # Запуск фонового мониторинга
        asyncio.create_task(monitoring_loop(bot, settings))
        
        # Запуск polling (блокирует до остановки)
        await dp.start_polling(bot)
        
    finally:
        await bot.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
