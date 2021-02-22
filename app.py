import telebot
from config import TOKEN
from extentions import GetCurrency, APIException, Price

# Пустой список валют
keys = {}


bot = telebot.TeleBot(TOKEN)

#заполняем список доступных валют c ресурса Dadata.ru
try:
    keys = GetCurrency.update_currency()
except Exception:
    keys = {
            'доллар':'USD',
            'рубль':'RUB',
            'евро':'EUR'
    }
    # raise APIException(f'Невозможно обновить список всех валют. Список ограничен общеупотребимыми валютами.')


# Начало работы бота
@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту, без пробелов в формате:\n <имя валюты цену которой необходимо узнать>,\n\
<имя валюты в которой необходимо узнать цену первой валюты>,\n\
<количество первой валюты>\nПример:\nюань,российский рубль,1\n\
\nПросмотреть список доступных валют: /values'
    bot.reply_to(message, text)

 # Показ списка валют
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
        base = base.lower()
        quote = quote.lower()
        result = Price.get_price(base, quote, amount, keys)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Стоимость {amount} {base} составляет {result} {quote}.'
        bot.send_message(message.chat.id, text)

bot.polling()