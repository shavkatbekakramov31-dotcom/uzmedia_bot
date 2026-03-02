import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

# ================== SOZLAMALAR ==================
# Yangi tokenni joylashtirdim
TOKEN = "8534298068:AAGyjMyx3z0jEYkOS4VqWXsTQN--tgTkJWE"
KANAL_ID = "@Showmedia123"
KANAL_URL = "https://t.me/Showmedia123"

# Bot obyektini yaratishda to'g'ri formatdan foydalanamiz
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== DATABASE ==================
db = sqlite3.connect("users.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")
db.commit()

# ================== FILMLAR ==================
FILMLAR = {
    "101": "🎬 Qasoskorlar: https://t.me/Showmedia123/1",
    "102": "🎬 Avatar 2: https://t.me/Showmedia123/2",
    "777": "🎬 Mahluq 1-qism: https://t.me/Showmedia123/3"
}

# ================== OBUNA TEKSHIRISH ==================
async def check_sub(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=KANAL_ID, user_id=user_id)
        # Member, administrator yoki creator bo'lsa True qaytaradi
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        return False

# ================== START ==================
@dp.message(CommandStart())
async def start_cmd(message: Message):
    user_id = message.from_user.id

    # Avval bazada borligini tekshiramiz
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    is_sub = await check_sub(user_id)

    if not is_sub:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url=KANAL_URL)],
                [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
            ]
        )
        return await message.answer("Botdan foydalanish uchun kanalga a'zo bo'ling!", reply_markup=keyboard)

    # Agar obuna bo'lgan bo'lsa va bazada yo'q bo'lsa, qo'shamiz
    if not user:
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        db.commit()

    await message.answer(
        f"👋 Assalomu alaykum, {message.from_user.full_name}!\n\n"
        "🎬 Kino ko'rish uchun kod yuboring.",
        parse_mode=ParseMode.HTML
    )

# ================== TEKSHIRISH TUGMASI ==================
@dp.callback_query(F.data == "check_sub")
async def recheck_sub(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_sub = await check_sub(user_id)

    if is_sub:
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        db.commit()

        await callback.message.edit_text(
            "✅ Obuna tasdiqlandi!\n\n🎬 Endi kino kodini yuboring."
        )
    else:
        await callback.answer("❌ Hali ham obuna emassiz!", show_alert=True)

# ================== KINO KODI ==================
@dp.message(F.text)
async def send_movie(message: Message):
    user_id = message.from_user.id
    
    # Bazadan foydalanuvchini tekshirish
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        # Foydalanuvchi bazada bo'lmasa, uni qo'shib qo'yamiz
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        db.commit() # Bu yerda db_connection o'rniga o'z ulanishingiz nomini yozing

    kod = message.text.strip()

    if kod in FILMLAR:
        await message.answer(FILMLAR[kod])
    else:
        await message.answer("❌ Bunday kod topilmadi.")
# ================== MAIN ==================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
