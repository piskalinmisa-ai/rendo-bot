import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread
from google import genai

# --- WEB SERVER ---
app = Flask(__name__)
@app.route('/')
def index(): return "Rendo is Online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- НАСТРОЙКИ ---
# Твои ключи
GEMINI_KEYS = [
    "AIzaSyDoDxX6wHo8bnC5DltArDXaGFd42XbWB0o",
    "AIzaSyB2OYt9rhEPR2VgbWOzTLPRvqM4m0mhoQA"
]
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_ai_response(prompt):
    for key in GEMINI_KEYS:
        try:
            # Новый способ подключения к Google Gemini
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Ошибка ключа: {e}")
            continue
    return None

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот обновлен и готов к работе! 🚀")

@dp.message()
async def ai_msg(message: types.Message):
    await bot.send_chat_action(message.chat.id, action="typing")
    answer = await get_ai_response(message.text)
    if answer:
        await message.answer(answer)
    else:
        await message.answer("❌ Ошибка: лимиты исчерпаны или ключи не работают.")

async def main():
    Thread(target=run_web, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
