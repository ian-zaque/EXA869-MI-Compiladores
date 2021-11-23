# -*- coding: utf-8 -*-
# coding: utf-8

class SimboloVarConst:
    
    def __init__(self, nome, tipo, categoria, dimensao, escopo, init):
        self.nome = nome
        self.tipo = tipo
        self.categoria = categoria
        self.dimensao = dimensao
        self.escopo = escopo
        self.init = init

    def getNome(self):
        return self.nome

    def getTipo(self):
        return self.tipo

    def getCategoria(self):
        return self.categoria
    
    def getDimensao(self):
        return self.dimensao
    
    def getEscopo(self):
        return self.escopo
    
    def getInit(self):
        return self.init
    
    def toString(self):
        print('\n')
        print('-------------')
        print('| Nome -',self.getNome())
        print('| Tipo -',self.getTipo())
        print('| Categoria -',self.getCategoria())
        print('| Dimensao -',self.getDimensao())
        print('| Escopo -',self.getEscopo())
        print('| Init -',self.getInit())
        print('-------------')
    