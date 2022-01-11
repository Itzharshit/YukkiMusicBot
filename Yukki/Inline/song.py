from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)


def song_markup(videoid, duration, user_id, query, query_type):
    buttons = [
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"song_right B|{query_type}|{query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❰𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙❱",
                callback_data=f"qwertyuiopasdfghjkl {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"song_right F|{query_type}|{query}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❰🗑 𝘾𝙡𝙤𝙨𝙚 𝙎𝙚𝙖𝙧𝙘𝙝❱",
                callback_data=f"forceclose {query}|{user_id}",
            )
        ],
    ]
    return buttons


def song_download_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="❰⬇️ 𝙂𝙚𝙩 𝘼𝙪𝙙𝙞𝙤❱",
                callback_data=f"gets audio|{videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❰⬇️ 𝙂𝙚𝙩 𝙑𝙞𝙙𝙚𝙤❱",
                callback_data=f"gets video|{videoid}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❰🗑 𝘾𝙡𝙤𝙨𝙚 𝙈𝙚𝙣𝙪❱",
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]
    return buttons
