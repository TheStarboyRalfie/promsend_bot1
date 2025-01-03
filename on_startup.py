import asyncio
from aiogram import Bot

from datetime import datetime

from db.commands import get_all_ads, stop_distributing

async def on_startup(bot: Bot):
    while True:
        ads = await get_all_ads()
        for ad in ads:
            if not datetime.now() > ad['tariff_ends'] and not ad['is_distr'] == False and not ad['ad_text'] == 'no_text':
                if ad['ad_photo'] == 'no_photo':
                    await bot.send_message('-1001777678253', ad['ad_text'])
                else:
                    await bot.send_photo('-1001777678253', photo=ad['ad_photo'], caption=ad['ad_text'])
            elif datetime.now() > ad['tariff_ends'] and ad['is_warned'] == False:
                await stop_distributing(ad['user_id'], bot)
        await asyncio.sleep(3600)