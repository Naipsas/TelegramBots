#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018
#
# DB manager class

import sqlite3

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class DBmanager:

    def __init__(self, file):
        self.db_con = sqlite3.connect(file)

    def createUserTable(self, user):
        query_list = ["CREATE TABLE ", user,
         " (manga TEXT PRIMARY KEY     NOT NULL,"
         "  notificado TEXT            NOT NULL);"]
        createQuery = "".join(query_list)
        self.db_con.execute(createQuery)

    def deleteUserTable(self, user):
        query_list = ["DROP TABLE ", user, ";"]
        deleteQuery = "".join(query_list)
        self.db_con.execute(deleteQuery)

    def readUserTable(self, user):
        query_list = ["SELECT * FROM ", user, ";"]
        readQuery = "".join(query_list)
        return self.db_con.execute(readQuery)

    def addMangaToUser(self, user, manga, notificado):
        query_list = ["INSERT INTO ", user,
         " (manga, notificado)",
         "  VALUES (\"",
         manga, "\", \"", notificado, "\");"]
        insertQuery = "".join(query_list)
        self.db_con.execute(insertQuery)
        self.db_con.commit()

    def delMangaFromUser(self, user, manga):
        query_list = ["DELETE * FROM ", user,
         " WHERE manga = \"", manga, "\";"]
        deleteQuery = "".join(query_list)
        self.db_con.execute(deleteQuery)

    def readMangaFromUser(self, user, manga):
        query_list = ["SELECT * FROM ", user,
         " WHERE manga = \"", manga, "\";"]
        askQuery = "".join(query_list)
        return self.db_con.execute(askQuery)

    def updateMangaFromUser(self, user, manga, notificado):
        query_list = ["UPDATE ", user,
         " set notificado = \"", notificado, "\" ",
         "  where manga = \"", manga, "\";"]
        updateQuery = "".join(query_list)
        self.db_con.execute(updateQuery)
        self.db_con.commit()

    def closeDB(self):
        self.db_con.close()