# -*- coding: utf-8 -*-
# coding: utf-8


from Token import Token
from lexemas import Lexemas
from AnalisadorSemantico import AnalisadorSemantico
from SimboloVarConst import SimboloVarConst
from SimboloFuncao import SimboloFuncao
from SimboloRegistro import SimboloRegistro
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
        self.value = ['NRO', 'CAD', 'CAR', 'verdadeiro', 'falso']
        self.palavra = ''
        self.grammars = ['registro', 'constantes', 'variaveis', 'funcao']
        self.grammar = 0
        self.origin = []
        self.analisadorSemantico = AnalisadorSemantico()
        self.semanticItem = {}
        self.returnType = None

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
            return self.tokens[1]
        else:
            return Token("EOF", "EOF", -1)

    def isPrimitiveType(self, word):
        return word in self.primitives_types

    def isvalue(self, token):
        if token.getType() in self.value:
            if token.getType() == 'NRO':
                if (token.getWord().find('.') == -1):
                    return 'inteiro'
                else:
                    return 'real'
            return True

        elif token.getWord() == 'verdadeiro' or token.getWord() == 'falso':
            return True

        else:
            return False

    def isReservedWord(self, word):
        return word in Lexemas().getReservedWords()

    def isRelOperator(self, word):
        return word in ['==', '>=', '<=', '!=', '<', '>']

    def checkSemanticItem(self, name, match):
        error = 'Linha ' + str(self.getToken().getLine()
                               ) + ': Erro semantico encontrado: ' + "\"" + name + '\" ' + match
        print(error)
        self.errors.append(error)

    def isSemanticItemValueOk(self):
        if self.semanticItem['init'] == True and self.semanticItem['categoria'] != 'vector' and self.semanticItem['categoria'] != 'matrix':
            valor = self.semanticItem['valor']

            if valor.getType() == 'NRO':
                if (valor.getWord().find('.') == -1):
                    return 'inteiro' == self.semanticItem['tipo']
                else:
                    return 'real' == self.semanticItem['tipo']

            elif valor.getType() == 'CAD':
                return 'cadeia' == self.semanticItem['tipo']

            elif valor.getType() == 'CAR':
                return 'char' == self.semanticItem['tipo']

            elif valor.getWord() == 'verdadeiro' or valor.getWord() == 'falso':
                return 'booleano' == self.semanticItem['tipo']

        elif self.semanticItem['init'] == True and (self.semanticItem['categoria'] == 'vector' or self.semanticItem['categoria'] == 'matrix'):
            return True

        elif self.semanticItem['init'] == False:
            return True

        else:
            return None

    def errorSintatico(self, match):
        if(self.forward().getWord() != 'EOF'):
            error = 'Linha ' + str(self.getToken().getLine()
                                   ) + ': Erro sintatico encontrado (' + self.palavra
            for idx, k in enumerate(self.grammars):
                if k == self.grammars[self.grammar]:
                    if len(self.grammars) > (idx + 1):
                        self.next_grammar = self.grammars[idx+1]
                        if len(self.tokens) > 1:
                            while (self.getToken().getWord() != self.next_grammar and self.getToken().getWord() != self.grammars[self.grammar]) and self.forward().getWord() != 'EOF':
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
        return self.errors

    # <Program> ::= <declaracao_reg> <declaration_const> <declaration_var> <function_declaration>
    def start(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            while (self.getToken().getWord() == 'registro'):
                self.declaracao_reg()

            while (self.getToken().getWord() == 'constantes'):
                self.declaracao_const('global')

            while (self.getToken().getWord() == 'variaveis'):
                self.declaracao_var('global')

            while (self.getToken().getWord() == 'funcao'):
                self.declaracao_funcao()

    # <declaracao_reg> ::= registro id '{' <declaracao_reg1> |
    def declaracao_reg(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            # FIRST DERIV.
            ############## registro ##############
            if self.getToken().getWord() == 'registro':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.declaracao_reg()
            ############## fim registro ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == 'registro':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.getToken().getWord()
                    self.semanticItem['atributos'] = []
                    self.semanticItem['dimensao'] = ''
                    self.getNextToken()
                    return self.declaracao_reg()
                else:
                    self.errorSintatico('registro before IDE')
                    self.palavra = ''
                    return
            ############## fim id ##############

            ############## '{' ##############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.declaracao_reg1()
                else:
                    self.errorSintatico('IDE before {')
                    self.palavra = ''
                    return
            ############## fim '{' ##############

            # SECOND DERIV.
            ############## vazio ##############
            if self.getToken().getType() == 'PRE' and self.getToken().getWord() != 'registro' and (not self.isPrimitiveType(self.getToken().getWord())):
                return
            ############## fim vazio ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_reg')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg1> ::= <primitive_type> id <declaracao_reg4> <declaracao_reg2> | id id <declaracao_reg4> <declaracao_reg2>
    def declaracao_reg1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            ############## <type> ##############
            if ((self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE')
                    and (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == ';')):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem['tipo'] = self.getToken().getWord()
                self.getNextToken()
                return self.declaracao_reg1()
            ############## fim <type> ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getType() == 'IDE' and self.forward().getType() == 'IDE':
                    self.errorSintatico('only 2 IDEs')
                    self.palavra = ''
                    return

                elif self.isPrimitiveType(self.getPrevToken().getWord()) or self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    isInRegistro = self.analisadorSemantico.isAtributoInRegistro(
                        self.getToken().getWord(), self.semanticItem['atributos'])

                    if isInRegistro == False:
                        self.semanticItem['atributos'].append({
                            'nome': self.getToken().getWord(),
                            'tipo': self.semanticItem['tipo'],
                            'dimensao': self.semanticItem['dimensao']
                        })
                        self.semanticItem['dimensao'] = ''
                    elif isInRegistro == True:
                        self.checkSemanticItem(self.getToken().getWord(
                        ), 'ja declarado(a) no Registro ' + self.semanticItem['nome'])

                    self.getNextToken()
                    return self.declaracao_reg4()

                else:
                    self.errorSintatico(' IDE or PRE before IDE')
                    self.palavra = ''
                    return
            ############## fim id ##############

            ############## <declaracao_reg2> ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ']':
                    return self.declaracao_reg2()
                else:
                    self.errorSintatico(
                        'um IDE ou ] antes de ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <declaracao_reg2> ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_reg1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg2>  ::= ',' id <declaracao_reg2> | ';' <declaracao_reg5>
    def declaracao_reg2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            # FIRST DERIV.
            ############## ',' ##############
            if self.getToken().getWord() == ',':
                if self.getPrevToken().getType() == 'IDE' or self.getToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.declaracao_reg2()
                else:
                    self.errorSintatico('um IDE antes da ,')
                    self.palavra = ''
                    return
            ############## fim ',' ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE' and self.getPrevToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + ' '

                isInRegistro = self.analisadorSemantico.isAtributoInRegistro(
                    self.getToken().getWord(), self.semanticItem['atributos'])

                if isInRegistro == False:
                    self.semanticItem['atributos'].append({
                        'nome': self.getToken().getWord(),
                        'tipo': self.semanticItem['tipo'],
                        'dimensao': self.semanticItem['dimensao']
                    })
                    self.semanticItem['dimensao'] = ''
                elif isInRegistro == True:
                    self.checkSemanticItem(self.getToken().getWord(
                    ), 'ja declarado(a) no Registro ' + self.semanticItem['nome'])

                self.getNextToken()
                return self.declaracao_reg2()
            ############## fim id ##############

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.declaracao_reg3()
                else:
                    self.errorSintatico('um IDE antes de ;')
                    self.palavra = ''
                    return
            ############## fim ';' ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_reg2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg3>   ::= '}' <declaracao_reg>
    def declaracao_reg3(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            # FIRST DERIV.
            ############## '}' ##############
            if self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    semanticSymbol = SimboloRegistro(
                        self.semanticItem['nome'], self.semanticItem['atributos'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaRegistro(
                        semanticSymbol.getNome())
                    self.semanticItem = {}

                    if isInTable == False:
                        self.analisadorSemantico.addSimboloRegistro(
                            semanticSymbol)
                    elif isInTable == True:
                        self.checkSemanticItem(semanticSymbol.getNome(
                        ), 'registro ' + semanticSymbol.getNome() + ' ja declarado!')

                    self.palavra = ''
                    self.getNextToken()
                    return self.declaracao_reg()
                else:
                    self.errorSintatico(' ; before }')
                    self.palavra = ''
                    return
            ############## fim '}' ##############

            # SECOND DERIV.
            ############## <declaracao_reg1> ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == ';':
                    return self.declaracao_reg1()
                else:
                    self.errorSintatico('um IDE ou PRE antes de ;')
                    self.palavra = ''
                    return
            ############## fim <declaracao_reg1> ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_reg2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaracao_reg4>   ::= <v_m_access> |
    def declaracao_reg4(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            # FIRST DERIV.
            ############## <v_m_access> ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.origin.append('declaracao_reg2')
                    return self.v_m_access()
                else:
                    self.errorSintatico('um IDE antes de [')
                    self.palavra = ''
                    return
            ############## fim <v_m_access> ##############

            # SECOND DERIV.
            ############## <> ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if self.getPrevToken().getType() == 'IDE':
                    return self.declaracao_reg2()
            ############## fim <> ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_reg4')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <v_m_access>  ::= '[' <v_m_access1>
    def v_m_access(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            ############## '[' ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('v_m_access')
                    return self.expr_number()
                else:
                    self.errorSintatico(' IDE before [')
                    self.palavra = ''
                    return
            ############## fim '[' ##############

            ############## <v_m_access1> ##############
            elif self.getToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.v_m_access1()
            ############## fim <v_m_access1> ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on v_m_access_0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <v_m_access1>  ::= '[' <expr_number> ']' |
    def v_m_access1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            # FIRST DERIV.
            ############## [ <expr_number> ##############
            if self.getToken().getWord() == '[':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('v_m_access1')
                return self.expr_number()
            ############## fim [ <expr_number> ##############

            ############## ] ##############
            elif self.getToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()

                if len(self.origin) > 0:

                    if self.origin[-1] == 'declaracao_reg2':
                        self.origin.pop()
                        return self.declaracao_reg2()
                    elif self.origin[-1] == 'nested_elem_registro1':
                        self.origin.pop()
                        return self.nested_elem_registro1()
                    elif self.origin[-1] == 'read_value0':
                        self.origin.pop()
                        return self.read_value0()
                    elif self.origin[-1] == 'var_list2':
                        self.origin.pop()
                        return self.var_list2()
                    elif self.origin[-1] == 'expr_multi':
                        self.origin.pop()
                        return self.expr_multi()
                    elif self.origin[-1] == 'operator_auto':
                        self.origin.pop()
                        return self.operator_auto()
                    elif self.origin[-1] == 'leia':
                        self.origin.pop()
                        return self.leia()
                    elif self.origin[-1] == 'read_value_list':
                        self.origin.pop()
                        return self.read_value_list()
                    elif self.origin[-1] == 'var_atr':
                        self.origin.pop()
                        return self.var_atr()
                    elif self.origin[-1] == 'expr_multi_pos':
                        self.origin.pop()
                        return self.expr_multi_pos()
                    else:
                        self.errorSintatico(
                            ' an origin before v_m_access1 return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim ] ##############

            # SECOND DERIV.
            ############## vazio #############
            else:
                if len(self.origin) > 0:
                    if self.getPrevToken().getWord() == ']':
                        if self.origin[-1] == 'declaracao_reg2':
                            self.origin.pop()
                            return self.declaracao_reg2()
                        elif self.origin[-1] == 'nested_elem_registro':
                            self.origin.pop()
                            return self.nested_elem_registro()
                        elif self.origin[-1] == 'read_value0':
                            self.origin.pop()
                            return self.read_value0()
                        elif self.origin[-1] == 'var_list2':
                            self.origin.pop()
                            return self.var_list2()
                        elif self.origin[-1] == 'expr_multi':
                            self.origin.pop()
                            return self.expr_multi()
                        elif self.origin[-1] == 'operator_auto':
                            self.origin.pop()
                            return self.operator_auto()
                        elif self.origin[-1] == 'leia':
                            self.origin.pop()
                            return self.leia()
                        elif self.origin[-1] == 'read_value_list':
                            self.origin.pop()
                            return self.read_value_list()
                        elif self.origin[-1] == 'var_atr':
                            self.origin.pop()
                            return self.var_atr()
                        elif self.origin[-1] == 'expr_multi_pos':
                            self.origin.pop()
                            return self.expr_multi_pos()
                        else:
                            self.errorSintatico(
                                ' an origin before v_m_access1 return')
                            self.palavra = ''
                            return
                    else:
                        return

                ############## erro ##############
                else:
                    self.errorSintatico('other token on v_m_access_1')
                    self.palavra = ''
                    return
            ############## fim erro ##############

    # <elem_registro>  ::= '.' id <nested_elem_registro>
    def elem_registro(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            ############## '.' ##############
            if self.getToken().getWord() == '.':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.semanticItem['nome'] + \
                        self.getToken().getWord()
                    self.getNextToken()
                    return self.elem_registro()
                else:
                    self.errorSintatico(' IDE or ] before .')
                    self.palavra = ''
                    return
            ############## fim '.' ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == '.':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    
                    self.semanticItem['nome'] = self.semanticItem['nome'] + self.getToken().getWord()
                    
                    # DOES THIS VARIABLE IS IN VarConst Table??
                    isVarInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(
                        self.semanticItem['initialName'].getWord())

                    if isVarInTabelaVarConst == True:
                        field = self.getToken().getWord()

                        # GETTING TIPO Registro
                        varItem = self.analisadorSemantico.getSimboloVarConst(
                            self.semanticItem['initialName'].getWord())
                        registroItem = self.analisadorSemantico.getSimboloRegistro(
                            varItem.getTipo())

                        if registroItem != None:
                            # DOES THIS FIELD FROM THIS REGISTRO EXISTES
                            isFieldInRegistro = self.analisadorSemantico.isAtributoInRegistro(
                                field, registroItem.getAtributos())

                            if isFieldInRegistro == True:
                                self.semanticItem['init'] = False
                                self.semanticItem['tipo'] = registroItem.getTipoDeAtributo(
                                    field)
                                self.semanticItem['categoria'] = 'variavel'
                                semanticSymbol = SimboloVarConst(self.semanticItem['nome'], self.semanticItem['tipo'], self.semanticItem['categoria'],
                                                                 self.semanticItem['dimensao'], varItem.getEscopo(), self.semanticItem['init'])

                                isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(
                                    semanticSymbol.getNome())
                                isValueOk = self.isSemanticItemValueOk()

                                tipo = self.semanticItem['tipo']
                                nome = self.semanticItem['nome']
                                initialName = self.semanticItem['initialName']
                                self.semanticItem = {}
                                self.semanticItem['nome'] = nome
                                self.semanticItem['var'] = initialName
                                self.semanticItem['tipo'] = tipo

                                if isInTable == False and isValueOk == True:
                                    self.analisadorSemantico.addSimboloVarConst(
                                        semanticSymbol)
                                elif isValueOk == False:
                                    self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() +
                                                           ' tem tipo de valor associado diferente do declarado: ' + semanticSymbol.getTipo())
                                # elif isInTable == True:
                                #     self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' +
                                #                semanticSymbol.getCategoria() + ' ja declarado (a)!')

                            elif isFieldInRegistro == False:
                                self.checkSemanticItem(field, 'nao existe no Registro ' + registroItem.getNome() +
                                                       '. Os atributos existentes sao: ' + registroItem.printAtributos() + '!')

                        elif registroItem == None:
                            self.checkSemanticItem(self.semanticItem['nome'], "o campo \"" + varItem.getNome() +"\"" + ' nao e de tipo Registro!')

                    elif isVarInTabelaVarConst == False:
                        self.checkSemanticItem(
                            self.semanticItem['initialName'].getWord(), 'nao foi declarada!')

                    self.getNextToken()
                    return self.nested_elem_registro()
                else:
                    self.errorSintatico(' IDE or ] before .')
                    self.palavra = ''
                    return
            ############## fim id ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on elem_registro')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <nested_elem_registro>  ::= '.' id <nested_elem_registro1> | <v_m_access> <nested_elem_registro1> |

    def nested_elem_registro(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            # FIRST DERIV.
            ############## '.' ##############
            if self.getToken().getWord() == '.':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.semanticItem['nome'] + \
                        self.getToken().getWord()
                    self.semanticItem['initialName'] = self.getPrevToken()
                    self.semanticItem['dimensao'] = ''
                    self.getNextToken()
                    return self.nested_elem_registro()
                else:
                    self.errorSintatico(' IDE before .')
                    self.palavra = ''
                    return
            ############## fim '.' ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == '.':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    self.semanticItem['nome'] = self.semanticItem['nome'] + self.getToken().getWord()

                    # DOES THIS VARIABLE IS IN VarConst Table??
                    isVarInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(
                        self.semanticItem['initialName'].getWord())

                    if isVarInTabelaVarConst == True:
                        field = self.getToken().getWord()

                        # GETTING TIPO Registro
                        varItem = self.analisadorSemantico.getSimboloVarConst(self.semanticItem['initialName'].getWord())
                        registroItem = self.analisadorSemantico.getSimboloRegistro(varItem.getTipo())

                        if registroItem != None:
                            # DOES THIS FIELD FROM THIS REGISTRO EXISTES
                            isFieldInRegistro = self.analisadorSemantico.isAtributoInRegistro(
                                field, registroItem.getAtributos())

                            if isFieldInRegistro == True:
                                self.semanticItem['init'] = False
                                self.semanticItem['tipo'] = registroItem.getTipoDeAtributo(field)
                                self.semanticItem['categoria'] = 'variavel'
                                semanticSymbol = SimboloVarConst(self.semanticItem['nome'], self.semanticItem['tipo'], self.semanticItem['categoria'],
                                                                 self.semanticItem['dimensao'], varItem.getEscopo(), self.semanticItem['init'])

                                isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(
                                    semanticSymbol.getNome())
                                isValueOk = self.isSemanticItemValueOk()

                                tipo = self.semanticItem['tipo']
                                nome = self.semanticItem['nome']
                                initialName = self.semanticItem['initialName']
                                self.semanticItem = {}
                                self.semanticItem['nome'] = nome
                                self.semanticItem['var'] = initialName
                                self.semanticItem['tipo'] = tipo

                                if isInTable == False and isValueOk == True:
                                    self.analisadorSemantico.addSimboloVarConst(
                                        semanticSymbol)
                                elif isValueOk == False:
                                    self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() +
                                                           ' tem tipo de valor associado diferente do declarado: ' + semanticSymbol.getTipo())
                                elif isInTable == True:
                                    self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' +
                                                           semanticSymbol.getCategoria() + ' ja declarado (a)!')

                            elif isFieldInRegistro == False:
                                self.checkSemanticItem(field, 'nao existe no Registro ' + registroItem.getNome() +
                                                       '. Os atributos existentes sao: ' + registroItem.printAtributos() + '!')

                        elif registroItem == None:
                            self.checkSemanticItem(self.semanticItem['nome'], "o campo \"" + varItem.getNome() +"\"" + ' nao e de tipo Registro!')

                    elif isVarInTabelaVarConst == False:
                        self.checkSemanticItem(
                            self.semanticItem['initialName'].getWord(), 'nao foi declarada!')

                    self.getNextToken()
                    return self.nested_elem_registro1()
                else:
                    self.errorSintatico(' . before IDE')
                    self.palavra = ''
                    return
            ############## fim id ##############

            # SECOND DERIV.
            ############## <v_m_access> ##############
            elif self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.origin.append('nested_elem_registro1')
                    return self.v_m_access()
                else:
                    self.errorSintatico(' IDE before [')
                    self.palavra = ''
                    return
            ############## fim <v_m_access> ##############

            ############## erro ##############
            else:
                if self.getPrevToken().getType() == 'IDE':
                    if len(self.origin) > 0:
                        if self.origin[-1] == 'var_list2':
                            self.origin.pop()
                            return self.var_list2()

                        elif self.origin[-1] == 'expr_multi':
                            self.origin.pop()
                            return self.expr_multi()

                        elif self.origin[-1] == 'leia':
                            self.origin.pop()
                            return self.leia()

                        elif self.origin[-1] == 'read_value_list':
                            self.origin.pop()
                            return self.read_value_list()

                        elif self.origin[-1] == 'var_atr':
                            self.origin.pop()
                            return self.var_atr()

                        elif self.origin[-1] == 'expr_multi_pos':
                            self.origin.pop()
                            return self.expr_multi_pos()

                        elif self.origin[-1] == 'operator_auto':
                            self.origin.pop()
                            return self.operator_auto()

                        else:
                            self.errorSintatico(
                                ' an origin before nested_elem_registro return')
                            self.palavra = ''
                            return
                    else:
                        return

                ############## erro ##############
                else:
                    self.errorSintatico('other token on nested_elem_registro')
                    self.palavra = ''
                    return
            ############## fim erro ##############

    # <nested_elem_registro1> ::= <elem_registro> |
    def nested_elem_registro1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:

            # FIRST DERIV.
            ############## <elem_registro> ##############
            if self.getToken().getWord() == '.':
                return self.elem_registro()
            ############## fim <elem_registro> ##############

            else:
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    if len(self.origin) > 0:

                        if self.origin[-1] == 'var_list2':
                            self.origin.pop()
                            return self.var_list2()

                        elif self.origin[-1] == 'expr_multi':
                            self.origin.pop()
                            return self.expr_multi()

                        elif self.origin[-1] == 'leia':
                            self.origin.pop()
                            return self.leia()

                        elif self.origin[-1] == 'read_value_list':
                            self.origin.pop()
                            return self.read_value_list()

                        elif self.origin[-1] == 'var_atr':
                            self.origin.pop()
                            return self.var_atr()

                        elif self.origin[-1] == 'expr_multi_pos':
                            self.origin.pop()
                            return self.expr_multi_pos()

                        elif self.origin[-1] == 'operator_auto':
                            self.origin.pop()
                            return self.operator_auto()

                        else:
                            self.errorSintatico(
                                ' an origin before nested_elem_registro1 return')
                            self.palavra = ''
                            return
                    else:
                        return

                ############## erro ##############
                else:
                    self.errorSintatico('other token on nested_elem_registro1')
                    self.palavra = ''
                    return
                ############## fim erro ##############

    # <declaration_const>  ::= constantes '{' <declaration_const1>
    def declaracao_const(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo

            ############## constantes ##############
            if self.getToken().getWord() == 'constantes':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.declaracao_const(escopo)
            ############## fim constantes ##############

            ############## '{' <declaracao_const1> ##############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == 'constantes':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.declaracao_const1(escopo)
                else:
                    self.errorSintatico('constantes antes de {')
                    self.palavra = ''
                    return
            ############## fim '{' <declaracao_const1> ##############

            ############### erro ##############
            else:
                self.errorSintatico('one declaracao_const')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
    def declaracao_const1(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo
            # FIRST DERIV.
            ############## <primitive_type> ##############
            if self.isPrimitiveType(self.getToken().getWord()):
                if self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['tipo'] = self.getToken().getWord()
                    self.getNextToken()
                    return self.declaracao_const1(escopo)
                else:
                    self.errorSintatico('{ or ; before PrimitiveType')
                    self.palavra = ''
                    return
            ############## fim <declaracao_const1> ##############

            ############## <id> ##############
            elif self.getToken().getType() == 'IDE':
                if self.isPrimitiveType(self.getPrevToken().getWord()):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    self.semanticItem['nome'] = self.getToken().getWord()
                    self.getNextToken()
                    return self.declaracao_const1(escopo)
                else:
                    self.errorSintatico('PrimitiveType before IDE')
                    self.palavra = ''
                    return
            ############## <id> ##############

            ############## '=' ##############
            elif self.getToken().getWord() == '=':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.semanticItem['init'] = True
                    return self.declaracao_const1(escopo)
                else:
                    self.errorSintatico('IDE before =')
                    self.palavra = ''
                    return
            ############## fim '=' ##############

            ############## <value> ##############
            elif (self.isvalue(self.getToken()) == 'real' or self.isvalue(self.getToken()) == 'inteiro'
                    or self.isvalue(self.getToken())):
                if self.getPrevToken().getWord() == '=':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['categoria'] = 'constante'
                    self.semanticItem['dimensao'] = None
                    self.semanticItem['valor'] = self.getToken()
                    self.getNextToken()
                    return self.declaracao_const2(escopo)
                else:
                    self.errorSintatico('= before value')
                    self.palavra = ''
                    return
            ############## fim <value> ##############

            # SECOND DERIV.
            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.palavra = ''
                    self.getNextToken()

                    if len(self.origin) > 0:

                        if self.origin[-1] == 'corpo_funcao1':
                            self.origin.pop()
                            return self.corpo_funcao1()
                        else:
                            self.errorSintatico(
                                ' an origin before declaracao_const1 return')
                            self.palavra = ''
                            return
                    else:
                        return
                else:
                    self.errorSintatico(' ; or { before }')
                    self.palavra = ''
                    return
            ############## fim '}' ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_const1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
    def declaracao_const2(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo

            # FIRST DERIV.
            if self.getToken().getWord() == ',':
                if (self.isvalue(self.getPrevToken()) == 'real' or self.isvalue(self.getPrevToken()) == 'inteiro'
                        or self.isvalue(self.getPrevToken())):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    semanticSymbol = SimboloVarConst(self.semanticItem['nome'], self.semanticItem['tipo'], self.semanticItem[
                                                     'categoria'], self.semanticItem['dimensao'], self.semanticItem['escopo'], self.semanticItem['init'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(
                        semanticSymbol.getNome())
                    isValueOk = self.isSemanticItemValueOk()

                    tipo = self.semanticItem['tipo']
                    self.semanticItem = {}
                    self.semanticItem['tipo'] = tipo

                    if isInTable == False and isValueOk == True:
                        self.analisadorSemantico.addSimboloVarConst(
                            semanticSymbol)
                    elif isValueOk == False:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() +
                                               ' tem tipo de valor associado diferente do declarado: ' + semanticSymbol.getTipo())
                    elif isInTable == True:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' +
                                               semanticSymbol.getCategoria() + ' ja declarado (a)!')

                    self.getNextToken()
                    return self.declaracao_const2(escopo)
                else:
                    self.errorSintatico('value before , ')
                    self.palavra = ''
                    return

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getType() == 'DEL' and self.getPrevToken().getWord() == ',':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.getToken().getWord()
                    self.getNextToken()
                    return self.declaracao_const2(escopo)
                else:
                    self.errorSintatico(' , before IDE')
                    self.palavra = ''
                    return
            ############## fim id ##############

            ############## '=' ##############
            elif self.getToken().getWord() == '=':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.semanticItem['init'] = True
                    return self.declaracao_const2(escopo)
                else:
                    self.errorSintatico(' IDE before =')
                    self.palavra = ''
                    return
            ############## fim '=' ##############

            ############## <value> ##############
            elif (self.isvalue(self.getToken()) == 'real' or self.isvalue(self.getToken()) == 'inteiro'
                    or self.isvalue(self.getToken())):
                if self.getPrevToken().getWord() == '=':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['categoria'] = 'constante'
                    self.semanticItem['dimensao'] = None
                    self.semanticItem['valor'] = self.getToken()
                    self.getNextToken()
                    return self.declaracao_const2(escopo)
                else:
                    self.errorSintatico('= before value')
                    self.palavra = ''
                    return
            ############## fim <value> ##############

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                if (self.isvalue(self.getPrevToken()) == 'real' or self.isvalue(self.getPrevToken()) == 'inteiro'
                        or self.isvalue(self.getPrevToken())):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    semanticSymbol = SimboloVarConst(self.semanticItem['nome'], self.semanticItem['tipo'], self.semanticItem[
                                                     'categoria'], self.semanticItem['dimensao'], self.semanticItem['escopo'], self.semanticItem['init'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(
                        semanticSymbol.getNome())
                    isValueOk = self.isSemanticItemValueOk()

                    self.semanticItem = {}

                    if isInTable == False and isValueOk == True:
                        self.analisadorSemantico.addSimboloVarConst(
                            semanticSymbol)
                    elif isValueOk == False:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() +
                                               ' tem tipo de valor associado diferente do declarado: ' + semanticSymbol.getTipo())
                    elif isInTable == True:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' +
                                               semanticSymbol.getCategoria() + ' ja declarado (a)!')

                    self.getNextToken()
                    return self.declaracao_const1(escopo)
                else:
                    self.errorSintatico(' value before ; ')
                    self.palavra = ''
                    return
            ############## fim ';' ##############

            ############## erro ##############
            else:
                self.errorSintatico('Other token on declaracao_const2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var>  ::= variaveis '{' <declaration_var1>
    def declaracao_var(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo

            ############## 'variaveis' ##############
            if self.getToken().getWord() == 'variaveis':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.declaracao_var(escopo)
            ############## fim 'variaveis' ##############

            ############## '{' ##############
            elif self.getToken().getType() == 'DEL' and self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == 'variaveis':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.declaracao_var1(escopo)
                else:
                    self.errorSintatico('variaveis before { ')
                    self.palavra = ''
                    return
            ############## fim '}' ##############

            ############## erro ##############
            else:
                self.errorSintatico('Other token on declaration_var')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var1> ::= <type> id <declaration_var2> | '}'
    def declaracao_var1(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo

            # FIRST DERIV.
            ############## <type> ##############
            if ((self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE')
                    and (self.getPrevToken().getWord() == ';' or self.getPrevToken().getWord() == '{')):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem['tipo'] = self.getToken().getWord()
                self.getNextToken()
                return self.declaracao_var1(escopo)
            ############## fim <type> ##############

            ############## id ##############
            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getType() == 'IDE' and self.forward().getType() == 'IDE':
                    self.errorSintatico('only 2 IDE')
                    self.palavra = ''
                    return
                else:
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.getToken().getWord()
                    self.semanticItem['init'] = False
                    self.getNextToken()
                    return self.declaracao_var2(escopo)
            ############## fim id ##############

            ############## '}' ##############
            # 2 DERIVACAO DE <declaracao_var1>. FECHAMENTO DE BLOCO  DE VARIAVEL
            elif self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == ';' or self.getPrevToken().getWord() == '{':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.palavra = ''
                    self.getNextToken()

                    if len(self.origin) > 0:
                        if self.origin[-1] == 'corpo_funcao2':
                            self.origin.pop()
                            return self.corpo_funcao2()
                        else:
                            self.errorSintatico(
                                ' an origin before declaracao_var1 return')
                            self.palavra = ''
                            return
                    else:
                        return
                else:
                    self.errorSintatico(' { ou ; before } ')
                    self.palavra = ''
                    return
            ############## fim '}' ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_var1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
    def declaracao_var2(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo
            self.semanticItem['dimensao'] = None
            self.semanticItem['categoria'] = 'variavel'
            self.semanticItem['valor'] = ''

            # FIRST DERIV.
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['init'] = True
                    self.getNextToken()
                    return self.declaracao_var2(escopo)
                else:
                    self.errorSintatico(' IDE before = ')
                    self.palavra = ''
                    return
            ############## fim '=' ##############

            ############## <value> ##############
            elif (self.isvalue(self.getToken()) == 'real' or self.isvalue(self.getToken()) == 'inteiro'
                  or self.isvalue(self.getToken())):
                if self.getPrevToken().getWord() == '=':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['valor'] = self.getToken()
                    self.getNextToken()
                    return self.declaracao_var3(escopo)
                else:
                    self.errorSintatico(' = before value ')
                    self.palavra = ''
                    return
            ############## fim <value> ##############

            # SECOND DERIV.
            ############# <vector_matrix> ##############
            elif self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.semanticItem['dimensao'] = ''
                    return self.vector_matrix()
                else:
                    self.errorSintatico(' IDE before [ ')
                    self.palavra = ''
                    return
            ############## fim <vector_matrix> ##############

            # THIRD DERIV.
            ############## <declaracao_var3>  ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if self.getPrevToken().getType() == 'IDE':
                    return self.declaracao_var3(escopo)
                else:
                    self.errorSintatico(' IDE before , ')
                    self.palavra = ''
                    return
            ############## fim <declaracao_var3> ::= ';' ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_var2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1>
    def declaracao_var3(self, escopo):
        if self.getToken().getType() == 'EOF':
            return

        elif len(self.tokens) > 1:
            self.semanticItem['escopo'] = escopo

            # FIRST DERIV.
            ############## <declaracao_var3> ##############
            if self.getToken().getWord() == ',':
                if (self.getPrevToken().getType() == 'IDE' or self.isvalue(self.getPrevToken()) == 'real'
                        or self.isvalue(self.getPrevToken()) == 'inteiro' or self.isvalue(self.getPrevToken())
                        or self.getPrevToken().getWord() == ']'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    semanticSymbol = SimboloVarConst(self.semanticItem['nome'], self.semanticItem['tipo'], self.semanticItem[
                                                     'categoria'], self.semanticItem['dimensao'], self.semanticItem['escopo'], self.semanticItem['init'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(
                        semanticSymbol.getNome())
                    isValueOk = self.isSemanticItemValueOk()

                    tipo = self.semanticItem['tipo']
                    self.semanticItem = {}
                    self.semanticItem['tipo'] = tipo

                    if isInTable == False and isValueOk == True:
                        self.analisadorSemantico.addSimboloVarConst(
                            semanticSymbol)
                    elif isValueOk == False:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() +
                                               ' tem tipo de valor associado diferente do declarado: ' + semanticSymbol.getTipo())
                    elif isInTable == True:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' +
                                               semanticSymbol.getCategoria() + ' ja declarado (a)!')

                    self.getNextToken()
                    return self.declaracao_var3(escopo)
                else:
                    self.errorSintatico(' IDE or value or ] before , ')
                    self.palavra = ''
                    return
            ############## fim <declaracao_var3> ##############

            ############## id ##############
            if self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == ',':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.getToken().getWord()
                    self.semanticItem['init'] = False
                    self.getNextToken()
                    return self.declaracao_var2(escopo)
                else:
                    self.errorSintatico(' , before IDE ')
                    self.palavra = ''
                    return
            ############## fim id ##############

            # LAST PART OF FIRST DERIV. AND THIRD DERIV.
            ############## <declaracao_var3> ##############
            elif self.getToken().getWord() == ';':
                if (self.getPrevToken().getType() == 'IDE' or self.isvalue(self.getPrevToken()) == 'real'
                        or self.isvalue(self.getPrevToken()) == 'inteiro' or self.isvalue(self.getPrevToken())
                        or self.getPrevToken().getWord() == ']'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    semanticSymbol = SimboloVarConst(self.semanticItem['nome'], self.semanticItem['tipo'], self.semanticItem[
                                                     'categoria'], self.semanticItem['dimensao'], self.semanticItem['escopo'], self.semanticItem['init'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(
                        semanticSymbol.getNome())
                    isValueOk = self.isSemanticItemValueOk()
                    self.semanticItem = {}

                    if isInTable == False and isValueOk == True:
                        self.analisadorSemantico.addSimboloVarConst(
                            semanticSymbol)
                    elif isValueOk == False:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() +
                                               ' tem tipo de valor associado diferente do declarado: ' + semanticSymbol.getTipo())
                    elif isInTable == True:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' +
                                               semanticSymbol.getCategoria() + ' ja declarado (a)!')

                    self.getNextToken()
                    return self.declaracao_var1(escopo)
                else:
                    self.errorSintatico(' IDE or value before ; ')
                    self.palavra = ''
                    return
            ############## fim <declaracao_var3> ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on declaracao_var3')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_declaration>  ::= funcao <type> <function_declaration1>
    def declaracao_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############# funcao ##############
            if self.getToken().getWord() == 'funcao':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.declaracao_funcao()

            ############## fim funcao ##############

            ############## <type> ##############
            elif self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType == 'IDE':
                if self.getPrevToken().getWord() == 'funcao':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['retorno'] = self.getToken().getWord()
                    self.returnType = self.getToken().getWord()
                    self.getNextToken()
                    return self.declaracao_funcao1()
                else:
                    self.errorSintatico(
                        ' funcao before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <type> ##############

            ############## erro ##############
            else:
                self.errorSintatico('other token on function_declaration')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_declaration1> ::= algoritmo <main_function> | <function_declaration2>
    def declaracao_funcao1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############# algoritmo #############
            ############# <main_function> #############
            if self.getToken().getWord() == 'algoritmo':
                if self.isPrimitiveType(self.getPrevToken().getWord()) or self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['nome'] = self.getToken().getWord()
                    self.getNextToken()
                    return self.main_function()
                else:
                    self.errorSintatico(' IDE or PrimitiveType before algoritmo ')
                    self.palavra = ''
                    return
            ############# fim algoritmo #############
            ############# fim <main_function> #############

            # SECOND DERIV.
            ############# <function_declaration2>  #############
            elif self.getToken().getType() == 'IDE':
                if (self.isPrimitiveType(self.getPrevToken().getWord()) or self.getPrevToken().getType() == 'IDE'
                        and self.forward().getWord() == '('):
                    self.semanticItem['nome'] = self.getToken().getWord()
                    return self.declaracao_funcao2()
                else:
                    self.errorSintatico(
                        ' IDE or PrimitiveType before IDE and ( after ')
                    self.palavra = ''
                    return

            ############# erro ##############
            else:
                self.errorSintatico('Other token on function_declaration1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_declaration2> ::= id <function_parameters> '{' <function_body> '}' <function_declaration>
    def declaracao_funcao2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            self.semanticItem['qtdParam'] = 0
            self.semanticItem['params'] = []

            # FIRST DERIV.
            ############# id #############
            ############# <function_parameters> #############
            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('declaracao_funcao2')
                return self.parametros_funcao()
            ############# fim id #############
            ############# fim <function_parameters> #############

            ############## <function_body> ##############
            ############# '{' #############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == ')':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('declaracao_funcao2')
                    return self.corpo_funcao()
                else:
                    self.errorSintatico(') before {')
                    self.palavra = ''
                    return
            ############# fim '{' #############
            ############## fim <function_body> ##############

            # '}' #############
            elif self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.palavra = ''
                    self.getNextToken()
                    return self.declaracao_funcao()
                else:
                    self.errorSintatico('; before }')
                    self.palavra = ''
                    return
            ############# fim '}' #############

            ############# erro ##############
            else:
                self.errorSintatico('other token on function_declaration2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <main_function> ::= <function_parameters> '{' <function_body> '}'
    def main_function(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            self.semanticItem['qtdParam'] = 0
            self.semanticItem['params'] = []

            # FIRST DERIV.
            ############# '(' #############
            if self.getToken().getWord() == '(':
                if self.getPrevToken().getWord() == 'algoritmo':
                    self.origin.append('main_function')
                    return self.parametros_funcao()
                else:
                    self.errorSintatico('algoritmo before (')
                    self.palavra = ''
                    return
            ############# fim '(' #############

            ############# '{' #############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == ')':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('main_function')
                    return self.corpo_funcao()
                else:
                    self.errorSintatico(') before {')
                    self.palavra = ''
                    return
            ############# fim '{' #############

            ############# '}' #############
            elif self.getToken().getWord() == '}':
                if self.getPrevToken().getWord() == ';':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return
                else:
                    self.errorSintatico('; before }')
                    self.palavra = ''
                    return
            ############# fim '}' #############

            ############# erro ##############
            else:
                self.errorSintatico('other token on main_function')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters>   ::= '(' <function_parameters1>

    def parametros_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############# '(' #############
            if self.getToken().getWord() == '(':
                if self.getPrevToken().getWord() == 'algoritmo' or self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.parametros_funcao1()
                else:
                    self.errorSintatico('algoritmo or IDE before (')
                    self.palavra = ''
                    return

            ############# erro ##############
            else:
                self.errorSintatico('Other token on function_parameters')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters1>  ::= <type> id <function_parameters2> | ')'
    def parametros_funcao1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############# <type> #############
            if (self.isPrimitiveType(self.getToken().getWord()) or self.getToken().getType() == 'IDE'
                    and (self.getPrevToken().getWord() == '(' or self.getPrevToken().getWord() == ',')):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                
                if self.getToken().getType() == 'IDE' and not self.isPrimitiveType(self.getToken().getWord()):
                    isTipoInTabelaRegistro = self.analisadorSemantico.isSimboloInTabelaRegistro(self.getToken().getWord())
                
                    if isTipoInTabelaRegistro == False and (self.getToken().getWord() != 'verdadeiro' and self.getToken().getWord() != 'falso'):
                        self.checkSemanticItem(self.getToken().getWord(), 'e um tipo de Registro nao declarado!')
                    
                self.getNextToken()
                return self.parametros_funcao1()

            elif self.getToken().getType() == 'IDE':
                if self.getPrevToken().getType() == 'IDE' and self.forward().getType() == 'IDE':
                    self.errorSintatico('Only 2 IDE')
                    self.palavra = ''
                    return
                elif (self.isPrimitiveType(self.getPrevToken().getWord()) or self.getPrevToken().getType() == 'IDE'
                      and (self.forward().getWord() == '[' or self.forward().getWord() == ','
                      or self.forward().getWord() == ')')):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '

                    self.semanticItem['qtdParam'] = self.semanticItem['qtdParam'] + 1
                    self.semanticItem['params'].append(self.getPrevToken().getWord())

                    semanticSymbol = SimboloVarConst(self.getToken().getWord(), self.getPrevToken().getWord(), 'variavel', None, 'local', False)
                    isInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(semanticSymbol.getNome())

                    if isInTable == False:
                        self.analisadorSemantico.addSimboloVarConst(semanticSymbol)
                    else:
                        self.checkSemanticItem(semanticSymbol.getNome(), 'de categoria ' + semanticSymbol.getCategoria() + ' ja declarado(a)!')

                    self.getNextToken()
                    return self.parametros_funcao2()
                else:
                    self.errorSintatico('PrimitiveType or IDE before IDE')
                    self.palavra = ''
                    return

            # SECOND DERIV.
            ############# ') #############
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getWord() == '(':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.palavra = ''
                    self.getNextToken()

                    semanticSymbol = SimboloFuncao(
                        self.semanticItem['nome'], self.semanticItem['retorno'], self.semanticItem['qtdParam'], self.semanticItem['params'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaFuncao(
                        semanticSymbol.getHash())
                    self.semanticItem = {}

                    if isInTable == False:
                        self.analisadorSemantico.addSimboloFuncao(
                            semanticSymbol)
                    else:
                        self.checkSemanticItem(semanticSymbol.getNome(
                        ), 'função ' + semanticSymbol.getNome() + ' ja declarada!')

                    if len(self.origin) > 0:

                        if self.origin[-1] == 'declaracao_funcao2':
                            self.origin.pop()
                            return self.declaracao_funcao2()

                        elif self.origin[-1] == 'main_function':
                            self.origin.pop()
                            return self.main_function()
                        else:
                            self.errorSintatico(
                                ' an origin before parametros_funcao1 return')
                            self.palavra = ''
                            return
                    else:
                        return
                else:
                    self.errorSintatico('( before )')
                    self.palavra = ''
                    return
            ############# ') #############

            ############# erro ##############
            else:
                self.errorSintatico('Other token on function_parameters1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters2>  ::= '[' ']' <function_parameters3>  | <function_parameters4>
    def parametros_funcao2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############# '[' #############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.parametros_funcao2()
                else:
                    self.errorSintatico('IDE before [')
                    self.palavra = ''
                    return
            ############# fim '[' #############

            ############# ']' #############
            elif self.getToken().getWord() == ']':
                if self.getPrevToken().getWord() == '[':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.parametros_funcao3()
                else:
                    self.errorSintatico(' [ before ]')
                    self.palavra = ''
                    return
            ############# fim ']' #############

            # SECOND DERIV.
            ############# <function_parameters4> #############
            elif self.getToken().getWord() == ',':
                if self.getPrevToken().getType() == 'IDE':
                    return self.parametros_funcao4()
                else:
                    self.errorSintatico(' IDE before ,')
                    self.palavra = ''
                    return
            ############# fim <function_parameters4> #############

            ############# ') #############
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getType() == 'IDE':
                    return self.parametros_funcao4()
                else:
                    self.errorSintatico(' IDE before )')
                    self.palavra = ''
                    return
            ############# ') #############

            ############# erro ##############
            else:
                self.errorSintatico('Other token on function_parameters2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters3>  ::= '[' ']' <function_parameters4>  | <function_parameters4>

    def parametros_funcao3(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############# '[' #############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.parametros_funcao3()
                else:
                    self.errorSintatico(' ] before [')
                    self.palavra = ''
                    return
            ############# fim '[' #############

            ############# ']' #############
            elif self.getToken().getWord() == ']':
                if self.getPrevToken().getWord() == '[':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.parametros_funcao4()
                else:
                    self.errorSintatico(' [ before ]')
                    self.palavra = ''
                    return
            ############# fim ']' #############

            ############# <function_parameters4> #############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ')':
                if self.getPrevToken().getWord() == ']':
                    return self.parametros_funcao4()
                else:
                    self.errorSintatico(
                        ' ] before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############# fim <function_parameters4> #############

            ############# erro ##############
            else:
                self.errorSintatico('other token on function_parameters3')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_parameters4>  ::= ','  <function_parameters1>  | ')'
    def parametros_funcao4(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            if self.getToken().getWord() == ',':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.parametros_funcao1()
                else:
                    self.errorSintatico(' ] or IDE before ,')
                    self.palavra = ''
                    return

            # SECOND DERIV.
            ############# ') #############
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.palavra = ''
                    self.getNextToken()

                    semanticSymbol = SimboloFuncao(
                        self.semanticItem['nome'], self.semanticItem['retorno'], self.semanticItem['qtdParam'], self.semanticItem['params'])
                    isInTable = self.analisadorSemantico.isSimboloInTabelaFuncao(
                        semanticSymbol.getHash())
                    self.semanticItem = {}

                    if isInTable == False:
                        self.analisadorSemantico.addSimboloFuncao(
                            semanticSymbol)
                    else:
                        self.checkSemanticItem(semanticSymbol.getNome(
                        ), 'função ' + semanticSymbol.getNome() + ' ja declarada!')

                    if len(self.origin) > 0:

                        if self.origin[-1] == 'declaracao_funcao2':
                            self.origin.pop()
                            return self.declaracao_funcao2()

                        elif self.origin[-1] == 'main_function':
                            self.origin.pop()
                            return self.main_function()
                        else:
                            self.errorSintatico(
                                ' an origin before parametros_funcao4 return')
                            self.palavra = ''
                            return
                    else:
                        return

                else:
                    self.errorSintatico(' ] or IDE before )')
                    self.palavra = ''
                    return
            ############# ') #############

            ############# erro ##############
            else:
                self.errorSintatico('other token on function_parameters4')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <var_atr> ::= <read_value> '=' <atr_value> <atr_1>

    def var_atr(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############# <read_value> #############
            if self.getToken().getType() == 'IDE':
                if self.forward().getWord() == '[' or self.forward().getWord() == '.' or self.forward().getWord() == '=':
                    self.origin.append('var_atr')
                    return self.read_value()
                else:
                    self.errorSintatico(' [ or . or = after IDE')
                    self.palavra = ''
                    return
            ############# fim <read_value> #############

            ############# '=' #############

            elif self.getToken().getWord() == '=':
                if (self.forward().getType() == 'CAD' or self.forward().getType() == 'CAR'
                        or self.forward().getWord() == '+' or self.forward().getWord() == '-'
                        or self.forward().getType() == 'NRO' or self.forward().getWord() == '++'
                        or self.forward().getWord() == '--' or self.forward().getType() == 'IDE'
                        or self.forward().getWord() == 'verdadeiro' or self.forward().getWord() == 'falso'
                        or self.forward().getWord() == '(' or self.forward().getWord() == '!'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.atr_value()

            ############# fim '=' #############

            else:
                self.errorSintatico('other token on var_atr')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <read_value> ::= id <read_value0>

    def read_value(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            if self.getToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + ' '

                isVarConstInTable = self.analisadorSemantico.isSimboloInTabelaVarConst(self.getToken().getWord())
                
                if isVarConstInTable == False:
                    self.checkSemanticItem(self.getToken().getWord(), 'nao foi declarada!')
                    
                elif isVarConstInTable == True:
                    self.semanticItem['var'] = self.getToken()
                    self.semanticItem['nome'] = self.getToken().getWord()
                    
                    if self.origin[-1] == 'var_list2':
                        self.semanticItem['qtdParam'] = self.semanticItem['qtdParam'] + 1
                        self.semanticItem['params'].append(self.getToken().getWord())
                
                self.getNextToken()
                return self.read_value0()

            ############# erro ##############
            else:
                self.errorSintatico('other token on read_value')
                self.palavra = ''
                return
            ############## fim erro ##############

    def read_value0(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # <read_value0> ::= <v_m_access> | <elem_registro> | <>
            # <v_m_access>
            if self.getToken().getWord() == '[' and self.getPrevToken().getType() == 'IDE':
                self.semanticItem['nome'] = self.getPrevToken().getWord()
                self.semanticItem['dimensao'] = ''
                
                # checar se variavel é de tipo array
                isVarInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(self.semanticItem['nome'])
                
                if isVarInTabelaVarConst == True:
                    varItem = self.analisadorSemantico.getSimboloVarConst(self.semanticItem['nome'])
                    tipo = varItem.getCategoria()
                    
                    if tipo != 'vector' and tipo != 'matrix':
                        self.checkSemanticItem(varItem.getNome(), 'e do tipo ' + tipo + ' e foi utilizada como vetor/matriz!')
                    
                elif isVarInTabelaVarConst == False:
                    self.checkSemanticItem(self.semanticItem['initialName'].getWord(), 'nao foi declarada!')
                
                return self.v_m_access()

            # <elem_registro>
            elif self.getToken().getWord() == '.' and self.getPrevToken().getType() == 'IDE':
                self.semanticItem['nome'] = self.getPrevToken().getWord()
                self.semanticItem['initialName'] = self.getPrevToken()
                self.semanticItem['dimensao'] = ''
                return self.elem_registro()

            ############# erro ##############
            else:
                if len(self.origin) > 0:
                    if self.origin[-1] == 'var_list2':
                        self.origin.pop()
                        return self.var_list2()

                    elif self.origin[-1] == 'expr_multi_pos':
                        self.origin.pop()
                        return self.expr_multi_pos()

                    elif self.origin[-1] == 'operator_auto':
                        self.origin.pop()
                        return self.operator_auto()

                    elif self.origin[-1] == 'read_value_list':
                        self.origin.pop()
                        return self.read_value_list()

                    elif self.origin[-1] == 'var_atr':
                        self.origin.pop()
                        return self.var_atr()

                    else:
                        self.errorSintatico(
                            ' an origin before read_value0 return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim erro ##############

    # <atr_1> ::= ',' <var_atr> | ';'

    def atr_1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <var_atr> ##############
            if self.getToken().getWord() == ',' and self.forward().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.var_atr()
            ############## fim <var_atr> ##############

            # SECOND DERIV.
            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem = {}
                self.palavra = ''
                self.getNextToken()

                if len(self.origin) > 0:
                    if self.origin[-1] == 'corpo_funcao2':
                        self.origin.pop()
                        return self.corpo_funcao2()

                    elif self.origin[-1] == 'com_body':
                        self.origin.pop()
                        return self.com_body()

                    elif self.origin[-1] == 'para':
                        self.origin.pop()
                        return self.para()

                    elif self.origin[-1] == 'stop':
                        self.origin.pop()
                        return self.stop()

                    else:
                        self.errorSintatico(
                            ' an origin before atr_1 return')
                        self.palavra = ''
                        return
                else:
                    return

            ############# erro ##############
            else:
                self.errorSintatico('other token on atr_1')
                self.palavra = ''
                return
                ############## fim erro ##############

    # <atr_value> ::= <value_with_expressao> | <functionCall>

    def atr_value(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # SECOND DERIV.
            ############## <functionCall> ##############
            if self.getToken().getType() == 'IDE' and self.forward().getWord() == '(':
                self.origin.append('atr_1')
                return self.chamada_funcao()
            ############## fim <functionCall> ##############

            # FIRST DERIV.
            ############## <value_with_expressao> ##############
            elif self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR':
                self.palavra = self.palavra + self.getToken().getWord() + ' '

                isSimboloInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(self.semanticItem['nome'])
                
                if isSimboloInTabelaVarConst == True:
                    simboloVarConst = self.analisadorSemantico.getSimboloVarConst(self.semanticItem['nome'])

                    if simboloVarConst.getCategoria() == 'constante':
                        self.checkSemanticItem(self.semanticItem['nome'], 'atribuicao de constante fora do bloco!')

                    elif simboloVarConst.getCategoria() == 'variavel':
                        item = simboloVarConst
                        self.semanticItem = {}
                        self.semanticItem['categoria'] = item.getCategoria()
                        self.semanticItem['init'] = True
                        self.semanticItem['tipo'] = item.getTipo()
                        self.semanticItem['nome'] = item.getNome()
                        self.semanticItem['valor'] = self.getToken()

                        isValueOk = self.isSemanticItemValueOk()
                        
                        if isValueOk == False:
                            self.checkSemanticItem(self.semanticItem['nome'], 'de categoria ' + self.semanticItem['categoria'] +
                                                ' tem tipo de valor associado diferente do declarado: ' + self.semanticItem['tipo'])
                        elif isValueOk == True:
                            self.analisadorSemantico.updateTabelaVarConst(self.semanticItem['nome'], True)
                        
                elif isSimboloInTabelaVarConst == False:
                        self.checkSemanticItem(self.semanticItem['nome'], 'nao foi declarada')
                        
                self.getNextToken()
                return self.atr_1()

            elif (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                self.origin.append('atr_1')
                return self.expressao()
            ############## fim <value_with_expressao> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on atr_value')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <functionCall> ::= id '(' <varList0> ')' ';'

    def chamada_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############## id ##############
            if self.getToken().getType() == 'IDE' and self.forward().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem['nome'] = self.getToken().getWord()
                self.semanticItem['qtdParam'] = 0
                self.semanticItem['params'] = []
                self.getNextToken()
                return self.chamada_funcao()
            ############## fim id ##############

            ############## '(' ##############
            if self.getToken().getWord() == '(' and self.getPrevToken().getType() == 'IDE':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.var_list0()
            ############## fim '(' ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')' and self.forward().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.chamada_funcao()
            ############## fim ')' ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';' and self.getPrevToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                
                params = self.semanticItem['params']
                self.semanticItem['params'] = []
                
                for param in params:
                    if param.getType() == 'IDE' and (param.getWord() != 'verdadeiro' and param.getWord() != 'falso'):
                        isVarInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(param.getWord())
                        
                        if isVarInTabelaVarConst == True:
                            varItem = self.analisadorSemantico.getSimboloVarConst(param.getWord())
                            tipo = varItem.getTipo()
                            self.semanticItem['params'].append(tipo)
                            
                        elif isVarInTabelaVarConst == False:
                            self.semanticItem['params'].append(param.getWord())
                            self.checkSemanticItem(param.getWord(), 'parametro nao declarado!')
                        
                    elif param.getType() == 'NRO':
                        if (param.getWord().find('.') == -1):
                            tipo = 'inteiro'
                            self.semanticItem['params'].append(tipo)
                        else:
                            tipo = 'real'
                            self.semanticItem['params'].append(tipo)

                    elif param.getType() == 'CAD':
                        tipo = 'cadeia'
                        self.semanticItem['params'].append(tipo)

                    elif param.getType() == 'CAR':
                        tipo = 'char'
                        self.semanticItem['params'].append(tipo)

                    elif param.getWord() == 'verdadeiro' or param.getWord() == 'falso':
                        tipo = 'booleano'
                        self.semanticItem['params'].append(tipo)
                
                semanticSymbol = SimboloFuncao(self.semanticItem['nome'], None, self.semanticItem['qtdParam'], self.semanticItem['params'])
                isFuncInTabelaFuncao = self.analisadorSemantico.isSimboloInTabelaFuncao(semanticSymbol.getHash())
                    
                if isFuncInTabelaFuncao == False:
                    functionsWithSameName = self.analisadorSemantico.getFunctionsWithSameName(semanticSymbol.getNome())
                    
                    if len(functionsWithSameName) == 0:        
                        self.checkSemanticItem(semanticSymbol.getNome(), 'funcao nao declarada!')
                        
                    elif len(functionsWithSameName) > 0:
                        signatures = self.analisadorSemantico.getFunctionSignatures(functionsWithSameName)
                        self.checkSemanticItem(semanticSymbol.getFunctionSignature(), 'nao foi declarada. Foram encontrada(s) outra(s) funcao(os) com este nome: '+ signatures)
                
                self.palavra = ''
                self.getNextToken()
                self.semanticItem = {}

                if len(self.origin) > 0:
                    if self.origin[-1] == 'corpo_funcao2':
                        self.origin.pop()
                        return self.corpo_funcao2()

                    elif self.origin[-1] == 'atr_1':
                        if self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                            self.origin.pop()
                            return self.atr_1()
                        else:
                            self.errorSintatico(
                                ' , or ; before functionCall return to atr_1')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'com_body':
                        self.origin.pop()
                        return self.com_body()

                    else:
                        self.errorSintatico(
                            ' an origin before functionCall return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim ';' ##############
            else:
                self.errorSintatico('other token on functionCall')
                self.palavra = ''
                return

    # <varList0> ::= <value> <varList2> | <read_value> <varList2> | <>

    def var_list0(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV. OR SECOND DERIV.
            ############## <varList2> ##############
            if (self.isvalue(self.getToken()) or self.isvalue(self.getToken()) == 'inteiro'
                    or self.isvalue(self.getToken()) == 'inteiro'):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem['qtdParam'] = self.semanticItem['qtdParam'] + 1
                self.semanticItem['params'].append(self.getToken())
                self.getNextToken()
                return self.var_list2()

            elif self.getToken().getType() == 'IDE':
                self.origin.append('var_list2')
                return self.read_value()
            ############## fim <varList2> ##############

            ############## <> ##############
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getWord() == '(':
                    return self.chamada_funcao()
                else:
                    self.errorSintatico(' ( before )')
                    self.palavra = ''
                    return

            ############# erro ##############
            else:
                self.errorSintatico(' other token on varList0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <varList1> ::= <value> <varList2> | <read_value> <varList2>
    def var_list1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV. OR SECOND DERIV.
            ############## <varList2> ##############
            if (self.isvalue(self.getToken()) or self.isvalue(self.getToken()) == 'inteiro'
                    or self.isvalue(self.getToken()) == 'inteiro'):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem['qtdParam'] = self.semanticItem['qtdParam'] + 1
                self.semanticItem['params'].append(self.getToken())
                self.getNextToken()
                return self.var_list2()

            elif self.getToken().getType() == 'IDE':
                self.origin.append('var_list2')
                return self.read_value()
            ############## fim <varList2> ##############

            ############# erro ##############
            else:
                self.errorSintatico(' other token on varList1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <varList2> ::= ',' <varList1> | <>

    def var_list2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            if self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.var_list1()

            elif self.getToken().getWord() == ')':
                return self.chamada_funcao()

            ############# erro ##############
            else:
                self.errorSintatico(' other token on varList2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <vector_matrix>   ::= '[' <expr_number> ']' <vector_matrix_1>
    def vector_matrix(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############## '[' <expr_number> ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getType() == 'IDE':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['categoria'] = 'vector'
                    self.getNextToken()
                    self.origin.append('vector_matrix')
                    return self.expr_number()
                else:
                    self.errorSintatico('IDE before [')
                    self.palavra = ''
                    return
            ############## fim '[' <expr_number> ##############

            ############## ']' ##############
            elif self.getToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.vector_matrix1()
            ############## fim ']' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on vector_matrix')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <vector_matrix_1> ::= '[' <expr_number> ']' <vector_matrix_2> | '=' <init_vector> <declaration_var3> | <declaration_var3>

    def vector_matrix1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['categoria'] = 'matrix'
                    self.getNextToken()
                    self.origin.append('vector_matrix1')
                    return self.expr_number()
                else:
                    self.errorSintatico('[ before [')
                    self.palavra = ''
                    return
            ############## fim '[' ##############

            ############## ']' ##############
            elif self.getToken().getWord() == ']':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.vector_matrix2()
            ############## fim ']' ##############

            # SECOND DERIV.
            ############## '=' ##############
            elif self.getToken().getWord() == '=':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.semanticItem['init'] = True
                    return self.init_vector()
                else:
                    self.errorSintatico('] before =')
                    self.palavra = ''
                    return
            ############## fim '=' ##############

            # SECOND DERIV. AND THIRD DERIV.
            ############## <declaration_var3> ##############
            elif self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ']':
                    return self.declaracao_var3(self.semanticItem['escopo'])
                else:
                    self.errorSintatico('] before , or ;')
                    self.palavra = ''
                    return
            ############## fim <declaration_var3> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on vector_matrix')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <vector_matrix_2> ::= '=' <init_matrix> <declaration_var3> | <declaration_var3>

    def vector_matrix2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## '=' ##############
            if self.getToken().getWord() == '=':
                if self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem['init'] = True
                    self.getNextToken()
                    return self.init_matrix()
                else:
                    self.errorSintatico('] before =')
                    self.palavra = ''
                    return
            ############## fim '=' ##############

            # SECOND DERIV.
            ############## <declaration_var3> ##############
            if self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ']':
                    return self.declaracao_var3(self.semanticItem['escopo'])
                else:
                    self.errorSintatico('] before , or ;')
                    self.palavra = ''
                    return
            ############## <declaration_var3> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on vector_matrix_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <init_vector> ::= '[' <init_vector_1>

    def init_vector(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getWord() == '=':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init_vector1()
                else:
                    self.errorSintatico('= before [')
                    self.palavra = ''
                    return
            ############## fim '[' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on init_vector')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <init_vector_1>  ::=  <value_with_IDE> <init_vector_2>

    def init_vector1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############## FIRST DERIV OF <value_with_IDE> ##############
            if (self.isvalue(self.getToken()) == 'real' or self.isvalue(self.getToken()) == 'inteiro'
                    or self.isvalue(self.getToken()) or self.getToken().getType() == 'IDE'):
                if self.getPrevToken().getWord() == ',' or self.getPrevToken().getWord() == '[':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init_vector2()
                else:
                    self.errorSintatico(
                        ' , or [ before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <value_with_IDE> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on init_vector_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <init_vector_2>  ::= ',' <init_vector_1> | ']'

    def init_vector2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            if self.getToken().getWord() == ',':
                if (self.isvalue(self.getPrevToken()) == 'real' or self.isvalue(self.getPrevToken()) == 'inteiro'
                        or self.isvalue(self.getPrevToken()) or self.getPrevToken().getType() == 'IDE'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init_vector1()
                else:
                    self.errorSintatico(' value or IDE before , ')
                    self.palavra = ''
                    return

            elif self.getToken().getWord() == ']':
                if (self.isvalue(self.getPrevToken()) == 'real' or self.isvalue(self.getPrevToken()) == 'inteiro'
                        or self.isvalue(self.getPrevToken()) or self.getPrevToken().getType() == 'IDE'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.declaracao_var3(self.semanticItem['escopo'])
                else:
                    self.errorSintatico(' value or IDE before ] ')
                    self.palavra = ''
                    return

            ############# erro ##############
            else:
                self.errorSintatico('other token on init_vector_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <init_matrix> ::= '[' <init_matrix_1>

    def init_matrix(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## '[' ##############
            if self.getToken().getWord() == '[':
                if self.getPrevToken().getWord() == '=':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init_matrix1()
                else:
                    self.errorSintatico(' = before [ ')
                    self.palavra = ''
                    return
            ############## fim '[' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on init_matrix')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <init_matrix_1> ::= <value_with_IDE> <init_matrix_2>

    def init_matrix1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            if (self.isvalue(self.getToken()) == 'real' or self.isvalue(self.getToken()) == 'inteiro'
                    or self.isvalue(self.getToken()) or self.getToken().getType() == 'IDE'):
                if (self.getPrevToken().getWord() == ',' or self.getPrevToken().getWord() == '['
                        or self.getPrevToken().getWord() == ';'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init_matrix2()
                else:
                    self.errorSintatico(
                        ' , or ; or [ before ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            ############# erro ##############
            else:
                self.errorSintatico('other token on init_matrix_1')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <init_matrix_2>   ::= ',' <init_matrix_1> | ';' <init_matrix_1> | ']

    def init_matrix2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV. OR  SECOND DERIV.
            if self.getToken().getWord() == ',' or self.getToken().getWord() == ';':
                if (self.isvalue(self.getPrevToken()) == 'real' or self.isvalue(self.getPrevToken()) == 'inteiro'
                        or self.isvalue(self.getPrevToken()) or self.getPrevToken().getType() == 'IDE'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init_matrix1()
                else:
                    self.errorSintatico(
                        ' value or IDE before ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            # THIRD DERIV
            ############## ']' ##############
            elif self.getToken().getWord() == ']':
                if (self.isvalue(self.getPrevToken()) == 'real' or self.isvalue(self.getPrevToken()) == 'inteiro'
                        or self.isvalue(self.getPrevToken()) or self.getPrevToken().getType() == 'IDE'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.palavra = ''
                    self.getNextToken()
                    return self.declaracao_var3(self.semanticItem['escopo'])
                else:
                    self.errorSintatico(' value or IDE before ]')
                    self.palavra = ''
                    return
            ############## fim ']' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on init_matrix_2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expressao>   ::= <expr_rel> <expr_log1> | '(' <expressao> ')' <expr_log2> | '!' <expressao>

    def expressao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <expr_rel> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO' or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'):
                self.origin.append('expr_log1')
                return self.expr_rel()
            ############## fim <expr_rel> ##############

            # SECOND DERIV.
            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('expressao')
                return self.expressao()
            ############## fim '(' ##############

             ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expr_log2()
            ############## fim ')' ##############

            # THIRD DERIV.
            ############## '!' ##############
            elif self.getToken().getWord() == '!':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expressao()
            ############## fim '!' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expressao')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expr_log1> ::=  <operatorLog> <expressao> | <>

    def expr_log1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <operatorLog> ##############
            if self.getToken().getWord() == '&&' or self.getToken().getWord() == '||':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expressao()
            ############## fim <operatorLog> ##############

            ############## <> ##############
            else:

                if len(self.origin) > 0:

                    if self.origin[-1] == 'retornar_funcao':
                        if self.getToken().getWord() == ';':
                            self.origin.pop()
                            return self.retornar_funcao()
                        else:
                            self.errorSintatico(' ; after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'com_retornar':
                        if self.getToken().getWord() == ';':
                            self.origin.pop()
                            return self.com_retornar()
                        else:
                            self.errorSintatico(' ; after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'enquanto':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.enquanto()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'para':
                        if self.getToken().getWord() == ';' or self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.para()
                        else:
                            self.errorSintatico(' ; or ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'expr_rel0':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.expr_rel0()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'se':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.se()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'expressao':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.expressao()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'atr_1':
                        self.origin.pop()
                        return self.atr_1()

                    elif self.origin[-1] == 'write_value_list':
                        self.origin.pop()
                        return self.write_value_list()

                    else:
                        self.errorSintatico(
                            ' an origin before expr_log1 return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim <> ##############
            ############## erro ##############
            ############## fim erro ##############

    # <expr_log2> ::= <operatorLog> <expressao> | <operator_multi> <expressao> | <operator_rel> <expressao> | <operator_soma> <expressao> | <>

    def expr_log2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <operatorLog> ##############
            if (self.getToken().getWord() == '&&' or self.getToken().getWord() == '||'
                    or self.getToken().getWord() == '*' or self.getToken().getWord() == '/'
                    or self.getToken().getWord() == '==' or self.getToken().getWord() == '>='
                    or self.getToken().getWord() == '<=' or self.getToken().getWord() == '!='
                    or self.getToken().getWord() == '>' or self.getToken().getWord() == '<'
                    or self.getToken().getWord() == '+' or self.getToken().getWord() == '-'):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expressao()
            ############## fim <operatorLog> ##############

            ############## <> ##############
            else:

                if len(self.origin) > 0:

                    if self.origin[-1] == 'retornar_funcao':
                        if self.getToken().getWord() == ';':
                            self.origin.pop()
                            return self.retornar_funcao()
                        else:
                            self.errorSintatico(' ; after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'com_retornar':
                        if self.getToken().getWord() == ';':
                            self.origin.pop()
                            return self.com_retornar()
                        else:
                            self.errorSintatico(' ; after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'enquanto':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.enquanto()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'para':
                        if self.getToken().getWord() == ';' or self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.para()
                        else:
                            self.errorSintatico(' ; or ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'expr_rel0':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.expr_rel0()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'se':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.se()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'expressao':
                        if self.getToken().getWord() == ')':
                            self.origin.pop()
                            return self.expressao()
                        else:
                            self.errorSintatico(' ) after an expressao')
                            self.palavra = ''
                            return

                    elif self.origin[-1] == 'atr_1':
                        self.origin.pop()
                        return self.atr_1()

                    elif self.origin[-1] == 'write_value_list':
                        self.origin.pop()
                        return self.write_value_list()

                ############## erro ##############
                    else:
                        self.errorSintatico(
                            ' an origin before expr_log2 return')
                        self.palavra = ''
                        return
            ############## fim erro ##############
                else:
                    return

    # <expr_valor_mod> ::=  number | <operator_auto0> <read_value> | <read_value> <operator_auto>

    def expr_valor_mod(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## number ##############
            if (self.isvalue(self.getToken()) == 'real' or self.isvalue(self.getToken()) == 'inteiro'):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                # self.palavra = ''
                self.getNextToken()
                return self.expr_multi_pos()
            ############## fim number ##############

            # SECOND DERIV.
            # <operator_auto0> ::= '++' | '--'
            ############## <operator_auto0> ##############
            elif self.getToken().getWord() == '++' or self.getToken().getWord() == '--':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('expr_multi_pos')
                return self.read_value()
            ############## fim <operator_auto0> ##############

            # THIRD DERIV.
            ############## <read_value> ##############
            elif self.getToken().getType() == 'IDE':
                self.origin.append('operator_auto')
                return self.read_value()
            ############## fim <read_value> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expr_valor_mod')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <operator_auto> ::= '++' | '--' | <>

    def operator_auto(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############## <operator_auto> ##############
            if (self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    and (self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']')):
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.palavra = ''
                self.getNextToken()
                return self.expr_multi_pos()
            ############## fim <operator_auto> ##############
            else:
                return self.expr_multi_pos()

    # <expr_multi> ::= <operator_soma> <expr_valor_mod> <expr_multi_pos> | <expr_valor_mod> <expr_multi_pos>

    def expr_multi(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            # <operator_soma> ::= '+' | '-'
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                
                self.semanticItem['var'] = self.getToken()
                var = self.semanticItem['var'].getWord()
                simboloVarConst = self.analisadorSemantico.getSimboloVarConst(var)

                if simboloVarConst.getCategoria() == 'variavel':
                    item = simboloVarConst
                    self.semanticItem = {}
                    self.semanticItem['categoria'] = item.getCategoria()
                    self.semanticItem['init'] = item.getInit()
                    self.semanticItem['tipo'] = item.getTipo()
                    self.semanticItem['nome'] = item.getNome()
                    self.semanticItem['escopo'] = item.getEscopo()
                    self.semanticItem['dimensao'] = item.getDimensao()
                    self.semanticItem['valor'] = self.getToken()

                    isValueOk = self.isSemanticItemValueOk()

                    if isValueOk == False:
                        self.checkSemanticItem(self.semanticItem['nome'], 'de categoria ' + self.semanticItem['categoria'] +
                                               ' tem tipo de valor associado diferente do declarado: ' + self.semanticItem['tipo'])
                    elif isValueOk == True:
                        self.analisadorSemantico.updateTabelaVarConst(
                            self.semanticItem['nome'], True)
                
                self.getNextToken()
                self.origin.append('expr_art1')
                return self.expr_valor_mod()
            ############## fim <operator_soma> ##############

            ############## <expr_valor_mod> ##############
            elif (self.getToken().getType() == 'NRO' or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'):
                self.origin.append('expr_art1')
                return self.expr_valor_mod()
            ############## fim <expr_valor_mod> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expr_multi')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expr_multi_pos> ::= <operator_multi> <expr_multi> | <>

    def expr_multi_pos(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <operator_multi> ##############
            if self.getToken().getWord() == '*' or self.getToken().getWord() == '/':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expr_multi()
            ############## fim <operator_multi> ##############

            ############## <> ##############
            else:

                if len(self.origin) > 0:

                    if self.origin[-1] == 'expr_number1':
                        self.origin.pop()
                        return self.expr_number1()

                    elif self.origin[-1] == 'expr_art1':
                        self.origin.pop()
                        return self.expr_art1()
                    else:
                        self.errorSintatico(
                            ' an origin before expr_multi_pos return')
                        self.palavra = ''
                        return
                else:
                    return

            ############## fim <> ##############

    # <expr_art> ::= number <expr_multi> <expr_art1>

    def expr_art(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.

            ############## <expr_multi> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                return self.expr_multi()

            elif (self.getToken().getType() == 'NRO' or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'):
                return self.expr_multi()
            ############## fim <expr_multi> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expr_art')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expr_art1> ::= <operator_soma> <expr_number> | <>

    def expr_art1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expr_number()
            ############## fim <operator_soma> ##############

            ############## <expr_number> ##############
            else:
                if len(self.origin) > 0:
                    if self.origin[-1] == 'expr_rel1':
                        self.origin.pop()
                        return self.expr_rel1()

                    elif self.origin[-1] == 'expr_number':
                        self.origin.pop()
                        return self.expr_number()

                    elif self.origin[-1] == 'vector_matrix':
                        self.origin.pop()
                        return self.vector_matrix()

                    elif self.origin[-1] == 'vector_matrix1':
                        self.origin.pop()
                        return self.vector_matrix1()

                    elif self.origin[-1] == 'v_m_access':
                        self.origin.pop()
                        return self.v_m_access()

                    elif self.origin[-1] == 'v_m_access1':
                        self.origin.pop()
                        return self.v_m_access1()
                ############## fim <expr_number> ##############

                ############# erro ##############
                    else:
                        self.errorSintatico(
                            ' an origin before expr_art1 return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim erro ##############

    # <expr_number> ::= <expr_art> | '(' <expr_number> ')' <expr_multi_pos> <expr_number1>

    def expr_number(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <expr_art> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO' or self.getToken().getWord() == '++'
                    or self.getToken().getWord() == '--' or self.getToken().getType() == 'IDE'):
                if (self.getPrevToken().getWord() == '[' or self.getPrevToken().getWord() == '('
                        or self.getPrevToken().getWord() == '+' or self.getPrevToken().getWord() == '-'):

                    if len(self.semanticItem['dimensao']) == 0:
                        self.semanticItem['dimensao'] = self.getToken(
                        ).getWord()
                    else:
                        self.semanticItem['dimensao'] = self.semanticItem['dimensao'] + \
                            'x' + self.getToken().getWord()

                    return self.expr_art()
                else:
                    self.errorSintatico(
                        ' [ or ( or + or - before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <expr_art> ##############

            # SECOND DERIV.
            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                if (self.getPrevToken().getWord() == '[' or self.getPrevToken().getWord() == '('
                        or self.getPrevToken().getWord() == '+' or self.getPrevToken().getWord() == '-'):
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('expr_number')
                    return self.expr_number()
                else:
                    self.errorSintatico(
                        ' [ or ( or + or - before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim '(' ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('expr_number1')
                return self.expr_multi_pos()
            ############## fim ')' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expr_number')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expr_number1>  ::= <operator_soma> <expr_number> | <>

    def expr_number1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <operator_soma> ##############
            if self.getToken().getWord() == '+' or self.getToken().getWord() == '-':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.expr_number()
            ############## fim <operator_soma> ##############

            else:

                if len(self.origin) > 0:

                    if self.origin[-1] == 'vector_matrix':
                        self.origin.pop()
                        return self.vector_matrix()

                    elif self.origin[-1] == 'vector_matrix1':
                        self.origin.pop()
                        return self.vector_matrix1()

                    elif self.origin[-1] == 'v_m_access':
                        self.origin.pop()
                        return self.v_m_access()

                    elif self.origin[-1] == 'v_m_access1':
                        self.origin.pop()
                        return self.v_m_access1()

                    elif self.origin[-1] == 'expr_rel1':
                        self.origin.pop()
                        return self.expr_rel1()

                    elif self.origin[-1] == 'expr_number':
                        self.origin.pop()
                        return self.expr_number()

                ############# erro ##############
                    else:
                        self.errorSintatico(
                            ' an origin before expr_number1 return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim erro ##############

    # <expr_rel0>   ::= <expr_rel> | '(' <expressao> ')'

    def expr_rel0(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <expr_rel> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO' or self.getToken().getWord() == '++'
                    or self.getToken().getWord() == '--' or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'):
                return self.expr_rel()
            ############## fim <expr_rel> ##############

            # SECOND DERIV.
            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('expr_rel0')
                return self.expressao()
            ############## fim '(' ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                if len(self.origin) > 0:
                    if self.origin[-1] == 'expr_log1':
                        self.origin.pop()
                        return self.expr_log1()
                    else:
                        self.errorSintatico(
                            ' an origin before expr_rel0 return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim ')' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expr_rel0')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expr_rel> ::= <expr_art> <expr_rel1> | boolean <expr_rel1>

    def expr_rel(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <expr_art> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO' or self.getToken().getWord() == '++'
                    or self.getToken().getWord() == '--' or self.getToken().getType() == 'IDE'
                    and (self.getToken().getWord() != 'verdadeiro' and self.getToken().getWord() != 'falso')):
                self.origin.append('expr_rel1')
                
                if self.getToken().getType() == 'NRO':
                    if self.semanticItem != {}:
                        var = self.semanticItem['var'].getWord()
                        isSimboloInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(self.semanticItem['nome'])
                        
                        if isSimboloInTabelaVarConst == True:
                            simboloVarConst = self.analisadorSemantico.getSimboloVarConst(self.semanticItem['nome'])
                            
                            if simboloVarConst.getCategoria() == 'constante':
                                self.checkSemanticItem(self.semanticItem['nome'], 'atribuicao de constante fora do bloco!')                        
                            
                            if simboloVarConst.getCategoria() == 'variavel':
                                self.semanticItem = {}
                                self.semanticItem['categoria'] = simboloVarConst.getCategoria()
                                self.semanticItem['init'] = True
                                self.semanticItem['tipo'] = simboloVarConst.getTipo()
                                self.semanticItem['nome'] = simboloVarConst.getNome()
                                self.semanticItem['escopo'] = simboloVarConst.getEscopo()
                                self.semanticItem['dimensao'] = simboloVarConst.getDimensao()
                                self.semanticItem['valor'] = self.getToken()

                                isValueOk = self.isSemanticItemValueOk()

                                if isValueOk == False:
                                    self.checkSemanticItem(self.semanticItem['nome'], 'de categoria ' + self.semanticItem['categoria'] +
                                                        ' tem tipo de valor associado diferente do declarado: ' + self.semanticItem['tipo'])
                                elif isValueOk == True:
                                    self.analisadorSemantico.updateTabelaVarConst(self.semanticItem['nome'], True)

                        elif isSimboloInTabelaVarConst == False:
                            self.checkSemanticItem(self.semanticItem['nome'], 'nao foi declarada')
                    
                elif self.getToken().getType() == 'IDE' and (self.getToken().getWord() != 'verdadeiro' or self.getToken().getWord() == 'falso'):
                    if self.semanticItem != {}:
                        isSimboloInTabelaVarConst = self.analisadorSemantico.isSimboloInTabelaVarConst(self.getToken().getWord())
                        
                        if isSimboloInTabelaVarConst == True:
                            self.semanticItem['var'] = self.getToken()
                            var = self.semanticItem['var'].getWord()
                            simboloVarConst = self.analisadorSemantico.getSimboloVarConst(var)

                            if simboloVarConst.getCategoria() == 'variavel':
                                item = simboloVarConst
                                self.semanticItem = {}
                                self.semanticItem['categoria'] = item.getCategoria()
                                self.semanticItem['init'] = item.getInit()
                                self.semanticItem['tipo'] = item.getTipo()
                                self.semanticItem['nome'] = item.getNome()
                                self.semanticItem['escopo'] = item.getEscopo()
                                self.semanticItem['dimensao'] = item.getDimensao()
                                self.semanticItem['valor'] = self.getToken()

                                isValueOk = self.isSemanticItemValueOk()

                                if isValueOk == False:
                                    self.checkSemanticItem(self.semanticItem['nome'], 'de categoria ' + self.semanticItem['categoria'] +
                                                        ' tem tipo de valor associado diferente do declarado: ' + self.semanticItem['tipo'])
                                elif isValueOk == True:
                                    self.analisadorSemantico.updateTabelaVarConst(self.semanticItem['nome'], True)

                        elif isSimboloInTabelaVarConst == False:
                            self.checkSemanticItem(self.semanticItem['nome'], 'nao foi declarada')
                    else:
                        self.checkSemanticItem(self.getToken().getWord(), 'nao foi declarada')

                return self.expr_art()
            ############## fim <expr_art> ##############

            # SECOND DERIV.
            ############## boolean ##############
            elif self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso':
                if self.semanticItem != {}:
                    var = self.semanticItem['var'].getWord()
                    simboloVarConst = self.analisadorSemantico.getSimboloVarConst(var)

                    if simboloVarConst.getCategoria() == 'variavel':
                        item = simboloVarConst
                        self.semanticItem = {}
                        self.semanticItem['categoria'] = item.getCategoria()
                        self.semanticItem['init'] = item.getInit()
                        self.semanticItem['tipo'] = item.getTipo()
                        self.semanticItem['nome'] = item.getNome()
                        self.semanticItem['valor'] = self.getToken()

                        isValueOk = self.isSemanticItemValueOk()

                        if isValueOk == False:
                            self.checkSemanticItem(self.semanticItem['nome'], 'de categoria ' + self.semanticItem['categoria'] +
                                                ' tem tipo de valor associado diferente do declarado: ' + self.semanticItem['tipo'])
                        elif isValueOk == True:
                            self.analisadorSemantico.updateTabelaVarConst(self.semanticItem['nome'], True)
                else:
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    
                return self.expr_rel1()
            ############## fim boolean ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on expr_rel')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <expr_rel1> ::= <operator_rel> <expr_rel0> | <>

    def expr_rel1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            if self.isRelOperator(self.getToken().getWord()):
                self.palavra = self.palavra + self.getToken().getWord() + ' '

                if self.semanticItem != {}:
                    var = self.semanticItem['var'].getWord()
                    simboloVarConst = self.analisadorSemantico.getSimboloVarConst(var)

                    if simboloVarConst.getCategoria() == 'variavel':
                        item = simboloVarConst
                        self.semanticItem = {}
                        self.semanticItem['categoria'] = item.getCategoria()
                        self.semanticItem['init'] = item.getInit()
                        self.semanticItem['tipo'] = item.getTipo()
                        self.semanticItem['nome'] = item.getNome()
                        self.semanticItem['valor'] = self.getToken()

                        isValueOk = self.isSemanticItemValueOk()

                        if isValueOk == False:
                            self.checkSemanticItem(self.semanticItem['nome'], 'de categoria ' + self.semanticItem['categoria'] +
                                                ' tem tipo de valor associado diferente do declarado: ' + self.semanticItem['tipo'])
                        elif isValueOk == True:
                            self.analisadorSemantico.updateTabelaVarConst(
                                self.semanticItem['nome'], True)

                self.getNextToken()
                return self.expr_rel0()

            else:
                if len(self.origin) > 0:
                    if self.origin[-1] == 'expr_log1':
                        self.origin.pop()
                        return self.expr_log1()

                    ############# erro ##############
                    else:
                        self.errorSintatico(
                            ' an origin before expr_rel1 return')
                        self.palavra = ''
                        return
                else:
                    return
                ############## fim erro ##############

    # <write_cmd> ::= escreva '(' <value_with_expressao> <write_value_list> ')' ';'

    def escreva(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'escreva' ##############
            if self.getToken().getWord() == 'escreva':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.escreva()
            ############## fim 'escreva' ##############

            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                if self.getPrevToken().getWord() == 'escreva':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.escreva()

                else:
                    self.errorSintatico('escreva before (')
                    self.palavra = ''
                    return
            ############## fim '(' ##############

            ############## <value_with_expressao> ##############
            elif self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.write_value_list()

            elif (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                self.origin.append('write_value_list')
                return self.expressao()
            ############## fim <value_with_expressao> ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.escreva()
            ############## fim ')' ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ')':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem = {}
                    self.palavra = ''
                    self.getNextToken()

                    if len(self.origin) > 0:

                        if self.origin[-1] == 'corpo_funcao2':
                            self.origin.pop()
                            return self.corpo_funcao2()

                        elif self.origin[-1] == 'com_body':
                            self.origin.pop()
                            return self.com_body()

                        else:
                            self.errorSintatico(
                                ' an origin before write_cmd return')
                            self.palavra = ''
                            return

                    else:
                        return

                else:
                    self.errorSintatico(') before ;')
                    self.palavra = ''
                    return

            ############## fim ';' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on write_value_list')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <write_value_list> ::= ',' <value_with_expressao> <write_value_list> | <>

    def write_value_list(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## ',' ##############
            if self.getToken().getWord() == ',':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.write_value_list()
            ############## fim ',' ##############

             ############## <value_with_expressao> ##############
            elif self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR':
                if self.getPrevToken().getWord() == ',':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.write_value_list()

                else:
                    self.errorSintatico(
                        ', before ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            elif (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                if self.getPrevToken().getWord() == ',':
                    self.origin.append('write_value_list')
                    return self.expressao()

                else:
                    self.errorSintatico(
                        ', before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <value_with_expressao> ##############

            elif self.getToken().getWord() == ')':
                return self.escreva()

            ############# erro ##############
            else:
                self.errorSintatico('other token on write_value_list')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <read_cmd> ::= leia '(' <read_value> <read_value_list> ')' ';'

    def leia(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'leia' ##############
            if self.getToken().getWord() == 'leia':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.leia()
            ############## fim 'leia' ##############

            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                if self.getPrevToken().getWord() == 'leia':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('read_value_list')
                    return self.read_value()
                else:
                    self.errorSintatico('leia before (')
                    self.palavra = ''
                    return
            ############## fim '(' ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.leia()

                else:
                    self.errorSintatico('IDE or ] before )')
                    self.palavra = ''
                    return
            ############## fim ')' ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ')':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.semanticItem = {}
                    self.palavra = ''
                    self.getNextToken()

                    if len(self.origin) > 0:

                        if self.origin[-1] == 'corpo_funcao2':
                            self.origin.pop()
                            return self.corpo_funcao2()

                        elif self.origin[-1] == 'com_body':
                            self.origin.pop()
                            return self.com_body()

                        else:
                            self.errorSintatico(
                                ' an origin before read_cmd return')
                            self.palavra = ''
                            return
                    else:
                        return
                else:
                    self.errorSintatico(' ) before ;')
                    self.palavra = ''
                    return
            ############## fim ';' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on read_cmd')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <read_value_list> ::= ',' <read_value> <read_value_list> |

    def read_value_list(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## ',' ##############
            if self.getToken().getWord() == ',':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.origin.append('read_value_list')
                    self.getNextToken()
                    return self.read_value()
                else:
                    self.errorSintatico('IDE or ] before ,')
                    self.palavra = ''
                    return
            # fim ',' ##############:

            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getType() == 'IDE' or self.getPrevToken().getWord() == ']':
                    return self.leia()
                else:
                    self.errorSintatico('IDE or ] before )')
                    self.palavra = ''
                    return

            ############# erro ##############
            else:
                self.errorSintatico('other token on read_value_list')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <com_enquanto> ::= enquanto '(' <args> ')' '{' <com_body> '}'

    def enquanto(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'enquanto' ##############
            if self.getToken().getWord() == 'enquanto':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.enquanto()
            ############## fim 'enquanto' ##############

            ############## '(' ##############
            elif self.getToken().getWord() == '(' and self.getPrevToken().getWord() == 'enquanto':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.args()
            ############## fim '(' ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.enquanto()
            ############## fim ')' ##############

            ############## '{' ##############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == ')':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('enquanto')
                    return self.com_body()
                else:
                    self.errorSintatico(') before {')
                    self.palavra = ''
                    return
            ############## fim '{' ##############

            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.palavra = ''
                self.getNextToken()

                if len(self.origin) > 0:

                    if self.origin[-1] == 'corpo_funcao2':
                        self.origin.pop()
                        return self.corpo_funcao2()

                    elif self.origin[-1] == 'com_body':
                        self.origin.pop()
                        return self.com_body()

                    else:
                        self.errorSintatico(
                            ' an origin before com_enquanto return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim '}' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on com_enquanto')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <args> ::= <expressao> |
    def args(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <args> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                self.origin.append('enquanto')
                return self.expressao()
            ############## fim <args> ##############

            ############## <> ##############
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getWord() == '(':
                    return self.enquanto()

                else:
                    self.errorSintatico(' ( before )')
                    self.palavra = ''
                    return
            ############## fim <> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on args')
                self.palavra = ''
                return
            ############# fim erro ##############

    # <com_para> ::= para '(' <init> <stop> ';' <step> ')' '{' <com_body> '}'

    def para(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'para' ##############
            if self.getToken().getWord() == 'para':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.para()
            ############## fim 'para' ##############

            ############## '(' ##############
            elif self.getToken().getWord() == '(':
                if self.getPrevToken().getWord() == 'para':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.init()
                else:
                    self.errorSintatico('para before (')
                    self.palavra = ''
                    return
            ############## fim '(' ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.step()
            ############## fim ';' ##############

            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.para()

            ############## '{' ##############
            elif self.getToken().getWord() == '{':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                self.origin.append('para')
                return self.com_body()
            ############## fim '{' ##############

            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.semanticItem = {}
                self.palavra = ''
                self.getNextToken()

                if len(self.origin) > 0:

                    if self.origin[-1] == 'corpo_funcao2':
                        self.origin.pop()
                        return self.corpo_funcao2()

                    elif self.origin[-1] == 'com_body':
                        self.origin.pop()
                        return self.com_body()

                    else:
                        self.errorSintatico(
                            ' an origin before com_para return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim '}' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on com_para')
                self.palavra = ''
                return
            ############## fim erro ##############

    def init(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            ############## FIRST DERIV OF <init> ##############
            if self.getToken().getType() == 'IDE':
                if self.getPrevToken().getWord() == '(':
                    self.origin.append('stop')
                    return self.var_atr()
                else:
                    self.errorSintatico('( before IDE')
                    self.palavra = ''
                    return

            ############## SECOND DERIV OF <init> ##############
            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == '(':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.stop()
            ############## fim <init> ##############
            ############## fim <init> ##############

            else:
                self.errorSintatico('other token on init')
                self.palavra = ''
                return

    def stop(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <stop> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                if self.getPrevToken().getWord() == ';':
                    self.origin.append('para')
                    return self.expressao()
                else:
                    self.errorSintatico('; before expressao')
                    self.palavra = ''
                    return
            ############## fim <stop> ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                if self.getPrevToken().getWord() == ';':
                    return self.para()
                else:
                    self.errorSintatico(' ; before ;')
                    self.palavra = ''
                    return
            ############## fim ';' ##############

            else:
                self.errorSintatico('other token on stop')
                self.palavra = ''
                return

    def step(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'para' ##############
            ############## <step> ##############
            if (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                if self.getPrevToken().getWord() == ';':
                    self.origin.append('para')
                    return self.expressao()
                else:
                    self.errorSintatico('; before expressao')
                    self.palavra = ''
                    return
            elif self.getToken().getWord() == ')':
                if self.getPrevToken().getWord() == ';':
                    return self.para()
                else:
                    self.errorSintatico(' ; before )')
                    self.palavra = ''
                    return
            ############## fim <step> ##############
            else:
                self.errorSintatico('other token on step')
                self.palavra = ''
                return

    # <se> ::= 'se' '(' <expressao> ')' '{' <com_body> '}' <se_body>

    def se(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'se' ##############
            if self.getToken().getWord() == 'se':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.se()
            ############## fim 'se' ##############

            ############## '(' ##############
            ############## <expressao> ##############
            elif self.getToken().getWord() == '(':
                if self.getPrevToken().getWord() == 'se':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('se')
                    return self.expressao()
                else:
                    self.errorSintatico('se before (')
                    self.palavra = ''
                    return
            ############## fim '(' ##############
            ############## fim <expressao> ##############

            ############## ')' ##############
            elif self.getToken().getWord() == ')':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.se()
            ############## fim ')' ##############

            ############## '{' ##############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == ')':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('se')
                    return self.com_body()
                else:
                    self.errorSintatico(' ) before {')
                    self.palavra = ''
                    return
            ############## fim '{' ##############

            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.palavra = ''
                self.getNextToken()
                return self.se_body()
            ############## fim '}' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on se')
                self.palavra = ''
                return
            ############## fim erro ##############

    def se_body(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'senao' ##############

            # <se_body>  ::= <senao> | <>
            if self.getToken().getWord() == 'senao':
                if self.getPrevToken().getWord() == '}':
                    return self.senao()
                else:
                    self.errorSintatico('} before senao')
                    self.palavra = ''
                    return
            ############## fim <senao> ##############

            else:
                if len(self.origin) > 0:

                    if self.origin[-1] == 'corpo_funcao2':
                        self.origin.pop()
                        return self.corpo_funcao2()

                    elif self.origin[-1] == 'com_body':
                        self.origin.pop()
                        return self.com_body()

                    else:
                        self.errorSintatico(' an origin before se_body return')
                        self.palavra = ''
                        return
                else:
                    return

    # <senao>  ::= 'senao' <se_senao>

    def senao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## 'senao' ##############
            if self.getToken().getWord() == 'senao':
                if self.getPrevToken().getWord() == '}':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.se_senao()
                else:
                    self.errorSintatico('} before senao')
                    self.palavra = ''
                    return
            ############## fim 'senao' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on senao')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <se_senao>  ::= <se> | '{' <com_body> '}'

    def se_senao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <se> ##############
            if self.getToken().getWord() == 'se':
                if self.getPrevToken().getWord() == 'senao':
                    return self.se()
                else:
                    self.errorSintatico('senao before se')
                    self.palavra = ''
                    return
            ############## fim <se> ##############

            # SECOND DERIV.
            ############## {<com_body> ##############
            elif self.getToken().getWord() == '{':
                if self.getPrevToken().getWord() == 'senao':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    self.origin.append('se_senao')
                    return self.com_body()
                else:
                    self.errorSintatico('senao before {')
                    self.palavra = ''
                    return
            ############## fim {<com_body> ##############

            ############## '}' ##############
            elif self.getToken().getWord() == '}':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.palavra = ''
                self.getNextToken()
                if len(self.origin) > 0:

                    if self.origin[-1] == 'corpo_funcao2':
                        self.origin.pop()
                        return self.corpo_funcao2()

                    elif self.origin[-1] == 'com_body':
                        self.origin.pop()
                        return self.com_body()

                    else:
                        self.errorSintatico(
                            ' an origin before se_senao return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim '}' ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on se_senao')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <com_body> ::= <com_enquanto> <com_body> | <com_para> <com_body> | <se> <com_body> | <write_cmd> <com_body> | <read_cmd> <com_body> |
                # <functionCall> <com_body> | <var_atr> <com_body> | <com_retornar>

    def com_body(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <com_enquanto> ##############
            if self.getToken().getWord() == 'enquanto':
                self.origin.append('com_body')
                return self.enquanto()
            ############## fim <com_enquanto> ##############

            # SECOND DERIV.
            ############## <com_para> ##############
            if self.getToken().getWord() == 'para':
                self.origin.append('com_body')
                return self.para()
            ############## fim <com_para> ##############

            # THIRD DERIV.
            ############## <se> ##############
            if self.getToken().getWord() == 'se':
                self.origin.append('com_body')
                return self.se()
            ############## fim <se> ##############

            # FOURTH DERIV.
            ############## <escreva> ##############
            if self.getToken().getWord() == 'escreva':
                self.origin.append('com_body')
                return self.escreva()
            ############## fim <escreva> ##############

            # FIFTH DERIV.
            ############## <leia> ##############
            if self.getToken().getWord() == 'leia':
                self.origin.append('com_body')
                return self.leia()
            ############## fim <leia> ##############

            # SIXTH DERIV.
            ############## <functionCall> ##############
            if self.getToken().getType() == 'IDE' and self.forward().getWord() == '(':
                self.origin.append('com_body')
                return self.chamada_funcao()
            ############## fim <functionCall> ##############

            # SEVENTH DERIV.
            ############## <var_atr> ##############
            if self.getToken().getType() == 'IDE':
                self.origin.append('com_body')
                return self.var_atr()
            ############## fim <var_atr> ##############

            # EIGTH DERIV.
            ############## <com_retornar>##############
            if self.getToken().getWord() == 'retorno':
                return self.com_retornar()
            ############## fim <com_retornar> ##############

            elif self.getToken().getWord() == '}':

                if len(self.origin) > 0:

                    if self.origin[-1] == 'enquanto':
                        self.origin.pop()
                        return self.enquanto()

                    elif self.origin[-1] == 'para':
                        self.origin.pop()
                        return self.para()

                    elif self.origin[-1] == 'se':
                        self.origin.pop()
                        return self.se()

                    elif self.origin[-1] == 'se_senao':
                        self.origin.pop()
                        return self.se_senao()

                    else:
                        self.errorSintatico(
                            ' an origin before } return')
                        self.palavra = ''
                        return
                else:
                    return

            ############# erro ##############
            else:
                self.errorSintatico('other token on com_body')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <com_retornar> ::= retorno <com_retornar1> ';' | <>

    def com_retornar(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## retorno ##############
            if self.getToken().getWord() == 'retorno':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.com_retornar1()
            ############## fim retorno ##############

            ############## ';' ##############
            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.palavra = ''
                self.getNextToken()

                if len(self.origin) > 0:

                    if self.origin[-1] == 'enquanto':
                        self.origin.pop()
                        return self.enquanto()

                    elif self.origin[-1] == 'para':
                        self.origin.pop()
                        return self.para()

                    elif self.origin[-1] == 'se':
                        self.origin.pop()
                        return self.se()

                    elif self.origin[-1] == 'senao':
                        self.origin.pop()
                        return self.senao()

                    elif self.origin[-1] == 'se_senao':
                        self.origin.pop()
                        return self.se_senao()

                    else:
                        self.errorSintatico(
                            ' an origin before ; return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim ';' ##############

            ############# erro ##############
            else:
                if len(self.origin) > 0:

                    if self.origin[-1] == 'enquanto':
                        self.origin.pop()
                        return self.enquanto()

                    elif self.origin[-1] == 'para':
                        self.origin.pop()
                        return self.para()

                    elif self.origin[-1] == 'se':
                        self.origin.pop()
                        return self.se()

                    elif self.origin[-1] == 'senao':
                        self.origin.pop()
                        return self.senao()

                    elif self.origin[-1] == 'se_senao':
                        self.origin.pop()
                        return self.se_senao()

                    else:
                        self.errorSintatico(
                            ' an origin before return')
                        self.palavra = ''
                        return
                else:
                    return
            ############## fim ';' ##############
            ############## fim erro ##############

    def com_retornar1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <com_retornar1> ##############
            # <com_retornar1> ::= <value_with_expressao> | <>
            if self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR':
                if self.getPrevToken().getWord() == 'retorno':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.com_retornar()

                else:
                    self.errorSintatico('retorno before value_with_expressao')
                    self.palavra = ''
                    return

            elif (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                if self.getPrevToken().getWord() == 'retorno':
                    self.origin.append('com_retornar')
                    return self.expressao()
                else:
                    self.errorSintatico('retorno before value_with_expressao')
                    self.palavra = ''
                    return
            ############## fim <value_with_expressao> ##############
            ############## fim <com_retornar1> ##############
            else:
                return self.com_retornar()

    # <function_body> ::= <declaration_const> <function_body1> | <function_body1>
    def corpo_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <declaration_const> ##############
            if self.getToken().getWord() == 'constantes':
                if self.getPrevToken().getWord() == '{':
                    self.origin.append('corpo_funcao1')
                    return self.declaracao_const('local')
                else:
                    self.errorSintatico(' { antes de constantes')
                    self.palavra = ''
                    return
            ############## fim <declaration_const> ##############

            # SECOND DERIV.
            ############## <function_body1> ##############
            elif (self.getToken().getWord() == 'variaveis'):
                if self.getPrevToken().getWord() == '{':
                    return self.corpo_funcao1()
                else:
                    self.errorSintatico(
                        ' { before ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            elif (self.getToken().getWord() == 'enquanto' or self.getToken().getWord() == 'para'
                    or self.getToken().getWord() == 'se' or self.getToken().getWord() == 'escreva'
                    or self.getToken().getWord() == 'leia' or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'retorno'):
                if self.getPrevToken().getWord() == '{':
                    return self.corpo_funcao2()
                else:
                    self.errorSintatico(
                        ' { before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <function_body1> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on function_body')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <function_body1>  ::= <declaration_var> <function_body2> | <function_body2>

    def corpo_funcao1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

            # FIRST DERIV.
            ############## <declaration_var> ##############
            if self.getToken().getWord() == 'variaveis':
                if self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}':
                    self.origin.append('corpo_funcao2')
                    return self.declaracao_var('local')
                else:
                    self.errorSintatico(
                        ' } or { before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <declaration_var> ##############

            # SECOND DERIV.
            ############## <function_body2> ##############
            elif (self.getToken().getWord() == 'enquanto' or self.getToken().getWord() == 'para'
                    or self.getToken().getWord() == 'se' or self.getToken().getWord() == 'escreva'
                    or self.getToken().getWord() == 'leia' or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'retorno'):
                if self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}':
                    return self.corpo_funcao2()
                else:
                    self.errorSintatico(
                        ' { or } before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <function_body2> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on function_body1')
                self.palavra = ''
                return
            ############## fim erro ##############

    def corpo_funcao2(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

           # FIRST DERIV.
            ############## <com_enquanto> ##############
            if self.getToken().getWord() == 'enquanto':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.enquanto()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <com_enquanto> ##############

            # SECOND DERIV.
            ############## <com_para> ##############
            if self.getToken().getWord() == 'para':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.para()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <com_para> ##############

            # THIRD DERIV.
            ############## <se> ##############
            if self.getToken().getWord() == 'se':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.se()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <se> ##############

            # FOURTH DERIV.
            ############## <escreva> ##############
            if self.getToken().getWord() == 'escreva':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.escreva()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <escreva> ##############

            # FIFTH DERIV.
            ############## <leia> ##############
            if self.getToken().getWord() == 'leia':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.leia()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <leia> ##############

            # SIXTH DERIV.
            ############## <functionCall> ##############
            if self.getToken().getType() == 'IDE' and self.forward().getWord() == '(':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.chamada_funcao()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <functionCall> ##############

            # SEVENTH DERIV.
            ############## <var_atr> ##############
            if self.getToken().getType() == 'IDE':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    self.origin.append('corpo_funcao2')
                    return self.var_atr()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <var_atr> ##############

            # EIGTH DERIV.
            ############## <com_retornar>##############
            if self.getToken().getWord() == 'retorno':
                if (self.getPrevToken().getWord() == '{' or self.getPrevToken().getWord() == '}'
                        or self.getPrevToken().getWord() == ';'):
                    return self.retornar_funcao()
                else:
                    self.errorSintatico(
                        ' } or { or ; before ' + self.getToken().getWord())
                    self.palavra = ''
                    return
            ############## fim <com_retornar> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on function_body2')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <retornar> ::= retorno <retornar1> ';'

    def retornar_funcao(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):

           # FIRST DERIV.
            ############## retorno ##############
            if self.getToken().getWord() == 'retorno':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.getNextToken()
                return self.retornar_funcao1()
            ############## fim retorno ##############

            elif self.getToken().getWord() == ';':
                self.palavra = self.palavra + self.getToken().getWord() + ' '
                self.palavra = ''
                self.getNextToken()

                if len(self.origin) > 0:

                    if self.origin[-1] == 'main_function':
                        self.origin.pop()
                        return self.main_function()

                    elif self.origin[-1] == 'declaracao_funcao2':
                        self.origin.pop()
                        return self.declaracao_funcao2()
                    else:
                        self.errorSintatico(
                            ' an origin before retornar return')
                        self.palavra = ''
                        return
                else:
                    return
                # FIM DE CORPO DE FUNCAO

            ############# erro ##############
            else:
                self.errorSintatico('other token on retornar_funcao')
                self.palavra = ''
                return
            ############## fim erro ##############

    # <retornar1> ::= cad | char | <expressao> | <>

    def retornar_funcao1(self):
        if self.getToken().getType() == 'EOF':
            return

        elif self.counter < len(self.tokens):
            ############## cad | char ##############
            if self.getToken().getType() == 'CAD' or self.getToken().getType() == 'CAR':
                if self.getPrevToken().getWord() == 'retorno':
                    self.palavra = self.palavra + self.getToken().getWord() + ' '
                    self.getNextToken()
                    return self.retornar_funcao()
                else:
                    self.errorSintatico(' retorno before ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            ############## <expressao> ##############
            elif (self.getToken().getWord() == '+' or self.getToken().getWord() == '-'
                    or self.getToken().getType() == 'NRO'
                    or self.getToken().getWord() == '++' or self.getToken().getWord() == '--'
                    or self.getToken().getType() == 'IDE'
                    or self.getToken().getWord() == 'verdadeiro' or self.getToken().getWord() == 'falso'
                    or self.getToken().getWord() == '(' or self.getToken().getWord() == '!'):
                if self.getPrevToken().getWord() == 'retorno':
                    self.origin.append('retornar_funcao')
                    return self.expressao()
                else:
                    self.errorSintatico(
                        ' retorno before ' + self.getToken().getWord())
                    self.palavra = ''
                    return

            ############## <> ##############
            elif self.getToken().getWord() == ';':
                return self.retornar_funcao()
            ############## fim <retornar1> ##############

            ############# erro ##############
            else:
                self.errorSintatico('other token on retornar1')
                self.palavra = ''
                return
            ############## fim erro ##############
