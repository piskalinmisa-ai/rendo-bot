import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Берем ключи из настроек Railway (Variables)
TOKEN = os.environ.get("BOT_TOKEN", "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "AIzaSyAU2L4mcJZ3c8IydGVHQOuYxu_niCS7uTQ")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я Rendo на новом хостинге Railway. Теперь я должен работать идеально! 🚀")

@dp.message()
async def ai_msg(message: types.Message):
    await bot.send_chat_action(message.chat.id, action="typing")
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Что-то пошло не так. Проверь ключи!")

async def main():
    print("Бот запущен на Railway!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
