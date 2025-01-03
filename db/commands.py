import asyncpg

from config import PG_PASS

from aiogram import Bot

from aiogram.types import Message

from keyboards.keyboard import create_kb, start_kb_list

async def check_user(user_id) -> bool:
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    response = await conn.fetchrow(f'SELECT EXISTS(SELECT user_id from users WHERE user_id = {user_id});')
    await conn.close()
    return True if response['exists'] else False

async def get_ids():
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    ids = await conn.fetch('SELECT user_id FROM users')
    await conn.close()
    return ids

async def add_user(user_id, tariff, tariff_ends, ad_text, ad_photo):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.execute(
        f'INSERT INTO users (user_id, tariff, tariff_ends, ad_text, ad_photo, is_distr, is_warned) VALUES ($1, $2, $3, $4, $5, $6, $7);', 
        user_id, tariff, tariff_ends, ad_text, ad_photo, True, False
    )
    await conn.close()

async def add_existing_user(user_id, tariff, tariff_ends, ad_text, ad_photo):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.execute(
        f'UPDATE users SET tariff = $1, tariff_ends = $2, ad_text = $3, ad_photo = $4,  is_distr = $5, is_warned = $6 WHERE user_id = $7;',
        tariff, tariff_ends, ad_text, ad_photo, True, False, user_id
        )

async def get_ad(user_id):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    ad = await conn.fetchrow(f'SELECT ad_text, ad_photo, tariff FROM users WHERE user_id = $1;', user_id)
    await conn.close()
    return ad

async def get_tariff_info(user_id):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    tariff_info = await conn.fetchrow(f'SELECT tariff, tariff_ends FROM users WHERE user_id = $1;', user_id)
    await conn.close()
    return tariff_info

async def get_all_ads():
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    ads = await conn.fetch(f'SELECT user_id, ad_text, ad_photo, tariff, tariff_ends, is_distr, is_warned FROM users;')
    await conn.close()
    return ads

async def update_ad(user_id, ad_text, ad_photo):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.execute(
        f'UPDATE users SET ad_text = $1, ad_photo = $2 WHERE user_id = $3;', 
        ad_text, ad_photo, user_id
        )
    await conn.close()

async def stop_distributing(user_id, bot: Bot):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.execute(f'UPDATE users SET tariff = $1, is_distr = $2, is_warned = $3 WHERE user_id = $4;', 'no_tariff', False, True, user_id)
    await conn.close()
    await bot.send_message(user_id, 'Ваш тариф закончился. Спасибо, что пользуетесь нашим сервисом! ❤️', reply_markup=create_kb(start_kb_list))

async def add_promo(code_name, discount):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    discount = float(discount)
    await conn.execute(
        f'INSERT INTO promocodes (code_name, discount) VALUES ($1, $2);',
        code_name, discount
    )
    await conn.close()

async def get_promos():
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    codes = await conn.fetch(f'SELECT code_name, discount FROM promocodes;')
    await conn.close()
    return codes

async def del_promo(code_name):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.execute('DELETE FROM promocodes WHERE code_name = $1', code_name)
    await conn.close()

async def ban_user(user_id):
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.execute('INSERT INTO banned (user_id) VALUES ($1);', user_id)
    await conn.execute('DELETE FROM users WHERE user_id = $1;', user_id)
    await conn.close()

async def get_banned_users():
    conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
    await conn.fetch('SELECT user_id FROM banned;')
