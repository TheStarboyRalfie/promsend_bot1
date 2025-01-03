from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from aiogram.dispatcher.filters import Command, Text
from aiogram import F

from keyboards.keyboard import create_kb, newbie_kb_list, start_kb_list

from filters.filter import ChannelMemberFilter, BannedFilter

from db.commands import check_user

router = Router()
router.message.filter(F.chat.type.in_({'private'}))
router.message.filter(BannedFilter())


@router.message(Command(commands=['start']))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    user = await check_user(message.from_user.id)
    if user == True:
        await message.answer(
            f'Приветствуем тебя, {message.from_user.first_name}!',
            reply_markup=create_kb(start_kb_list)
        )
    else:
        await message.answer(
            f'Приветствуем тебя, {message.from_user.first_name}!',
            reply_markup=create_kb(newbie_kb_list)
        )

@router.message(Text(text='Как это работает?'))
async def how_cmd(message: Message):
    user = await check_user(message.from_user.id)
    if user == True:
        await message.answer(
            f'''
<b>❓ Что такое PROMSEND BOT?</b>

С помощью нашего бота вы сможете увеличить прибыль с вашего Telegram-канала в разы! Наш бот будет рассылать ваше сообщение с продажей/покупкой рекламы по тематическим телеграм чатам, где администраторы ищут рекламодателей и рекламодатели ищут администраторов.

<b>Как начать пользоваться ботом?</b>

В разделе “Тарифы” вы можете выбрать тариф на любой вкус и цвет. Они различаются ценой, количеством сообщений и продолжительностью рассылки. Далее, когда тариф выбран, вы должны отправить сообщение, которое мы будем рассылать, и оплатить наши услуги.
            ''',
            reply_markup=create_kb(start_kb_list)
        )
    else:
        await message.answer(
            f'''
<b>❓ Что такое PROMSEND BOT?</b>

С помощью нашего бота вы сможете увеличить прибыль с вашего Telegram-канала в разы! Наш бот будет рассылать ваше сообщение с продажей/покупкой рекламы по тематическим телеграм чатам, где администраторы ищут рекламодателей и рекламодатели ищут администраторов.

<b>Как начать пользоваться ботом?</b>

В разделе “Тарифы” вы можете выбрать тариф на любой вкус и цвет. Они различаются ценой, количеством сообщений и продолжительностью рассылки. Далее, когда тариф выбран, Вы должны отправить сообщение, которое мы будем рассылать, и оплатить наши услуги.

<b>❗️ Если вы пользуетесь нашим ботом впервые, то у вас есть возможность получить 1 день рассылки абсолютно бесплатно! Для этого вам всего лишь нужно перейти в раздел “Попробовать бесплатно” и подписаться на наш телеграм канал. Кстати, там мы регулярно выкладываем промокоды на скидку в нашем боте.</b>
            ''',
            reply_markup=create_kb(newbie_kb_list)
        )
