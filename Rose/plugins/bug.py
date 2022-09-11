from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import OWNER_ID
from config import OWNER_USERNAME as uWu
from Rose import SUPPORT_CHAT, app
from Rose.core.decorators.errors import capture_err
from button import Bug_Report

def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@app.on_message(filters.command("bug"))
@capture_err
async def bug(_, msg: Message):
    if msg.chat.username:
        chat_username = f"@{msg.chat.username}/`{msg.chat.id}`"
    else:
        chat_username = f"Private Group/`{msg.chat.id}`"

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = (
        "[" + msg.from_user.first_name + "](tg://user?id=" + str(msg.from_user.id) + ")"
    )
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    bug_report = f"""
**#Reported Bug :** @{uWu}

**Bug Reported By :** {mention}
**User Id :** {user_id}
**Bug Reported Chat : @{SUPPORT_CHAT}

**Bug :** {bugs}

**Bug Reported Time :** {datetimes}"""

    if msg.chat.type == "private":
        await msg.reply_text("<b>🔗This Command only preferred to Groups!</b>")
        return

    if user_id == OWNER_ID:
        if bugs:
            await msg.reply_text(
                "<b>Your making a comedy Your the Owner Of Me 😅</b>",
            )
            return
        else:
            await msg.reply_text("Owner!")
    elif user_id != OWNER_ID:
        if bugs:
            await msg.reply_text(
                f"<b>Bug Report : {bugs}</b>\n\n"
                f"<b>Your Bug successfully Report to @{SUPPORT_CHAT} Chat\n\n😘 Thank you For Bug Report</b>"
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Close", callback_data=f"close_reply")]]
                ),
            )
            await app.send_photo(
                SUPPORT_CHAT,
                photo=BUG_IMG,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("View Reported Bug 🐞", url=f"{msg.link}")],
                        [
                            InlineKeyboardButton(
                                "Close", callback_data="close_send_photo"
                            )
                        ],
                    ]
                ),
            )
        else:
            await msg.reply_text(
                f"<b>No Bug to Report</b>",
            )


@app.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    if CallbackQuery.from_user.id != OWNER_ID:
        return await CallbackQuery.answer(
            "You Don't have perform This Action", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()


__MODULE__ = Bug_Report
__HELP__ = """
**BUG REPORT**
Any type of **Bug** you will find on this Bot just Report To us\nUsing /bug command\nEx: `/bug call back problem`

Made By: [SzRoseTeam](https://t.me/szrosesupport) 
"""
