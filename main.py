import telebot
import os
import logging
from flask import Flask, request
from threading import Thread
import time

# Log sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Konfiguratsiya
TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://barber-queue-c0c6f.web.app")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# /start komandasi uchun handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Web ilovaga o'tish", 
                                                  url=f"{WEB_APP_URL}?telegram_id={user_id}")
        markup.add(button)
        
        bot.send_message(
            message.chat.id,
            "Assalomu alaykum! Botimizga xush kelibsiz!",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Xato: {str(e)}")

# Webhook endpointi
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    return "Bad request", 400

# Asosiy sahifa
@app.route('/')
def home():
    return "Bot ishlamoqda 🚀"

# Polling funksiyasi
def run_polling():
    logger.info("Polling ishga tushmoqda...")
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            logger.error(f"Polling xatosi: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    # Webhook yoki polling tanlash
    if os.getenv("USE_WEBHOOK", "false").lower() == "true":
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=os.getenv("WEBHOOK_URL"))
        logger.info("Webhook ishga tushirildi")
    else:
        Thread(target=run_polling, daemon=True).start()
    
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

# import telebot
# import os
# import logging

# # Log yozishni sozlash
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[logging.StreamHandler()]
# )
# logger = logging.getLogger(__name__)

# # Konfiguratsiya
# TOKEN = os.getenv("BOT_TOKEN")  # Faqat environmentdan olish
# WEB_APP_URL = os.getenv("WEB_APP_URL", "https://barber-queue-c0c6f.web.app")

# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     try:
#         user_id = message.from_user.id
#         encrypted_link = f"{WEB_APP_URL}?telegram_id={user_id}"

#         markup = telebot.types.InlineKeyboardMarkup()
#         button = telebot.types.InlineKeyboardButton("Web ilovaga o'tish", url=encrypted_link)
#         markup.add(button)

#         bot.send_message(
#             message.chat.id,
#             "Assalomu alaykum! Web ilovamizdan foydalanish uchun quyidagi tugmani bosing:",
#             reply_markup=markup
#         )
#     except Exception as e:
#         logger.error(f"Start command error: {str(e)}")

# if __name__ == "__main__":
#     logger.info("Bot ishga tushmoqda...")
#     while True:
#         try:
#             bot.polling(none_stop=True, interval=2, timeout=20)
#         except Exception as e:
#             logger.error(f"Xato: {str(e)}")
#             time.sleep(5)