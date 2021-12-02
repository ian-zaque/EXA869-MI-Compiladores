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
    
    def printAtributos(self):
        atrs = ''
        for value in self.atributos:
            if len(atrs) == 0:
                atrs = value['nome']
            else:
                atrs = atrs + ', ' + value['nome']
        return atrs
    
    def getTipoDeAtributo(self,field):
        tipo = None
        
        for value in self.atributos:
            if value['nome'] == field:
                tipo = value['tipo']
                break
            else:
                tipo = None
                
        return tipo
        
    def toString(self):
        print('\n')
        print('-------------')
        print('| Nome -',self.getNome())
        print('| Atributos -',self.getAtributos())
        print('-------------')
        