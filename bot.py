# (©) AswanthVK 

import os
import asyncio
import requests
import math
import time
from pyrogram import Client, filters
from helper_funcs.helpers import humanbytes, convert


TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

APP_ID = int(os.environ.get("APP_ID", ""))

API_HASH = os.environ.get("API_HASH", "")


app = Client("mdisk", bot_token=TG_BOT_TOKEN, api_hash=API_HASH, api_id=APP_ID)


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋\n\nSend me MDisk links to convert to Direct Download Link", reply_to_message_id=message.message_id)


@app.on_message(filters.private & filters.text)
async def link_extract(bot, message):
    urls = message.text
    
    if not message.text.startswith("https://mdisk.me"):
        await message.reply_text(
            f"**INVALID LINK**",
            reply_to_message_id=message.message_id
        )
        return
    a = await bot.send_message(
            chat_id=message.chat.id,
            text=f"Processing…",
            reply_to_message_id=message.message_id
        )
    inp = urls #input('Enter the Link: ')
    fxl = inp.split("/")
    cid = fxl[-1]
    URL=f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://mdisk.me/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    resp = requests.get(url=URL, headers=header).json()
    fn = resp['filename']
    dn = resp['display_name']
    dr = resp['duration']
    sz = resp['size']
    ht = resp['height']
    wt = resp['width']
    download = resp['download']
    
    await a.edit_text("**Title:** {}\n**Size:** {}\n**Duration:** {}\n**Resolution:** {}*{}\n**Uploader:** {}\n\n**Download Now:** {}".format(fn, humanbytes(sz), convert(dr), wt, ht, dn, download), disable_web_page_preview=True)
    


app.run()
