import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread
import google.generativeai as genai

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)
@app.route('/')
def index(): return "Rendo AI is Online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- НАСТРОЙКА GEMINI ---
# Я вставил твой первый ключ сюда:
GEMINI_KEY = "AIzaSyAU2L4mcJZ3c8IydGVHQOuYxu_niCS7uTQ"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ЛОГИКА ТЕЛЕГРАМ-БОТА ---
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Теперь я твой полноценный ИИ-помощник. Спрашивай о чём угодно! 🧠✨")

@dp.message()
async def ai_handler(message: types.Message):
    # Показываем статус "печатает"
    await bot.send_chat_action(message.chat.id, action="typing")
    
    try:
        # Запрос к нейросети
        response = model.generate_content(message.text)
        
        # Если Gemini прислал пустой ответ или ошибку
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Я задумался и не смог подобрать слов. Попробуй еще раз!")
            
    except Exception as e:
        print(f"Ошибка Gemini: {e}")
        await message.answer("Произошла ошибка при обработке запроса. Возможно, стоит проверить лимиты ключа.")

async def main():
    # Запуск сервера "обманки" для Render
    Thread(target=run_web, daemon=True).start()
    
    print("Rendo AI успешно запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
