import os
import time
from telethon import TelegramClient, events
from pyppeteer import launch
from settings import API_ID, API_HASH, BOT_TOKEN
from utils import fetch_urls
import logging

logging.basicConfig(level=logging.INFO)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hi! I am alive. \
        Send me any link, I will send you the screenshot of that page.')
    raise events.StopPropagation


@bot.on(events.NewMessage)
async def echo(event):
    browser = await launch()
    page = await browser.newPage()

    try:
        urls = fetch_urls(event.text)
        for url in urls:
            logging.info(url)
            await page.goto(url)

            file_name = f'{time.time()}.png'
            await page.screenshot(path=file_name,fullPage=False)
            await event.reply(event.text,file=file_name)
            os.remove(file_name)

    except Exception as err:
        await event.reply(event.text)
        await event.respond(str(err)[:2000])
        logging.exception(err)
        return
    await browser.close()





if __name__ == '__main__':
    bot.run_until_disconnected()
