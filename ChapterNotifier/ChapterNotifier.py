#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

from enum import Enum

import logging

from emoji import emojize
from functools import wraps

from telegram import ParseMode
from telegram import ChatAction

from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler, MessageHandler

from Classes.Manga import Manga
from Classes.MangaSet import MangaSet
from Classes.DBmanager import DBmanager
from Classes.UserBotState import UserBotState
from Classes.ChapterSeeker import ChapterSeeker

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

# Icons
info_icon = emojize(":information_source: ", use_aliases=True)
ok_icon = emojize(":white_check_mark:", use_aliases=True)
warn_icon = emojize(":warning:", use_aliases=True)
error_icon = emojize(":red_circle:", use_aliases=True)
critical_icon = emojize(":black_circle:", use_aliases=True)

bot_icon = emojize(":computer:", use_aliases=True)
user_icon = emojize(":bust_in_silhouette:", use_aliases=True)

exc_icon = emojize(":exclamation: ", use_aliases=True)

# Texts to user

welcome = ["¡Bienvenido al bot Chapter Notifier!\n\n",
" Este bot sirve para estar al tanto de tus mangas favoritos. Para ello, usamos la web MangaPanda.onl\n\n",
" Usa el comando /help para consultar todos los comandos disponibles en este bot"""] #\n\n" ,
#" Dime, ¿qué mangas quieres seguir? Recuerda decirmelos de uno en uno, y cuando acabes usa /done\n\n"]

add_usage = [exc_icon, " Por favor, use:\n\n",
            "/add Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo de la web!"]

add_msg = [info_icon, " Manga añadido a la colección."]
add_error = [error_icon, " ¡El manga ya existe en la colección!"]

del_usage = [exc_icon, " Por favor, use:\n\n",
            "/del Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo del listado!"]

del_msg = [info_icon, " Manga eliminado de la colección."]
del_error = [error_icon, " ¡El manga no está en la colección!"]

info_usage = [exc_icon, " Por favor, use:\n\n",
            "/info Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo del listado!"]

info_msg = [info_icon, " Manga: "]
info_error = [error_icon, " ¡El manga no está en la colección!"]


list_usage = [exc_icon, " Por favor, use solamente:\n\n",
            "/list\n"]

list_msg = [info_icon, "Tu colección incluye:\n\n"]
list_error = [error_icon, "¡La colección está vacía!"]

unknown_user = [exc_icon, " ¡Comando no reconocido!"]

# Logs Texts - Templates
# Bot log
bot_log = bot_icon + ' Funcion: %s - Mensaje: %s'
# User action (OK, NOK)
user_log = user_icon + ' : "@%s" - Comando: %s - Resultado: %s'

# Definitions

