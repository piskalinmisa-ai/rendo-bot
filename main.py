import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # токен берём из переменной окружения

if not TOKEN:
    raise ValueError("❌ Не задан BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Бот работает!")

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")

print("🤖 Бот запущен")
bot.infinity_polling()
