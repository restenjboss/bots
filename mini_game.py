# Импортируем необходимые библиотеки
import telebot
from telebot import types
import random

# Словарь для хранения статистики пользователей
user_stats = {}

# Токен бота Telegram
API_TOKEN = ' ' #вставьте свой токен

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Списки для генерации карт
CARD_RANK = ['2', '3', '4', '5', '6',
             '7', '8', '9', '10',
             'J', 'Q', 'K', 'A']  # Значения карт

CARD_SUITS = ['♥', '♦️', '♣️', '♠️']  # Масти карт

# Обработчик команд /help и /start
@bot.message_handler(commands = ['help', 'start'])
def send_welcome(message):
    # Создаем кнопки для выбора цвета
    red_button = types.InlineKeyboardButton('🟥', callback_data = 'R')
    black_button = types.InlineKeyboardButton('⬛', callback_data = 'B')
    
    # Отправляем приветственное сообщение с кнопками
    bot.send_message(
        chat_id = message.chat.id, 
        text='Привет! Это игра "Угадай цвет карты"!\nВыберите цвет:',
        reply_markup = types.InlineKeyboardMarkup().add(red_button, black_button)
    )

# Функция обновления статистики игрока    
def update_stats(user_id, won):
    # Создаем запись для нового пользователя
    if user_id not in user_stats:
        user_stats[user_id] = {'wins': 0, 'losses': 0}
    # Обновляем статистику побед/поражений
    if won:
        user_stats[user_id]['wins'] += 1
    else:
        user_stats[user_id]['losses'] += 1

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda c: c.data in ['R', 'B'])
def handle_user_callback(call):
    # Генерируем случайную карту
    card_rank = random.choice(CARD_RANK)
    card_suit = random.choice(CARD_SUITS)
    
    # Определяем цвет карты и выбор пользователя
    is_red = card_suit in ["♥", "♦️"]
    user_chose_red = call.data == 'R'
    user_id = str(call.from_user.id)
    
    # Проверяем, угадал ли пользователь
    won = (user_chose_red and is_red) or (not user_chose_red and not is_red)
    update_stats(user_id, won)
    
    # Формируем сообщение о результате
    msg = 'Поздравляю! Вы угадали!' if won else 'В следующий раз повезёт!'
    
    # Рассчитываем статистику
    stats = user_stats[user_id]
    total_games = stats['wins'] + stats['losses']
    win_rate = (stats['wins'] / total_games) * 100 if total_games > 0 else 0
    
    # Отправляем результат и статистику
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        f'{msg}\nЯ загадал карту: {card_suit}{card_rank}\n\n'
        f'📊 Ваша статистика:\n'
        f'Побед: {stats["wins"]}\n'
        f'Поражений: {stats["losses"]}\n'
        f'Процент побед: {win_rate:.1f}%'
    )
    send_welcome(call.message)

# Обработчик команды /stats для просмотра статистики
@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = str(message.from_user.id)
    
    # Проверяем, есть ли статистика у пользователя
    if user_id not in user_stats:
        bot.reply_to(message, "У вас пока нет статистики игр. Сыграйте несколько раз!")
        return
    
    # Рассчитываем и отправляем статистику
    stats = user_stats[user_id]
    total_games = stats['wins'] + stats['losses']
    win_rate = (stats['wins'] / total_games) * 100 if total_games > 0 else 0
    
    bot.reply_to(
        message,
        f'📊 Ваша статистика:\n'
        f'Побед: {stats["wins"]}\n'
        f'Поражений: {stats["losses"]}\n'
        f'Всего игр: {total_games}\n'
        f'Процент побед: {win_rate:.1f}%'
    )

# Запускаем бота в бесконечном режиме
bot.infinity_polling()
