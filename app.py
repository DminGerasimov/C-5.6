import telebot
from config import TOKEN
from extentions import GetCurrency, APIException, Price, keys




bot = telebot.TeleBot(TOKEN)

try:
    GetCurrency.update_currency()   #заполняем список доступных валют c ресурса Dadata.ru
except Exception:
    keys = {
    'доллар':'USD',
    'рубль':'RUB',
    'евро':'EUR'
    }
    # raise APIException(f'Невозможно обновить список валют')


@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту, без пробелов в формате:\n <имя валюты цену которой необходимо узнать>,\n\
<имя валюты в которой необходимо узнать цену первой валюты>,\n\
<количество первой валюты>\nПример: канадский доллар,российский рубль,100\n\
\nПросмотреть список доступных валют: /values'
    bot.reply_to(message, text)
    # Обновление списка валют


@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types = ['text',])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(',')
        if len(value) != 3:
            raise APIException('Некорректное количество параметров, воспользуйтесь командой /help.')

        base, quote, amount = value
        result = Price.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Стоимость {amount} {base} составляет {result} {quote}.'
        bot.send_message(message.chat.id, text)


bot.polling()