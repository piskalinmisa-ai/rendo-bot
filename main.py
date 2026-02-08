import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- НАСТРОЙКИ ---
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"
GEMINI_KEYS = [
    "AIzaSyDoDxX6wHo8bnC5DltArDXaGFd42XbWB0o",
    "AIzaSyB2OYt9rhEPR2VgbWOzTLPRvqM4m0mhoQA"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def ask_gemini(text):
    # Прямой URL к API Google без использования их кривых библиотек
    model = "gemini-1.5-flash"
    
    for key in GEMINI_KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {
            "contents": [{"parts": [{"text": text}]}]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    data = await resp.json()
                    
                    # Проверяем, есть ли ответ в структуре Google API
                    if "candidates" in data:
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    elif "error" in data:
                        print(f"Ключ {key[:10]} ошибка: {data['error']['message']}")
                        continue # Пробуем следующий ключ
        except Exception as e:
            print(f"Ошибка сети: {e}")
            continue
            
    return "❌ Ошибка: лимиты исчерпаны или сервера Google недоступны. Попробуй позже."

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🚀 Бот запущен на прямых запросах к Gemini! Теперь должно работать стабильно.")

@dp.message()
async def handle_msg(message: types.Message):
    if not message.text: return
    
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_gemini(message.text)
    await message.answer(answer)

async def main():
    print("Бот вышел в сеть!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
