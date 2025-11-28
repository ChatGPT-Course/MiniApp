import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Создаем Flask приложение
app = Flask(__name__)

# Создаем объект бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

# Создаем Application для обработки обновлений
application = Application.builder().token(BOT_TOKEN).build()

# Добавляем обработчики в Application
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await bot.send_message(
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

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Вы сказали: {text}")

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        # Получаем обновление от Telegram
        update = Update.de_json(request.get_json(), application.bot)
        
        # Обрабатываем обновление через Application
        await application.process_update(update)
        return 'ok'
    except Exception as e:
        print(f"Error: {e}")
        return 'error', 500

# Эндпоинт для проверки, что бот жив
@app.route('/')
def index():
    return 'Bot is alive!'

# Инициализируем Application при запуске
if __name__ == '__main__':
    # В продакшене это будет работать через вебхуки
    app.run(host='0.0.0.0', port=5000)
