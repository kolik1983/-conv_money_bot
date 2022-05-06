import telebot
from libr import TOKEN, money_keys
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def bot_info(message):
    text = 'Введите информацию в следующем порядке: \n <имя валюты, цену на которую надо узнать> \
<имя валюты, цену в которой надо узнать> <количество переводимой валюты>\n <информация о всех доступных валютах: /values>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Все доступные валюты:'
    for key in money_keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def text_conv(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Много слов и мимо цели')

        quote, base, amount = values
        all_base = MoneyConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не правильная команда\n{e}')
    else:
        text = f'Цена{amount} {quote} в {base} - {all_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
