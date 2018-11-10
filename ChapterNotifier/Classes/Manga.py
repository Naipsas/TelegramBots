#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

class Manga:

    def __init__(self, name="", notified="0"):
        if name == "":
            raise Exception("El nombre de un manga no puede estar vacío")
        else:
            self.name = name
            self.notified = str(notified)
