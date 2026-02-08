import os
import asyncio
import io
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image

# --- НАСТРОЙКИ ---
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
GEMINI_KEYS = [
    "AIzaSyDoDxX6wHo8bnC5DltArDXaGFd42XbWB0o",
    "AIzaSyB2OYt9rhEPR2VgbWOzTLPRvqM4m0mhoQA"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для работы с ИИ
async def ask_gemini(content):
    for key in GEMINI_KEYS:
        try:
            genai.configure(api_key=key)
            # Мы пробуем стабильную версию flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # content может быть текстом или списком [текст, картинка]
            response = model.generate_content(content)
            
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Ошибка ключа: {e}")
            continue
    return "❌ Ошибка: Не удалось получить ответ от ИИ. Попробуй позже."

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Бот запущен! Присылай текст или фото — я всё пойму.")

# Обработка фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Получаем фото
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_bin = await bot.download_file(file_info.file_path)
    
    # Превращаем в формат, который понимает Gemini
    img = Image.open(photo_bin)
    user_text = message.caption or "Что на этом фото?"
    
    answer = await ask_gemini([user_text, img])
    await message.reply(answer)

# Обработка текста
@dp.message()
async def handle_text(message: types.Message):
    if not message.text: return
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_gemini(message.text)
    await message.answer(answer)

async def main():
    print("Бот стартовал...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
