import os
import asyncio
import io
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from google import genai
from PIL import Image

# --- НАСТРОЙКИ ---
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
# Твои ключи (будут меняться, если кончится лимит)
GEMINI_KEYS = [
    "AIzaSyDoDxX6wHo8bnC5DltArDXaGFd42XbWB0o",
    "AIzaSyB2OYt9rhEPR2VgbWOzTLPRvqM4m0mhoQA"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция выбора ключа и получения ответа
async def ask_gemini(user_content):
    for key in GEMINI_KEYS:
        try:
            client = genai.Client(api_key=key)
            # Отправляем запрос (текст или список текст+фото)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=user_content
            )
            if response.text:
                return response.text
        except Exception as e:
            print(f"Ошибка ключа {key[:10]}: {e}")
            continue
    return "❌ Все ключи сейчас недоступны или лимит исчерпан."

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Rendo AI готов! Я понимаю текст и фото. Лимиты расширены за счет двух ключей.")

# Если прислали фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Качаем фото
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_bin = await bot.download_file(file_info.file_path)
    
    # Читаем картинку через PIL
    img = Image.open(photo_bin)
    caption = message.caption or "Что на этом фото?"
    
    # Отправляем в ИИ
    answer = await ask_gemini([caption, img])
    await message.reply(answer)

# Если прислали текст
@dp.message()
async def handle_text(message: types.Message):
    if not message.text: return
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_gemini(message.text)
    await message.answer(answer)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
