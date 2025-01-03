from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

promsend_link = InlineKeyboardBuilder().row(InlineKeyboardButton(text='Наш официальный канал', url='tg://reslove?domain=promsend'))

delete_code = InlineKeyboardBuilder().add(InlineKeyboardButton(text='Удалить промокод', callback_data='delete_code')).as_markup()

all_ads_ikb_list = [
    InlineKeyboardButton(text='Удалить объявление', callback_data='delete_ad'),
    InlineKeyboardButton(text='Забанить юзера', callback_data='ban_user')
]

def create_ikb(ikb_list):
    inline_keyboard = InlineKeyboardBuilder()
    for button in ikb_list:
        inline_keyboard.add(button)
    return inline_keyboard.as_markup()