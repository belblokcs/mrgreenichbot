import os
import telebot
import random
from gtts import gTTS
import tempfile

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

OWNER_TITLE = "Мистер Гринич"

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
        short_text = text[:250]
        tts = gTTS(text=short_text, lang='ru')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            with open(fp.name, 'rb') as audio:
                bot.send_voice(chat_id, audio)
        os.remove(fp.name)
    except Exception as e:
        print(f"Ошибка озвучки: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    text = f"Приветствую, {OWNER_TITLE}! Я ваш личный голосовой помощник. Напишите 'факт' или 'привет'."
    bot.send_message(message.chat.id, text)
    send_voice_response(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()
    
    if "привет" in text:
        answer = f"Здравствуйте, {OWNER_TITLE}! Рад вас слышать."
    elif "факт" in text:
        answer = f"Интересный факт для вас, {OWNER_TITLE}: {random.choice(FACTS)}"
    elif "как дела" in text:
        answer = f"У меня всё отлично, {OWNER_TITLE}! Готов помогать."
    else:
        answer = f"{OWNER_TITLE}, я вас услышал, но пока не знаю такой команды. Напишите 'факт' или 'привет'!"

    # Отправляем текст и голос
    bot.reply_to(message, answer)
    send_voice_response(message.chat.id, answer)

print("Бот запущен!")
bot.infinity_polling()