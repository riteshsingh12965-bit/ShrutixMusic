from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaVideo,
)

import config
from ShrutixMusic import app


# =========================
# START BUTTONS
# =========================

def start_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT,
            ),
        ]
    ]


def private_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_9"],
                url=config.SUPPORT_CHAT,
            ),
            InlineKeyboardButton(
                text=_["S_B_10"],
                url=config.SUPPORT_CHANNEL,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_7"],
                callback_data="gib_source",
            ),
            InlineKeyboardButton(
                text=_["S_B_5"],
                user_id=config.OWNER_ID,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="settings_back_helper",
            )
        ],
    ]


# =========================
# SOURCE CODE VIDEO
# =========================

@app.on_callback_query(filters.regex("^gib_source$"))
async def gib_repo_callback(_, callback_query):

    await callback_query.answer()

    await callback_query.edit_message_media(
        media=InputMediaVideo(
            "https://telegra.ph/file/b1367262cdfbcd0b2af07.mp4",
            has_spoiler=True,
            caption=(
                "<b>✦ 🌚 ʟᴜɴᴅ ʟᴇʟᴇ ᴍᴇʀᴀ ʀᴇᴘᴏ ᴋʏᴀ ᴋᴀʀᴇɢᴀ, ʟᴇɢᴀ ᴋʏᴀ ʙʜᴏsᴀᴅɪᴋᴇ..!!</b>"
            ),
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• ʙᴀᴄᴋ •",
                        callback_data="settings_back_helper",
                    ),
                    InlineKeyboardButton(
                        text="• ᴄʟᴏsᴇ •",
                        callback_data="close",
                    ),
                ]
            ]
        ),
    )
