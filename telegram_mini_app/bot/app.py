import os
from flask import Flask, request
from telegram import Bot, Update

app = Flask(__name__)

# Токен бота (добавим в настройки Render)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

# Главная страница для проверки
@app.route('/')
def home():
    return '🤖 Бот работает! Отправьте /start в Telegram'

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        update = Update.de_json(data, bot)
        
        # Обрабатываем команду /start
        if update.message and update.message.text == '/start':
            chat_id = update.message.chat.id
            
            # Отправляем сообщение с кнопкой веб-приложения
            bot.send_message(
                chat_id=chat_id,
                text="🎉 Добро пожаловать! Нажмите кнопку ниже чтобы открыть мини-приложение:",
                reply_markup={
                    "inline_keyboard": [[
                        {
                            "text": "🚀 Открыть Мини-Приложение",
                            "web_app": {"url": "https://your-webapp-url.onrender.com"}
                        }
                    ]]
                }
            )
        
        # Обработка обычных сообщений
        elif update.message and update.message.text:
            chat_id = update.message.chat.id
            user_text = update.message.text
            bot.send_message(
                chat_id=chat_id,
                text=f"📝 Вы написали: {user_text}\n\nОтправьте /start для открытия меню"
            )
            
        return 'ok'
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 'error', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
