# (c) AlenPaulVarghese
# -*- coding: utf-8 -*-

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from webshotbot import WebshotBot
from pyrogram import filters
from config import Config
import os

START_TEXT = """
<i>👋 Hᴇʏ,</i>{message.from_user.first_name}\n
<i>I'm Telegram Web Screenshot Bot</i>\n
<i>Cʟɪᴄᴋ ᴏɴ /help ᴛᴏ ɢᴇᴛ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</i>\n
<i><b>☘️ Bᴏᴛ Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ :</b>@FZBOTS</i>"""

HELP_TEXT = """
<i>- Send the link of the website you want to render, choose the desired setting, and click start render.</i>\n
<i>- This bot uses an actual browser under the hood to render websites.</i>"""

ABOUT_TEXT = """
<b>⚜ Mʏ ɴᴀᴍᴇ : Web Screenshot Bot</b>\n
<b>🔸Vᴇʀꜱɪᴏɴ : <a href='https://telegram.me/FZBOTS'>3.0.1</a></b>\n
<b>🔸GitHub : <a href='https://GitHub.com/Monster-ZeroX'>Fᴏʟʟᴏᴡ</a></b>\n
<b>🔹Dᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://telegram.me/Monster_ZeroX'>☠️👽Moͦns͛ᴛⷮeͤrͬ Zeͤrͬoͦ👽☠️</a></b>\n
<b>🔸Lᴀꜱᴛ ᴜᴘᴅᴀᴛᴇᴅ : <a href='https://telegram.me/FZBOTS'>[ 11-ᴊᴜʟʏ-21 ] 04:35 PM</a></b>"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url="t.me/FZBOTS"),
        InlineKeyboardButton('Group', url="t.me/FZBOTSSUPPORT"),
        InlineKeyboardButton('Status', url="t.me/FZBOTS/61")
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url="t.me/FZBOTS"),
        InlineKeyboardButton('Group', url="t.me/FZBOTSSUPPORT"),
        InlineKeyboardButton('Status', url="t.me/FZBOTS/61")
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url="t.me/FZBOTS"),
        InlineKeyboardButton('Group', url="t.me/FZBOTSSUPPORT"),
        InlineKeyboardButton('Status', url="t.me/FZBOTS/61")
        ]]
    )

@WebshotBot.on_message(
    filters.regex(pattern="http[s]*://.+") & filters.private & ~filters.edited
)
async def checker(client: WebshotBot, message: Message):
    msg = await message.reply_text("working", True)
    markup = []
    _settings = client.get_settings_cache(message.chat.id)
    if _settings is None:
        _settings = dict(
            type="pdf",
            fullpage=True,
            scroll_control="no",
            resolution="800x600",
            split=False,
        )
    markup.extend(
        [
            [
                InlineKeyboardButton(
                    text=f"Format - {_settings['type'].upper()}",
                    callback_data="format",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Page - {'Full' if _settings['fullpage'] else 'Partial'}",
                    callback_data="page",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Scroll Site - {_settings['scroll_control'].title()}",
                    callback_data="scroll",
                )
            ],
        ]
    )
    _split = _settings["split"]
    _resolution = _settings["resolution"]
    if _split or "600" not in _resolution:
        markup.extend(
            [
                [
                    InlineKeyboardButton(
                        text="hide additional options ˄", callback_data="options"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"resolution | {_resolution}", callback_data="res"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=f"Split - {'Yes' if _split else 'No'}",
                        callback_data="splits",
                    )
                ]
                if _settings["type"] != "pdf"
                else [],
                [
                    InlineKeyboardButton(
                        text="▫️ site statitics ▫️", callback_data="statics"
                    )
                ],
            ]
        )
    else:
        markup.append(
            [
                InlineKeyboardButton(
                    text="show additional options ˅", callback_data="options"
                )
            ]
        )
    markup.extend(
        [
            [InlineKeyboardButton(text="▫️ start render ▫️", callback_data="render")],
            [InlineKeyboardButton(text="cancel", callback_data="cancel")],
        ]
    )
    await msg.edit(
        text="Choose the prefered settings",
        reply_markup=InlineKeyboardMarkup(markup),
    )


@WebshotBot.on_message(filters.command(["start"]))
async def start(_, message: Message) -> None:
       await message.reply_text(
            text=START_TEXT,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )


@WebshotBot.on_message(filters.command(["about"]))
async def feedback(_, message: Message) -> None:
    await message.reply_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )


@WebshotBot.on_message(
    filters.command(["about", "feedback", "help"]) & filters.private
)
async def help_handler(_, message: Message) -> None:
    if Config.SUPPORT_GROUP_LINK is not None:
        await message.reply_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )

@WebshotBot.on_message(filters.command(["debug", "log"]) & filters.private)
async def send_log(_, message: Message) -> None:
    try:
        sudo_user = int(os.environ["SUDO_USER"])
        if sudo_user != message.chat.id:
            raise Exception
    except Exception:
        return
    if os.path.exists("debug.log"):
        await message.reply_document("debug.log")
    else:
        await message.reply_text("file not found")
