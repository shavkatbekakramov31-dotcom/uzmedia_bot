import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 1. SOZLAMALAR
TOKEN = "8534298068:AAE-uwZYioJz0mGvdkdf1vhOB9ifCO-CJzM"
KANAL_ID = "@Showmedia123" 
KANAL_URL = "https://t.me/Showmedia123"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Filmlar bazasi
FILMLAR = {"1": "https://t.me/showmedia123/3"
    "101" "🎬 'Qasoskorlar' filmi manzili: https://t.me/Showmedia123/1",
    "102": "🎬 'Avatar 2' filmi manzili: https://t.me/Showmedia123/2",
    "777": "🎬 'Mahluq 1-qism' filmi manzili: https://t.me/Showmedia123/3",
    "2":   'https://t.me/showmedia123/7'
}

# Kanalga a'zolikni tekshirish funksiyasi
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=KANAL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        print(f"Tekshirishda xatolik: {e}")
        return False

# /start buyrug'i
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    is_sub = await check_sub(message.from_user.id)
    
    if is_sub:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n"
                             f"Kino kodini yuboring.")
    else:
        btn = [[InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=KANAL_URL)]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=btn)
        await message.answer("⚠️ Botdan foydalanish uchun kanalimizga a'zo bo'ling!", reply_markup=keyboard)

# Kino kodini tekshirish
@dp.message(F.text)
async def send_movie(message: types.Message):
    is_sub = await check_sub(message.from_user.id)
    
    if not is_sub:
        btn = [[InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=KANAL_URL)]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=btn)
        return await message.answer("❌ Kino ko'rish uchun avval kanalga a'zo bo'ling!", reply_markup=keyboard)

    kod = message.text
    if kod in FILMLAR:
        await message.answer(FILMLAR[kod])
    else:
        await message.answer("😔 Kechirasiz, bunday kodli film bazada yo'q.")

# Botni ishga tushirish funksiyasi
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

# BU QISMDA XATO BOR EDI, MANA TO'G'RI VARIANTI:
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")
