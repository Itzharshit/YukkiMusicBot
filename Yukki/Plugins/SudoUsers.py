import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_SESSION, OWNER_ID
from Yukki import BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo,
                            set_video_limit)

__MODULE__ = "SudoUsers"
__HELP__ = """


/sudolist 
    Check the sudo user list of Bot. 


**Note:**
Only for Sudo Users. 


/addsudo [Username or Reply to a user]
- To Add A User In Bot's Sudo Users.

/delsudo [Username or Reply to a user]
- To Remove A User from Bot's Sudo Users.

/restart 
- Restart Bot [All downloads, cache, raw files will be cleared too]. 

/maintenance [enable / disable]
- When enabled Bot goes under maintenance mode. No one can play Music now!

/logger [enable / disable]
- When enabled Bot logs the searched queries in logger group.

/clean
- Clean Temp Files and Logs.
"""
# Add Sudo Users!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "𝙍𝙚𝙥𝙡𝙮 𝙩𝙤 𝙖 𝙪𝙨𝙚𝙧𝙨 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙤𝙧 𝙜𝙞𝙫𝙚 𝙪𝙚𝙧𝙣𝙖𝙢𝙚 𝙤𝙧 𝙪𝙨𝙚𝙧 𝙄𝙙 𝙩𝙤 𝙥𝙚𝙧𝙛𝙤𝙧𝙢 𝙩𝙝𝙞𝙨 𝙖𝙘𝙩𝙞𝙤𝙣."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                f"{user.mention} 𝙄𝙨 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙖 𝙨𝙪𝙙𝙤 𝙪𝙨𝙚𝙧."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"𝘼𝙙𝙙𝙚𝙙 **{user.mention}** 𝙩𝙤 𝙨𝙪𝙙𝙤 𝙪𝙨𝙚𝙧𝙨."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} is already a sudo user."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"𝘼𝙙𝙙𝙚𝙙 **{message.reply_to_message.from_user.mention}** 𝙩𝙤 𝙨𝙪𝙙𝙤 𝙪𝙨𝙚𝙧𝙨"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("Failed")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "𝙍𝙚𝙥𝙡𝙮 𝙩𝙤 𝙖 𝙪𝙨𝙚𝙧𝙨 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙤𝙧 𝙜𝙞𝙫𝙚 𝙪𝙚𝙧𝙣𝙖𝙢𝙚 𝙤𝙧 𝙪𝙨𝙚𝙧 𝙄𝙙 𝙩𝙤 𝙥𝙚𝙧𝙛𝙤𝙧𝙢 𝙩𝙝𝙞𝙨 𝙖𝙘𝙩𝙞𝙤𝙣."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"Not a part of Bot's Sudo.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"𝙍𝙚𝙢𝙤𝙫𝙚𝙙 **{user.mention}** 𝙛𝙧𝙤𝙢 {MUSIC_BOT_NAME}'s 𝙎𝙪𝙙𝙤."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        await message.reply_text(f"𝙎𝙤𝙢𝙚𝙩𝙝𝙞𝙣𝙜 𝙬𝙧𝙤𝙣𝙜 𝙝𝙖𝙥𝙥𝙚𝙣𝙚𝙙.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"𝙉𝙤𝙩 𝙖 𝙥𝙖𝙧𝙩 𝙤𝙛 {MUSIC_BOT_NAME}'s 𝙎𝙪𝙙𝙤."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"𝙍𝙚𝙢𝙤𝙫𝙚𝙙 **{mention}** 𝙛𝙧𝙤𝙢 {MUSIC_BOT_NAME}'s 𝙎𝙪𝙙𝙤."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    await message.reply_text(f"𝙎𝙤𝙢𝙚𝙩𝙝𝙞𝙣𝙜 𝙬𝙧𝙤𝙣𝙜 𝙝𝙖𝙥𝙥𝙚𝙣𝙚𝙙.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "⭐️<u> **𝙊𝙬𝙣𝙚𝙧𝙨:**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **𝙎𝙪𝙙𝙤 𝙪𝙨𝙚𝙧𝙨:**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("No Sudo Users")
    else:
        await message.reply_text(text)


### Video Limit


