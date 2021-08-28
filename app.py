import telebot
import configparser
from extensions import APIException, CryptoConverter

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")

token = config.get('section', 'TOKEN')
key = config.get('section', 'keys')
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start', 'help'])
def starting(message: telebot.types.Message):
    text = 'Чтобы начать работу бота введите команду в следующем формате: \n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \nУзнать все доступные валюты: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands =['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for k in key:
        text = '\n'.join((text, k, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неправильно введен запрос')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {key[quote.lower()]} в {key[base.lower()]} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()