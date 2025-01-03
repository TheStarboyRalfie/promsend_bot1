#from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

newbie_kb_list = [
    [KeyboardButton(text='Попробовать бесплатно')],
    [KeyboardButton(text='Моя рассылка')],
    [
        KeyboardButton(text='Тарифы'),
        KeyboardButton(text='Как это работает?')
    ]
]

start_kb_list = [
    [KeyboardButton(text='Моя рассылка')],
    [
        KeyboardButton(text='Тарифы'),
        KeyboardButton(text='Как это работает?')
    ]
]

tariffs_kb_list = [
    [
        KeyboardButton(text='1 день'),
        KeyboardButton(text='3 дня'),
    ],
    [
        KeyboardButton(text='7 дней'),
        KeyboardButton(text='30 дней')
    ],
    [KeyboardButton(text='В главное меню')]
]

tariff_kb_list = [
    [KeyboardButton(text='Купить этот тариф')],
    [KeyboardButton(text='В меню')]
]

promo_kb_list = [
    [KeyboardButton(text='Купить без промокода')],
    [KeyboardButton(text='Отмена')]
]

run_free_kb_list = [
    [KeyboardButton(text='Начать рассылку')],
    [KeyboardButton(text='Отмена')]
]

admin_start_list = [
    [
        KeyboardButton(text='Добавить промокод'), 
        KeyboardButton(text='Удалить промокод')
    ],
    [
        KeyboardButton(text='Сделать пост в боте'), 
        KeyboardButton(text='Объявления')
    ],
    [KeyboardButton(text='В главное меню')]
]

my_distr_kb_kist = [
    [
        KeyboardButton(text='Изменить объявление'),
        KeyboardButton(text='Удалить объявление')
    ],
    [
        KeyboardButton(text='Мой тариф'),
        KeyboardButton(text='Остановить рассылку')
    ],
    [KeyboardButton(text='В главное меню')]
]

no_ad_kb_list = [
    [KeyboardButton(text='Создать объявление')],
    [KeyboardButton(text='Мой тариф')],
    [KeyboardButton(text='В главное меню')]
]

def create_kb(kb_list: List) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True
    )



''' def start_kb(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True) '''


''' def get_checkin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Поддтвердить', callback_data='confirm')
    return kb.as_markup() '''
