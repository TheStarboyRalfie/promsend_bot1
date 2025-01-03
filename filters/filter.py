import asyncpg

import string
import json

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message
from aiogram.types import ChatMemberMember, ChatMemberOwner

from aiogram import Bot

from aiogram.methods import get_chat_member

from config import PG_PASS, ADMIN_ID_0, ADMIN_ID_1

class BannedFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
        response = await conn.fetchrow(f'SELECT EXISTS(SELECT user_id FROM banned WHERE user_id = {message.from_user.id});')
        await conn.close()
        return True if not response['exists'] else False

class ChannelMemberFilter(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        user = await bot.get_chat_member(chat_id='-1001243427849', user_id=message.from_user.id)
        if isinstance(user, ChatMemberMember) or isinstance(user, ChatMemberOwner):
            return True
        else:
            return False

class DBMemberFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
        response = await conn.fetchrow(f'SELECT EXISTS(SELECT user_id FROM users WHERE user_id = {message.from_user.id});')
        await conn.close()
        return True if not response['exists'] else False
    
class TariffFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
        tariff_response = await conn.fetchval(f'SELECT tariff FROM users WHERE user_id = $1', message.from_user.id)
        exists_response = await conn.fetchrow(f'SELECT EXISTS(SELECT user_id FROM users WHERE user_id = {message.from_user.id});')
        await conn.close()
        if tariff_response != 'no_tariff' and exists_response['exists']:
            return True
        else:
            return False

class PromocodeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        conn = await asyncpg.connect(user='postgres', password=PG_PASS, database='postgres', host='localhost')
        response = await conn.fetchrow(f'SELECT EXISTS(SELECT code_name FROM promocodes WHERE code_name = $1);', message.text)
        await conn.close()
        return True if response['exists'] else False

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == ADMIN_ID_0 or ADMIN_ID_1:
            return True
        else:
            return False
        
class BadWordsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        def distance(a, b):
            n, m = len(a), len(b)
            if n > m:
                a, b = b, a
                n, m = m, n
            current_row = range(n + 1)
            for i in range(1, m + 1):
                previous_row, current_row = current_row, [i] + [0] * n
                for j in range(1, n + 1):
                    add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                    if a[j - 1] != b[i - 1]:
                        change += 1
                    current_row[j] = min(add, delete, change)
            return current_row[n]
        bad_words = ['блять', 'пизда', 'пиздец', 'хуй', 'хуйня', 'ебать', 'ахуеть', 'пидор', 'пидорас', 'пидарас', 'сука', 'ебало']
        d =   {
                'а' : ['а', 'a', '@'],
                'б' : ['б', '6', 'b'],
                'в' : ['в', 'b', 'v'],
                'г' : ['г', 'r', 'g'],
                'д' : ['д', 'd'],
                'е' : ['е', 'e'],
                'ё' : ['ё', 'e'],
                'ж' : ['ж', 'zh', '*'],
                'з' : ['з', '3', 'z'],
                'и' : ['и', 'u', 'i'],
                'й' : ['й', 'u', 'i'],
                'к' : ['к', 'k', 'i{', '|{'],
                'л' : ['л', 'l', 'ji'],
                'м' : ['м', 'm'],
                'н' : ['н', 'h', 'n'],
                'о' : ['о', 'o', '0'],
                'п' : ['п', 'n', 'p'],
                'р' : ['р', 'r', 'p'],
                'с' : ['с', 'c', 's'],
                'т' : ['т', 'm', 't'],
                'у' : ['у', 'y', 'u'],
                'ф' : ['ф', 'f'],
                'х' : ['х', 'x', 'h' , '}{'],
                'ц' : ['ц', 'c', 'u,'],
                'ч' : ['ч', 'ch'],
                'ш' : ['ш', 'sh'],
                'щ' : ['щ', 'sch'],
                'ь' : ['ь', 'b'],
                'ы' : ['ы', 'bi'],
                'ъ' : ['ъ'],
                'э' : ['э', 'e'],
                'ю' : ['ю', 'io'],
                'я' : ['я', 'ya']
                }
        if message.photo:
            phrase = message.caption.lower().replace(" ", "")
        else:
            phrase = message.text.lower().replace(" ", "")
        for key, value in d.items():
            for letter in value:
                for phrase_letter in phrase:
                    if letter == phrase_letter:
                        phrase = phrase.replace(phrase_letter, key)
        for word in bad_words:
            for part in range(len(phrase)):
                fragment = phrase[part: part+len(word)]
                if distance(fragment, word) <= len(word)*0.25:
                    return True