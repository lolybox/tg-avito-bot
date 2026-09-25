from aiogram import Router, types
from aiogram.types import Message


router = Router()


@router.message(types.Command("start"))
async def process_start(message: Message):
    """Обработка команды /start"""
    
    welcome_text = (
        "👋 Привет!\n\n"
        "Я бот для поиска свежих объявлений на Avito.\n\n"
        "<b>Как использовать:</b>\n\n"
        "1️⃣ Просто напишите название товара\n"
        "2️⃣ Укажите город\n"
        "3️⃣ Укажите максимальную цену (или 'нет' для всех цен)\n\n"
        "Бот будет искать новые объявления каждые 5 минут!"
    )
    
    try:
        await message.answer(
            welcome_text,
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.message(types.Command("help"))
async def process_help(message: Message):
    """Справка по использованию"""
    
    help_text = (
        "<b>⚙️ Настройки бота:</b>\n\n"
        "/start — Запустить бота\n"
        "/help — Показать эту справку\n\n"
        "<b>📝 Как начать поиск:</b>\n\n"
        "Просто отправьте текст сообщения с названием товара,\n"
        "а затем следуйте инструкциям бота."
    )
    
    await message.answer(help_text, parse_mode="HTML")
