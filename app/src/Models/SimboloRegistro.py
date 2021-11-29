# -*- coding: utf-8 -*-
# coding: utf-8

class SimboloRegistro:
    
    def __init__(self, nome, atributos):
        self.nome = nome
        self.atributos = atributos

    def getNome(self):
        return self.nome

    def getAtributos(self):
        return self.atributos
    
    def toString(self):
        print('\n')
        print('-------------')
        print('| Nome -',self.getNome())
        print('| Atributos -',self.getAtributos())
        print('-------------')
        