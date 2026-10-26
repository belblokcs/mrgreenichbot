import os
import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- НАСТРОЙКИ ТВОЕГО БОТА ---
BOT_NAME = "Титан"  # Можешь поменять имя бота здесь
OWNER_NAME = "Мой Создатель" # Впиши сюда свой ник или имя

# --- БАЗА СОВЕТОВ И ФАКТОВ ---
FACTS = [
    "Осьминоги имеют три сердца!",
    "Мед не портится, его можно есть даже через 3000 лет.",
    "В Python можно перемножать строки: 'а' * 3 даст 'ааа'.",
    "Самый быстрый поезд в мире разгоняется до 600 км/ч.",
    "У улитки около 14 000 зубов."
]

TIPS = [
    "Пей больше воды, особенно когда сидишь за компьютером.",
    "Делай перерывы каждые 40 минут, чтобы размять глаза.",
    "Если застрял на задаче — попробуй объяснить её вслух игрушке.",
    "Не забывай сохранять код (Commit), иначе Render не увидит изменения!",
    "Учись новому понемногу, но каждый день."
]

# --- МЕНЮ ---
def get_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📜 Правила", callback_data="rules"), 
               InlineKeyboardButton("💡 Совет", callback_data="tip"))
    markup.row(InlineKeyboardButton("🎲 Бросить кубик", callback_data="dice"),
               InlineKeyboardButton("🎯 Случайный факт", callback_data="fact"))
    return markup

# --- КОМАНДА /start ---
@bot.message_handler(commands=['start'])
def start(message):
    text = (f"Привет, {message.from_user.first_name}! 👋\n"
            f"Я — {BOT_NAME}, твой личный помощник.\n"
            f"Меня создал {OWNER_NAME}.\n\n"
            f"Выбирай, что хочешь сделать:")
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# --- ОБРАБОТКА КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "rules":
        bot.answer_callback_query(call.id, "Загружаю правила...")
        bot.send_message(call.message.chat.id, "📜 *Правила чата:*\n1. Будь вежлив.\n2. Не спамь.\n3. Слушай создателя!", parse_mode='Markdown')
        
    elif call.data == "tip":
        bot.answer_callback_query(call.id, "Вот тебе совет!")
        bot.send_message(call.message.chat.id, f"💡 {random.choice(TIPS)}")
        
    elif call.data == "fact":
        bot.answer_callback_query(call.id, "Интересный факт!")
        bot.send_message(call.message.chat.id, f"🎯 {random.choice(FACTS)}")
        
    elif call.data == "dice":
        # Кидаем кубик от 1 до 6
        result = random.randint(1, 6)
        bot.answer_callback_query(call.id, f"Выпало число: {result}!")
        bot.send_message(call.message.chat.id, f"🎲 Кубик брошен! Выпало: *{result}*", parse_mode='Markdown')

# --- ОТВЕТ НА ОБЫЧНЫЙ ТЕКСТ ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Если пользователь пишет что-то кроме кнопок
    text = message.text.lower()
    if "привет" in text:
        bot.reply_to(message, f"Привет, {message.from_user.first_name}! Нажми /start, чтобы открыть меню 😎")
    elif "помощь" in text:
        bot.reply_to(message, f"Я умею кидать кубик, рассказывать факты и давать советы! Мой создатель — {OWNER_NAME}. Нажми /start")
    elif "как дела" in text:
        bot.reply_to(message, "У меня всё отлично, я же робот! А у тебя как?")
    else:
        bot.reply_to(message, "Я тебя не понял. Я же локальный бот, я знаю только кнопки из меню. Нажми /start!")

print(f"Локальный бот {BOT_NAME} запущен!")
bot.infinity_polling()
