# -*- coding: utf-8 -*-
#coding: utf-8
class Token:
    def __init__(self, word, type, line):
        self.word = word
        self.type = type
        self.line = line

    def getType(self):
        return self.type

    def getWord(self):
        return self.word

    def getLine(self):
        return self.line

    def toString(self):
        line = self.line
        typeToken = self.type
        word = self.word
        return {line, typeToken, word}
