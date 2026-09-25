import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import logging
from config.settings import Settings


logger = logging.getLogger(__name__)


class AvitoItem:
    """Класс представления товара с Avito"""
    
    def __init__(self, title: str, price: int, url: str, city: str,
                 posted_at: datetime, description: str = ""):
        self.title = title
        self.price = price
        self.url = url
        self.city = city
        self.posted_at = posted_at
        self.description = description
    
    def to_message(self) -> str:
        """Форматирует сообщение для Telegram"""
        message = (f"🛒 <b>{self.title}</b>\n"
                  f"💰 Цена: {self.price:,} ₽\n"
                  f"📍 Город: {self.city}\n"
                  f"⏰ Добавлено: {self.posted_at.strftime('%d.%m.%Y %H:%M')}\n"
                  f"🔗 <a href='{self.url}>Перейти к объявлению</a>")
        
        return message


class AvitoMonitor:
    """Монитор новых объявлений на Avito"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session: Optional[aiohttp.ClientSession] = None
        self.seen_items: set[str] = set()  # Для отслеживания уже просмотренных товаров
        
        # Шапки для запросов (имитация браузера)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def start(self):
        """Создание HTTP сессии"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        logger.info("AvitoMonitor started")
    
    async def close(self):
        """Закрытие HTTP сессии"""
        if self.session:
            await self.session.close()
            logger.info("AvitoMonitor stopped")
    
    async def search_items(self, query: str, city: str, max_price: Optional[int] = None,
                          limit: int = None) -> List[AvitoItem]:
        """Поиск товаров по запросу"""
        if not self.session:
            await self.start()
        
        limit = limit or self.settings.RESULTS_LIMIT
        
        try:
            # Формируем URL для поиска
            encoded_query = query.replace(' ', '+')
            
            # Базовый URL для поиска (автоматически определяет домен)
            base_url = "https://avito.ru/search"
            
            # Параметры запроса
            params = {
                'category_id': '1',  # Все категории
                'location': city,    # Город
                'text': query,       # Поиск по названию
                'page_size': limit,  # Количество результатов
            }
            
            # Если есть ограничение по цене
            if max_price:
                params['price_max'] = max_price
            
            logger.info(f"Searching for: {query} in {city}")
            
            # Выполняем поиск через API
            items = await self._fetch_avito_items(encoded_query, params, city)
            
            return items
            
        except Exception as e:
            logger.error(f"Error searching items: {e}")
            return []
    
    async def _fetch_avito_items(self, query: str, params: dict, city: str) -> List[AvitoItem]:
        """Получение товаров через реальный поиск Avito"""
        if not self.session:
            return []
        
        items = []
        
        # Используем реальный API Avito
        url = f"{self.settings.AVITO_BASE_URL}/search"
        
        async with self.session.get(url, params=params) as response:
            if response.status != 200:
                logger.warning(f"Status code: {response.status}")
                return items
            
            data = await response.json()
            
            # Парсим результаты
            if 'items' in data:
                for item_data in data['items']:
                    item = self._parse_item(item_data, city)
                    if item and self._is_new(item):
                        items.append(item)
                        self.seen_items.add(item.url)
            
            return items
    
    def _parse_item(self, data: dict, city: str) -> Optional[AvitoItem]:
        """Парсинг одного товара из данных"""
        try:
            title = data.get('title', '')
            price = data.get('price', {}).get('value', 0)
            url = data.get('url', '')
            posted = data.get('timestamp', {})
            
            if not title or not url:
                return None
            
            # Дата публикации
            posted_at = datetime.fromtimestamp(posted.get('relative', 0)) if posted else datetime.now()
            
            return AvitoItem(
                title=title,
                price=price,
                url=url,
                city=city,
                posted_at=posted_at,
                description=data.get('description', '')
            )
            
        except Exception as e:
            logger.error(f"Error parsing item: {e}")
            return None
    
    def _is_new(self, item: AvitoItem) -> bool:
        """Проверка, является ли товар новым"""
        if item.url in self.seen_items:
            return False
        
        # Проверяем, что товар действительно свежий (в течение последних 2 часов)
        age_hours = (datetime.now() - item.posted_at).total_seconds() / 3600
        return age_hours < 2  # Менее 2 часов
    
    async def monitor_loop(self, callback):
        """Циклический мониторинг"""
        while True:
            try:
                await asyncio.sleep(self.settings.CHECK_INTERVAL)
                logger.info("Running monitoring check...")
                
                # Здесь должна быть логика проверки по последнему поиску
                # Пока просто заглушка
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Пауза при ошибке
