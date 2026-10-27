import os
import telebot
import random
import requests
import urllib.parse

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- ТВОИ НАСТРОЙКИ (ЗАПОЛНИ ПОД СЕБЯ) ---
OWNER_NAME = "Мистер Гринич"
CHANNEL_LINK = "https://t.me/твой_канал"  # Ссылка на твой канал
CONTACT_LINK = "https://t.me/твой_ник"    # Ссылка для связи с тобой
RULES_TEXT = "1. Будь вежлив.\n2. Не спамь.\n3. Соблюдай тематику канала."

FACTS = [
    "Осьминоги имеют три сердца!",
    "Мед не портится, его можно есть даже через 3000 лет.",
    "В Python можно перемножать строки: 'а' * 3 даст 'ааа'.",
    "Самый быстрый поезд в мире разгоняется до 600 км/ч.",
    "У улитки около 14 000 зубов."
]

# Функция озвучки
def send_voice_response(chat_id, text):
    try:
        bot.send_chat_action(chat_id, 'record_voice')
        short_text = text[:200] # Ограничиваем для озвучки
        encoded_text = urllib.parse.quote(short_text)
        voice_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl=ru&client=tw-ob"
        response = requests.get(voice_url)
        if response.status_code == 200:
            bot.send_voice(chat_id, response.content)
    except Exception as e:
        print(f"Ошибка голоса: {e}")

# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    # Берем имя подписчика (если нет, то "друг")
    user_name = message.from_user.first_name if message.from_user.first_name else "друг"
    text = (f"Привет, {user_name}! 👋\n"
            f"Я официальный бот канала.\n"
            f"Мой создатель — {OWNER_NAME}.\n\n"
            f"Вот что я умею:\n"
            f"🔗 /links — все ссылки\n"
            f"📜 /rules — правила\n"
            f"🎲 /fact — случайный факт\n"
            f"📞 /contact — связь с автором")
    bot.send_message(message.chat.id, text)
    send_voice_response(message.chat.id, f"Привет, {user_name}! Я бот канала {OWNER_NAME}.")

# Команды
@bot.message_handler(commands=['links'])
def links(message):
    bot.reply_to(message, f"🔗 Вот наши ссылки:\nКанал: {CHANNEL_LINK}\nСвязь: {CONTACT_LINK}")

@bot.message_handler(commands=['rules'])
def rules(message):
    bot.reply_to(message, f"📜 Правила:\n{RULES_TEXT}")

@bot.message_handler(commands=['contact'])
def contact(message):
    bot.reply_to(message, f"📞 Связаться с {OWNER_NAME} можно тут: {CONTACT_LINK}")

@bot.message_handler(commands=['fact'])
def fact(message):
    answer = f"🎲 {random.choice(FACTS)}"
    bot.reply_to(message, answer)
    send_voice_response(message.chat.id, answer)

# Ответ на обычный текст
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()
    if "привет" in text:
        bot.reply_to(message, f"Привет, {message.from_user.first_name}! Нажми /start, чтобы увидеть меню.")
    elif "ссылка" in text or "канал" in text:
        bot.reply_to(message, f"Вот ссылка на канал: {CHANNEL_LINK}")
    else:
        bot.reply_to(message, "Я тебя не понял. Нажми /start, чтобы увидеть, что я умею!")

print(f"Бот для подписчиков запущен!")
bot.infinity_polling()