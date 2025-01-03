from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, KeyboardButton

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from aiogram.dispatcher.filters import Text
from aiogram import F

from keyboards.keyboard import create_kb, newbie_kb_list, start_kb_list, my_distr_kb_kist, no_ad_kb_list
from keyboards.inline_kbs import create_ikb

from filters.filter import ChannelMemberFilter, DBMemberFilter, BadWordsFilter, BannedFilter

from db.commands import check_user, get_ad, update_ad, get_tariff_info

router = Router()
router.message.filter(F.chat.type.in_({'private'}))
router.message.filter(BannedFilter())

class AdChangig(StatesGroup):
    start = State()
    new_ad_sending = State()

class AdCreating(StatesGroup):
    start = State()
    text_entering = State()

@router.message(Text(text='Моя рассылка'))
async def my_distr(message: Message, state: FSMContext):
    user = await check_user(message.from_user.id)
    if user == True:
        user_ad = await get_ad(message.from_user.id)
        if user_ad['ad_text'] != 'no_text':
            if user_ad['tariff'] != 'no_tariff':
                await message.answer('⬇️ Вот так выглядит ваше объявление:')
                if user_ad['ad_photo'] == 'no_photo':
                    await message.answer(f'{user_ad["ad_text"]}', reply_markup=create_kb(my_distr_kb_kist))
                    await state.set_state(AdChangig.start)
                else:
                    await message.answer_photo(user_ad['ad_photo'], f'{user_ad["ad_text"]}', reply_markup=create_kb(my_distr_kb_kist))
                    await state.set_state(AdChangig.start)
            else:
                await message.answer('❗️ Ваш тариф закончился! Вы можете купить любой понравившийся вам тариф во вкладке <b>"Тарифы"</b>')
                await message.answer('⬇️ Вот так выглядело ваше объявление:')
                if user_ad['ad_photo'] == 'no_photo':
                    await message.answer(f'{user_ad["ad_text"]}')
                else:
                    await message.answer_photo(user_ad['ad_photo'], f'{user_ad["ad_text"]}')
        elif user_ad['ad_text'] == 'no_text' and user_ad['tariff'] == 'no_tariff':
            await message.answer('❗️ Ваш тариф закончился! Вы можете купить любой понравившийся вам тариф во вкладке <b>"Тарифы"</b>')
        elif user_ad['ad_text'] == 'no_text':
            await message.answer('❗️ У вас нет объявления. Вы можете создать его', reply_markup=create_kb(no_ad_kb_list))
            await state.set_state(AdCreating.start)
    else:
        await message.answer(
                '''
У вас ещё нет объявления. Вы можете приобрести понравившийся вам тариф во вкладке <b>"Тарифы"</b>

<b>❗️ Если вы пользуетесь нашим ботом впервые, то у Вас есть возможность получить 1 день рассылки абсолютно бесплатно! Для этого Вам всего лишь нужно перейти в раздел “Попробовать бесплатно” и подписаться на наш телеграм канал. Кстати, там мы регулярно выкладываем промокоды на скидку в нашем боте.</b>
                ''', 
                reply_markup=create_kb(newbie_kb_list)
                )

@router.message(AdChangig.start, Text(text='В главное меню'))
async def to_main_menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    user = await check_user(user_id=message.from_user.id)
    if user == True:
        await message.reply('↩️ Возварщаю главное меню', reply_markup=create_kb(start_kb_list))
    else:
        await message.reply('↩️ Возварщаю главное меню', reply_markup=create_kb(newbie_kb_list))

@router.message(AdChangig.start, Text(text='Мой тариф'))
async def display_tariff(message: Message):
    tariff_info = await get_tariff_info(message.from_user.id)
    await message.answer(f'''🏷 Ваш действующий тариф: <b>"{tariff_info['tariff']}"</b>\n\n📅 Дата окончания тарифа: {tariff_info['tariff_ends'].strftime("%d.%m.%Y")}''')

@router.message(AdChangig.start, Text(text='Изменить объявление'))
async def ad_updating(message: Message, state: FSMContext):
    await message.answer('📝 Отправьте одним сообщением текст вашего нового объявления и одно фото (необязательно):', reply_markup=create_kb([[KeyboardButton(text='Отмена')]]))
    await state.set_state(AdChangig.new_ad_sending)

@router.message(AdChangig.new_ad_sending, Text(text='Отмена'))
async def updating_cancel(message: Message, state: FSMContext):
    await state.set_state(AdChangig.start)
    await message.reply('↩️ Изменение объявления отменено', reply_markup=create_kb(my_distr_kb_kist))

