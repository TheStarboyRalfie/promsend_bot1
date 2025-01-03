# from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


''' def is_weekend() -> bool:
    return datetime.utcnow().weekday() in (5, 6)

# inner-мидлварь на сообщения


class WeekndMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if is_weekend():
            return await handler(event, data)


# outer-мидлварь на любые коллбэки
class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if is_weekend():
            return await handler(event, data)
        await event.answer('Бот не работает!', show_alert=True) '''
