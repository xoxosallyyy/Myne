import os
import asyncio
import psutil
from telegraph.aio import Telegraph
from pyrogram import filters
from Rose import dbn,app
from config import Config
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes
from Rose.mongo.rulesdb import Rules
from Rose.mongo.usersdb import get_served_users,gets_served_users,remove_served_user
from Rose.mongo.chatsdb import get_served_chats
from pyrogram import __version__ as pyrover
from pyrogram.errors import InputUserDeactivated,FloodWait, UserIsBlocked, PeerIdInvalid


@app.on_message(filters.command("stats"))
async def gstats(_, message):
    response = await message.reply_text(text="Getting Stats!"
    )
    notesdb = Notes()
    rulesdb = Rules
    fldb = Filters()
    served_chats = len(await get_served_chats())
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))   
    serve_users = len(await gets_served_users())
    serve_users = []
    user = await gets_served_users()
    for use in user:
        serve_users.append(int(use["bots_users"]))  
    ram = (str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB")
    supun = dbn.command("dbstats")
    datasiz = supun["dataSize"] / 1024
    datasiz = str(datasiz)
    storag = supun["storageSize"] / 1024
    smex = f"""
** General Stats of Rose Bot**

• **Ram:** `{ram}`
• **Pyrogram Version:** `{pyrover}`
• **DB Size:** `{datasiz[:6]} Mb`
• **Storage:** `{storag} Mb`
• **Total Chats:** `{len(served_chats)}`
• **Bot PM Users:** `{len(served_users)}`
• **Filter Count** : `{(fldb.count_filters_all())}`  **In**  `{(fldb.count_filters_chats())}`  **chats**
• **Notes Count** : `{(notesdb.count_all_notes())}`  **In**  `{(notesdb.count_notes_chats())}`  **chats**
• **Rules:** `{(rulesdb.count_chats_with_rules())}` 
• **Total Users I see:**`{len(serve_users)}`
• **Total languages** : `10`

"""
    await response.edit_text(smex)
    return


async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await remove_served_user(user_id)
        return False, "Deleted"
    except UserIsBlocked:
        await remove_served_user(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_user(user_id)
        return False, "Error"
    except Exception as e:
        return False, "Error"

@app.on_message(filters.private & filters.command("bcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message
    served_users = []
    users = await get_served_users() 
    for user in users: 
        served_users.append(int(user["bot_users"]))   
    count = len(served_users)
    chats = await get_served_users() 
    m = await message.reply_text(f"<strong>Broadcast in progress for</strong><code>{str(len(served_users))}</code><b>User</b>")
    success = 0
    failed = 0
    deleted = 0
    blocked = 0
    done = 0
    Invalid = 0
    for chat in chats:
        try:
            error, suc = await broadcast_messages(int(chat['bot_users']), b_msg)
            if suc:
                success += 1
            elif suc == False:
                if error == "Blocked":
                    blocked+=1
                elif error == "Deleted":
                    deleted += 1
                elif error == "Error":
                    failed += 1
                elif error == "Invalid":
                    Invalid += 1
            done += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass  
    telegraph = Telegraph()
    await telegraph.create_account(short_name=f'{success}')
    response = await telegraph.create_page(
        f'Broadcast Message Successfully {success}',
        html_content=f"""
<b>📮 Broadcast Message Successfully</b><br><br>
📥 Chats Left : <b>{done}/{count}</b><br>
✅ Success : <b>{success}</b><br>
❌ Error : <b>{failed}</b><br><br>
🤦‍♂️ Blocked Users : <b>{blocked}</b><br>
💔 Deactivated users: <b>{deleted}</b><br>
🤷‍♂️ Chat NotFound : <b>{Invalid}</b><br>
😶 Unknown Error : <b>{failed}</b><br><br>
🤝 Thank you very much for advertising with us ! <b>if you satisfied with our advertising please be kind to review us </b>💫 If you give us a good review, we will surely broadcast your post in our group for free 😍<br><br>
--------------------------------------------<br>
🤗 Have a Nice Day !!!
""",)
    link = response['url']
    await m.edit(f"""
<b>🔰 Broadcast Message Done🚀</b>

📥 Chats Left : <b>{done}/{count}</b>
✅ Success : <b>{success}</b>
❌ Error : <b>{failed}</b>

🤦‍♂️ Blocked Users : <b>{blocked}</b>
💔 Deactivated users: <b>{deleted}</b>
🤷‍♂️ Chat NotFound : <b>{Invalid}</b>

😶 Unknown Error : <b>{failed}</b>

🗂 Result Here :`{link}` """) 
