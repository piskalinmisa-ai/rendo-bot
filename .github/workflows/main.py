import asyncio, base64, requests, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
TG_TOKEN = "8347791766:AAESWCAxgTiHoSKayIi76aNDNMlJk6-q1Jo"
KEYS = ["AIzaSyBKebrtxU3FklDbOQrQyfHCn20lyJevaGo", "AIzaSyDTsNv542p1b6-nfjWVRSYY4IgvypOqeEI"]

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
current_key_index = 0

def get_api_key(): return KEYS[current_key_index]
def switch_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(KEYS)

def get_best_model(api_key):
    try:
        res = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}", timeout=10).json()
        models = [m['name'] for m in res.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        for m in models:
            if "flash" in m.lower(): return m
        return models[0] if models else None
    except: return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Rendo запущен 24/7 с телефона!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    for _ in range(len(KEYS)):
        api_key = get_api_key()
        model = get_best_model(api_key)
        if not model:
            switch_key(); continue
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"
        parts = [{"text": message.text or message.caption or "Опиши"}]
        if message.photo:
            file = await bot.get_file(message.photo[-1].file_id)
            photo = await bot.download_file(file.file_path)
            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(photo.getvalue()).decode('utf-8')}})
        try:
            res = requests.post(url, json={"contents": [{"parts": parts}]}, timeout=30)
            if res.status_code == 200:
                await message.answer(res.json()['candidates'][0]['content']['parts'][0]['text'])
                return
            switch_key()
        except: switch_key()
    await message.answer("😴 Лимит. Подожди минуту.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
