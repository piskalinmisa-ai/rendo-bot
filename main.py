import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Rendo Bot is Alive!"

def run_web():
    # Render передает порт в переменные окружения
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- BOT LOGIC ---
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Теперь я работаю на Render без перебоев! 🚀")

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# --- MAIN RUNNER ---
async def main():
    # Запускаем веб-сервер в фоне, чтобы Render не ругался на порты
    Thread(target=run_web, daemon=True).start()
    
    print("Бот запускается...")
    # Запускаем опрос Telegram
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
