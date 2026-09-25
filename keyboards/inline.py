from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_search_keyboard(query: str = "") -> InlineKeyboardMarkup:
    """Создает клавиатуру для поиска"""
    keyboard = [
        [
            InlineKeyboardButton(text="🔍 Найти товар", callback_data="search_start")
        ]
    ]
    
    if query:
        keyboard.append([
            InlineKeyboardButton(text="⏹ Остановить поиск", callback_data="stop_search")
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_city_selector(cities: list[str]) -> InlineKeyboardMarkup:
    """Селектор городов"""
    keyboard = []
    for city in cities[:8]:  # Ограничиваем количество кнопок
        keyboard.append([
            InlineKeyboardButton(text=city, callback_data=f"city_{city}")
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
