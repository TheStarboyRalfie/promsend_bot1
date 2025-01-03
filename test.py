from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest

import asyncio

from config import API_ID, API_HASH

client = TelegramClient('ralfiee', API_ID, API_HASH)

async def main():
    await client(ImportChatInviteRequest('Helix_shop_Chat0'))

with client:
    client.loop.run_until_complete(main())
