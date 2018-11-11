#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018
#
# DB manager class

import sqlite3
import threading

from Manga import Manga
from MangaSet import MangaSet

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class DBmanager:

    def __init__(self, file):
        self.db_con = sqlite3.connect(file, check_same_thread = False)
        self.lock = threading.Lock()

    def getAllUsernames(self):
        query_list = ["SELECT name FROM sqlite_master where type = 'table';"]
        askQuery = "".join(query_list)
        self.lock.acquire()
        result = self.db_con.execute(askQuery).fetchall()
        self.lock.release()
        return result

    def createUserTable(self, user):
        query_list = ["CREATE TABLE ", user,
         " (manga TEXT PRIMARY KEY     NOT NULL,"
         "  notificado TEXT            NOT NULL);"]
        createQuery = "".join(query_list)
        self.lock.acquire()
        self.db_con.execute(createQuery)
        self.lock.release()

    def deleteUserTable(self, user):
        query_list = ["DROP TABLE ", user, ";"]
        deleteQuery = "".join(query_list)
        self.lock.acquire()
        self.db_con.execute(deleteQuery)
        self.lock.release()

    def readUserTable(self, user):
        query_list = ["SELECT * FROM ", user, ";"]
        readQuery = "".join(query_list)
        self.lock.acquire()
        result = self.db_con.execute(readQuery)
        self.lock.release()
        return result

    def addMangaToUser(self, user, manga):
        query_list = ["INSERT INTO ", user,
         " (manga, notificado)",
         "  VALUES (\"",
         manga, "\", \"last\");"]
        insertQuery = "".join(query_list)
        self.lock.acquire()
        self.db_con.execute(insertQuery)
        self.db_con.commit()
        self.lock.release()

    def delMangaFromUser(self, user, manga):
        query_list = ["DELETE from ", user,
         " where manga = \"", manga, "\";"]
        deleteQuery = "".join(query_list)
        self.lock.acquire()
        self.db_con.execute(deleteQuery)
        self.lock.release()

    def readMangaFromUser(self, user, manga):
        query_list = ["SELECT * FROM ", user,
         " WHERE manga = \"", manga, "\";"]
        askQuery = "".join(query_list)
        self.lock.acquire()
        result = self.db_con.execute(askQuery)
        self.lock.release()
        return result

    def updateMangaFromUser(self, user, manga, notificado):
        query_list = ["UPDATE ", user,
         " set notificado = \"", notificado, "\" ",
         "  where manga = \"", manga, "\";"]
        updateQuery = "".join(query_list)
        self.lock.acquire()
        self.db_con.execute(updateQuery)
        self.db_con.commit()
        self.lock.release()

    def closeDB(self):
        self.lock.acquire()
        self.db_con.close()
        self.lock.release()