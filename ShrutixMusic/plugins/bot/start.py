import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from py_yt import VideosSearch

import config
from ShrutixMusic import app
from ShrutixMusic.misc import _boot_
from ShrutixMusic.plugins.sudo.sudoers import sudoers_list
from ShrutixMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutixMusic.utils.decorators.language import LanguageStart
from ShrutixMusic.utils.formatters import get_readable_time
from ShrutixMusic.utils.inline import (
    help_pannel,
    private_panel,
    start_panel,
)
from config import BANNED_USERS, SHASHANK_PIC
from strings import get_string


# ==========================================================
# FIXED START IMAGE
# ==========================================================

if isinstance(SHASHANK_PIC, (list, tuple)):
    START_IMAGE = SHASHANK_PIC[0]
else:
    START_IMAGE = SHASHANK_PIC


# ==========================================================
# TELEGRAM MESSAGE EFFECTS
# PRIVATE/PERSONAL CHAT ONLY
# ==========================================================

EFFECT_IDS = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]


# ==========================================================
# PRIVATE START
# ==========================================================

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    if len(message.text.split()) > 1:

        name = message.text.split(None, 1)[1]

        # ==================================================
        # HELP
        # ==================================================

        if name[0:4] == "help":
            keyboard = help_pannel(_)

            return await message.reply_photo(
                photo=START_IMAGE,
                has_spoiler=True,
                message_effect_id=random.choice(EFFECT_IDS),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        # ==================================================
        # SUDO
        # ==================================================

        if name[0:3] == "sud":
            await sudoers_list(
                client=client,
                message=message,
                _=_,
            )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"✦ {message.from_user.mention} "
                        f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                        f"<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> "
                        f"<code>{message.from_user.id}</code>\n"
                        f"<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                        f"@{message.from_user.username}"
                    ),
                )

            return

        # ==================================================
        # TRACK INFO
        # ==================================================

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")

            query = str(name).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"

            results = VideosSearch(query, limit=1)
            result_data = await results.next()

            if not result_data.get("result"):
                await m.edit_text("❌ Track information not found.")
                return

            for result in result_data["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title,
                duration,
                views,
                published,
                channellink,
                channel,
                app.mention,
            )

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=_["S_B_8"],
                            url=link,
                        ),
                        InlineKeyboardButton(
                            text=_["S_B_9"],
                            url=config.SUPPORT_CHAT,
                        ),
                    ],
                ]
            )

            await m.delete()

            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                has_spoiler=True,
                message_effect_id=random.choice(EFFECT_IDS),
                caption=searched_text,
                reply_markup=key,
            )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"✦ {message.from_user.mention} "
                        f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                        f"✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> "
                        f"<code>{message.from_user.id}</code>\n"
                        f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                        f"@{message.from_user.username}"
                    ),
                )

    # ======================================================
    # NORMAL PRIVATE START
    # ======================================================

    else:
        out = private_panel(_)

        await message.reply_photo(
            photo=START_IMAGE,
            has_spoiler=True,
            message_effect_id=random.choice(EFFECT_IDS),
            caption=_["start_2"].format(
                message.from_user.mention,
                app.mention,
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )

        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"✦ {message.from_user.mention} "
                    f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                    f"✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> "
                    f"<code>{message.from_user.id}</code>\n"
                    f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                    f"@{message.from_user.username}"
                ),
            )


# ==========================================================
# GROUP START
# NO EFFECT HERE
# ==========================================================

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        photo=START_IMAGE,
        has_spoiler=True,
        caption=_["start_1"].format(
            app.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(message.chat.id)


# ==========================================================
# BOT ADDED TO NEW GROUP
# NO EFFECT HERE
# ==========================================================

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            # ==============================================
            # BANNED USER CHECK
            # ==============================================

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

            # ==============================================
            # BOT ADDED
            # ==============================================

            if member.id == app.id:

                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                # ==========================================
                # WELCOME MESSAGE
                # NO EFFECT HERE
                # ==========================================

                out = start_panel(_)

                await message.reply_photo(
                    photo=START_IMAGE,
                    has_spoiler=True,
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )

                await add_served_chat(message.chat.id)

                await message.stop_propagation()

        except Exception as ex:
            print(f"Welcome Error: {ex}")
