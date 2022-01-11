from pyrogram import filters

from Yukki import LOG_GROUP_ID, OWNER_ID, SUDOERS, app
from Yukki.Database import is_gbanned_user, is_on_off


@app.on_message(filters.private & ~filters.user(SUDOERS))
async def bot_forward(client, message):
    if await is_on_off(5):
        if message.text == "/start":
            return
        try:
            await app.forward_messages(
                chat_id=LOG_GROUP_ID,
                from_chat_id=message.from_user.id,
                message_ids=message.message_id,
            )
        except Exception as err:
            print(err)
            return
    else:
        return


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"{checking} 𝙞𝙨 𝙜𝙡𝙤𝙗𝙖𝙡𝙡𝙮 𝙗𝙖𝙣𝙣𝙚𝙙 𝙗𝙮 𝙎𝙪𝙙𝙤 𝙐𝙨𝙚𝙧𝙨 𝙖𝙣𝙙 𝙝𝙖𝙨 𝙗𝙚𝙚𝙣 𝙠𝙞𝙘𝙠𝙚𝙙 𝙤𝙪𝙩 𝙤𝙛 𝙩𝙝𝙚 𝙘𝙝𝙖𝙩..\n\n**𝙋𝙤𝙨𝙨𝙞𝙗𝙡𝙚 𝙧𝙚𝙖𝙨𝙤𝙣:** 𝙋𝙤𝙩𝙚𝙣𝙩𝙞𝙖𝙡 𝙎𝙥𝙖𝙢𝙢𝙚𝙧 𝙖𝙣𝙙 𝘼𝙗𝙪𝙨𝙚𝙧."
        )
