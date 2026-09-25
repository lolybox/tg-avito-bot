from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime


router = Router()


class SearchState(StatesGroup):
    """Состояния для поиска"""
    waiting_for_query = State()
    waiting_for_city = State()
    waiting_for_price = State()


# Хранилище активных поисков {user_id: search_data}
active_searches = {}


@router.message(SearchState.waiting_for_query)
async def handle_query_text(message: Message, state: FSMContext):
    """Обработка текста как запроса на поиск"""
    
    query = message.text.strip()
    
    # Проверяем, что это не команда
    if query.startswith('/'):
        return
    
    await state.update_data(query=query)
    
    await message.answer(
        f"✅ Поиск добавлен: `{query}`\n\n"
        "Отправьте город (или напишите название города):",
        parse_mode="Markdown"
    )
    await state.set_state(SearchState.waiting_for_city)


@router.message(SearchState.waiting_for_city)
async def handle_city_text(message: Message, state: FSMContext):
    """Обработка названия города"""
    
    city = message.text.strip()
    
    await state.update_data(city=city)
    
    await message.answer(
        f"🏙️ Город выбран: `{city}`\n\n"
        "Теперь укажите максимальную цену в рублях (или 'нет' без лимита):",
        parse_mode="Markdown"
    )
    await state.set_state(SearchState.waiting_for_price)


@router.message(SearchState.waiting_for_price)
async def handle_price_text(message: Message, state: FSMContext):
    """Обработка максимальной цены"""
    
    price_text = message.text.strip().lower()
    
    # Если написано 'нет' или 'all' - лимит нет
    if price_text in ['нет', 'all', 'any', 'неограничен']:
        max_price = None
    else:
        try:
            max_price = int(price_text.replace(',', '').replace(' ', ''))
        except ValueError:
            await message.answer("⚠️ Не удалось распознать цену. Попробуйте снова:")
            return
    
    # Сохраняем активный поиск
    user_id = message.from_user.id
    active_searches[user_id] = {
        'query': await state.get_data() or {},
        'started_at': datetime.now()
    }
    
    await message.answer(
        f"🎉 Поиск успешно настроен!\n\n"
        f"📝 Товар: {await state.get_data()['query']}\n"
        f"🏙️ Город: {await state.get_data()['city']}\n"
        f"💰 Цена до: {'Любая' if not max_price else max_price} ₽\n\n"
        "Бот будет искать новые объявления каждые 5 минут!",
        parse_mode="Markdown"
    )
    
    await state.clear()
