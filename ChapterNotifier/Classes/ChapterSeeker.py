#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

import time
import logging

from emoji import emojize

from Manga import Manga
from SeekerList import SeekerList

# Logs Texts - Templates
bot_icon = emojize(":computer:", use_aliases=True)
bot_log = bot_icon + ' Seeker - Funcion: %s - Mensaje: %s'

info_icon = emojize(":information_source: ", use_aliases=True)
warn_icon = emojize(":warning:", use_aliases=True)
error_icon = emojize(":red_circle:", use_aliases=True)
critical_icon = emojize(":black_circle:", use_aliases=True)

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class ChapterSeeker:

    def __init__(self, logger):

        # basicConfig
        self.sleepTime = 3600

        # Unique list to check
        self.mangaList = SeekerList()

        # We keep the logger as well
        self.logger = logger

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
            self.mangaList.addManga(manga, user, chat_id)
            self.log("info", ["addMangaSuscription", user + " añadió " + manga])
        except Exception as e:
            self.log("info", ["addMangaSuscription", user + " ya estaba suscrito a " + manga])
            raise e

    def delMangaSuscription(self, manga, user, chat_id):
        try:
            self.mangaList.deleteManga(manga, user, chat_id)
            self.log("info", ["delMangaSuscription", user + " eliminó " + manga])
        except Exception as e:
            # It doesn't exist
            self.log("info", ["delMangaSuscription", user + " no estaba suscrito a " + manga])
            self.log("info", ["delMangaSuscription", e.message])
            raise e

    def run(self):

        while (True):

            i = 0

            # Manga by manga
            for item in self.mangaList.mangas:

                # Look for a new Chapter
                last = self.checkManga(item)

                # Compare with the latests one we had
                if last != self.mangaList.last_notified[i]:
                    # Notify followers if it's new
                    self.notifyManga(item)

                i += 1

            # After work done, we sleep
            time.sleep(self.sleepTime)


