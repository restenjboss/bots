import telebot

API_TOKEN = ' '

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Я бот-калькулятор! Используйте команду /calc для вычислений')

@bot.message_handler(commands=['calc'])
def calculator(message):
    bot.reply_to(message, 'Введите математическое выражение')
    
def safe_eval(expression):
    return eval(expression)

@bot.message_handler(func=lambda message: True)
def calculate(message):
    try:
        result = safe_eval(message.text)
        bot.reply_to(message, f'Результат: {result}')
    except:
        bot.reply_to(message, 'Ошибка! Проверьте правильность выражения')

bot.infinity_polling()
