#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

import logging
from enum import Enum

from emoji import emojize
from telegram import ParseMode
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler, MessageHandler

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

# Texts

welcome = ["¡Bienvenido al bot Chapter Notifier!\n\n",
" Este bot sirve para estar al tanto de tus mangas favoritos. Para ello, usamos la web MangaPanda.onl\n\n",
" Usa el comando /help para consultar todos los comandos disponibles en este bot\n\n",
" Dime, ¿qué mangas quieres seguir? Recuerda decirmelos de uno en uno, y cuando acabes usa /done\n\n"]

# Definitions

class userBotState(Enum):
    NONE = 0
    NEW = 1
    MANGA_RECORDING = 2
    RUNNING = 3

class Bot:

    def __init__(self):

        # Logs
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        # Library objects
        self.updater = Updater(token="BotFather_provided_token")
        self.dp = self.updater.dispatcher

        # Commands binding + Conversation Handlers
        """
        bot_start_handler = ConversationHandler(

            entry_points=[CommandHandler('start', self.start)],

            states={
                botState.MANGA_RECORDING: [RegexHandler('^(Daily|Weekday Only|Close|/cancel)$', self.alarm_type)],

                botState.RUNNING: [RegexHandler('^([0-2][0-9]:[0-5][0-9]|[0-9]:[0-5][0-9]|/cancel)$', self.hour)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        self.dispatcher.add_handler(bot_start_handler)
        """

        self.dp.add_handler(CommandHandler('start', self.start, pass_args=False))
        self.dp.add_handler(CommandHandler('add', self.add, pass_args=True))
        self.dp.add_handler(CommandHandler('del', self.delete, pass_args=True))
        #self.dp.add_handler(CommandHandler('list', self.list, pass_args=False))
        #self.dp.add_handler(CommandHandler('info', self.info, pass_args=True))
        #self.dp.add_handler(CommandHandler('done', self.done, pass_args=False))
        self.dp.add_handler(CommandHandler('help', self.help, pass_args=False))
        self.dp.add_handler(MessageHandler(Filters.command, unknown))

    def run(self):
        self.logger.info("Survey Bot en funcionamiento")

        self.updater.start_polling()
        self.updater.idle()

    # COMMAND FUNCTIONS
    def start(self, bot, update):
        self.logger.info('\tBot iniciado por: "@%s"', update.effective_user.username)
        bot.send_message(chat_id=update.message.chat_id, text="".join(welcome))

    def help(self, bot, update):
        icon = emojize(":information_source: ", use_aliases=True)
        text = icon + " Comandos disponibles en este bot:\n\n"

        commands = [["",  "*Gestión de los mangas*\n"],
                    ["/add",  "Añade un nuevo manga a la lista de seguimiento"],
                    ["/del",  "Elimina el manga indicado de la lista de seguimiento\n"],
                    ["",  "*Información y comportamiento del bot*\n"],
                    ["/list", "Muestra los mangas en seguimiento"],
                    ["/info", "Muestra la información del manga indicado"],
                    ["/done", "Detiene la entrada de mangas al iniciar el bot"],
                    ["/help", "Muestra este mensaje"]
                    ]

        for command in commands:
            text += command[0] + " " + command[1] + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=text,
                            parse_mode=ParseMode.MARKDOWN)

    def add(self, bot, update, args):
        if (len(args) == 0):

            icon = emojize(":exclamation: ", use_aliases=True)
            info_msg = [icon, "Por favor, use:\n",
                        "/add Nombre del manga\n",
                        "Para evitar errores, se recomienda copiarlo de la web!"]
            bot.send_message(chat_id=update.message.chat_id, text="".join(info_msg))

        else:
            icon = emojize(":information_source: ", use_aliases=True)
            manga = ""
            for item in args:
                manga += item + " "
            info_msg = [icon, "Manga añadido: ",
                        manga]
            bot.send_message(chat_id=update.message.chat_id, text="".join(info_msg))

            self.logger.info('El usuario "@%s" ha añadido el manga: "%s"',
                            update.effective_user.username,
                            manga)

    def delete(self, bot, update, args):
        if (len(args) == 0):

            icon = emojize(":exclamation: ", use_aliases=True)
            info_msg = [icon, "Por favor, use:\n",
                        "/del Nombre del manga\n",
                        "Para evitar errores, se recomienda copiarlo del listado!"]
            bot.send_message(chat_id=update.message.chat_id, text="".join(info_msg))

        else:
            icon = emojize(":information_source: ", use_aliases=True)
            manga = ""
            for item in args:
                manga += item + " "
            info_msg = [icon, "Manga eliminado: ",
                        manga]
            bot.send_message(chat_id=update.message.chat_id, text="".join(info_msg))

            self.logger.info('El usuario "@%s" ha eliminado el manga: "%s"',
                            update.effective_user.username,
                            manga)

def unknown(self, bot, update):
    icon = emojize(":exclamation: ", use_aliases=True)
    info_msg = [icon, "¡Comando no reconocido!"]
    bot.send_message(chat_id=update.message.chat_id, text=info_msg)
    self.logger.info('El usuario "@%s" ha introducido un comando no existente: "%s"',
                    update.effective_user.username,
                    update.message)

if __name__ == '__main__':

    mybot = Bot()
    mybot.run()