@router.message(BadWordsFilter(), AdChangig.new_ad_sending)
async def bad_words(message: Message):
    await message.answer('🤬 В вашем объявлении присутствует нецензурная брань! Попробуйте ещё раз')    

@router.message(AdChangig.new_ad_sending)
async def new_ad(message: Message, state: FSMContext):
    if message.photo:
        await update_ad(user_id=message.from_user.id, ad_text=message.caption, ad_photo=message.photo[-1].file_id)
    else:
        await update_ad(user_id=message.from_user.id, ad_text=message.text, ad_photo='no_photo')
    await state.set_state(AdChangig.start)
    await message.answer('✅ Ваше объявление успешно обновлено!\n\n⬇ Теперь оно выглядит так:', reply_markup=create_kb(my_distr_kb_kist))
    user_ad = await get_ad(message.from_user.id)
    if user_ad['ad_photo'] == 'no_photo':
        await message.answer(f"{user_ad['ad_text']}")
    else:
        await message.answer_photo(user_ad['ad_photo'], f"{user_ad['ad_text']}")

@router.message(AdChangig.start, Text(text='Удалить объявление'))
async def delete_ad(message: Message, state: FSMContext):
    await message.answer(
        '⚠️ Вы уверены, что хотите удалить ваше объявление? В таком случае оно перестанет рассылаться', 
        reply_markup=create_kb([[KeyboardButton(text='Всё равно удалить')], [KeyboardButton(text='Отмена')]])
        )

@router.message(AdChangig.start, Text(text='Отмена'))
async def deleting_cancel(message: Message, state: FSMContext):
    await state.set_state(AdChangig.start)
    await message.reply('↩️ Удаление объявления отменено', reply_markup=create_kb(my_distr_kb_kist))

@router.message(AdChangig.start, Text(text='Всё равно удалить'))
async def ad_deleting(message: Message, state: FSMContext):
    await update_ad(message.from_user.id, 'no_text', 'no_photo')
    await state.set_state(AdCreating.start)
    await message.answer('✅ Ваше объявление успешно удалено!', reply_markup=create_kb(no_ad_kb_list))
    
@router.message(AdCreating.start, Text(text='Создать объявление'))
async def create_ad(message: Message, state: FSMContext):
    await message.answer('📝 Отправьте одним сообщением текст вашего объявления и одно фото (необязательно):', reply_markup=create_kb([[KeyboardButton(text='Отмена')]]))
    await state.set_state(AdCreating.text_entering)

@router.message(AdCreating.start, Text(text='Мой тариф'))
async def display_tariff(message: Message):
    tariff_info = await get_tariff_info(message.from_user.id)
    await message.answer(f'''🏷 Ваш действующий тариф: <b>"{tariff_info['tariff']}"</b>\n\n📅 Дата окончания тарифа: {tariff_info['tariff_ends'].strftime("%d.%m.%Y")}''')
    
@router.message(AdCreating.start, Text(text='В главное меню'))
async def to_main_menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    user = await check_user(user_id=message.from_user.id)
    if user == True:
        await message.reply('↩️ Возвращаю главное меню', reply_markup=create_kb(start_kb_list))
    else:
        await message.reply('↩️ Возвращаю главное меню', reply_markup=create_kb(newbie_kb_list))

@router.message(AdCreating.text_entering, Text(text='Отмена'))
async def creating_cancel(message: Message, state: FSMContext):
    await state.set_state(AdCreating.start)
    await message.reply('↩️ Создание объявления отменено', reply_markup=create_kb(no_ad_kb_list))        

@router.message(BadWordsFilter(), AdCreating.text_entering)
async def bad_words(message: Message):
    await message.answer('🤬 В вашем объявлении присутствует нецензурная брань! Попробуйте ещё раз')

@router.message(AdCreating.text_entering)
async def new_ad(message: Message, state: FSMContext):
    if message.photo:
        await update_ad(user_id=message.from_user.id, ad_text=message.caption, ad_photo=message.photo[-1].file_id)
    else:
        await update_ad(user_id=message.from_user.id, ad_text=message.text, ad_photo='no_photo')
    await state.set_state(AdChangig.start)
    await message.answer('✅ Ваше объявление успешно создано!\n\n⬇ Теперь оно выглядит так:', reply_markup=create_kb(my_distr_kb_kist))
    user_ad = await get_ad(message.from_user.id)
    if user_ad['ad_photo'] == 'no_photo':
        await message.answer(f"{user_ad['ad_text']}")
    else:
        await message.answer_photo(user_ad['ad_photo'], f"{user_ad['ad_text']}")
