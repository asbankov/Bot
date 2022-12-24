import telebot
from telebot import types
import redis
import datetime
import time


TOKEN = ''
r = redis.Redis(host='redis', port=6379)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def hello_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if r.exists(str(message.chat.id)):
        item_1 = types.KeyboardButton("Извлечь запись")
    else:
        item_1 = types.KeyboardButton("Добавить запись")
    item_2 = types.KeyboardButton("Узнать точное время")
    markup.add(item_1, item_2)
    bot.send_message(message.chat.id, "Привет! На связи SomeFuncsBot!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def buttons_reply(message):
    if message.text == 'Извлечь запись':
        bot.send_message(message.chat.id, r.get(str(message.chat.id)))
        r.delete(str(message.chat.id))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton("Добавить запись")
        item_2 = types.KeyboardButton("Узнать точное время")
        markup.add(item_1, item_2)
        bot.send_message(message.chat.id, "Запись извлечена и удалена из хранилища", reply_markup=markup)
    elif message.text == 'Добавить запись':
        bot.send_message(message.chat.id, "Ваше следующее сообщение будет добавлено в хранилище")
        bot.register_next_step_handler(message, add_to_db)
    elif message.text == 'Узнать точное время':
        bot.send_message(message.chat.id, datetime.datetime.now())

def add_to_db(message):
    r.set(str(message.chat.id), message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_1 = types.KeyboardButton("Извлечь запись")
    item_2 = types.KeyboardButton("Узнать точное время")
    markup.add(item_1, item_2)
    bot.send_message(message.chat.id, "Запись добавлена в хранилище", reply_markup=markup)


if __name__=='__main__':
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
        except:
            time.sleep(5)
            continue
