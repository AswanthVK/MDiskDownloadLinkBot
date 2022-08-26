import os
import re
import string
import asyncio
import cloudscraper
import requests
import math
import time
from pyrogram import Client, filters


TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")


app = Client("tgid", bot_token=TG_BOT_TOKEN, api_hash=API_HASH, api_id=API_ID)


def mdisk(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "mdisk", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋\n\n Send me MDisk links to convert to Direct Download Link", reply_to_message_id=message.message_id)


@app.on_message(filters.private & filters.text)
async def link_extract(bot, message):
    url = message.text

    if not message.text.startswith("https://mdisk"):
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
    
    mdisk(url)
    mdisk_url = mdisk(url=url)
    
    r = requests.head(mdisk_url)
    fname = None
    if "Content-Disposition" in r.headers.keys():
        fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
        file_ext_f_name = os.path.splitext(str(fname).replace('"', ""))[1]
    file_size = int(requests.head(mdisk_url).headers['Content-Length'])
    await a.edit_text("Title: {}\nSize: {}\n\nDL URL: {}".format(fname, humanbytes(file_size), mdisk_url))
    print(mdisk(url=url))
    


app.run()
