# -*- coding: utf-8 -*-
# coding: utf-8

class SimboloFuncao:
    
    def __init__(self, nome, retorno, qtdParam, param):
        self.nome = nome
        self.retorno = retorno
        self.qtdParam = qtdParam
        self.param = param
        self.uniqueName = self.setHashFuncao()
        self.hash = hash(self.uniqueName)

    def getNome(self):
        return self.nome

    def getRetorno(self):
        return self.retorno

    def getQtdParam(self):
        return self.qtdParam
    
    def getParam(self):
        return self.param
    
    def getHash(self):
        return self.hash
    
    def getUniqueName(self):
        return self.uniqueName
    
    def setHashFuncao(self):
        toHash = self.nome + str(self.qtdParam) + ''.join(self.param)
        return toHash
    
    def toString(self):
        print('\n')
        print('-------------')
        print('| Nome -',self.getNome())
        print('| Retorno -',self.getRetorno())
        print('| QtdParam -',self.getQtdParam())
        print('| Param -',self.getParam())
        print('| Hash -',self.getHash())
        print('| Unique Name -',self.getUniqueName())
        print('-------------')
        