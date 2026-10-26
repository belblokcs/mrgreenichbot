import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Бот берет токен из переменных окружения (безопасный способ)
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👤 Профиль", callback_data="profile"))
    markup.add(InlineKeyboardButton("⚙️ Настройки", callback_data="settings"))
    bot.send_message(message.chat.id, "Привет! Это главное меню:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "profile":
        bot.edit_message_text("Это твой профиль.", call.message.chat.id, call.message.message_id)
    elif call.data == "settings":
        bot.edit_message_text("Тут будут настройки.", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я пока не знаю такой команды. Нажми /start")

print("Бот запущен...")
bot.infinity_polling()