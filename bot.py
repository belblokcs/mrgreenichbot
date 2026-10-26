import os
import telebot
import requests
import urllib.parse
from gtts import gTTS
import tempfile

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

OWNER_TITLE = "Мистер Гринич"

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
    bot.send_message(message.chat.id, f"Приветствую, {OWNER_TITLE}! Я ваш умный голосовой помощник. Спрашивайте что угодно!")

@bot.message_handler(func=lambda message: True)
def ai_answer(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        prompt = f"Отвечай дружелюбно. Обращайся ко мне '{OWNER_TITLE}'. Вопрос: {message.text}"
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}"
        
        response = requests.get(url, timeout=25)
        
        if response.status_code == 200:
            answer = response.text
            bot.reply_to(message, answer)
            send_voice_response(message.chat.id, answer)
        else:
            bot.reply_to(message, f"Секунду, {OWNER_TITLE}, мои сервера перегружены. Попробуйте еще раз!")
            
    except Exception as e:
        bot.reply_to(message, f"Ой, {OWNER_TITLE}, у меня что-то сломалось. Попробуйте позже!")

print(f"Голосовой бот запущен!")
bot.infinity_polling()