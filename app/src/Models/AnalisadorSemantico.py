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
                for item in value.values():
                    if item.getNome() == symbol:
                        isInRegistro = True
                        break
                    
                    elif item.getNome() != symbol:
                        isInRegistro = False
                        
        return isInRegistro

    def addSimboloVarConst(self,symbol):
        self.tabelaSimbolosVarConst.append({symbol.getNome(): symbol})
        self.printTabelaVarConst()
        return symbol
        
    def addSimboloFuncao(self,symbol):
        self.tabelaSimbolosFuncao.append({symbol.getHash(): symbol})
        self.printTabelaFuncao()
        return symbol
    
    def addSimboloRegistro(self,symbol):
        self.tabelaSimbolosFuncao.append({symbol.getHash(): symbol})
        self.printTabelaFuncao()
        return symbol
    
    def getSimboloFuncao(self,symbol):       
        for value in self.tabelaSimbolosFuncao:
            for item in value.values():
                if item.getHash() == symbol:
                    return value
    
        return False
    
    def getSimboloVarConst(self,symbol):        
        for value in self.tabelaSimbolosVarConst:
            for item in value.values():
                if item.getNome() == symbol:
                    return value
    
        return False
    
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
    