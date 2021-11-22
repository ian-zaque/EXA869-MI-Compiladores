# -*- coding: utf-8 -*-
# coding: utf-8

from SimboloVarConst import *
from SimboloFuncao import *

class AnalisadorSemantico:
    
    def __init__(self):
        self.tabelaSimbolosVarConst = []
        self.tabelaSimbolosFuncao = []
        

    def addSimboloVarConst(self,symbol):
        # isInTable = False
        
        # for value in self.tabelaSimbolosVarConst:
        #     if value.getNome() == symbol.getNome():
        #         isInTable = True
        #         break
        #     else:
        #         isInTable = False
        #         continue
        
        # if isInTable == False:
        print({symbol.getNome(): symbol})
        self.tabelaSimbolosVarConst.append({symbol.getNome(): symbol})
        return symbol
        # else:
        #     return False
        
    def addSimboloFuncao(self,symbol):
        # isInTable = False
        
        # for value in self.tabelaSimbolosFuncao:
        #     if value.getHash() == symbol.getHash():
        #         isInTable = True
        #         break
        #     else:
        #         isInTable = False
        #         continue
        
        # if isInTable == False:
        self.tabelaSimbolosFuncao.append({symbol.getHash(): symbol})
        return symbol
        # else:
        #     return False
    
    def getSimboloFuncao(self,symbol):       
        for value in self.tabelaSimbolosFuncao:
            if value.getHash() == symbol.getHash():
                return value
    
        return False
    
    def getSimboloVarConst(self,symbol):        
        for value in self.tabelaSimbolosVarConst:
            if value.getNome() == symbol.getNome():
                return value
    
        return False
    
    def getTabelaSimbolosVarConst(self):
        return self.tabelaSimbolosVarConst
    
    def getTabelaSimbolosFuncao(self):
        return self.tabelaSimbolosFuncao
    
    def printTabelaVarConst(self):        
        for value in self.tabelaSimbolosVarConst:
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',value)
            # print('Nome',value.getNome())
            # print('Tipo',value.getTipo())
            # print('Categoria',value.getCategoria())
            # print('Dimensao',value.getDimensao())
            # print('Escopo',value.getEscopo())
            # print('Init',value.getInit())
            
        
        
        
        
        