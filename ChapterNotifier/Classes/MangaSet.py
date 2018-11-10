#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

from Manga import Manga

class MangaSet:

    def __init__(self, user=""):
        if user == "":
            raise Exception("El usuario de una colección no puede estar vacío")
        else:
            self.user = user
            self.mangas = []

    def addManga(self, manga):
        found = False

        for item in self.mangas:
            if item.name == manga.name:
                found = True

        if found:
            raise Exception("El manga ya existe en la colección")
        else:
            self.mangas.append(manga)

    def deleteManga(self, name):
        if name == "":
            raise Exception("El nombre de un manga no puede estar vacío")
        else:
            found = False
            for item in self.mangas:
                if item.name == name:
                    self.mangas.remove(item)
                    found = True

            if not found:
                raise Exception("El manga no existe en la colección")

    def deleteAll(self):
        for item in self.mangas:
            self.mangas.remove(item)

    def getManga(self, name):
        if name == "":
            raise Exception("El nombre del manga no puede estar vacío")
        else:
            index = -1
            for item in self.mangas:
                if item.name == name:
                    index = self.mangas.index(item)

            if index >= 0:
                return self.mangas[index]
            else:
                raise Exception("El manga no existe en la colección")

    def updateManga(self, name, notified):
        if name == "":
            raise Exception("El nombre del manga no puede estar vacío")
        else:
            found = False
            for item in self.mangas:
                if item.name == name:
                    item.notified = notified
                    found = True

            if not found:
                raise Exception("El manga no existe en la colección")