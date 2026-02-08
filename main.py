import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from g4f.client import Client

# Твой токен телеграм (оставляем прежний)
TOKEN = "8347791766:AAEO0E7gfjPSqK6Vsy-KqZQbnGX02UsIVSc"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = Client()

async def get_ai_response(user_text):
    try:
        # Прямой запрос к бесплатному ИИ без всяких ключей
        response = client.chat.completions.create(
            model="gpt-4o", # Или "gpt-3.5-turbo", если этот будет занят
            messages=[{"role": "user", "content": user_text}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}. Попробуй написать еще раз через минуту."

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я перешел на максимально простую систему. Теперь ключи не нужны. Просто спрашивай!")

@dp.message()
async def handle_msg(message: types.Message):
    if not message.text: return
    
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Получаем ответ
    answer = await get_ai_response(message.text)
    await message.answer(answer)

async def main():
    print("Бот запущен без ключей!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
