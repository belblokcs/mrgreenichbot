import os
import telebot
import random
import requests
import urllib.parse

# Берем токен из настроек Render
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- НАСТРОЙКИ ТВОЕГО КАНАЛА ---
CHANNEL_LINK = "https://t.me/teammrgreenbro"
OWNER_NAME = "Мистер Гринич"

FACTS = [
    "Осьминоги имеют три сердца!",
    "Мед не портится, его можно есть даже через 3000 лет.",
    "В Python можно перемножать строки: 'а' * 3 даст 'ааа'.",
    "Самый быстрый поезд в мире разгоняется до 600 км/ч.",
    "У улитки около 14 000 зубов."
]

# Простая озвучка через ссылку (не ломает сервер)
def send_voice(chat_id, text):
    try:
        bot.send_chat_action(chat_id, 'record_voice')
        # Обрезаем текст, чтобы ссылка не была слишком длинной
        short_text = text[:200] 
        encoded = urllib.parse.quote(short_text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded}&tl=ru&client=tw-ob"
        
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            bot.send_voice(chat_id, r.content)
    except Exception:
        pass # Если голос не отправился, бот просто промолчит, но текст пришлет

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name or "друг"
    text = (
        f"Привет, {name}! 👋\n"
        f"Я бот канала {OWNER_NAME}.\n\n"
        f"🔗 Ссылка на канал: {CHANNEL_LINK}\n"
        f"🎲 Напиши 'факт', чтобы получить случайный факт.\n"
        f"📜 Напиши 'правила', чтобы узнать правила."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()
    name = message.from_user.first_name or "друг"

    if "привет" in text:
        bot.reply_to(message, f"Привет, {name}! Добро пожаловать в канал {OWNER_NAME}. Ссылка: {CHANNEL_LINK}")
    elif "факт" in text:
        fact = random.choice(FACTS)
        answer = f"🎲 {fact}"
        bot.reply_to(message, answer)
        send_voice(message.chat.id, answer)
    elif "правила" in text:
        bot.reply_to(message, "📜 Правила канала:\n1. Будь вежлив.\n2. Не спамь.\n3. Читай канал!")
    elif "канал" in text or "ссылка" in text:
        bot.reply_to(message, f"🔗 Вот ссылка на наш канал: {CHANNEL_LINK}")
    else:
        bot.reply_to(message, "Я тебя не понял. Напиши 'факт', 'правила' или 'привет'.")

print("Бот успешно запущен!")
bot.infinity_polling()