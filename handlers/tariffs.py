import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, KeyboardButton

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from aiogram.dispatcher.filters import Command, Text
from aiogram import F

from keyboards.keyboard import create_kb, newbie_kb_list, start_kb_list, tariffs_kb_list, tariff_kb_list, promo_kb_list

from filters.filter import PromocodeFilter, TariffFilter, DBMemberFilter, BadWordsFilter, BannedFilter

from db.commands import check_user, get_promos, get_ad, add_user, add_existing_user

from datetime import datetime, timedelta

tariffs_dict = {
    '1 день':
        ''' 
<b>Тариф "1 день"</b>

Мы отправим 7200 сообщений с вашей рекламой в течении 24 часов.

<b>Цена — 99₽</b>
        ''',
    '3 дня':
        '''
<b>Тариф "3 дня"</b>

Мы отправим 21600 сообщений с вашей рекламой в течении 3 дней.

<b>Цена — 199₽</b>
        ''',
    '7 дней':
        '''
<b>Тариф "7 дней"</b>

Мы отправим 50400 сообщений с вашей рекламой в течении 7 дней.

<b>Цена — 399₽</b>
        ''',
    '30 дней':
        '''
<b>Тариф "30 дней"</b>

Мы отправим 216000 сообщений с вашей рекламой в течении 3 дней.

<b>Цена — 1299₽</b>
        '''
}

tariffs_days_dict = {
    '1 день': 1,
    '3 дня': 3,
    '7 дней': 7,
    '30 дней': 30
}



router = Router()
router.message.filter(F.chat.type.in_({'private'}))
router.message.filter(BannedFilter())

class TariffPurchase(StatesGroup):
    tariff_choosing = State()
    text_entering = State()
    promo_entering = State()
    data_saving = State()

@router.message(Text(text='Тарифы'))
async def tariffs_cmd(message: Message, state: FSMContext):
    await state.set_data({})
    user = await check_user(user_id=message.from_user.id)
    if user == False:
        await message.answer(
           f'''
    ❗️ Если ты впервые пользуешься нашим ботом, то у тебя есть шанс получить бесплатную рассылку на день! Тебе всего лишь нужно подписаться на наш телеграм-канал: @promsend
            '''
        )
    await message.answer('Список действующих тарифов на данный момент.\n\n⬇️ Выберите понравившийся и нажмите на него на клавиатуре, чтобы узнать больше:', reply_markup=create_kb(tariffs_kb_list))
    await state.set_state(TariffPurchase.tariff_choosing)


@router.message(TariffPurchase.tariff_choosing, Text(text='В главное меню'))
async def to_main_menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    user = await check_user(user_id=message.from_user.id)
    if user == True:
        await message.reply('↩️ Возварщаю главное меню', reply_markup=create_kb(start_kb_list))
    else:
        await message.reply('↩️ Возварщаю главное меню', reply_markup=create_kb(newbie_kb_list))

@router.message(TariffPurchase.tariff_choosing, Text(text='В меню'))
async def to_tariffs_menu_cmd(message: Message, state: FSMContext):
    await state.set_data({})
    await state.set_state(TariffPurchase.tariff_choosing)
    await message.reply('↩️ Возвращаю меню', reply_markup=create_kb(tariffs_kb_list))

@router.message(TariffPurchase.tariff_choosing, F.text.in_(tariffs_dict))
async def tariff(message: Message, state: FSMContext):
    await state.update_data(tariff=message.text)
    tariff_info = tariffs_dict.get(message.text)
    await message.answer(f'{tariff_info}', reply_markup=create_kb(tariff_kb_list))

@router.message(TariffFilter(), TariffPurchase.tariff_choosing, Text(text='Купить этот тариф'))
async def tariff_rejection(message: Message, state: FSMContext):
    await message.answer('🚫 Вы не можете приобрести этот тариф, так как у вас уже есть действующий тариф. Дождитесь его окончания', reply_markup=create_kb(tariffs_kb_list))

