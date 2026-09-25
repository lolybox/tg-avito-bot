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
import os
import sys

from aiogram import Bot, Dispatcher
from aiohttp import web
from aiohttp.client_exceptions import ClientConnectorError

# Добавим путь к родительским модулям для импорта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.settings import Settings
from handlers.search import router as search_router
from handlers.start import router as start_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def health_check(request):
    """Health check endpoint для Render"""
    return web.json_response({"status": "ok", "service": "avito-telegram-bot"})


async def run_health_server():
    """HTTP-сервер health check. Render выдаёт порт в переменной окружения PORT."""
    port = int(os.getenv("PORT", "8080"))

    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Health check server running on port {port}")
    return runner


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

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    bot = None
    health_runner = None
    try:
        logger.info("Начало работы Telegram Avito Bot...")

        settings = Settings()

        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()

        dp.include_router(start_router)
        dp.include_router(search_router)

        health_runner = await run_health_server()

        asyncio.create_task(monitoring_loop(bot, settings))

        await dp.start_polling(bot)

    except ClientConnectorError as e:
        logger.error(f"Network connection error: {e}")
        logger.error("Не удалось подключиться к api.telegram.org (см. QUICK_FIX_WINDOWS.md)")
        raise
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
    finally:
        if health_runner:
            await health_runner.cleanup()
        if bot:
            await bot.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
