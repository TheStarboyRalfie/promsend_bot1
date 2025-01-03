from aiogram import Router
from aiogram.types import Message, CallbackQuery, KeyboardButton

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from aiogram.dispatcher.filters import Command, Text
from aiogram import F

from keyboards.keyboard import create_kb, admin_start_list, start_kb_list
from keyboards.inline_kbs import create_ikb, delete_code, all_ads_ikb_list

from filters.filter import AdminFilter

from db.commands import add_promo, get_promos, del_promo, get_ids, get_all_ads, update_ad, ban_user

from aiogram import Bot

router = Router()
router.message.filter(F.chat.type.in_({'private'}))

class AdminPanel(StatesGroup):
    start = State()

class AddPromo(StatesGroup):
    discount = State()
    saving =  State()

class DelPromo(StatesGroup):
    promo_choosing = State()

class CreatePost(StatesGroup):
    text_entering = State()

@router.message(AdminFilter(), Command(commands=['administrator']))
async def admin_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Панель администрирования открыта:', reply_markup=create_kb(admin_start_list))
    await state.set_state(AdminPanel.start)

@router.message(AdminPanel.start, Text(text='В главное меню'))
async def to_main_menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.reply('Возварщаю главное меню', reply_markup=create_kb(start_kb_list))

@router.message(AdminPanel.start, Text(text='Добавить промокод'))
async def add_promocode(message: Message, state: FSMContext):
    await message.answer('Введите название промокода:', reply_markup=create_kb([[KeyboardButton(text='Отмена')]]))
    await state.set_state(AddPromo.discount)

@router.message(AddPromo.discount, Text(text='Отмена'))
async def cancel_discount(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.start)
    await message.reply('Добавление промокода отменено', reply_markup=create_kb(admin_start_list))

@router.message(AddPromo.discount)
async def enter_disc(message: Message, state: FSMContext):
    await state.update_data(code_name=message.text)
    await message.answer('Введите скидку:', reply_markup=create_kb([[KeyboardButton(text='Отмена')]]))
    await state.set_state(AddPromo.saving)

@router.message(AddPromo.saving, Text(text='Отмена'))
async def cancel_discount(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.start)
    await message.reply('Добавление промокода отменено', reply_markup=create_kb(admin_start_list))
        
@router.message(AddPromo.saving)
async def saving(message: Message, state: FSMContext):
    code_data = await state.get_data()
    code_name = code_data['code_name']
    discount = message.text
    await add_promo(code_name, discount)
    await message.answer(f'Промокод {code_name} со скидкой {discount} добавлен', reply_markup=create_kb(admin_start_list))
    await state.set_state(AdminPanel.start)

@router.message(AdminPanel.start, Text(text='Удалить промокод'))
async def display_promocodes(message: Message, state: FSMContext):
    codes = await get_promos()
    for row in codes:
        await message.answer(f'{row["code_name"]}\n\nСкидка: {row["discount"]}', reply_markup=delete_code)

@router.callback_query(text='delete_code')
async def delete_promocode(callback: CallbackQuery):
    code_name = callback.message.text.split('\n\n')[0]
    await del_promo(code_name)
    await callback.message.delete()
    await callback.answer(f'Промокод {code_name} удалён')
    #await state.set_state(AdminPanel.start)

@router.message(AdminPanel.start, Text(text='Сделать пост в боте'))
async def create_post(message: Message, state: FSMContext):
    await message.answer('Введите сообщение для отправки:', reply_markup=create_kb([[KeyboardButton(text='Отмена')]]))
    await state.set_state(CreatePost.text_entering)

@router.message(CreatePost.text_entering, Text(text='Отмена'))    
async def post_cancel(message: Message, state: FSMContext):
    await message.reply('Пост отменён', reply_markup=create_kb(admin_start_list))
    await state.set_state(AdminPanel.start)

@router.message(CreatePost.text_entering)
async def post_distibuting(message: Message, state: FSMContext, bot: Bot):
    ids = await get_ids()
    if message.photo:
        for user_id in ids:
            await bot.send_photo(user_id['user_id'], message.photo[-1].file_id, message.caption)
    else:
        for user_id in ids:
            await bot.send_message(user_id['user_id'], message.text)
    await message.answer('Пост сделан!', reply_markup=create_kb(admin_start_list))
    await state.set_state(AdminPanel.start)

@router.message(AdminPanel.start, Text(text='Объявления'))
async def display_posts(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Объявления в базе данных:')
    ads = await get_all_ads()
    for ad in ads:
        user = await bot.get_chat(ad['user_id'], ad['user_id'])
        if ad['ad_photo'] == 'no_photo':
            await message.answer(f'@{user.username}\nID: ({user.id})\n\n{ad["ad_text"]}\n\nТариф: {ad["tariff"]}\nДата окончания тарифа: {ad["tariff_ends"]}', reply_markup=create_ikb(all_ads_ikb_list))
        else:
            await message.answer_photo(ad['ad_photo'], f'@{user.username}\n ID: ({user.id})\n\n{ad["ad_text"]}\n\nТариф: {ad["tariff"]}\nДата окончания тарифа: {ad["tariff_ends"]}', reply_markup=create_ikb(all_ads_ikb_list))

@router.callback_query(text='delete_ad')
async def delete_ad(callback: CallbackQuery):
    if callback.message.photo:
        user_id = int(callback.message.caption.split('(')[1].split(')')[0])
    else:
        user_id = int(callback.message.text.split('(')[1].split(')')[0])
    await update_ad(user_id, 'no_text', 'no_photo')
    await callback.message.delete()

@router.callback_query(text='ban_user')
async def banning_user(callback: CallbackQuery):
    if callback.message.photo:
        user_id = int(callback.message.caption.split('(')[1].split(')')[0])
    else:
        user_id = int(callback.message.text.split('(')[1].split(')')[0])
    await ban_user(user_id)
    await callback.message.delete()
    await callback.answer(f'Пользователь забанен')
