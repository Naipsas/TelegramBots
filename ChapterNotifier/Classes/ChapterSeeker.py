#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

import time
import logging

from emoji import emojize

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

    def __init__(self, logger, bot):

        # basicConfig
        self.sleepTime = 50 # 3600

        # Unique list to check
        self.mangaList = []

        # We keep the logger and bot as well
        self.logger = logger
        self.bot = bot

    def log(self, type, args):

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

    def addMangaSuscription(self, manga, user, chat_id):
        try:
            found = False
            for item in self.mangaList:
                if item.name == manga:
                    item.addSuscriber(user, chat_id)
                    found = True

            if found == False:
                self.mangaList.append(SeekedManga(manga, 0, self.logger))
                self.mangaList[len(self.mangaList)-1].addSuscriber(user, chat_id)

        except Exception as e:
            self.log("info", ["addMangaSuscription", e])
            raise e

    def delMangaSuscription(self, manga, user, chat_id):
        try:
            for item in self.mangaList:
                if item.name == manga:
                    item.deleteSuscriber(user, chat_id)

        except Exception as e:
            self.log("info", ["delMangaSuscription", e])
            raise e

    def getInfo(self, manga, user):
        try:
            result = "No está suscrito"

            for item in self.mangaList:
                if item.name == manga:
                    if item.checkSuscriber(user):
                        result = item.last_notified

            return result
        except Exception as e:
            raise e

    def getMangasFromUser(self, user):
        try:
            results = []

            for item in self.mangaList:
                if item.checkSuscriber(user):
                    results.append([item.name, item.last_notified])

            return results

        except Exception as e:
            raise e

    def run(self):

        while (True):

            i = 0

            for item in self.mangaList:

                # Look for a new Chapter
                last = item.checkManga(self.bot)

            # After work done, we sleep
            time.sleep(self.sleepTime)

