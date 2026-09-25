#!/usr/bin/env python3
"""Проверка подключения к Telegram API (токен берётся из .env)"""

import asyncio
import sys
from dotenv import load_dotenv
import os
from aiohttp import ClientSession


async def test_telegram_api():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN не найден в .env")
        return False

    url = f"https://api.telegram.org/bot{token}/getMe"
    print("Testing connection to api.telegram.org...")

    async with ClientSession() as session:
        try:
            async with session.get(url, timeout=15) as response:
                data = await response.json()
                if data.get("ok"):
                    r = data["result"]
                    print(f"OK! Bot connected: @{r['username']} (id {r['id']})")
                    return True
                print(f"Telegram returned: {data}")
                return False
        except Exception as e:
            print(f"Connection failed: {type(e).__name__}: {e}")
            print("\nВозможные причины:")
            print("  - Антивирус/фаервол блокирует HTTPS (см. QUICK_FIX_WINDOWS.md)")
            print("  - Нет доступа к api.telegram.org (нужен VPN/прокси)")
            return False


if __name__ == "__main__":
    sys.exit(0 if asyncio.run(test_telegram_api()) else 1)
