import os
import asyncio
from aiogram import Bot, Dispatcher, types
from threading import Thread
from flask import Flask

# --- БЛОК ДЛЯ RENDER (WEB SERVER) ---
# Это заставит Render думать, что мы - сайт, и он не будет убивать процесс
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    # Render сам подставит нужный порт в переменную PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -------------------------------------

# ТВОЙ ТОКЕН (лучше добавить его в Settings -> Environment Variables на Render)
TOKEN = os.environ.get("BOT_TOKEN", "ТВОЙ_ТОКЕН_ТУТ")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я теперь живу на Render и больше не засыпаю! 🚀")

@dp.message_handler()
async def echo(message: types.Message):
    # Здесь твоя логика ИИ или просто эхо
    await message.answer(f"Ты написал: {message.text}")

async def main():
    print("Запуск сервера...")
    keep_alive()  # Запускаем "обманку" для Render
    print("Бот запущен и слушает Telegram!")
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
