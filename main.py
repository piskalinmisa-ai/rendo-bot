import telebot
import requests

TELEGRAM_TOKEN = "ВСТАВЬ_НОВЫЙ_TELEGRAM_TOKEN"
HF_TOKEN = "ВСТАВЬ_НОВЫЙ_HUGGINGFACE_TOKEN"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# память диалогов
user_memory = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет 👋 Я ИИ-бот 🤖\nПиши что угодно — я отвечу!"
    )

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "/start — начать\n/help — помощь\n\nПросто пиши текст 👇"
    )

@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    user_id = message.chat.id
    text = message.text

    history = user_memory.get(user_id, "")
    prompt = history + "\nПользователь: " + text + "\nБот:"

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-base",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )

    try:
        answer = response.json()[0]["generated_text"]
    except:
        answer = "Я немного завис 😅 попробуй ещё раз"

    user_memory[user_id] = prompt + answer
    bot.send_message(user_id, answer)

bot.polling()
