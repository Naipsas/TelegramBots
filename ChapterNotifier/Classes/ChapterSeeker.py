#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

import time
import logging

from emoji import emojize

from Classes.DBmanager import DBmanager
from Classes.SeekedManga import SeekedManga

# Logs Texts - Templates
bot_icon = emojize(":computer:", use_aliases=True)
bot_log = bot_icon + ' ChapterSeeker - Funcion: %s - Mensaje: %s'

info_icon = emojize(":information_source: ", use_aliases=True)
warn_icon = emojize(":warning:", use_aliases=True)
error_icon = emojize(":red_circle:", use_aliases=True)
critical_icon = emojize(":black_circle:", use_aliases=True)

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class ChapterSeeker:

    def __init__(self, logger, updater, db_file):

        # basicConfig
        self.__sleepTime = 50 # 3600

        # Unique list to check
        self.__mangaList = []

        # We keep the logger, bot and db objects
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        self.__updater = updater

        # Open DB file and prepare it
        try:
            self.__db = DBmanager(db_file)
            self.__log("info", ["init", "DB Conectada: " + db_file])
        except Exception as e:
            self.__log("critical", ["init", "No se pudo conectar a la base de datos: " + db_file])
            exit()

        try:
            self.__db.createSeekerTable()
            self.__log("info", ["init", "Seeker DB creada"])
        except Exception as e:
            self.__log("info", ["init", "Seeker DB ya existe"])

        # Load data from Database
        mangas_cursor = self.__db.readSeekerTable()
        latest = []
        for manga_item in mangas_cursor:
            # Manga, Latest
            latest.append([manga_item[0], manga_item[1]])

        users_cursor = self.__db.getAllUsernames()
        for user_item in users_cursor:
            if user_item[0] != "Seeker":
                user_cursor = self.__db.readUserTable(user_item[0])
                for manga_item in user_cursor:
                    self.seeker.addMangaSuscription(manga_item[0], user_item[0], manga_item[1], "0")

    def __log(self, type, args):

        if type == "info":
            prefix = info_icon
            self.__logger.info(prefix + bot_log, args[0], args[1])

        elif type == "warn":
            prefix = warn_icon
            self.__logger.warn(prefix + bot_log, args[0], args[1])

        elif type == "error":
            prefix = error_icon
            self.__logger.error(prefix + bot_log, args[0], args[1])

        else: # type == "critical"
            prefix = critical_icon
            self.__logger.critical(prefix + bot_log, args[0], args[1])

    def addMangaSuscription(self, manga, user, chat_id, last):
        try:
            found = False
            for item in self.__mangaList:
                if item.name == manga:
                    item.addSuscriber(user, chat_id)
                    found = True

            if found == False:
                self.__mangaList.append(SeekedManga(manga, last, self.__logger))
                self.__mangaList[len(self.__mangaList)-1].addSuscriber(user, chat_id)
                print("Manga: #%s#" % (manga))
                self.__db.addMangaToSeeker(manga, last)

        except Exception as e:
            self.__log("info", ["addMangaSuscription", e])
            raise e

    def delMangaSuscription(self, manga, user, chat_id):
        try:
            for item in self.__mangaList:
                if item.name == manga:
                    item.deleteSuscriber(user, chat_id)
                    # If it's empty already
                    if item.getSuscribersNum() == 0:
                        self.__mangaList.remove(item)
                        self.__db.delMangaFromSeeker(manga)

        except Exception as e:
            self.__log("info", ["delMangaSuscription", e])
            raise e

    def getInfo(self, manga, user):
        try:
            result = "No está suscrito"

            for item in self.__mangaList:
                if item.name == manga:
                    if item.checkSuscriber(user):
                        result = item.last_notified

            return result
        except Exception as e:
            raise e

    def getMangasFromUser(self, user):
        try:
            results = []

            for item in self.__mangaList:
                if item.checkSuscriber(user):
                    results.append([item.name, item.last_notified])

            return results

        except Exception as e:
            raise e

    def run(self):

        while (True):

            i = 0

            for item in self.__mangaList:

                # Look for a new Chapter
                last = item.checkManga(self.__updater, self.__db)

            # After work done, we sleep
            time.sleep(self.__sleepTime)

