#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

import urllib2
import logging

from emoji import emojize

from MParser import MParser

# Logs Texts - Templates
bot_icon = emojize(":computer:", use_aliases=True)
bot_log = bot_icon + ' SeekedManga - Funcion: %s - Mensaje: %s'

ok_icon = emojize(":white_check_mark:", use_aliases=True)
info_icon = emojize(":information_source: ", use_aliases=True)
warn_icon = emojize(":warning:", use_aliases=True)
error_icon = emojize(":red_circle:", use_aliases=True)
critical_icon = emojize(":black_circle:", use_aliases=True)

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class SeekedManga:

    def __init__(self, name, last, logger):
        self.name = name
        self.last_notified = 0
        self.suscriptors = []

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

    def addSuscriber(self, user, chat_id):
        found = False
        for item in self.suscriptors:
            if item[0] == user:
                found = True

        if not found:
            self.suscriptors.append([user, chat_id])
            self.log("info", ["addSuscriber", user + " añadido a " + self.name])
        else:
            self.log("info", ["addSuscriber", user + " ya suscrito a " + self.name])
            #raise Exception(user + " ya suscrito a " + manga)

    def deleteSuscriber(self, user, chat_id):
        found = False
        for item in self.suscriptors:
            if item[0] == user:
                self.suscriptors.remove(item)
                self.log("info", ["deleteSuscriber", user + " eliminado de " + self.name])
                found = True

        if not found:
            raise Exception("El usuario no está suscrito")

    def checkSuscriber(self, user):
        found = False
        for item in self.suscriptors:
            if item[0] == user:
                found = True

        return found

    def checkManga(self):
        newAvailable = False
        # Check if new chapter is available
        try:

            hdr = {'User-Agent':'Mozilla/5.0'}
            req = urllib2.Request('https://www.mangapanda.onl/', headers=hdr)

            try:
                page = urllib2.urlopen(req)
            except urllib2.HTTPError, e:
                print e.fp.read()

            myParser = MParser()
            myParser.feed(page.read())

            for item in myParser.items:
                if self.name.lower() in item.title.lower():
                    for chapter in item.chapters:
                        print chapter.number + " - " + str(self.last_notified)
                        if float(chapter.number) > float(self.last_notified):
                            self.last_notified = chapter.number
                            myChapter = chapter
                            newAvailable = True

            page.close()
        except Exception as e:
            page.close()
            #self.log("warning", ["checkManga", "No se ha podido conectar con la URL"])
            print e.message

        if newAvailable:
            newChapter = "#" + myChapter.number + " " + myChapter.title
            self.log("info", ["checkManga", self.name + " ahora tiene el capítulo:  " + newChapter])
            self.notifyUsers(newChapter, myChapter.link)

    def notifyUsers(self, chapter, link):
        self.log("info", ["notifyUsers", manga + " está siendo notificado a los suscriptores!"])

        msg = [ok_icon, " *Capítulo disponible*:\n\n",
                manga + " - " + "[" + chapter + "](" + link + ")" ]

        for user in self.suscriptors:
            bot.send_message(chat_id=user[1],
                text="".join(msg),
                parse_mode=telegram.ParseMode.MARKDOWN)

