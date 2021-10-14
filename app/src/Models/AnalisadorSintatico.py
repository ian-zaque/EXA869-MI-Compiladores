# -*- coding: utf-8 -*-
#coding: utf-8

class AnalisadorSintatico:
    
    def __init__(self, tokens):
        self.tokens = tokens['states']
        self.primitives_types = [
            'inteiro', 'real', 'booleano', 'char', 'cadeia', 'vazio'
        ]
        self.palavra = ''
    
    def parse(self):
        for idxToken, token in enumerate(self.tokens):
            print(token.getType())
            # CHAMAR FUNCAO START AQUI -- ELA VAI CONTER ::=
            #   <declaracao_reg> <declaration_const> <declaration_var> <function_declaration> | <var_atr> | <expressao>
            self.declaracao_const(token)
        
    
    # <declaration_const>  ::= constantes '{' <declaration_const1>
    def declaracao_const(self,token):
        print('PALAVRA',self.palavra)
        if token.getType() == 'IDE' and token.getWord() == 'constantes':
            self.palavra = token.getWord() + self.palavra
            self.declaracao_const(token)
            
            if token.getType() == 'DEL':
                self.palavra = token.getWord() + self.palavra
                self.declaracao_const(token)
                
            elif token.getType() == 'IDE' and token.getWord() in self.primitives_types:
                self.palavra = token.getWord() + self.palavra
                self.declaracao_const1(token)
            
        else:
            #erro
            print('erro',self.palavra)
    
    
    # <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
    def declaracao_const1(self,token):
        print('PALAVRA 1',self.palavra)
        
        #FIRST DERIV.
        if token.getType() == 'IDE':
            self.palavra = token.getWord() + self.palavra
            self.declaracao_const1(token)
            
            if token.getType() == 'REL':
                self.palavra = token.getWord() + self.palavra
                self.declaracao_const1(token)
                
            elif token.getType() == 'PRE':
                self.declaracao_const1(token)
                
            elif token.getType() == 'DEL':
                self.palavra = token.getWord() + self.palavra
                self.declaracao_const2(token)
        
        #SECOND DERIV.
        elif token.getType() == 'DEL':
            # FIM DERIVACAO 2
            print('fim',self.palavra)
            
        else:
            #erro
            print('erro',self.palavra)
    
    #<declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
    def declaracao_const2(self,token):
        print('PALAVRA 2',self.palavra)
        
        #FIRST DERIV.
        if token.getType() == 'IDE':
            self.palavra = token.getWord() + self.palavra
            self.declaracao_const2(token)
            
            if token.getType() == 'PRE':
                self.palavra = token.getWord() + self.palavra
                self.declaracao_const1(token)

            elif token.getType() == 'DEL':
                self.declaracao_const2(token)
                
        #SECOND DERIV.
        elif token.getType() == 'DEL':
            self.palavra = token.getWord() + self.palavra
            self.declaracao_const1(token)
        
        else:
            #erro
            print('erro',self.palavra)
        