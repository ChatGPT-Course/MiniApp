import os
from flask import Flask, request, jsonify
import telegram
from telegram import Update

# Создаем Flask приложение
app = Flask(__name__)

# Создаем объект бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=BOT_TOKEN)

# Эндпоинт для проверки, что бот жив
@app.route('/')
def index():
    return 'Bot is alive!'

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Получаем обновление от Telegram
        data = request.get_json()
        update = Update.de_json(data, bot)
        
        # Обрабатываем команду /start
        if update.message and update.message.text == '/start':
            chat_id = update.message.chat.id
            bot.send_message(
                chat_id=chat_id,
                text="Добро пожаловать в мое мини-приложение! 🚀",
                reply_markup={
                    "inline_keyboard": [[
                        {
                            "text": "🎮 Открыть Мини-Приложение",
                            "web_app": {"url": "https://your-webapp-url.onrender.com"} # ЗАМЕНИТЕ НА СВОЙ URL!
                        }
                    ]]
                }
            )
        
        # Обработка обычных сообщений
        elif update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text
            bot.send_message(
                chat_id=chat_id,
                text=f"Вы сказали: {text}"
            )
            
        return 'ok'
    
    except Exception as e:
        print(f"Error: {e}")
        return 'error', 500

# Запускаем сервер
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
