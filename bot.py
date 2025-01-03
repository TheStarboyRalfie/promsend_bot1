import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

from on_startup import on_startup

from handlers import start, tariffs, try_free, admin, my_distr
#from middlewares.weekend import WeekendCallbackMiddleware

logging.basicConfig(level=logging.INFO, format='%(filename)s - [%(asctime)s] - %(levelname)s - %(name)s - %(message)s')

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(try_free.router)
    dp.include_router(tariffs.router)
    dp.include_router(my_distr.router)
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(bot))
    # dp.callback_query.outer_middleware(WeekendCallbackMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())

#КОМЕНТ :)))
