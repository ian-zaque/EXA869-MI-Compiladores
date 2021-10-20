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
    
    def isPrimitiveType(self,word):
        return word in self.primitives_types
    
    def parse(self):
        self.getNextToken()
        self.start()
    
    # <Program> ::= <declaracao_reg> <declaration_const> <declaration_var> <function_declaration> | <var_atr> | <expressao>
    def start(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            self.declaracao_reg()
            
            self.getNextToken()
            self.declaracao_const()
        
            self.getNextToken()
            self.declaracao_var()
    
    # <declaration_const>  ::= constantes '{' <declaration_const1>
    def declaracao_const(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('CONSTANTES_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())
            
            ############## constantes ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'constantes':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const()
            ############## fim constantes ##############
            
            
            ############## '{' ##############
            if self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const()
            ############## fim '{' ##############
            
            
            ############## <declaracao_const1> ##############
            elif self.getToken().getType() == 'PRE' and self.isPrimitiveType(self.getToken().getWord()):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim <declaracao_const1> ##############
            
            
            ############## '}' ############## 
            # 2 DERIVACAO DE <declaracao_const1>. FECHAMENTO DE BLOCO VAZIO DE CONSTANTE
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_constantes',self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############
            
            
            ############## erro ##############
            else:
                print('erro 0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
    def declaracao_const1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('CONSTANTES_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())
            
            #FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim id ##############
            
            
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim '=' ##############
            
            
            ############## <value> ##############    
            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'PRE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim <value> ##############
            
            
            ############## <declaracao_const2> ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() != '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim <declaracao_const2> ##############
            
            
            #SECOND DERIV.
            ############## '}' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
                # FIM DERIVACAO 2
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_constantes',self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############
                
                
            ############## erro ##############
            else:
                print('erro 1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
        
    # <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
    def declaracao_const2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('CONSTANTES_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())
            
            #FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim id ##############    
                
            
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim '=' ##############

            
            ############## <value> ##############
            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'PRE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim <value> ##############


            ############## declaracao_const2> ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() != ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim <declaracao_const2> ##############
            
                    
            #SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim ';' ##############
            
            
            ############## erro ##############
            else:
                print('erro 2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
    # <declaration_var>  ::= variaveis '{' <declaration_var1>
    def declaracao_var(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('VARIAVEIS_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())
            
            ############## 'variaveis' ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'variaveis':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var()
            ############## fim 'variaveis' ##############
            
            
            ############## '{' ##############   
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var()
            ############## fim '}' ##############


            ############## <declaracao_var1> ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            ############## fim <declaracao_var1> ##############
            
            
            ############## '}' ############## 
            # 2 DERIVACAO DE <declaracao_var1>. FECHAMENTO DE BLOCO  DE VARIAVEL
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_variaveis',self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############
            
            
            ############## erro ##############
            else:
                print('erro_variaveis_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
            
    # <declaration_var1> ::= <type> id <declaration_var2> | '}'
    def declaracao_var1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('VARIAVEIS_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())

            #FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            ############## fim id ##############
            

            ############## <declaracao_var2> ##############
            #add teste de vetor e matriz
            elif self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim <declaracao_var2> ##############
            
            
            ############## erro ##############
            else:
                print('erro_variaveis_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    # <declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
    def declaracao_var2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('VARIAVEIS_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())

            #FIRST DERIV.
            ############## <value> ##############
            if self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'PRE' or self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim <value> ##############
            
            
            ############## '=' ##############
            elif self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim '=' ##############
            
            
            #SECOND DERIV.
            ############## <vector_matrix> ##############
            # TESTAR INICIO DE MATRIZ E VETOR AQUI
            ############## fim <vector_matrix> ##############
            
            
            #LAST PART OF FIRST DERIV. AND THIRD DERIV.
            ############## <declaracao_var3> ##############
            elif self.getToken().getType() == 'DEL' and (self.getToken().getWord() == ',' or self.getToken().getWord() == ';'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim <declaracao_var3> ##############
            
            
            ############## erro ##############
            else:
                print('erro_variaveis_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    # <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1>
    def declaracao_var3(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('VARIAVEIS_3',self.palavra)
            print('TOKEN_3',self.getToken().getWord())

            #FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim id ##############
            
            
            ############## <declaracao_var2> ##############
            #add teste de matriz/vetor aqui para declaracao var 2
            elif self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim <declaracao_var2> ##############
            
            
            #SECOND DERIV.
            ############## <declaracao_var1> ##############
            elif (self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            ############## fim <declaracao_var1> ##############
            
            
            ############## '}' ############## 
            # 2 DERIVACAO DE <declaracao_var1>. FECHAMENTO DE BLOCO  DE VARIAVEL
            elif self.getToken().getWord() == '}':
                return self.declaracao_var()
            ############## fim '}' ##############
            
            
            ############## erro ##############
            else:
                print('erro_variaveis_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
        
    
    # <declaracao_reg> ::= registro id '{' <declaracao_reg1> |
    def declaracao_reg(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('REGISTRO_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            #FIRST DERIV.
            ############## registro ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'registro':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim registro ##############
            
            
            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim id ##############
            
            
            ############## '{' ##############   
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim '{' ##############
            
            
            ############## '}' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_registro_1',self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############
            
            
            ############## <declaracao_reg1> ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg1()
            ############## fim <declaracao_reg1> ##############
    
            
            ############## erro ##############
            else:
                print('erro_registro_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <declaracao_reg1> ::= <primitive_type> id <declaracao_reg4> <declaracao_reg2> | id id <declaracao_reg4> <declaracao_reg2> 
    def declaracao_reg1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('REGISTRO_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())

            #FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg1()
            ############## fim id ##############
            
            
            ############## <v_m_access> OR VAZIO ##############
            # TESTAR ACESSO DE MATRIZ E VETOR AQUI
                # self.palavra = self.palavra + self.getToken().getWord() + '$'
                # self.getNextToken()
                # return self.declaracao_reg4()
            ############## fim <v_m_access> OR VAZIO ##############

            
            #SECOND DERIV. OR <declaracao_reg2>
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg2()

            
            ############## erro ##############
            else:
                print('erro_registro_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <declaracao_reg2>  ::= ',' id <declaracao_reg2> | ';' <declaracao_reg5>
    def declaracao_reg2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('REGISTRO_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())

            #FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg2()
            ############## fim id ##############
            

            ############## ',' ##############
            elif self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg2()
            ############## fim ',' ##############

            
            # SECOND DERIV.
            ############## ';' ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg2()
            ############## fim ';' ##############


            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_registro_2',self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim '}' ##############    
                
                
            ############## erro ##############
            else:
                print('erro_registro_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
    # <declaracao_reg3>   ::= '}' <declaracao_reg>
    def declaracao_reg3(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('REGISTRO_3',self.palavra)
            print('TOKEN_3',self.getToken().getWord())

            ############## '}' ##############
            if self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_registro_3',self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim '}' ##############
    

            ############## erro ##############
            else:
                print('erro_registro_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    # <declaracao_reg4>   ::= <v_m_access> |
    def declaracao_reg4(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('REGISTRO_4',self.palavra)
            print('TOKEN_4',self.getToken().getWord())

            #FIRST DERIV.
            
    
    # <declaracao_reg5> ::= <declaracao_reg1> | <declaracao_reg3>
    def declaracao_reg5(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('REGISTRO_5',self.palavra)
            print('TOKEN_5',self.getToken().getWord())

            #FIRST DERIV.
            ############## <declaracao_reg1> ##############
            if self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg1()
            ############## fim id ##############
            
            
            #SECOND DERIV.
            ############## <declaracao_reg3> ##############
            elif self.getToken().getWord() == 'registro':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_reg3()
            ############## fim '}' ##############
            
            
            ############## erro ##############
            else:
                print('erro_registro_5',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            