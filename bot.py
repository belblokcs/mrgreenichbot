import os
import telebot
import requests
import urllib.parse

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я ИИ-бот. Напиши мне любой вопрос, и я отвечу!")

@bot.message_handler(func=lambda message: True)
def ai_answer(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # Отправляем запрос в бесплатный API без ключей
        prompt = urllib.parse.quote(message.text)
        url = f"https://text.pollinations.ai/{prompt}"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            answer = response.text[:4000] # Обрезаем для лимита Телеграма
            bot.reply_to(message, answer)
        else:
            bot.reply_to(message, "Ой, нейросеть перегружена. Попробуй еще раз!")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка. Попробуй позже.")

print("ИИ-бот запущен...")
bot.infinity_polling()