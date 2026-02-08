import os
import asyncio
import io
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from google import genai
from google.genai import types as genai_types
from PIL import Image

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
# Список твоих ключей для ротации (лимит будет суммироваться)
GEMINI_KEYS = [
    "AIzaSyDoDxX6wHo8bnC5DltArDXaGFd42XbWB0o",
    "AIzaSyB2OYt9rhEPR2VgbWOzTLPRvqM4m0mhoQA"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для выбора рабочего ключа и получения ответа
async def ask_gemini(prompt, photo_bytes=None):
    for key in GEMINI_KEYS:
        try:
            client = genai.Client(api_key=key)
            
            if photo_bytes:
                # Если пришло фото, используем мультимодальный запрос
                img = Image.open(io.BytesIO(photo_bytes))
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt or "Что на этом фото?", img]
                )
            else:
                # Если только текст
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
            
            if response.text:
                return response.text
        except Exception as e:
            print(f"Ключ {key[:10]}... выдал ошибку: {e}")
            continue # Пробуем следующий ключ
    return "❌ К сожалению, все мои ключи сейчас исчерпали лимит. Попробуй позже!"

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой продвинутый ИИ-ассистент Rendo.\n\n"
        "✅ Я использую несколько ключей Gemini для больших лимитов.\n"
        "🖼️ Ты можешь прислать мне фото, и я расскажу, что на нем!\n"
        "✍️ Просто напиши мне что-нибудь."
    )

# Обработка фотографий
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Скачиваем фото в память
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_bin = await bot.download_file(file_info.file_path)
    photo_bytes = photo_bin.read()
    
    # Текст к фото (если есть)
    user_text = message.caption or "Что на этом изображении?"
    
    answer = await ask_gemini(user_text, photo_bytes=photo_bytes)
    await message.reply(answer)

# Обработка обычного текста
@dp.message()
async def handle_text(message: types.Message):
    if not message.text: return
    
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_gemini(message.text)
    await message.answer(answer)

# --- ЗАПУСК ---
async def main():
    print("🚀 Rendo AI запущен на Railway!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
