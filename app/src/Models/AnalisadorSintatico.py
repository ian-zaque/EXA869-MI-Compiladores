# -*- coding: utf-8 -*-
# coding: utf-8

from Token import Token
from lexemas import Lexemas
import copy

class AnalisadorSintatico:

    def __init__(self, tokens):
        self.errors = copy.deepcopy(tokens['errors'])
        self.tokens = copy.deepcopy(tokens['states'])
        self.prevToken = []
        self.tokens.append(Token("EOF", "EOF", -1))
        self.counter = -1
        self.primitives_types = ['inteiro', 'real',
                                 'booleano', 'char', 'cadeia', 'vazio']
        self.palavra = ''
        self.grammars = ['registro', 'constantes', 'variaveis', 'funcao']
        self.grammar = 0

    def getCounter(self):
        return self.counter

    def getToken(self):
        if len(self.tokens) > 1:
            return self.tokens[0]
        else:
            return Token("EOF", "EOF", -1)

    def getPrevToken(self):
        if len(self.prevToken) > 0:
            return self.prevToken[-1]
        else:
            return Token("EOF", "EOF", -1)

    def getNextToken(self):
        if len(self.tokens) > 1:
            if(len(self.grammars) > self.grammar+1):
                if(self.grammars[self.grammar+1] == self.tokens[0].getWord()):
                    self.grammar = self.grammar+1
            self.prevToken.append(self.tokens[0])
            return self.tokens.pop(0)
        else:
            return Token("EOF", "EOF", -1)

    def lookahead(self, match):
        if len(self.tokens) > 1:
            return self.tokens[1].getWord() == match
        else:
            return Token("EOF", "EOF", -1).getWord()

    def forward(self):
        if len(self.tokens) > 1:
            return self.tokens[1].getWord()
        else:
            return Token("EOF", "EOF", -1).getWord()

    def isPrimitiveType(self, word):
        return word in self.primitives_types

    def isReservedWord(self, word):
        return word in Lexemas().getReservedWords()

    def isRelOperator(self,word):
        return word in ['<', '>', '==', '<=', '>=', '!=']
    
    def errorSintatico(self, match):
        if(self.forward() != 'EOF'):
            error = 'Linha ' + str(self.getToken().getLine()
                                   ) + ': Erro(s) sintatico(s) encontrado (' + self.palavra
            for idx, k in enumerate(self.grammars):
                if k == self.grammars[self.grammar]:
                    if len(self.grammars) >= (idx + 1):
                        self.next_grammar = self.grammars[idx+1]
                        if len(self.tokens) > 1:
                            while (self.getToken().getWord() != self.next_grammar and self.getToken().getWord() != self.grammars[self.grammar]) and self.forward() != 'EOF':
                                error = error + ',' + self.getToken().getWord()
                                self.getNextToken()
                            error = error + '). Pois era esperado: ' + match
                            print(error)
                            self.errors.append(error)
        else:
            error = 'Linha ' + str(self.getToken().getLine()) + \
                ': Fim de arquivo encontrado era esperado o seguinte:' + match
            print(error)
            self.errors.append(error)
            return

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
        self.start()

    # <Program> ::= <declaracao_reg> <declaration_const> <declaration_var> <function_declaration>
    def start(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            while (self.getToken().getWord() == 'registro'):
                self.declaracao_reg()

            while (self.getToken().getWord() == 'constantes'):
                self.declaracao_const()

            while (self.getToken().getWord() == 'variaveis'):
                self.declaracao_var()

            while (self.getToken().getWord() == 'funcao'):
                self.declaracao_funcao()

    # <declaracao_reg> ::= registro id '{' <declaracao_reg1> |
    def declaracao_reg(self):
        print('ok')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('REGISTRO_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            # FIRST DERIV.
            ############## registro ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'registro':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim registro ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == 'registro':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg()
                else:
                    self.errorSintatico('a palavra registro antes de um IDE')
                    self.palavra = ''
                    return
            ############## fim id ##############

            ############## '{' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg1()
                else:
                    self.errorSintatico('um IDE antes de {')
                    self.palavra = ''
                    return
            ############## fim '{' ##############

            ############## '}' ##############
            # elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
            #     self.palavra = self.palavra + self.getToken().getWord() + '$ '
            #     print('fim_registro_1',self.palavra, '\n')
            #     self.palavra = ''
            #     return
            ############## fim '}' ##############

            ############## vazio ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() != 'registro' and (not self.isPrimitiveType(self.getToken().getWord())):
                # self.palavra = self.getToken().getWord() + '$ '
                return
            ############## fim vazio ##############

            ############## erro ##############
            else:
                self.errorSintatico('uma Declaração de Registro correta')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg1> ::= <primitive_type> id <declaracao_reg4> <declaracao_reg2> | id id <declaracao_reg4> <declaracao_reg2>
    def declaracao_reg1(self):
        print('ok')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('REGISTRO_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            ############## <declaracao_reg1> ##############
            if (self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE') and self.getPrevToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_reg1()

            ############## fim <declaracao_reg1> ##############

            # FIRST DERIV.
            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.isPrimitiveType(self.getPrevToken().getWord()) or self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg1()
                else:
                    self.errorSintatico('um IDE ou PRE antes de um IDE')
                    self.palavra = ''
                    return
            ############## fim id ##############

            ############## <declaracao_reg4> OR VAZIO ##############
            elif self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg4()
                else:
                    self.errorSintatico('um IDE antes de [')
                    self.palavra = ''
                    return
            ############## fim <declaracao_reg4> OR VAZIO ##############

            # SECOND DERIV. OR <declaracao_reg2>
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ']' or self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg2()
                else:
                    self.errorSintatico(
                        'um IDE ou ] antes de ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            ############## erro ##############
            else:
                self.errorSintatico('um outro token em declaracao_reg1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg2>  ::= ',' id <declaracao_reg2> | ';' <declaracao_reg5>
    def declaracao_reg2(self):
        print('ok')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('REGISTRO_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE' and self.getPrevToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_reg2()
            ############## fim id ##############

            ############## ',' ##############
            elif self.getToken().getWord() == ',':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg2()
                else:
                    self.errorSintatico('um IDE antes da ,')
                    self.palavra = ''
                    return
            ############## fim ',' ##############

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg3()
                else:
                    self.errorSintatico('um IDE antes de ;')
                    self.palavra = ''
                    return

            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg1()
                else:
                    self.errorSintatico('um ; antes de IDE ou PRE')
                    self.palavra = ''
                    return
            ############## fim ';' ##############

            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    print('fim_registro_2', self.palavra, '\n')
                    self.palavra = ''
                    self.getNextToken()
                    return self.declaracao_reg()
                else:
                    self.errorSintatico(' ; antes de }')
                    self.palavra = ''
                    return
            ############## fim '}' ##############

            ############## erro ##############
            else:
                self.errorSintatico('um outro token em declaracao_reg2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg3>   ::= '}' <declaracao_reg>
    def declaracao_reg3(self):
        print('ok')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('REGISTRO_3', self.palavra)
            print('TOKEN_3', self.getToken().getWord())

            ############## '}' ##############
            if self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    print('fim_registro_3', self.palavra, '\n')
                    self.palavra = ''
                    self.getNextToken()
                    return self.declaracao_reg()
                else:
                    self.errorSintatico(' ; antes de }')
                    self.palavra = ''
                    return
            ############## fim '}' ##############

            if self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg1()
                else:
                    self.errorSintatico('um IDE ou PRE antes de ;')
                    self.palavra = ''
                    return

            ############## erro ##############
            else:
                self.errorSintatico('um outro token em declaracao_reg3')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg4>   ::= <v_m_access> |
    def declaracao_reg4(self):
        print('ok')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('REGISTRO_4', self.palavra)
            print('TOKEN_4', self.getToken().getWord())

            # FIRST DERIV.
            ############## <v_m_access> ##############
            if self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.v_m_access()
            ############## fim <v_m_access> ##############

            # elif self.getPrevToken().getWord() == ']' and (self.getToken().getWord() == ',' or self.getToken().getWord() == ';'):
            #     self.palavra = self.palavra + self.getToken().getWord() + '$ '
            #     return self.declaracao_reg2()

            ############## erro ##############
            else:
                self.errorSintatico('um IDE ou um NRO depois de [')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg5> ::= <declaracao_reg1> | <declaracao_reg3>
    def declaracao_reg5(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('REGISTRO_5', self.palavra)
            print('TOKEN_5', self.getToken().getWord())

            # FIRST DERIV.
            ############## <declaracao_reg1> ##############
            if self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_reg1()
            ############## fim <declaracao_reg1> ##############

            # SECOND DERIV.
            ############## <declaracao_reg3> ##############
            elif self.getToken().getWord() == 'registro':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_reg3()
            ############## fim '}' ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token5')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <v_m_access>  ::= '[' <v_m_access1>
    def v_m_access(self):
        print('error')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VM_ACCESS_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############## '[' ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.v_m_access1()
                else:
                    self.errorSintatico(' IDE antes de [')
                    self.palavra = ''
                    return
            ############## fim '[' ##############

            ############## <v_m_access1> ##############
            elif self.getToken().getWord() == '.' or self.getToken().getWord() == ']':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getType() == 'NRO':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.v_m_access1()
            ############## fim <v_m_access1> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em v_m_access_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <v_m_access1>  ::= id <v_m_access2> | number ']' <v_m_access3>
    def v_m_access1(self):

        print('test')

        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VM_ACCESS_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.v_m_access1()
            ############## fim id ##############

            ############## <v_m_access2> ##############
            elif (self.getToken().getWord() == '.' or self.getToken().getWord() == ']') and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.v_m_access2()
            ############## fim <v_m_access2> #############

            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_reg2()

            # SECOND DERIV.
            ############## ']' ##############
            elif self.getToken().getWord() == ']':
                if self.getPrevToken().getType() == 'NRO':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.v_m_access1()
                else:
                    self.errorSintatico(' NRO antes de ]')
                    self.palavra = ''
                    return
            ############## fim ']' ##############

            ############## <v_m_access3> ##############
            elif self.getToken().getWord() == '[':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.v_m_access3()
                else:
                    self.errorSintatico(' ] antes de [')
                    self.palavra = ''
                    return
            ############## fim <v_m_access3> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em v_m_access_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <v_m_access2>  ::= <elem_registro> ']' <v_m_access3> | ']' <v_m_access3>
    def v_m_access2(self):
        print('ok')
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VM_ACCESS_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
            ############## <elem_registro> ##############
            if self.getToken().getWord() == '.':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.elem_registro()
                else:
                    self.errorSintatico(' um IDE antes de .')
                    self.palavra = ''
                    return
            ############## fim <elem_registro> ##############

            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.declaracao_reg2()
                else:
                    self.errorSintatico(' ] antes de ;')
                    self.palavra = ''
                    return

            ############## ']' ##############
            # ADD TESTE DE ULTIMO CARACTER DE ELEM_REGISTRO
            elif self.getToken().getWord() == ']':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.v_m_access2()
                else:
                    self.errorSintatico(' ] antes de .')
                    self.palavra = ''
                    return

            ############## fim ']' ##############

            # SECOND DERIV.
            ############## <v_m_access3> ##############
            elif self.getToken().getWord() == '[':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + '$ '
                    self.getNextToken()
                    return self.v_m_access3()
                else:
                    self.errorSintatico(' ] antes de [')
                    self.palavra = ''
                    return
            ############## fim <v_m_access3> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em v_m_access_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <v_m_access3>  ::= '[' <v_m_access1> |
    def v_m_access3(self):
        print('ok')

        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VM_ACCESS_3', self.palavra)
            print('TOKEN_3', self.getToken().getWord())

            # FIRST DERIV.
            ##############  <v_m_access1> ##############
            if self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.v_m_access1()
            ############## fim <v_m_access1> ##############

            ############## erro ##############
            else:
                self.errorSintatico('uma IDE ou NRO em v_m_access_3')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <elem_registro>  ::= '.' id <nested_elem_registro>
    def elem_registro(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('elem_registro_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############## '.' ##############
            if self.getToken().getWord() == '.':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.elem_registro()
            ############## fim '.' ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.elem_registro()
            ############## fim id ##############

            ############## <nested_elem_registro> ##############
            elif self.getPrevToken().getWord() == '.' or self.getPrevToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.nested_elem_registro()
            ############## fim <nested_elem_registro> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em elem_registro_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <nested_elem_registro>  ::= '.' id <nested_elem_registro1> | <v_m_access> <nested_elem_registro1> |

    def nested_elem_registro(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('elem_registro_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############## '.' ##############
            if self.getToken().getWord() == '.':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.nested_elem_registro()
            ############## fim '.' ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.nested_elem_registro()
            ############## fim id ##############

            ############## <nested_elem_registro1> ##############
            elif self.getPrevToken().getType() == 'IDE' and self.getToken().getWord() == '.':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.nested_elem_registro1()
            ############## fim <nested_elem_registro1> ##############

            # SECOND DERIV.
            ############## <v_m_access> ##############
            elif self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.v_m_access()
            ############## fim <v_m_access> ##############

            ############## <nested_elem_registro1> ##############
            # TESTAR ULTIMO CARACTER DE V_M_ACCESS
            elif self.getPrevToken().getType() == 'IDE' and self.getToken().getWord() == '.':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.nested_elem_registro1()
            ############## fim <nested_elem_registro1> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em elem_registro_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <nested_elem_registro1> ::= <elem_registro> |
    def nested_elem_registro1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('elem_registro_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
            ############## <elem_registro> ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.v_m_access()
            ############## fim <elem_registro> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em elem_registro_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_const>  ::= constantes '{' <declaration_const1>
    def declaracao_const(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('CONSTANTES_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############## constantes ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'constantes':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                if(self.lookahead('{')):
                    self.getNextToken()
                    return self.declaracao_const()
                else:
                    self.errorSintatico('{')
            ############## fim constantes ##############

            ############## '{' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const()
            ############## fim '{' ##############

            ############## <declaracao_const1> ##############
            elif self.getToken().getType() == 'PRE' and self.isPrimitiveType(self.getToken().getWord()):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim <declaracao_const1> ##############

            ############## '}' ##############
            # 2 DERIVACAO DE <declaracao_const1>. FECHAMENTO DE BLOCO VAZIO DE CONSTANTE
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_constantes', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim '}' ##############

            if self.getToken().getType() == 'PRE' and self.getToken().getWord() != 'constantes' and (not self.isPrimitiveType(self.getToken().getWord())):
                return

            ############## erro ##############
            else:
                self.errorSintatico('Outro token0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
    def declaracao_const1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('CONSTANTES_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim id ##############

            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim '=' ##############

            ############## <value> ##############
            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim <value> ##############

            ############## <declaracao_const2> ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() != '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim <declaracao_const2> ##############

            # SECOND DERIV.
            ############## '}' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '}':
                # FIM DERIVACAO 2
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_constantes', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim '}' ##############

            if self.getToken().getType() == 'PRE' and self.getToken().getWord() != 'constantes' and (not self.isPrimitiveType(self.getToken().getWord())):
                return

            ############## erro ##############
            else:
                self.errorSintatico('Outro token1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
    def declaracao_const2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('CONSTANTES_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim id ##############

            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim '=' ##############

            ############## <value> ##############
            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim <value> ##############

            ############## declaracao_const2> ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() != ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const2()
            ############## fim <declaracao_const2> ##############

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_const1()
            ############## fim ';' ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var>  ::= variaveis '{' <declaration_var1>
    def declaracao_var(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VARIAVEIS_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############## 'variaveis' ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() == 'variaveis':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var()
            ############## fim 'variaveis' ##############

            ############## '{' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var()
            ############## fim '}' ##############

            ############## <declaracao_var1> ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var1()
            ############## fim <declaracao_var1> ##############

            ############## '}' ##############
            # 2 DERIVACAO DE <declaracao_var1>. FECHAMENTO DE BLOCO  DE VARIAVEL
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_variaveis', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim '}' ##############

            if self.getToken().getType() == 'PRE' and self.getToken().getWord() != 'variaveis' and (not self.isPrimitiveType(self.getToken().getWord())):
                return

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em variaveis_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var1> ::= <type> id <declaration_var2> | '}'
    def declaracao_var1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VARIAVEIS_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var1()
            ############## fim id ##############

            ############## <declaracao_var2> ##############
            elif self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';' or self.getToken().getWord() == '[':
                return self.declaracao_var2()
            ############## fim <declaracao_var2> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em variaveis_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
    def declaracao_var2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VARIAVEIS_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim '=' ##############
            
            ############## <value> ##############
            elif self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var2()
            ############## fim <value> ##############

            # SECOND DERIV.
            ############## <vector_matrix> ##############
            elif self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.vector_matrix()          
            ############## fim <vector_matrix> ##############

            # LAST PART OF FIRST DERIV. AND THIRD DERIV.
            ############## <declaracao_var3> ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim <declaracao_var3> ##############

            ############## erro ##############
            else:
                self.errorSintatico('Outro token em variaveis_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1>
    def declaracao_var3(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            print('VARIAVEIS_3', self.palavra)
            print('TOKEN_3', self.getToken().getWord())

            # FIRST DERIV.
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim '=' ##############            
            
            ############## id ##############
            if self.getToken().getType() == 'IDE' and self.getPrevToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim id ##############

            ############## <declaracao_var2> ##############
            elif (self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';' or self.getToken().getWord() == '[') and (self.getPrevToken().getType() == 'IDE'):
                return self.declaracao_var2()
            ############## fim <declaracao_var2> ##############

            # SECOND DERIV.
            ############## <declaracao_var1> ##############
            elif (self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
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
                self.errorSintatico('Outro token em variaveis_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_declaration>  ::= funcao <type> <function_declaration1>
    def declaracao_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('funcao_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############# funcao ##############
            if self.getToken().getWord() == 'funcao':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao()
            ############## fim funcao ##############

            ############## <type> ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao()
            ############## fim <type> ##############

            ############## <function_declaration1> ##############
            elif (self.getToken().getWord() == 'algoritmo' or self.getToken().getType() == 'IDE') and (self.isPrimitiveType(self.getPrevToken().getWord()) or self.getPrevToken().getType == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao1()
            ############## fim <function_declaration1> ##############

            if self.getToken().getType() == 'PRE' and self.getToken().getWord() != 'funcao' and (not self.isPrimitiveType(self.getToken().getWord())):
                return

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em funcao_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_declaration1> ::= algoritmo <main_function> | <function_declaration2>
    def declaracao_funcao1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('funcao_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############# algoritmo #############
            if self.getToken().getWord() == 'algoritmo':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao1()
            ############# fim algoritmo #############

            ############# <main_function> #############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getWord() == 'algoritmo':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.main_function()
            ############# fim <main_function> #############

            # SECOND DERIV.
            ############# <function_declaration2>  #############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# fim <function_declaration2> #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em funcao_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_declaration2> ::= id <function_parameters> '{' <function_body> '}' <function_declaration>
    def declaracao_funcao2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('funcao_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            # FIRST DERIV.
            ############# id #############
            if self.getToken().getType() == 'IDE' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# fim id #############

            elif self.getToken().getWord() == ')' and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()

            ############# <function_parameters> #############
            elif (self.getToken().getType() == 'IDE' or self.isPrimitiveType(self.getToken().getWord())) and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao()
            ############# fim <function_parameters> #############

            ############# '{' #############
            elif self.getPrevToken().getWord() == ')' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# fim '{' #############

            ############# <function_body> #############
            # TESTAR FUNCTION_BODY AQUI
            ############# fim <function_body> #############

            # ADD TESTE DE FUM DE CORPO DE FUNCAO OR getPrevToken().getWord == '{'
            ############# '}' #############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_declaracao_funcao_2', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return self.declaracao_funcao()
            ############# fim '}' #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em declaracao_funcao_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <main_function> ::= <function_parameters> '{' <function_body> '}'
    def main_function(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('main_function_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            # FIRST DERIV.
            if self.getToken().getWord() == ')' and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.main_function()

            ############# <function_parameters> #############
            elif (self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getWord() == ')') and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao()
            ############# fim <function_parameters> #############

            ############# '{' #############
            elif self.getPrevToken().getWord() == ')' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# fim '{' #############

            ############# <function_body> #############
            # TESTAR FUNCTION_BODY AQUI
            ############# fim <function_body> #############

            # ADD TESTE DE FUM DE CORPO DE FUNCAO
            ############# '}' #############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_main_function', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return self.declaracao_funcao()
            ############# fim '}' #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em main_function_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters>   ::= '(' <function_parameters1>
    def parametros_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('parametros_funcao_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############# '(' #############
            if self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao()
            ############# fim '(' #############

            ############# <function_parameters1>  #############
            elif (self.getToken().getType() == 'IDE' or self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getWord() == ')'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao1()
            ############# fim <function_parameters1>  #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em parametros_funcao_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters1>  ::= <function_parameters2> id <function_parameters3> | ')'
    def parametros_funcao1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('parametros_funcao_1', self.palavra)
            print('TOKEN_1', self.getToken().getWord())

            # FIRST DERIV.
            ############# id #############
            if (self.getPrevToken().getType() == 'IDE' or self.isPrimitiveType(self.getPrevToken().getWord())) and self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao1()
            ############# fim id #############

            ############# <function_parameters3> #############
            elif self.getPrevToken().getType() == 'IDE' and (self.getToken().getWord() == '[' or self.getToken().getWord() == ',' or self.getToken().getWord() == ')'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao3()
            ############# fim <function_parameters3> #############

            # SECOND DERIV.
            ############# ') #############
            # SE VEIO DE main_function() retornar main_function()
            # SE VEIO DE declaracao_funcao2() retornar declaracao_funcao2()
            elif self.getPrevToken().getWord() == ')' and self.getToken().getWord() == '{':
                print('fim_parametros_funcao_1', self.palavra, '\n')
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# ') #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em parametros_funcao_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters2>  ::= <primitive_type> | id

    # <function_parameters3>  ::= '[' ']' <function_parameters4>  | <function_parameters5>
    def parametros_funcao3(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('parametros_funcao_3', self.palavra)
            print('TOKEN_3', self.getToken().getWord())

            # FIRST DERIV.
            ############# ']' #############
            if self.getToken().getWord() == ']' and self.getPrevToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao3()
            ############# fim ']' #############

            ############# <function_parameters4> #############
            elif (self.getToken().getWord() == '[' or self.getToken().getWord() == ',' or self.getToken().getWord() == ')') and self.getPrevToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao4()
            ############# fim <function_parameters4> #############

            # SECOND DERIV.
            elif (self.getPrevToken().getWord() == ',' or self.getPrevToken().getWord() == ')'):
                return self.parametros_funcao5()

            ############# ') #############
            # TESTAR AQUI SE VEIO DE main_function() OU DE declaracao_funcao2()
            # SE VEIO DE main_function() retornar main_function()
            # SE VEIO DE declaracao_funcao2() retornar declaracao_funcao2()
            elif self.getPrevToken().getWord() == ')' and self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# ') #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em parametros_funcao_3')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters4>  ::= '[' ']' <function_parameters5>  | <function_parameters5>
    def parametros_funcao4(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('parametros_funcao_4', self.palavra)
            print('TOKEN_4', self.getToken().getWord())

            # FIRST DERIV.
            ############# ']' #############
            if self.getToken().getWord() == ']' and self.getPrevToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao4()
            ############# fim ']' #############

            ############# <function_parameters4> #############
            elif (self.getToken().getWord() == '[' or self.getToken().getWord() == ',' or self.getToken().getWord() == ')') and self.getPrevToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao5()
            ############# fim <function_parameters4> #############

            ############# erro ##############
            else:
                self.errorSintatico('Outro token em parametros_funcao_4')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters5>  ::= ','  <function_parameters1>  | ')'
    def parametros_funcao5(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('parametros_funcao_5', self.palavra)
            print('TOKEN_5', self.getToken().getWord())

            # FIRST DERIV.
            if (self.getToken().getType() == 'IDE' or self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getWord() == ')') and self.getPrevToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.parametros_funcao1()

            # SECOND DERIV.
            ############# ') #############
            # SE VEIO DE main_function() retornar main_function()
            # SE VEIO DE declaracao_funcao2() retornar declaracao_funcao2()
            elif self.getPrevToken().getWord() == ')' and self.getToken().getWord() == '{':
                print('fim_parametros_funcao_5', self.palavra, '\n')
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.declaracao_funcao2()
            ############# ') #############

            ############# erro ##############
            else:
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.errorSintatico('Outro token em parametros_funcao_5')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <var_atr> ::= <read_value> '=' <atr_value> <atr_1>

    def var_atr(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('var_atr_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############# <read_value> #############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.read_value()
            ############# fim <read_value> #############

            ############# '=' #############
            # TESTAR AQUI ULTIMO TOKEN DE read_value()
            elif self.getToken().getWord() == '=' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.var_atr()
            ############# fim '=' #############

            ############# <atr_value> #############
            elif self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or self.getToken().getType() == 'IDE' or self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!':
                return self.atr_value()
            ############# fim <atr_value> #############

            ############# <atr_1> FIRST DERIV. #############
            # ','
            elif self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                self.getNextToken()
                return self.atr_1()
            ############# fim <atr_1> #############

            ############# <atr_1> SECOND DERIV. #############
            # ';'
            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_var_atr_0', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############# <atr_1> #############

            ############# erro ##############
            else:
                print('erro_var_atr_0', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <read_value> ::= id <read_value0>

    def read_value(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('read_value_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            # <read_value0> ::= <v_m_access> | <elem_registro> | <>

            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.var_atr()

            ############## <read_value0> ##############
            # <v_m_access>
            elif (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO') and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.v_m_access()
            ############## fim <read_value0> ##############

            ############## <read_value0> ##############
            # <elem_registro>
            elif self.getToken().getWord() == '.' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.elem_registro()
            ############## fim <read_value0> ##############

            ############# erro ##############
            else:
                print('erro_read_value_0', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <atr_1> ::= ',' <var_atr> | ';'

    def atr_1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('atr_1', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            # FIRST DERIV.
            ############## <var_atr> ##############
            if self.getPrevToken().getWord() == ',' and self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.var_atr()
            ############## fim <var_atr> ##############

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_atr_1', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############# ';' #############

            ############# erro ##############
            else:
                print('erro_atr_1', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <atr_value> ::= <value_with_expressao> | <functionCall>

    def atr_value(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('atr_value_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            # FIRST DERIV.
            ############## <value_with_expressao> ##############
            if self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or self.getToken().getType() == 'IDE' or self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()                
            ############## fim <value_with_expressao> ##############
                
            #SECOND DERIV.
            ############## <functionCall> ##############
            if self.getToken().getWord() == '(' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.chamada_funcao()
            ############## fim <functionCall> ##############

            ############# erro ##############
            else:
                print('erro_atr_value_0', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <functionCall> ::= id '(' <varList0> ')' ';'

    def chamada_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('chamada_funcao_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            ############## id ##############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.chamada_funcao()
            ############## fim id ##############

            ############## '(' ##############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.chamada_funcao()
            ############## fim '(' ##############

            ############## <varList0> ##############
            elif (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso')) and (self.getPrevToken().getWord() == '('):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.var_list0()
            ############## fim <varList0> ##############

            ############## ')' ##############
            # ADD TESTE DE ULTIMO CARACTER DE <var_list0>
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.chamada_funcao()
            ############## fim ')' ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';' and self.getPrevToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_chamada_funcao_0', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim ';' ##############

    # <varList0> ::= <value> <varList2> | <read_value> <varList2> | <>

    def var_list0(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('varList_0', self.palavra)
            print('TOKEN_0', self.getToken().getWord())

            # FIRST DERIV. OR SECOND DERIV.
            ############## <varList2> ##############
            if self.getToken().getWord() == ',' and (self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getType() == 'CAD' or self.getPrevToken().getType() == 'CAR' or (self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso')):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.var_list2()
            ############## fim <varList2> ##############

            ############# erro ##############
            else:
                print('erro_varList_0', self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    # <varList1> ::= <value> <varList2> | <read_value> <varList2>
    # def var_list1(self):
    #     if self.getToken().getType() == 'EOF':
    #         return

    #     elif self.counter < len(self.tokens):
    #         print('varList_1',self.palavra)
    #         print('TOKEN_1',self.getToken().getWord())

    # <varList2> ::= ',' <varList1> | <>

    def var_list2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            print('varList_2', self.palavra)
            print('TOKEN_2', self.getToken().getWord())

            ############## <varList1> ##############
            if (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso')) and (self.getPrevToken().getWord() == ','):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.var_list2()
            ############## fim <varList1> ##############

            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.chamada_funcao()

            ############# erro ##############
            else:
                print('erro_varList_2', self.palavra)
                # self.getNextToken()
            ############## fim erro ############## 
    
    # <vector_matrix>   ::= '[' <expr_number> ']' <vector_matrix_1>
    def vector_matrix(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('vector_matrix_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())
            
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix()
            ############## fim '[' ##############
    
            ############## <expr_number> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == '(') and self.getPrevToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number()
            ############## fim <expr_number> ############## 

            ############## ']' ##############
            elif self.getToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix()
            ############## fim ']' ##############

            ############## <vector_matrix_1> ##############
            elif (self.getToken().getWord() == '[' or self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';') and self.getPrevToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix1()
            ############## fim <vector_matrix_1> ##############

            ############# erro ##############
            else:
                print('erro_varList_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ############## 
    
    
    # <vector_matrix_1> ::= '[' <expr_number> ']' <vector_matrix_2> | '=' <init_vector> <declaration_var3> | <declaration_var3>
    def vector_matrix1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('vector_matrix_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())
    
            # FIRST DERIV.
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix1()
            ############## fim '[' ############## 

            ############## <expr_number> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == '(') and self.getPrevToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number()
            ############## fim <expr_number> ##############
    
            ############## ']' ##############
            elif self.getToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix1()
            ############## fim ']' ##############
    
            ############## <vector_matrix_2> ##############
            elif (self.getToken().getWord() == '=' or self.getToken().getWord() == ',' or self.getToken().getWord() == ';') and (self.getPrevToken().getWord() == ']'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix2()
            ############## fim <vector_matrix_2> ##############
    
            # SECOND DERIV.
            ############## '=' ##############
            elif self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix1()
            ############## fim '=' ############## 
    
            ############## <init_vector> ##############
            elif self.getToken().getWord() == '[' and self.getPrevToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_vector()
            ############## fim <init_vector> ############## 
    
            ############## <declaration_var3> ##############
            # ADD TESTE DE ULTIMO CARACTER DE <init_vector>
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim <declaration_var3> ##############

            # THIRD DERIV.
            ############## <declaration_var3> ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## <declaration_var3> ##############
    
            ############# erro ##############
            else:
                print('erro_vector_matrix_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <vector_matrix_2> ::= '=' <init_matrix> <declaration_var3> | <declaration_var3> 
    def vector_matrix2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('vector_matrix_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())
    
            # FIRST DERIV.
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.vector_matrix2()
            ############## fim '=' ############## 
    
            ############## <init_matrix> ##############
            elif self.getToken().getWord() == '[' and self.getPrevToken().getWord() == '=':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_matrix()
            ############## fim <init_matrix> ##############

            ############## <declaration_var3> ##############
            # ADD TESTE DE ULTIMO CARACTER DE <init_matrix>
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## fim <declaration_var3> ##############

            # SECOND DERIV.
            ############## <declaration_var3> ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.declaracao_var3()
            ############## <declaration_var3> ##############
    
            ############# erro ##############
            else:
                print('erro_vector_matrix_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <init_vector> ::= '[' <init_vector_1>
    def init_vector(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('init_vector_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())
    
            # FIRST DERIV.
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_vector()
            ############## fim '[' ##############

            ############## <init_vector_1> ##############
            elif (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso')) and (self.getPrevToken().getWord() == '['):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_vector1()
            ############## fim <init_vector_1> ##############
            
            ############# erro ##############
            else:
                print('erro_init_vector_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
            
    # <init_vector_1>  ::=  <value_with_IDE> <init_vector_2>     
    def init_vector1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('init_vector_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())
    
            ############## FIRST DERIV OF <init_vector_2> ##############
            if (self.getToken().getWord() == ',') and (self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getType() == 'CAD' or self.getPrevToken().getType() == 'CAR' or (self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso')):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_vector2()
            ############## fim <init_vector_2> ##############

            ############## SECOND DERIV OF <init_vector_2> ##############
            elif self.getToken().getWord() == ']' and (self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getType() == 'CAD' or self.getPrevToken().getType() == 'CAR' or (self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso')):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_init_vector_1', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
             ############## fim <init_vector_2> ##############

            ############# erro ##############
            else:
                print('erro_init_vector_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <init_vector_2>  ::= ',' <init_vector_1> | ']' 
    def init_vector2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('init_vector_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())
    
            # FIRST DERIV.
            if (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso')) and (self.getPrevToken().getWord() == ','):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_vector1()
                
            ############# erro ##############
            else:
                print('erro_init_vector_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <init_matrix> ::= '[' <init_matrix_1>
    def init_matrix(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('init_matrix_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())
    
            # FIRST DERIV.
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_vector()
            ############## fim '[' ##############
    
            ############## <init_matrix_1> ##############
            elif (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso')) and (self.getPrevToken().getWord() == '['):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_matrix1()
            ############## fim <init_matrix_1> ##############
    
            ############# erro ##############
            else:
                print('erro_init_matrix_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <init_matrix_1> ::= <value_with_IDE> <init_matrix_2> 
    def init_matrix1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('init_matrix_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())
            
            ############## FIRST AND SECOND DERIV OF <init_matrix_2> ##############
            if (self.getToken().getWord() == ',' or self.getToken().getWord() == ';') and (self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getType() == 'CAD' or self.getPrevToken().getType() == 'CAR' or (self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso')):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_matrix2()
            ############## fim <init_matrix_2> ##############
            
            ############## THIRD DERIV OF <init_matrix_2> ##############
            elif self.getToken().getWord() == ']' and (self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getType() == 'CAD' or self.getPrevToken().getType() == 'CAR' or (self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso')):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_init_matrix_1', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
             ############## fim <init_matrix_2> ##############
    
            ############# erro ##############
            else:
                print('erro_init_matrix_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <init_matrix_2>   ::= ',' <init_matrix_1> | ';' <init_matrix_1> | ']
    def init_matrix2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('init_matrix_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())
    
            # FIRST DERIV.
            if (self.getToken().getType() == 'IDE' or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or (self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso')) and (self.getPrevToken().getWord() == ',' or self.getPrevToken().getWord() == ';'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init_matrix1()
    
            ############# erro ##############
            else:
                print('erro_init_matrix_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <expressao>   ::= <expr_rel> <expr_log1> | '(' <expressao> ')' <expr_log2> | '!' <expressao> 
    def expressao(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expressao_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## <expr_rel> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso': 
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel()
            ############## fim <expr_rel> ############## 
    
            ############## <expr_log1> ##############
            elif self.getToken().getWord() == '&&' or self.getToken().getWord() == '||':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log1()
            ############## fim <expr_log1> ##############

            # SECOND DERIV.
            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim '(' ##############
            
            ############## <expressao> ##############
            elif self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## <expressao> ##############
            
            ############## ')' ##############
            elif self.getToken().getWord() == ')' and (self.getPrevToken().getWord() == '*' or self.getPrevToken().getWord() == '/' or self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso' or self.getPrevToken().getWord() == '(' or self.getPrevToken().getWord() == '!'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim ')' ##############
            
            ############## <expr_log2> ##############
            elif ((self.getToken().getWord() == '&&' or self.getToken().getWord() == '||') or (self.getToken().getWord() == '*' or self.getToken().getWord() == '/') or self.isRelOperator(self.getToken().getWord())) and (self.getPrevToken().getWord() == ')'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log2()
            ############## fim <expr_log2> ##############
    
            # THIRD DERIV.
            ############## '!' ##############
            elif self.getToken().getWord() == '!':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim '!' ##############

            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and self.getPrevToken().getWord() == '!':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## <expressao> ##############
            
            ############# erro ##############
            else:
                print('erro_expressao_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <expr_log1> ::=  <operatorLog> <expressao> | <>
    def expr_log1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_log_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())

            # FIRST DERIV.
            ############## <operatorLog> ##############
            if self.getToken().getWord() == '&&' or self.getToken().getWord() == '||':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log1()
            ############## fim <operatorLog> ##############
            
            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == '&&' or self.getPrevToken().getWord() == '||'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <expressao> ##############
    
            ############# erro ##############
            else:
                print('erro_expr_log_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <expr_log2> ::= <operatorLog> <expressao> | <operator_multi> <expressao> | <operator_rel> <expressao> | <operator_soma> <expressao> | <>
    def expr_log2(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_log_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())

            # FIRST DERIV.
            ############## <operatorLog> ##############
            if self.getToken().getWord() == '&&' or self.getToken().getWord() == '||':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log2()
            ############## fim <operatorLog> ##############
            
            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == '&&' or self.getPrevToken().getWord() == '||'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <expressao> ##############
            
            # SECOND DERIV.
            ############## <operator_multi> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log2()
            ############## fim <operator_multi> ##############
            
            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == '*' or self.getPrevToken().getWord() == '/'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <expressao> ##############
            
            # THIRD DERIV.
            ############## <operator_rel> ##############
            if self.isRelOperator(self.getToken().getWord()):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log2()
            ############## fim <operator_rel> ##############
            
            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.isRelOperator(self.getPrevToken().getWord())):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <expressao> ##############
            
            # FOURTH DERIV.
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_log2()
            ############## fim <operator_soma> ##############
            
            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == '+' or self.getPrevToken().getWord() == '-'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <expressao> ##############
            
            ############# erro ##############
            else:
                print('erro_expr_log_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <expr_valor_mod> ::=  number | <operator_auto0> <read_value> | <read_value> <operator_auto>  
    def expr_valor_mod(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_valor_mod_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## number ##############
            if self.getToken().getType() == 'NRO':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_expr_valor_mod_0',self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim number ##############
            
            # SECOND DERIV.
            # <operator_auto0> ::= '++' | '--'
            ############## <operator_auto0> ##############
            elif self.getToken().getWord() == '++' or self.getToken().getWord() == '--':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_valor_mod()
            ############## fim <operator_auto0> ##############

            ############## <read_value> ##############
            elif self.getToken().getWord() == 'IDE' and (self.getPrevToken().getWord() == '++' or self.getPrevToken().getWord() == '--'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value()
            ############## fim <read_value> ##############

            # THIRD DERIV.
            ############## <read_value> ##############
            elif self.getToken().getWord() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value()
            ############## fim <read_value> ##############
            
            # <operator_auto> ::= '++' | '--' | <>
            ############## <operator_auto> ##############
            elif self.getToken().getWord() == '++' or self.getToken().getWord() == '--' and (self.getPrevToken().getWord() == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_expr_valor_mod_1',self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim <operator_auto> ##############
                
            ############# erro ##############
            else:
                print('erro_expr_valor_mod_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ############## 
    
            
    # <expr_multi> ::= <operator_soma> <expr_valor_mod> <expr_multi_pos> | <expr_valor_mod> <expr_multi_pos>    
    def expr_multi(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_multi_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            # <operator_soma> ::= '+' | '-'
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_multi()
            ############## fim <operator_soma> ############## 
        
            ############## <expr_valor_mod> ##############
            elif (self.getToken().getType() == 'NRO' or self.getToken().getWord() == '++' or self.getToken().getWord() == '--' or self.getToken().getWord() == 'IDE') and (self.getPrevToken().getWord() == '+' or self.getPrevToken().getWord() == '-'):
                return self.expr_valor_mod()
            ############## fim <expr_valor_mod> ##############
            
            ############## <expr_multi_pos> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/') and (self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getWord() == '++' or self.getPrevToken().getWord() == '--' or self.getPrevToken().getWord() == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_multi_pos()
            ############## fim <expr_multi_pos> ##############
            
            #SECOND DERIV.
            ############## <expr_valor_mod> ##############
            elif self.getToken().getType() == 'NRO' or self.getToken().getWord() == '++' or self.getToken().getWord() == '--' or self.getToken().getWord() == 'IDE':
                return self.expr_valor_mod()
            ############## fim <expr_valor_mod> ##############
            
            ############## <expr_multi_pos> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/') and (self.getPrevToken().getType() == 'NRO' or self.getPrevToken().getWord() == '++' or self.getPrevToken().getWord() == '--' or self.getPrevToken().getWord() == 'IDE'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_multi_pos()
            ############## fim <expr_multi_pos> ##############
            
            ############# erro ##############
            else:
                print('erro_expr_multi_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ############## 
            
    
    # <expr_multi_pos> ::= <operator_multi> <expr_multi> | <>
    def expr_multi_pos(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_multi_pos_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## <operator_multi> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_multi_pos()
            ############## fim <operator_multi> ##############
            
            ############## <expr_multi> ##############
            elif self.getToken().getWord() == '+' or self.getToken().getWord() == '-' or self.getToken().getType() == 'NRO' or self.getToken().getWord() == '++' or self.getToken().getWord() == '--' or self.getToken().getWord() == 'IDE':
                return self.expr_multi_pos()
            ############## fim <expr_multi> ##############
            
            ############# erro ##############
            else:
                print('erro_multi_pos_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ############## 
            
    
    # <expr_art> ::= <expr_multi> <expr_art1>
    def expr_art(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_art_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## <expr_multi> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_art()
            ############## fim <expr_multi> ##############

            ############## <expr_art1> ##############
            elif (self.getToken().getWord() == '+' or self.getToken().getWord() == '-') and (self.getPrevToken().getWord() == '*' or self.getPrevToken().getWord() == '/'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_art1()
            ############## fim <expr_art1> ##############
            
            ############# erro ##############
            else:
                print('erro_expr_art_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <expr_art1> ::= <operator_soma> <expr_number> | <>   
    def expr_art1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_art1_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_art1()
            ############## fim <operator_soma> ##############
            
            ############## <expr_number> ##############
            elif self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number()
            ############## fim <expr_number> ##############
            
            ############# erro ##############
            else:
                print('erro_expr_art1_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ############## 
    
    
    # <expr_number> ::= <expr_art> | '(' <expr_number> ')' <expr_multi_pos> <expr_number1>
    def expr_number(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_number_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## <expr_art> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_art()
            ############## fim <expr_art> ##############
        
            # SECOND DERIV.
            ############## '(' ##############
            if self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number()
            ############## fim '(' ##############

            ############## <expr_number> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == '(') and (self.getPrevToken().getWord() == '('):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number()
            ############## fim <expr_number> ##############
            
            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number() 
            ############## fim ')' ##############
            
            ############## <expr_multi_pos> ##############
            elif self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_multi_pos()
            ############## fim <expr_multi_pos> ##############
            
            ############## <expr_number1> ##############
            elif self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number1()
            ############## fim <expr_number1> ##############
            
            ############# erro ##############
            else:
                print('erro_expr_number_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
            
    # <expr_number1>  ::= <operator_soma> <expr_number> | <> 
    def expr_number1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_number_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())

            # FIRST DERIV.
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number1() 
            ############## fim <operator_soma> ##############
    
            ############## <expr_number> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == '(') and (self.getPrevToken().getWord() == '+' or self.getPrevToken().getWord() == '-'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_number()
            ############## fim <expr_number> ##############
    
            ############# erro ##############
            else:
                print('erro_expr_number_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
    
    
    # <expr_rel0>   ::= <expr_rel> | '(' <expressao> ')'
    def expr_rel0(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_rel_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## <expr_rel> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso': 
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel()
            ############## fim <expr_rel> ##############            
            
            # SECOND DERIV.
            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel0()
            ############## fim '(' ##############
            
            ############## <expressao> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == '('):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <expressao> ##############
            
            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel0()
            ############## fim ')' ##############
            
            ############# erro ##############
            else:
                print('erro_expr_rel_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
    
    # <expr_rel> ::= <expr_art> <expr_rel1> | boolean <expr_rel1>
    def expr_rel(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_rel_1',self.palavra)
            print('TOKEN_1',self.getToken().getWord())

            # FIRST DERIV.
            ############## <expr_art> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_art()
            ############## fim <expr_art> ##############
            
            ############## <expr_rel1> ##############
            elif self.isRelOperator(self.getToken().getWord()) and (self.getPrevToken().getWord() == '*' or self.getPrevToken().getWord() == '/'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel1()
            ############## fim <expr_rel1> ##############
            
            # SECOND DERIV.
            ############## boolean ##############
            if self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel()
            ############## fim boolean ##############
            
            ############## <expr_rel1> ##############
            elif self.isRelOperator(self.getToken().getWord()) and (self.getPrevToken().getWord() == 'verdadeiro' or self.getPrevToken().getWord() == 'falso'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel1()
            ############## fim <expr_rel1> ##############
            
            ############# erro ##############
            else:
                print('erro_expr_rel_1',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
            
    # <expr_rel1> ::= <operator_rel> <expr_rel0> | <>
    def expr_rel1(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('expr_rel_2',self.palavra)
            print('TOKEN_2',self.getToken().getWord())

            # FIRST DERIV.
            if self.isRelOperator(self.getToken().getWord()):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel1()
    
            elif self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expr_rel0()
            
            ############# erro ##############
            else:
                print('erro_expr_rel_2',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############
            
    
    # <write_cmd> ::= escreva '(' <value_with_expressao> <write_value_list> ')' ';'
    def escreva(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('escreva_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## 'escreva' ##############
            if self.getToken().getWord() == 'escreva':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.escreva()
            ############## fim 'escreva' ##############
            
            ############## '(' ##############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getWord() == 'escreva':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.escreva()
            ############## fim '(' ##############
            
            ############## <value_with_expressao> ##############
            elif (self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or self.getToken().getType() == 'IDE' or self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == '('):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()                
            ############## fim <value_with_expressao> ##############
            
            ############## ',' ##############
            elif self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.write_value_list()
            ############## fim ',' ##############
            
            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.escreva()
            ############## fim ')' ##############
            
            ############## ';' ##############
            elif self.getToken().getWord() == ';' and self.getPrevToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_escreva_0', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim ';' ##############

            ############# erro ##############
            else:
                print('erro_escreva_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############

    
    # <write_value_list> ::= ',' <value_with_expressao> <write_value_list> | <>
    def write_value_list(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('write_value_list_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## ',' ##############
            if self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.write_value_list()
            ############## fim ',' ##############:
                
            ############## <value_with_expressao> ##############
            elif (self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR' or self.getToken().getType() == 'IDE' or self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == ','):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()                
            ############## fim <value_with_expressao> ##############

            ############## ',' ##############
            elif self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.write_value_list()
            ############## fim ',' ##############

            ############# erro ##############
            else:
                print('erro_write_value_list_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############


    # <read_cmd> ::= leia '(' <read_value> <read_value_list> ')' ';'
    def leia(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('leia_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## 'leia' ##############
            if self.getToken().getWord() == 'leia':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.leia()
            ############## fim 'leia' ##############
            
            ############## '(' ##############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getWord() == 'leia':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.leia()
            ############## fim '(' ##############
            
            ############## <read_value> ##############
            elif self.getToken().getWord() == 'IDE' and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value()
            ############## fim <read_value> ##############
            
            ############## ',' ##############
            elif self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value_list()
            ############## fim ',' ##############
            
            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.leia()
            ############## fim ')' ##############
            
            ############## ';' ##############
            elif self.getToken().getWord() == ';' and self.getPrevToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_leia_0', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim ';' ##############

            ############# erro ##############
            else:
                print('erro_leia_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############


    # <read_value_list> ::= ',' <read_value> <read_value_list> |
    def read_value_list(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('read_value_list_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## ',' ##############
            if self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value_list()
            ############## fim ',' ##############:

            ############## <read_value> ##############
            elif self.getToken().getWord() == 'IDE' and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value()
            ############## fim <read_value> ##############

            ############## ',' ##############
            elif self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.read_value_list()
            ############## fim ',' ##############

            ############# erro ##############
            else:
                print('erro_read_value_list_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############


    # <com_enquanto> ::= enquanto '(' <args> ')' '{' <com_body> '}'
    def enquanto(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('enquanto_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## 'enquanto' ##############
            if self.getToken().getWord() == 'enquanto':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.enquanto()
            ############## fim 'enquanto' ##############
            
            ############## '(' ##############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getWord() == 'enquanto':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.enquanto()
            ############## fim '(' ##############
            
            ############## <args> ##############
            # <args> ::= <expressao> |
            elif self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## <args> ##############
            
            ############## ')' ##############
            # ADD TESTE DE ULTIMO CARACTER DE EXPRESSAO
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.enquanto()
            ############## fim ')' ##############
            
            ############## '{' ##############
            elif self.getToken().getWord() == '{' and self.getPrevToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.enquanto()
            ############## fim '{' ##############
            
            #
            # ADD TESTE DE <com_body>
            #
            
            ############## '}' ##############
            # ADD TESTE DE ULTIMO CARACTER DE <com_body>
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_enquanto', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim '}' ##############

            ############# erro ##############
            else:
                print('erro_enquanto_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############


    # <com_para> ::= para '(' <init> <stop> ';' <step> ')' '{' <com_body> '}'
    def para(self):
        if self.getToken().getType() == 'EOF':
            return
        
        elif self.counter < len(self.tokens):
            print('para_0',self.palavra)
            print('TOKEN_0',self.getToken().getWord())

            # FIRST DERIV.
            ############## 'para' ##############
            if self.getToken().getWord() == 'para':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.para()
            ############## fim 'para' ##############
            
            ############## '(' ##############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getWord() == 'para':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.para()
            ############## fim '(' ##############
            
            ############## FIRST DERIV OF <init> ##############
            elif (self.getToken().getWord() == 'IDE') and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.init()
            ############## fim <init> ##############
            
            ############## SECOND DERIV OF <init> ##############
            elif self.getToken().getWord() == ';' and self.getPrevToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.para()
            ############## fim <init> ##############
            
            ############## <stop> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == ';'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <stop> ##############            
            
            ############## ';' ##############
            # ADD TESTE DE ULTIMO CARACTER DE EXPRESSAO
            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.para()
            ############## fim ';' ##############
            
            ############## <step> ##############
            elif (self.getToken().getWord() == '*' or self.getToken().getWord() == '/' or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso' or self.getToken().getWord() == '(' or self.getToken().getWord() == '!') and (self.getPrevToken().getWord() == ';'):
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.expressao()
            ############## fim <step> ##############   
            
            ############## '{' ##############
            # ADD TESTE DE ULTIMO CARACTER DE EXPRESSAO
            elif self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + '$'
                self.getNextToken()
                return self.para()
            ############## fim '{' ##############
            
            #
            # ADD TESTE DE <com_body>
            #
            
            ############## '}' ##############
            # ADD TESTE DE ULTIMO CARACTER DE <com_body>
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + '$ '
                print('fim_para', self.palavra, '\n')
                self.palavra = ''
                self.getNextToken()
                return
            ############## fim '}' ##############

            ############# erro ##############
            else:
                print('erro_para_0',self.palavra)
                # self.getNextToken()
            ############## fim erro ##############


    # <init> ::= <var_atr> | ';'


