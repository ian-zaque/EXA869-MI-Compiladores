# -*- coding: utf-8 -*-
# coding: utf-8

class SimboloFuncao:
    
    def __init__(self, nome, retorno, qtdParam, params):
        self.nome = nome
        self.retorno = retorno
        self.qtdParam = qtdParam
        self.params = params
        self.uniqueName = self.setHashFuncao()
        self.hash = hash(self.uniqueName)

    def getNome(self):
        return self.nome

    def getRetorno(self):
        return self.retorno

    def getQtdParam(self):
        return self.qtdParam
    
    def getParams(self):
        return self.params
    
    def getHash(self):
        return self.hash
    
    def getUniqueName(self):
        return self.uniqueName
    
    def setHashFuncao(self):
        toHash = self.nome + str(self.qtdParam) + ''.join(self.params)
        return toHash
    
    def toString(self):
        print('\n')
        print('-------------')
        print('| Nome -',self.getNome())
        print('| Retorno -',self.getRetorno())
        print('| QtdParam -',self.getQtdParam())
        print('| Param -',self.getParams())
        print('| Hash -',self.getHash())
        print('| Unique Name -',self.getUniqueName())
        print('-------------')
        