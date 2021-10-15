# -*- coding: utf-8 -*-
#coding: utf-8

from Token import Token

class AnalisadorSintatico:
    
    def __init__(self, tokens):
        self.tokens = tokens['states']
        self.tokens.append(Token("EOF","EOF",-1))
        self.counter = -1
        self.primitives_types = [
            'inteiro', 'real', 'booleano', 'char', 'cadeia', 'vazio'
        ]
        self.palavra = ''
    
    def getCounter(self):
        return self.counter
    
    def getToken(self):
        if self.counter < len(self.tokens):
            return self.tokens[self.counter]
        else:
            return Token("EOF","EOF",-1)
    
    def getNextToken(self):
        self.counter = self.counter + 1
        
        if self.counter < len(self.tokens):
            return self.tokens[self.counter]
        else:
            return Token("EOF","EOF",-1)
    
    def parse(self):
        #   <declaracao_reg> <declaration_const> <declaration_var> <function_declaration> | <var_atr> | <expressao>
        self.getNextToken()
        self.start()
    
    def start(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            self.declaracao_const()
        
            self.getNextToken()
            self.declaracao_var()
    
    # <declaration_const>  ::= constantes '{' <declaration_const1>
    def declaracao_const(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'constantes':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const()
                            
            if self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const()
                
            elif self.getToken().getType() == 'PRE' and self.getToken().getWord() in self.primitives_types:
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
                
            else:
                #erro
                print('erro 0',self.palavra)
                # self.getNextToken()
    
    
    # <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
    def declaracao_const1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('PALAVRA 1',self.palavra)
            
            #FIRST DERIV.
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
                
            if self.getToken().getType() == 'REL':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
                
            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'PRE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
                
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() != '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
            
            #SECOND DERIV.
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
                # FIM DERIVACAO 2
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_constantes',self.palavra, '\n')
                self.palavra = ''
                return
                
            else:
                #erro
                print('erro 1',self.palavra)
                # self.getNextToken()
    
    # <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
    def declaracao_const2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('PALAVRA 2',self.palavra)
            
            #FIRST DERIV.
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
                
            if self.getToken().getType() == 'REL':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()

            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'PRE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()

            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() != ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
                    
            #SECOND DERIV.
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            
            else:
                #erro
                print('erro 2',self.palavra)
                # self.getNextToken()
    
    # <declaration_var>  ::= variaveis '{' <declaration_var1>
    def declaracao_var(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('PALAVRA 3',self.palavra, self.getToken().getWord())
        
            #first deriv.
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'variaveis':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var()
                
            if self.getToken().getType() == 'DEL' and (self.getToken().getWord() == '{' or self.getToken().getWord() == ','):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var()
            
            elif (self.getToken().getWord() in self.primitives_types) or (self.getToken().getType() == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()

            else:
                #erro
                print('erro 3',self.palavra)
                # self.getNextToken()
        
    # <declaration_var1> ::= <type> id <declaration_var2> | '}'
    def declaracao_var1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('PALAVRA 4',self.palavra,self.getToken().getWord())
        
            #first deriv.
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            
            if self.getToken().getType() == 'DEL' and self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            
            if self.getToken().getType() == 'DEL' and self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
                
            if self.getToken().getType() == 'REL':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            
            # SECOND DERIV.
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
                #FIM
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_variaveis',self.palavra, '\n')
                self.palavra = ''
                return
            
            else:
                #erro
                print('erro 4',self.palavra)
                # self.getNextToken()
    
    # <declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
    def declaracao_var2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('PALAVRA 5',self.palavra)
            
            #first deriv.
            if self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'PRE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
                
            #SECOND DERIV.
            # elif token:
            #     self.palavra = token.getWord() + self.palavra
            #     #GO TO DEF. VECTOR_MATRIX
            
            #THIRD DERIV.
            elif self.getToken().getType() == 'DEL' and (self.getToken().getWord() == ',' or self.getToken().getWord() == ';'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
                
            else:
                #erro
                print('erro 5',self.palavra)
                # self.getNextToken()
    
    # <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1>
    def declaracao_var3(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('PALAVRA 6',self.palavra)
            
            #FRIST DERIV.
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            
            #SECOND DERIV.
            elif self.getToken().getType() == 'PRE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            
            else:
                #erro
                print('erro 6',self.palavra)
                # self.getNextToken()
                