from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, KeyboardButton

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from aiogram.dispatcher.filters import Text
from aiogram import F

from keyboards.keyboard import create_kb, newbie_kb_list, run_free_kb_list, start_kb_list

from filters.filter import ChannelMemberFilter, DBMemberFilter, BadWordsFilter, BannedFilter

from datetime import datetime, timedelta

from db.commands import add_user, get_ad

router = Router()
router.message.filter(F.chat.type.in_({'private'}))
router.message.filter(BannedFilter())

class FreeTryPurchase(StatesGroup):
    text_entering = State()
    data_saving = State()

@router.message(ChannelMemberFilter(), DBMemberFilter(), Text(text='Попробовать бесплатно'))
async def try_free_sub(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        '''
Вам доступен тариф <b>"1 день"</b>
        
📝 Отправьте одним сообщением текст вашего объявления и одно фото (необязательно):
        ''',
        reply_markup=create_kb([[KeyboardButton(text='Отмена')]])
    )
    await state.set_state(FreeTryPurchase.text_entering)

@router.message(DBMemberFilter(), Text(text='Попробовать бесплатно'))
async def try_free(message: Message):
    await message.answer(
        'Чтобы бесплатно попробовать рассылку на 1 день, вам нужно всего лишь подписаться на наш телеграм-канал: @promsend',
        reply_markup=create_kb(newbie_kb_list)
    )

@router.message(FreeTryPurchase.text_entering, Text(text='Отмена'))
async def purchase_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.reply('↩️ Получение бесплатного тарифа <b>"1 день"</b> отменено', reply_markup=create_kb(newbie_kb_list))

@router.message(BadWordsFilter(), FreeTryPurchase.text_entering)
async def bad_words(message: Message):
    await message.answer('🤬 В вашем объявлении присутствует нецензурная брань! Попробуйте ещё раз')
        
@router.message(FreeTryPurchase.text_entering)
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
    await message.answer('⬇️ Вот так будет выглядеть ваше объявление:')
    if ad_photo != 'no_photo':
        await message.answer_photo(photo=ad_photo, caption=ad_text, reply_markup=create_kb(run_free_kb_list))
    else:
        await message.answer(ad_text, reply_markup=create_kb(run_free_kb_list))
    await message.answer('📤 Начать рассылку?')
    await state.set_state(FreeTryPurchase.data_saving)

@router.message(FreeTryPurchase.data_saving, Text(text='Отмена'))
async def purchase_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.reply('↩️ Получение бесплатного тарифа <b>"1 день"</b> отменено', reply_markup=create_kb(newbie_kb_list))

@router.message(FreeTryPurchase.data_saving, Text(text='Начать рассылку'))
async def distrib_start(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data.get('user_id')
    ad_photo = user_data.get('ad_photo')
    ad_text = user_data.get('ad_text')
    tariff_ends = datetime.now() + timedelta(days=1)
    await add_user(user_id, '1 день', tariff_ends, ad_text, ad_photo)
    await state.clear()
    await message.answer('✅ Ваше объявление успешно добавлено в систему!', reply_markup=create_kb(start_kb_list))
    
    