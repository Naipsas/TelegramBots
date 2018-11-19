#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class SeekerList:

    def __init__(self):
        self.mangas = []
        self.last_notified = []
        self.followers = []
        self.chat_id = []

    def addManga(self, name, user, chat_id):
        index = -1
        for item in self.mangas:
            if item == name:
                index = self.mangas.index(item)

        if index != (-1):
            # Manga exist, does exist the user as well?
            try:
                index = self.followers[index].index(user)
                raise Exception("El usuario ya está suscrito")
            except ValueError as e:
                # Then this user is not in the list
                self.followers[index].append(user)
                self.chat_id[index].append(chat_id)
        else:
            self.mangas.append(name)
            self.last_notified.append("last")
            self.followers.append([user])
            self.chat_id.append([chat_id])

    def deleteManga(self, name, user, chat_id):
        if name == "":
            raise Exception("El nombre de un manga no puede estar vacío")
        else:
            for item in self.mangas:
                if item == name:
                    index = self.mangas.index(item)

                    self.followers[index].remove(user)
                    self.chat_id[index].remove(chat_id)

                    if len(self.followers[index]) == 0:
                        self.mangas.remove(item)
                        # Chapter numbers can be repeated among several mangas so
                        # we delete from the list like this
                        self.last_notified = self.last_notified[0:index] \
                        + self.last_notified[(index+1):len(self.last_notified)]

            if index == (-1):
                raise Exception("El manga no existe en la colección")