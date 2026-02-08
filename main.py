import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# --- ВЕБ-СЕРВЕР (для Render/Railway) ---
app = Flask(__name__)
@app.route('/')
def index(): return "Rendo Multi-Key AI is Online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- НАСТРОЙКА КЛЮЧЕЙ ---
# Список твоих ключей для обхода лимитов
GEMINI_KEYS = [
    "AIzaSyDoDxX6wHo8bnC5DltArDXaGFd42XbWB0o",
    "AIzaSyB2OYt9rhEPR2VgbWOzTLPRvqM4m0mhoQA"
]

TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения ответа, перебирающая ключи
async def get_ai_response(prompt):
    for key in GEMINI_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            if response.text:
                return response.text
        except Exception as e:
            print(f"Ключ выдал ошибку, пробуем следующий... Ошибка: {e}")
            continue # Переходим к следующему ключу в списке
    return None

# --- ЛОГИКА БОТА ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я Rendo. Теперь у меня двойная мощность и запас лимитов! 🚀")

@dp.message()
async def ai_msg(message: types.Message):
    await bot.send_chat_action(message.chat.id, action="typing")
    
    answer = await get_ai_response(message.text)
    
    if answer:
        await message.answer(answer)
    else:
        await message.answer("❌ Все ключи сейчас перегружены или недоступны. Попробуй позже!")

async def main():
    Thread(target=run_web, daemon=True).start()
    print("Бот запущен с системой ротации ключей!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
