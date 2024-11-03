import aiohttp
import asyncio
import json
import re
from datetime import datetime, timedelta

from collections import defaultdict
from aiogram import Router, types, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from logging.handlers import RotatingFileHandler

from config import TOKEN
from moralis_api import get_token_price
from birdeye_api import fetch_ohlcv_data


router = Router()
bot = Bot(token=TOKEN)

CHAT_ID = None
FRESH_TOKENS = defaultdict(lambda: {"hits": 0, "70%": False, "80%": False, "90%": False, "time": datetime.now()})
is_checking = False  # Flag for tracking if checking is running


def create_link_buttons(mint: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    trojan = InlineKeyboardButton(
        text=f"Trojan",
        url=f"https://t.me/achilles_trojanbot?start=r-bankx0-{mint}"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[trojan]])

    return keyboard


@router.message()
async def handle_text_messages(message: Message):
    global CHAT_ID
    global is_checking

    CHAT_ID = message.chat.id

    if message.text:

        mint_address = message.text 

        if mint_address:
            FRESH_TOKENS[mint_address]["hits"] += 1
            FRESH_TOKENS[mint_address]["time"] = datetime.now()
            await message.reply( 
                                f"🎯 Hits: {FRESH_TOKENS[mint_address]['hits']}\n\n"
                                f"Added: {mint_address}"
            )
        else:
            await message.reply("Token Address not found in the provided text.")
    else:
        await message.reply("Пожалуйста, укажите минт адрес после команды.")

    if not is_checking:
        for token in FRESH_TOKENS:
            if FRESH_TOKENS[token]["hits"] == 1:
                print("started checking...")
                is_checking = True
                asyncio.create_task(check_diff())
                break 

async def check_diff():
    global CHAT_ID
    global is_checking

    try:
        while True:

            for mint in list(FRESH_TOKENS.keys()):
                time_diff = datetime.now() - FRESH_TOKENS[mint]["time"]
                if time_diff >= timedelta(minutes=15):
                    del FRESH_TOKENS[mint]
                    continue
                else:
                    print(f"timediff = {time_diff}")

                if FRESH_TOKENS[mint]["hits"]:
                    ath = fetch_ohlcv_data(mint)
                    if ath is None or ath == 0: 
                        continue

                    current_price = get_token_price(mint)
                    if current_price is None or current_price == 0:  
                        continue

                    diff = round(100 - (current_price / ath) * 100, 2)

                    gmgn_link = f"https://gmgn.ai/sol/token/{mint}"
                    photon_link = f"https://photon-sol.tinyastro.io/en/lp/{mint}"
                    bullx_link = f"https://bullx.io/terminal?chainId=1399811149&address={mint}"
                    dexscreener = f"https://dexscreener.com/solana/{mint}"

                    if diff >= 90:
                        FRESH_TOKENS[mint]["90%"] = True
                        del FRESH_TOKENS[mint] 
                        thread_id = 11
                    elif diff >= 80 and FRESH_TOKENS[mint]["80%"] == False:
                        FRESH_TOKENS[mint]["80%"] = True
                        thread_id = 7
                    elif diff >= 70 and FRESH_TOKENS[mint]["70%"] == False:
                        FRESH_TOKENS[mint]["70%"] = True
                        thread_id = 2
                    # else:
                    #     #thread_id = 19

                    text = (
                        f"🚨 <strong>-{diff}% from ATH</strong>\n\n"
                        f"Now: {current_price} | ATH: {ath}\n\n"
                        f"CA: <code> {mint} </code>\n\n"
                        f"<a href='{photon_link}'>Photon</a> | <a href='{gmgn_link}'>GmGn</a> |<a href='{bullx_link}'>BullX</a> | <a href='{dexscreener}'>DexScreener</a>"
                    )

                    if text:
                        await bot.send_message(
                            CHAT_ID,
                            message_thread_id=thread_id,
                            text=text,
                            parse_mode="HTML",
                            reply_markup=create_link_buttons(mint)
                        )
                    

                    await asyncio.sleep(5)

            if len(FRESH_TOKENS) > 0:
                await asyncio.sleep(60 // len(FRESH_TOKENS))
            else:
                await asyncio.sleep(60)

    finally:
        is_checking = False  



@router.message(Command("aloha"))
async def function_name(message: Message, command: CommandObject):
    global CHAT_ID
    global is_checking

    CHAT_ID = message.chat.id

    if message.text:
        # Assuming message.text contains the full text you've provided
        full_text = message.text  # Get the full command text
        
        # Use regex to extract the Token Address
        match = re.search(r'\*Token Address:\* (.+)', full_text)
        if match:
            token_address = match.group(1).strip()  # Extract the address and remove any extra spaces
            await message.reply(f"Token Address: {token_address}")
        else:
            await message.reply("Token Address not found in the provided text.")
    else:
        await message.reply("Пожалуйста, укажите минт адрес после команды.")
        