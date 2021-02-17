import telebot

TOKEN = '1624360601:AAG_Dj_s3gwKpINIV7OVII_Cs5KHSzk43kI'

keys = {
    'доллар':'USD',
    'рубль':'RUB',
    'эфириум':'ETH',
    'биткоин':'BTC',
}


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в формате:\n <имя валюты> \
<в какую валюту перевести>\
<количество переводимой валюты>\nПросмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


bot.polling()