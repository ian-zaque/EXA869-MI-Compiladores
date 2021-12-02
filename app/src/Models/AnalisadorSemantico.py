# -*- coding: utf-8 -*-
# coding: utf-8

from SimboloVarConst import *
from SimboloFuncao import *
from SimboloRegistro import *

class AnalisadorSemantico:
    
    def __init__(self):
        self.tabelaSimbolosVarConst = []
        self.tabelaSimbolosFuncao = []
        self.tabelaSimbolosRegistro = []
        
    def isSimboloInTabelaVarConst(self,symbol):
        isInTable = False
        
        for value in self.tabelaSimbolosVarConst:
            if isInTable == True:
                break
            else:
                for item in value.values():
                    if item.getNome() == symbol:
                        isInTable = True
                        break
                    
                    elif item.getNome() != symbol or (item.getNome() == symbol and item.getEscopo() == 'local'):
                        isInTable = False
                    
        return isInTable
    
    def isSimboloInTabelaFuncao(self,symbol):
        isInTable = False
        
        for value in self.tabelaSimbolosFuncao:
            if isInTable == True:
                break
            else:
                for item in value.values():
                    if item.getHash() == symbol:
                        isInTable = True
                        break
                    
                    elif item.getHash() != symbol:
                        isInTable = False
                        
        return isInTable
    
    def isSimboloInTabelaRegistro(self,symbol):
        isInTable = False
        
        for value in self.tabelaSimbolosRegistro:
            if isInTable == True:
                break
            else:
                for item in value.values():
                    if item.getNome() == symbol:
                        isInTable = True
                        break
                    
                    elif item.getNome() != symbol:
                        isInTable = False
                        
        return isInTable

    def isAtributoInRegistro(self,symbol,atributos):
        isInRegistro = False
        for value in atributos:
            if isInRegistro == True:
                break
            else:
                if value['nome'] == symbol:
                    isInRegistro = True
                    break
                
                elif value['nome'] != symbol:
                    isInRegistro = False
                        
        return isInRegistro

    def addSimboloVarConst(self,symbol):
        self.tabelaSimbolosVarConst.append({symbol.getNome(): symbol})
        self.printTabelaVarConst()
        return symbol
        
    def addSimboloFuncao(self,symbol):
        self.tabelaSimbolosFuncao.append({symbol.getHash(): symbol})
        return symbol
    
    def addSimboloRegistro(self,symbol):
        self.tabelaSimbolosRegistro.append({symbol.getNome(): symbol})
        return symbol
    
    def getSimboloFuncao(self,symbol):       
        for value in self.tabelaSimbolosFuncao:
            for item in value.values():
                if item.getHash() == symbol:
                    return item
    
        return False
    
    def getSimboloVarConst(self,symbol):
        isInTable = False
        simbolo = None
        
        for value in self.tabelaSimbolosVarConst:
            if isInTable == True:
                break
            else:
                for item in value.values():
                    if item.getNome() == symbol:
                        isInTable = True
                        simbolo = item
                        break
                    
                    elif item.getNome() != symbol:
                        isInTable = False
                        simbolo = None
                    
        return simbolo
    
    def getSimboloRegistro(self,symbol):
        isInTable = False
        simbolo = None
        
        for value in self.tabelaSimbolosRegistro:
            if isInTable == True:
                break
            else:
                for item in value.values():
                    if item.getNome() == symbol:
                        isInTable = True
                        simbolo = item
                        break
                    
                    elif item.getNome() != symbol:
                        isInTable = False
                        simbolo = None
                    
        return simbolo
    
    def updateTabelaVarConst(self,symbol,valor):
        for (key,values) in enumerate(self.tabelaSimbolosVarConst):
            for value in values.values():
                if value.getNome() == symbol:
                    value.setInit(valor)
                    break
    
    def getTabelaSimbolosVarConst(self):
        return self.tabelaSimbolosVarConst
    
    def getTabelaSimbolosFuncao(self):
        return self.tabelaSimbolosFuncao
    
    def printTabelaVarConst(self):        
        for value in self.tabelaSimbolosVarConst:
            for item in value.values():
                item.toString()        
    
    def printTabelaFuncao(self):
        for value in self.tabelaSimbolosFuncao:
            for item in value.values():
                item.toString()
                
    def printTabelaRegistro(self):
        for value in self.tabelaSimbolosRegistro:
            for item in value.values():
                item.toString()  
    