@router.message(TariffPurchase.tariff_choosing, Text(text='Купить этот тариф'))
async def tariff_purchase(message: Message, state: FSMContext):
    user_data = await state.get_data()
    tariff = user_data.get('tariff')
    await message.answer(
        f'Вы выбрали тариф <b>"{tariff}"</b>.\n\n📝 Отправьте одним сообщением текст вашего объявления и одно фото (необязательно):', 
        reply_markup=create_kb([[KeyboardButton(text='Отмена')]])
        )
    await state.set_state(TariffPurchase.text_entering)

@router.message(TariffPurchase.text_entering, Text(text='Отмена'))
async def purchase_cancel(message: Message, state: FSMContext):
    await state.set_data({})
    await state.set_state(TariffPurchase.tariff_choosing)
    await message.reply('↩️ Покупка тарифа отменена', reply_markup=create_kb(tariffs_kb_list))

@router.message(BadWordsFilter(), TariffPurchase.text_entering)
async def bad_words(message: Message):
    await message.answer('🤬 В вашем объявлении присутствует нецензурная брань! Попробуйте ещё раз')

@router.message(TariffPurchase.text_entering)
async def data_saving(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    if message.photo:
        await state.update_data(ad_text=message.caption)
        await state.update_data(ad_photo=message.photo[-1].file_id)
    else:
        await state.update_data(ad_text=message.text)
        await state.update_data(ad_photo='no_photo')
    user_data = await state.get_data()
    ad_photo = user_data.get('ad_photo')
    ad_text = user_data.get('ad_text')
    await message.answer('⬇️ Так будет выглядет ваше объявление:')
    if ad_photo != 'no_photo':
        await message.answer_photo(photo=ad_photo, caption=ad_text)
    else:
        await message.answer(ad_text)
    await message.answer('🏷️ Введите промокод, если есть:', reply_markup=create_kb(promo_kb_list))
    await state.set_state(TariffPurchase.promo_entering)
    
@router.message(PromocodeFilter(), TariffPurchase.promo_entering)
async def with_promo(message: Message, state: FSMContext):
    await message.answer('Промокод совпадает!')
    user_data = await state.get_data()
    user_id = message.from_user.id
    ad_photo = user_data.get('ad_photo')
    ad_text = user_data.get('ad_text')
    tariff = user_data.get('tariff')
    tariff_ends = datetime.now() + timedelta(days=tariffs_days_dict.get(tariff))
    user = await check_user(user_id=message.from_user.id)
    if user == True:
        await add_existing_user(user_id, tariff, tariff_ends, ad_text, ad_photo)
    else:
        await add_user(user_id, tariff, tariff_ends, ad_text, ad_photo)
    await state.clear()
    await message.answer('✅ Ваше объявление успешно добавлено в систему!', reply_markup=create_kb(start_kb_list))

@router.message(TariffPurchase.promo_entering, Text(text='Отмена'))
async def promo_cancel(message: Message, state: FSMContext):
    await state.set_data({})
    await state.set_state(TariffPurchase.tariff_choosing)
    await message.reply('↩️ Покупка тарифа отменена', reply_markup=create_kb(tariffs_kb_list))

@router.message(TariffPurchase.promo_entering, Text(text='Купить без промокода'))
async def without_promo(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = message.from_user.id
    ad_photo = user_data.get('ad_photo')
    ad_text = user_data.get('ad_text')
    tariff = user_data.get('tariff')
    tariff_ends = datetime.now() + timedelta(days=tariffs_days_dict.get(tariff))
    user = await check_user(user_id=message.from_user.id)
    if user == True:
        await add_existing_user(user_id, tariff, tariff_ends, ad_text, ad_photo)
    else:
        await add_user(user_id, tariff, tariff_ends, ad_text, ad_photo)
    await state.clear()
    await message.answer('✅ Ваше объявление успешно добавлено в систему!', reply_markup=create_kb(start_kb_list))