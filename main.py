import os
import telebot
import openai

# Получаем токены из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN or not OPENAI_KEY:
    raise RuntimeError("❌ Задайте BOT_TOKEN и OPENAI_API_KEY в .env")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_KEY

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 Привет! Я ИИ-бот на GPT. Пиши что угодно!")

@bot.message_handler(content_types=['text'])
def chat(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # или "gpt-4", если доступно
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.infinity_polling()
