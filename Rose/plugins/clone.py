from Rose import app
import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import *
from config import API_ID, API_HASH


@app.on_message(filters.private & filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone token")
    cmd = msg.forward
    phone = msg.text.split(" ", maxsplit=2)[1]
    try:
        await text.edit("ᴄʟᴏɴɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ᴏɴ ᴍʏ sᴇʀᴠᴇʀ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴄʟᴏɴɪɴɢ...")
                   # change this Directry according to ur repo
        client = Client(":memory:", API_ID, API_HASH, bot_token=phone, plugins={"root": "Rose"})
        await client.start()
        user = await client.get_me()
        await msg.reply(f"ʏᴏᴜʀ ᴄʟɪᴇɴᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ ᴀs @{user.username}! ✅\n\nᴛʜᴀɴᴋs ғᴏʀ ᴄʟᴏɴɪɴɢ.")
    except Exception as e:
        await msg.reply(f"**ᴇʀʀᴏʀ:** `{str(e)}`\nPress /start to Start again.")

__MODULE__ = "Clone"
__HELP__ = """  
🤖 ʙᴏᴛ ᴄʀᴇᴀᴛɪᴏɴ.
 ├ ɢᴏ ᴛᴏ @BotFather.
 ├ sᴛᴀʀᴛ ɪᴛ ᴀɴᴅ ᴛʏᴘᴇ /newbot
 ├ ᴄʜᴏᴏsᴇ ɴᴀᴍᴇ ᴏғ ʙᴏᴛ.
 ├ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴜsᴇʀɴᴀᴍᴇ ᴏғ ᴛʜᴇ ʙᴏᴛ. 
 ├ ᴄᴏᴘʏ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴅᴏɴ'ᴛ ғᴏʀᴡᴀʀᴅ.
 └ ɢᴏ ᴛᴏ @szrosebot ᴀɴᴅ sᴇɴᴅ (`Ex: /clone bot token here`) 
"""
