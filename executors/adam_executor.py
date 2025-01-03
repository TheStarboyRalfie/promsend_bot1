from telethon import TelegramClient, events
from telethon import errors

import asyncio

import python_socks

import logging

# from config import API_ID, API_HASH

client = TelegramClient('adam_promsend', 29587725, '32b25b1bc8c0d5ddf425850a19f9717e')
# proxy=(python_socks.ProxyType.SOCKS5, '95.217.226.237', 36612)

logging.basicConfig(level=logging.INFO, format='%(filename)s - [%(asctime)s] - %(levelname)s - %(name)s - %(message)s')

async def ad_sending(event):
    successful_count = 0
    unsuccessful_count = 0
    groups = client.iter_dialogs()
    async for group in groups:
        if group.is_group:
            try:
                await client.forward_messages(group, event.message)
                await client.send_message(906066950, f'Объявление отправлено в {group.title}')
                successful_count += 1
            except errors.RPCError as e:
                await client.send_message(906066950, f'Объявление не отправлено в {group.title}\n\n{e.message}')
                unsuccessful_count +=1
    await client.send_message(906066950, f'Объявления отправлены в {successful_count} чатов\n\nНе отправлены в {unsuccessful_count} чатов')

with client:
    client.add_event_handler(ad_sending, events.NewMessage(chats=(-1001777678253)))
    client.run_until_disconnected()