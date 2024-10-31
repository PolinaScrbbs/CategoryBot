import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from .database import engine
from .database.models import Base
from .handlers import router


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await create_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        print("Бот запущен")
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        print("Бот выключен вручную")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
    