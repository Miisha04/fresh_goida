import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from handlers import router
from config import TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(router)

async def main():
    # Удаляем старые вебхуки
    await bot.delete_webhook(drop_pending_updates=True)

    # Начинаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Устанавливаем политику для совместимости с Windows
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
