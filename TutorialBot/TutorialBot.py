# Naipsas - Btc Sources
# Example bot - Telegram Bot Tutorial
# Nov 2018

from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler, MessageHandler

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bienvenido al bot!")

def eco(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def main():
    updater = Updater(token="BotFather_provided_token")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, eco))

    print "\tDEBUG: Tutorial Bot esta en funcionamiento!"
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
