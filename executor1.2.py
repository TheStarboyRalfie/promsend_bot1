from telethon import TelegramClient, events
import asyncio

import logging

from config import API_ID, API_HASH

client = TelegramClient('adam_promsend', API_ID, API_HASH)
client2 = TelegramClient('eva_promsend', API_ID, API_HASH)

logging.basicConfig(level=logging.INFO, format='%(filename)s - [%(asctime)s] - %(levelname)s - %(name)s - %(message)s')

async def ad_sending(event):
    with open('/promsend_bot/groups.txt', 'r') as groups_file:
        group_links = groups_file.readlines()
        for group_link in group_links:
            await client.forward_messages(group_link, event.message)

async def runn(client):
    async with client:
        client.add_event_handler(ad_sending, events.NewMessage(chats=(-1001777678253)))
        client.run_until_disconnected()

async def main():
    await asyncio.gather(runn(client), runn(client2))

asyncio.run(main())