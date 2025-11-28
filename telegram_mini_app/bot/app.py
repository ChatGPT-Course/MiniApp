import os
from flask import Flask, request, render_template
import telegram
from telegram import Update

app = Flask(__name__)

# Токен бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=BOT_TOKEN)

# Главная страница - отдаем HTML
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Мое Мини-Приложение</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                text-align: center;
                max-width: 400px;
                width: 100%;
            }
            h1 {
                color: #333;
                margin-bottom: 15px;
            }
            p {
                color: #666;
                line-height: 1.5;
                margin-bottom: 20px;
            }
            .btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px 5px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #5a6fd8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Мое Мини-Приложение</h1>
            <p>Добро пожаловать! Это приложение работает внутри Telegram.</p>
            
            <button class="btn" onclick="showMessage()">👋 Нажми меня</button>
            <button class="btn" onclick="changeColor()">🎨 Сменить цвет</button>
            
            <div id="result" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px; display: none;">
                <!-- Результат будет здесь -->
            </div>
        </div>

        <script>
            function showMessage() {
                const messages = ["Отлично! 🎉", "Так держать! 💪", "Превосходно! 👏"];
                const randomMessage = messages[Math.floor(Math.random() * messages.length)];
                
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = randomMessage;
                resultDiv.style.display = 'block';
                
                setTimeout(() => {
                    resultDiv.style.display = 'none';
                }, 3000);
            }

            function changeColor() {
                const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'];
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                document.body.style.background = `linear-gradient(135deg, ${randomColor} 0%, #${Math.floor(Math.random()*16777215).toString(16)} 100%)`;
                
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = "Цвет изменен! 🎨";
                resultDiv.style.display = 'block';
                
                setTimeout(() => {
                    resultDiv.style.display = 'none';
                }, 3000);
            }
        </script>
    </body>
    </html>
    '''

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
                            "web_app": {"url": "https://miniapp-vo6j.onrender.com"}
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
