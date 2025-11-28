import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

# Создаем Flask приложение
app = Flask(__name__)

# Создаем объект бота, токен берем из переменных окружения
bot = Bot(token=os.environ.get('BOT_TOKEN'))

# Главная команда /start
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    # Отправляем сообщение с кнопкой, которая открывает наше мини-приложение
    bot.send_message(
        chat_id=chat_id,
        text="Добро пожаловать в мое мини-приложение! 🚀",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "🎮 Открыть Мини-Приложение",
                    "web_app": {"url": "https://your-webapp-url.onrender.com"} # ЗАМЕНИТЕ НА СВОЙ URL ПОЗЖЕ!
                }
            ]]
        }
    )

# Обработчик текстовых сообщений (опционально)
def echo(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(f"Вы сказали: {text}")

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    # Создаем объект обновления из данных, пришедших от Telegram
    update = Update.de_json(request.get_json(), bot)
    
    # Создаем диспетчер для обработки обновления
    dispatcher = Dispatcher(bot, None, workers=0)
    
    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Обрабатываем обновление
    dispatcher.process_update(update)
    return 'ok'

# Эндпоинт для проверки, что бот жив (обязательно для Render)
@app.route('/')
def index():
    return 'Bot is alive!'

# Запускаем Flask сервер
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)