@app.on_message(
    filters.command(["set_video_limit", f"set_video_limit@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
)
async def set_video_limit_kid(_, message: Message):
    if len(message.command) != 2:
        usage = "**𝙐𝙨𝙖𝙜𝙚:**\n/set_video_limit [𝙉𝙪𝙢𝙗𝙚𝙧 𝙤𝙛 𝙘𝙝𝙖𝙩𝙨 𝙖𝙡𝙡𝙤𝙬𝙚𝙙.]"
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    try:
        limit = int(state)
    except:
        return await message.reply_text(
            "Please Use Numeric Numbers for Setting Limit."
        )
    await set_video_limit(141414, limit)
    await message.reply_text(
        f"𝙑𝙞𝙙𝙚𝙤 𝙘𝙖𝙡𝙡 𝙢𝙖𝙭𝙞𝙢𝙞𝙢𝙪𝙢 𝙡𝙞𝙢𝙞𝙩𝙨 𝙙𝙚𝙛𝙞𝙣𝙚𝙙 𝙩𝙤 {limit} 𝘾𝙝𝙖𝙩𝙨."
    )


## Maintenance Yukki


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**Usage:**\n/maintenance [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("Enabled for Maintenance")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("Maintenance Mode Disabled")
    else:
        await message.reply_text(usage)


## Logger


@app.on_message(filters.command("logger") & filters.user(SUDOERS))
async def logger(_, message):
    if LOG_SESSION == "None":
        return await message.reply_text(
            "No Logger Account Defined.\n\nPlease Set <code>LOG_SESSION</code> var and then try loggging."
        )
    usage = "**Usage:**\n/logger [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 5
        await add_on(user_id)
        await message.reply_text("Enabled Logging")
    elif state == "disable":
        user_id = 5
        await add_off(user_id)
        await message.reply_text("Logging Disabled")
    else:
        await message.reply_text(usage)


## Gban Module


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**𝙐𝙨𝙖𝙜𝙚:**\n/gban [𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚 | 𝙐𝙨𝙚𝙧 𝙄𝘿]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "You want to gban yourself? How Fool!"
            )
        elif user.id == BOT_ID:
            await message.reply_text("Should i block myself? Lmao Ded!")
        elif user.id in SUDOERS:
            await message.reply_text("You want to block a sudo user? KIDXZ")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Initializing Gobal Ban on {user.mention}**\n\nExpected Time : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**New Global Ban on {MUSIC_BOT_NAME}**__

**Origin:** {message.chat.title} [`{message.chat.id}`]
**Sudo User:** {from_user.mention}
**Banned User:** {user.mention}
**Banned User ID:** `{user.id}`
**Chats:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("You want to block yourself? How Fool!")
    elif user_id == BOT_ID:
        await message.reply_text("Should i block myself? Lmao Ded!")
    elif user_id in sudoers:
        await message.reply_text("You want to block a sudo user? KIDXZ")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Already Gbanned.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Initializing Gobal Ban on {mention}**\n\nExpected Time : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**New Global Ban on {MUSIC_BOT_NAME}**__

**Origin:** {message.chat.title} [`{message.chat.id}`]
**Sudo User:** {from_user_mention}
**Banned User:** {mention}
**Banned User ID:** `{user_id}`
**Chats:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚:**\n/ungban [𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚 | 𝙐𝙨𝙚𝙧 𝙄𝘿]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("You want to unblock yourself?")
        elif user.id == BOT_ID:
            await message.reply_text("Should i unblock myself?")
        elif user.id in sudoers:
            await message.reply_text("Sudo users can't be blocked/unblocked.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("He's already free, why bully him?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Ungbanned!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("You want to unblock yourself?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Should i unblock myself? But i'm not blocked."
        )
    elif user_id in sudoers:
        await message.reply_text("Sudo users can't be blocked/unblocked.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("He's already free, why bully him?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Ungbanned!")


# Broadcast Message


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙚𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙞𝙣 {sent}  𝘾𝙝𝙖𝙩𝙨 𝙒𝙞𝙩𝙝 {pin} 𝙋𝙞𝙣𝙨.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**𝙐𝙨𝙖𝙜𝙚**:\n/broadcast [𝙈𝙚𝙨𝙨𝙖𝙜𝙚] 𝙊𝙧 [𝙍𝙚𝙥𝙡𝙮𝙏𝙤 𝘼 𝙈𝙚𝙨𝙨𝙖𝙜𝙚]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙚𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙞𝙣 {sent}  𝘾𝙝𝙖𝙩𝙨 𝙒𝙞𝙩𝙝 {pin} 𝙋𝙞𝙣𝙨.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙚𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙞𝙣 {sent}  𝘾𝙝𝙖𝙩𝙨 𝙒𝙞𝙩𝙝 {pin} 𝙋𝙞𝙣𝙨.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**𝙐𝙨𝙖𝙜𝙚**:\n/broadcast [𝙈𝙚𝙨𝙨𝙖𝙜𝙚] 𝙊𝙧 [𝙍𝙚𝙥𝙡𝙮𝙏𝙤 𝘼 𝙈𝙚𝙨𝙨𝙖𝙜𝙚]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Broadcasted Message In {sent} Chats and {pin} Pins.**"
    )


@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙚𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚𝙨 𝙞𝙣 {sent} 𝘾𝙝𝙖𝙩𝙨.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**𝙐𝙨𝙖𝙜𝙚**:\n/broadcast [𝙈𝙚𝙨𝙨𝙖𝙜𝙚] 𝙤𝙧 [𝙍𝙚𝙥𝙡𝙮 𝙩𝙤 𝙖 𝙢𝙚𝙨𝙨𝙖𝙜𝙚]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙚𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚𝙨 𝙞𝙣 {sent} 𝘾𝙝𝙖𝙩𝙨.")


# Clean


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("Successfully cleaned all **temp** dir(s)!")