class Bot:

    def __init__(self):

        # Logs
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        # Database usage
        db_file = "ChapterNotifier.db"

        try:
            self.db = DBmanager(db_file)
            self.log("bot", "info", ["init", "DB Conectada: " + db_file])
        except Exception as e:
            self.log("bot", "critical", ["init", "No se pudo conectar a la base de datos: " + db_file])
            exit()

        # Dataset list for every user
        self.dataset = []
        self.seeker = ChapterSeeker(self.logger)

        # Load data from Database
        dbTables = self.db.getAllUsernames()
        for user_item in dbTables:
            # Create the MangaSet
            user_dataset = MangaSet(user_item[0])
            # Populate it
            mangas = self.db.readUserTable(user_item[0])
            for manga_item in mangas:
                user_dataset.addManga(Manga(manga_item[0], manga_item[1]))
            # Finally, add it to the list
            self.dataset.append(user_dataset)

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
        self.dp.add_handler(CommandHandler('list', self.list, pass_args=True))
        self.dp.add_handler(CommandHandler('info', self.info, pass_args=True))
        #self.dp.add_handler(CommandHandler('done', self.done, pass_args=False))
        self.dp.add_handler(CommandHandler('help', self.help, pass_args=False))
        self.dp.add_handler(MessageHandler(Filters.command, self.unknown))

    def run(self):
        self.log("bot", "info", ["run", "RUNNING"])
        self.updater.start_polling()
        self.updater.idle()

    # Auxiliar FUNCTIONS
    def send_action(action):
        """Sends `action` while processing func command."""

        def decorator(func):
            @wraps(func)
            def command_func(*args, **kwargs):
                self, bot, update = args
                bot.send_chat_action(chat_id=update.message.chat_id, action=action)
                func(self, bot, update, **kwargs)
            return command_func

        return decorator

    send_typing_action = send_action(ChatAction.TYPING)
    send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
    send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

    def user_collection(self, name, collection_list):
        for item in collection_list:
            if item.user == name:
                return item

    def log(self, origin, type, args):

        if origin == "user":

            if type == "OK":
                prefix = ok_icon
            else: # type == "NOK"
                prefix = error_icon

            # Both info, user faulires are not critical for the bot itself
            self.logger.info(prefix + user_log, args[0], args[1], args[2])

        else: # origin = bot

            if type == "info":
                prefix = info_icon
                self.logger.info(prefix + bot_log, args[0], args[1])

            elif type == "warn":
                prefix = warn_icon
                self.logger.warn(prefix + bot_log, args[0], args[1])

            elif type == "error":
                prefix = error_icon
                self.logger.error(prefix + bot_log, args[0], args[1])

            else: # type == "critical"
                prefix = critical_icon
                self.logger.critical(prefix + bot_log, args[0], args[1])

    # COMMAND FUNCTIONS
    @send_typing_action
    def start(self, bot, update):
        try:
            # Create the user in our data
            user = update.effective_user.username
            self.dataset.append(MangaSet(user))
            self.db.createUserTable(user)
            # Messages
            self.log("user", "OK", [user, "start", "Bot iniciado"])
        except Exception as e:
            self.log("user", "NOK", [user, "start", e.message])

        bot.send_message(chat_id=update.message.chat_id, text="".join(welcome))

    @send_typing_action
    def help(self, bot, update):
        icon = info_icon
        text = icon + " Comandos disponibles en este bot:\n\n"

        commands = [["",  "*Gestión de los mangas*\n"],
                    ["/add",  "Añade un nuevo manga a la lista de seguimiento"],
                    ["/del",  "Elimina el manga indicado de la lista de seguimiento\n"],
                    ["",  "*Información y comportamiento del bot*\n"],
                    ["/list", "Muestra los mangas en seguimiento"],
                    ["/info", "Muestra la información del manga indicado"],
                    #["/done", "Detiene la entrada de mangas al iniciar el bot"],
                    ["/help", "Muestra este mensaje"]
                    ]

        for command in commands:
            text += command[0] + " " + command[1] + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=text,
                            parse_mode=ParseMode.MARKDOWN)

    @send_typing_action
    def add(self, bot, update, args):
        if (len(args) == 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(add_usage))

        else:
            # Previous
            user = update.effective_user.username
            manga = ""
            for item in args:
                manga += item + " "
            manga.replace("\"", "")

            try:
                # Data work
                newManga = Manga(manga, "last")
                #self.seeker.addMangaSuscription(manga, user, update.message.chat_id)
                self.user_collection(user, self.dataset).addManga(newManga)
                self.db.addMangaToUser(user, newManga.name)
                # Messages
                bot.send_message(chat_id=update.message.chat_id, text="".join(add_msg))
                self.log("user", "OK", [user, "add", manga + " añadido!"])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(add_error))
                self.log("user", "NOK", [user, "add", manga + " ya existente!"])

    @send_typing_action
    def delete(self, bot, update, args):
        if (len(args) == 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(del_usage))

        else:
            # Previous
            user = update.effective_user.username
            manga = ""
            for item in args:
                manga += item + " "
            manga.replace("\"", "")

            try:
                # Data work
                #self.seeker.delMangaSuscription(manga, user, update.message.chat_id)
                self.user_collection(user, self.dataset).deleteManga(manga)
                try:
                    self.db.delMangaFromUser(user, manga)
                except Exception as e:
                    print ("Aqui excepcion, el lock se queda cogido")
                # Messages
                bot.send_message(chat_id=update.message.chat_id, text="".join(del_msg))
                self.log("user", "OK", [user, "delete", manga + " eliminado!"])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(del_error))
                self.log("user", "NOK", [user, "del", manga + " no existe!"])

    @send_typing_action
    def info(self, bot, update, args):
        if (len(args) == 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(info_usage))

        else:
            # Previous
            user = update.effective_user.username
            manga = ""
            for item in args:
                manga += item + " "
            manga.replace("\"", "")

            try:
                # Data work
                myManga = self.user_collection(user, self.dataset).getManga(manga)
                # Messages
                info_user_msg = "".join(info_msg) + myManga.name + "\nÚltimo capítulo: " + myManga.notified
                bot.send_message(chat_id=update.message.chat_id, text=info_user_msg)
                self.log("user", "OK", [user, "info", manga + " consultado!"])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(info_error))
                self.log("user", "NOK", [user, "info", manga + " no puede consultarse!"])

    @send_typing_action
    def list(self, bot, update, args):
        if (len(args) != 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(list_usage))

        else:
            # Previous
            user = update.effective_user.username

            try:
                # Data work
                myMangas = self.user_collection(user, self.dataset).getAllMangas()
                # Messages
                list_user_msg = "".join(list_msg)
                for manga in myMangas:
                    list_user_msg = list_user_msg + manga.name + " - Capítulo: " + manga.notified + "\n"
                bot.send_message(chat_id=update.message.chat_id, text=list_user_msg)
                self.log("user", "OK", [user, "list", "Colección consultada."])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(list_error))
                self.log("user", "NOK", [user, "list", "¡La colección está vacía!"])

    def unknown(self, bot, update):
        user = update.effective_user.username
        bot.send_message(chat_id=update.message.chat_id, text="".join(unknown_user))
        self.log("user", "NOK", [user, update.message.text, "Comando no existente"])

if __name__ == '__main__':

    mybot = Bot()
    mybot.run()
