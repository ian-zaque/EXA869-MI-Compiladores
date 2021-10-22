# -*- coding: utf-8 -*-
# coding: utf-8

from Token import Token


class AnalisadorSintatico:

    def __init__(self, tokens):
        self.errors = tokens['errors']
        self.tokens = tokens['states']
        self.tokens.append(Token("EOF", "EOF", -1))
        self.counter = 0
        self.primitives_types = ['inteiro', 'real',
                                 'booleano', 'char', 'cadeia', 'vazio']
        self.palavra = ''
        self.grammars = ['constantes', 'variaveis']
        self.grammar = 0

    def getCounter(self):
        return self.counter

    def getToken(self):
        if len(self.tokens) > 1:
            return self.tokens[0]
        else:
            return Token("EOF", "EOF", -1)

    def getNextToken(self):
        if len(self.tokens) > 1:
            if(len(self.grammars) > self.grammar+1):
                if(self.grammars[self.grammar+1] == self.tokens[0].getWord()):
                    self.grammar = self.grammar+1
            return self.tokens.pop(0)
        else:
            return Token("EOF", "EOF", -1)

    def lookahead(self, match):
        if len(self.tokens) > 1:
            return self.tokens[1].getWord() == match
        else:
            return Token("EOF", "EOF", -1)

    def follow(self):
        if len(self.tokens) > 1:
            return self.tokens[1].getWord()
        else:
            return Token("EOF", "EOF", -1)

    def isPrimitiveType(self, word):
        return word in self.primitives_types

    def parse(self, index):
        if len(self.errors) > 0:
            for i, lexema in enumerate(self.errors):
                lineTxt = str(lexema.getLine()+1) + ' ' + \
                    lexema.getType() + ' ' + lexema.getWord()
                print(lineTxt)
                print('\n')
            print(len(self.errors),
                  "erro(s) léxico(s) detectado no arquivo: entrada" + str(index) + '.txt')
            print('Por favor, corrija...')
            print('\n')

        self.errors = []
        self.getToken()
        self.start()

    # <Program> ::= <declaracao_reg> <declaration_const> <declaration_var> <function_declaration> | <var_atr> | <expressao>
    def start(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            self.declaracao_const()

            self.getNextToken()
            self.declaracao_var()

    def errorSintatico(self, match):
        if(self.follow() != 'EOF'):
            error = 'Linha ' + str(self.getToken().getLine()
                                   ) + ': Erro(s) sintatico(s) encontrado (' + self.getToken().getWord()
            for idx, k in enumerate(self.grammars):
                if k == self.grammars[self.grammar]:
                    if len(self.grammars) >= (idx + 1):
                        self.next_grammar = self.grammars[idx+1]
                        if len(self.tokens) > 1:
                            while self.follow() != self.next_grammar and self.follow() != 'EOF':
                                self.getNextToken()
                                error = error + ',' + self.getToken().getWord()
                            error = error + '). Pois era esperado o seguinte: ' + match
                            print(error)
                            self.errors.append(error)
        else:
            error = 'Linha ' + str(self.getToken().getLine()) + \
                ': Fim de arquivo encontrado era esperado o seguinte:' + match
            print(error)
            self.errors.append(error)
            return

    # <declaration_const>  ::= constantes '{' <declaration_const1>
    def declaracao_const(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('CONSTANTES_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############## constantes ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'constantes':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                if(self.lookahead('{')):
                    self.getNextToken()
                    return self.declaracao_const()
                else:
                    self.errorSintatico('{')
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
                print('fim_constantes', self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############

            ############## erro ##############
            else:

                print('erro 0', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'

    def declaracao_const1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('CONSTANTES_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
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

            # SECOND DERIV.
            ############## '}' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
                # FIM DERIVACAO 2
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                print('fim_constantes', self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############

            ############## erro ##############
            else:
                print('erro 1', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
    def declaracao_const2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('CONSTANTES_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
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

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim ';' ##############

            ############## erro ##############
            else:
                print('erro 2', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <declaration_var>  ::= variaveis '{' <declaration_var1>
    def declaracao_var(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('VARIAVEIS_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

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
                print('fim_variaveis', self.palavra, '\n')
                self.palavra = ''
                return
            ############## fim '}' ##############

            ############## erro ##############
            else:
                print('erro_variaveis_0', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <declaration_var1> ::= <type> id <declaration_var2> | '}'

    def declaracao_var1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('VARIAVEIS_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var1()
            ############## fim id ##############

            ############## <declaracao_var2> ##############
            # add teste de vetor e matriz
            elif self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim <declaracao_var2> ##############

            ############## erro ##############
            else:
                print('erro_variaveis_1', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
    def declaracao_var2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('VARIAVEIS_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
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

            # SECOND DERIV.
            ############## <vector_matrix> ##############
            # TESTAR INICIO DE MATRIZ E VETOR AQUI
            ############## fim <vector_matrix> ##############

            # LAST PART OF FIRST DERIV. AND THIRD DERIV.
            ############## <declaracao_var3> ##############
            elif self.getToken().getType() == 'DEL' and (self.getToken().getWord() == ',' or self.getToken().getWord() == ';'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim <declaracao_var3> ##############

            ############## erro ##############
            else:
                print('erro_variaveis_2', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1>
    def declaracao_var3(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('VARIAVEIS_3', self.palavra)
            print('TOKEN_3', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim id ##############

            ############## <declaracao_var2> ##############
            # add teste de matriz/vetor aqui para declaracao var 2
            elif self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim <declaracao_var2> ##############

            # SECOND DERIV.
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
                print('erro_variaveis_2', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
