# -*- coding: utf-8 -*-
# coding: utf-8
from Token import Token
from lexemas import Lexemas
from State import State


class Automato:

    def __init__(self, file):
        self.file = open(file, 'r')
        self.lexemas = Lexemas()
        self.states = []
        self.errors = []

    def getTokens(self):
        file = self.file.readlines()
        file[len(file)-1] = file[len(file)-1] + ' '
        file.append("\n")
        blockComment = False
        comments = []

        for idxLine, line in enumerate(file):
            sizePalavra = 0
            state = State(0)
            word = ''
            errou = False
            sizeFile = len(file)
            sizeFileid = idxLine

            for idxChar, char in enumerate(line):
                before = state.getStateNumber()

                if blockComment == True and state.getStateNumber() == 0 and not(sizeFile-1 == sizeFileid):
                    if len(self.errors) > 0:
                        if self.errors[len(self.errors)-1].getType() == 'CoMF':
                            word = comments[0]
                            comments.pop()
                            self.errors.pop()

                    if char == '#' or char == '}':
                        state = State(24)

                    else:
                        state = State(19)

                #####################{{ q0 }}#########################
                if state.getStateNumber() == 0:
                    if char == '\n' or char == '\t' or self.lexemas.isSpace(char):
                        state = State(0)

                    elif self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').islower():
                        # tamanho da palavra
                        sizePalavra += 1
                        state = State(1)
                        word = word + char

                    elif self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').isupper():
                        state = State(1)
                        word = word + char

                    elif self.lexemas.isDigit(char):
                        state = State(2)
                        word = word + char

                    elif char in ['=', '<', '>']:
                        state = State(6)
                        word = word + char

                    elif char == '!':
                        state = State(7)
                        word = word + char

                    elif char in ['*', '/']:
                        state = State(10)
                        word = word + char

                    elif char == '+':
                        state = State(11)
                        word = word + char

                    elif char == '-':
                        state = State(12)
                        word = word + char

                    elif char == '&':
                        state = State(13)
                        word = word + char

                    elif char == '|':
                        state = State(14)
                        word = word + char

                    elif char in self.lexemas.START_DELIMITERS and char != '{':
                        state = State(15)
                        word = word + char

                    elif char in self.lexemas.END_DELIMITERS:
                        state = State(16)
                        word = word + char

                    elif self.lexemas.isCommentDelimiter(char):
                        state = State(17)
                        word = word + char

                    elif char == '{':
                        state = State(18)
                        word = word + char

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracter(char):
                        word = word + char
                        state = State(20)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracters(char):
                        word = word + char
                        state = State(21)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isValidSimbol(char):
                        word = word + char
                        state = State(22)

                    elif not self.lexemas.isAsciiChar(char):
                        word = word + char
                        state = State(25)

                    else:
                        # ALGUM ERRO
                        word = word + char
                        state = State(22)
                #####################{{ FIM Q0 }}#########################

                #####################{{ q1 }}#########################
                elif state.getStateNumber() == 1:
                    if (self.lexemas.isAsciiChar(char) and (sizePalavra == 1 or sizePalavra <= 10) and bytes(char, 'ascii').islower()):
                        sizePalavra += 1
                        word = word + char

                    elif self.lexemas.isSpace(char) or char == '\n':
                        if (sizePalavra >= 2 and sizePalavra <= 10 and sizePalavra != 3) and self.lexemas.isReservedWord(word):
                            token = Token(word, 'PRE', idxLine)
                            self.states.append(token)
                            word = ''
                            state = State(0)
                            sizePalavra = 0

                        else:
                            token = Token(word, 'IDE', idxLine)
                            self.states.append(token)
                            word = ''
                            state = State(0)
                            sizePalavra = 0

                    elif self.lexemas.isLetter(char) or self.lexemas.isDigit(char) or char == '_':
                        word = word + char
                        state = State(1)

                    elif self.lexemas.isStartDelimiter(char):
                        token = Token(word, 'IDE', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(15)

                    elif self.lexemas.isEndDelimiter(char):
                        token = Token(word, 'IDE', idxLine)
                        self.states.append(token)

                        word = char
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = ''
                        state = State(0)

                    elif self.lexemas.isLogicalOperator(char) or self.lexemas.isArithmeticOperator(char) or self.lexemas.isRelationalOperator(char):
                        word = word + char
                        state = State(9)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isValidSimbol(char):
                        token = Token(word, 'IDE', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(22)

                    elif not self.lexemas.isAsciiChar(char):
                        word = word + char
                        state = State(25)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracter(char):
                        token = Token(word, 'IDE', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(20)
                        sizePalavra = 0

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracters(char):
                        token = Token(word, 'IDE', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(21)

                    else:
                        state = State(22)
                        # print('error')
                #####################{{ FIM q1 }}#########################

                #####################{{ q2 }}#########################
                elif state.getStateNumber() == 2:
                    if self.lexemas.isDigit(char):
                        state = State(2)
                        word = word + char

                    elif char == '.':
                        state = State(3)
                        word = word + char

                    elif self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'NRO', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif self.lexemas.isLetter(char):
                        state = State(5)
                        word = word + char

                    elif self.lexemas.isEndDelimiter(char):
                        token = Token(word, 'NRO', idxLine)
                        self.states.append(token)

                        token = Token(char, 'DEL', idxLine)
                        self.states.append(token)
                        word = ''
                        state = State(0)

                    elif self.lexemas.isLogicalOperator(char) or self.lexemas.isArithmeticOperator(char) or self.lexemas.isRelationalOperator(char):
                        word = word + char
                        state = State(5)

                    elif not self.lexemas.isAsciiChar(char) or self.lexemas.isValidSimbol(char):
                        word = word + char
                        state = State(5)

                    else:
                        word = word + char
                        state = State(5)
                #####################{{ FIM q2 }}#########################

                #####################{{ q3 }}#########################
                elif state.getStateNumber() == 3:
                    if self.lexemas.isDigit(char):
                        state = State(4)
                        word = word + char

                    else:
                        word = word + char
                        state = State(5)
                #####################{{ FIM q3 }}#########################

                #####################{{ q4 }}#########################
                elif state.getStateNumber() == 4:
                    if self.lexemas.isDigit(char):
                        state = State(4)
                        word = word + char

                    elif self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'NRO', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif self.lexemas.isEndDelimiter(char) and char != '.':
                        token = Token(word, 'NRO', idxLine)
                        self.states.append(token)

                        token = Token(char, 'DEL', idxLine)
                        self.states.append(token)

                        word = ''
                        state = State(0)

                    elif self.lexemas.isLogicalOperator(char) or self.lexemas.isArithmeticOperator(char) or self.lexemas.isRelationalOperator(char):
                        token = Token(word, 'NRO', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(9)

                    else:
                        word = word + char
                        state = State(5)
                #####################{{ FIM q4 }}#########################

                #####################{{ q5 }}#########################
                elif state.getStateNumber() == 5:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'NMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char == '.':
                        word = word + char
                        state = State(5)

                    elif self.lexemas.isStartDelimiter(char):
                        token = Token(word, 'NMF', idxLine)
                        self.errors.append(token)

                        word = char
                        state = State(15)

                    elif self.lexemas.isEndDelimiter(char) and char != '.':
                        token = Token(word, 'NMF', idxLine)
                        self.errors.append(token)

                        word = char
                        state = State(16)

                    else:
                        state = State(5)
                        word = word + char
                #####################{{ FIM q5 }}#########################

                #####################{{ q6 }}#########################
                elif state.getStateNumber() == 6:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'REL', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif char == '=':
                        word = word + char
                        state = State(8)

                    elif char != '=' and self.lexemas.isLogicalOperator(char) or self.lexemas.isArithmeticOperator(char) or self.lexemas.isRelationalOperator(char):
                        word = word + char
                        state = State(9)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q6 }}#########################

                #####################{{ q7 }}#########################
                elif state.getStateNumber() == 7:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'LOG', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif char == '=':                   # !=
                        word = word + char
                        token = Token(word, 'REL', idxLine)
                        self.states.append(token)
                        word = ''
                        state = State(0)

                    # ! or !! or !!! ...
                    elif bytes(char, 'ascii').isupper() or bytes(char, 'ascii').islower() or char == '!':
                        word = word + char
                        state = State(9)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q7 }}#########################

                #####################{{ q8 }}#########################
                elif state.getStateNumber() == 8:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'REL', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q8 }}#########################

                #####################{{ q9 }}#########################
                elif state.getStateNumber() == 9:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'OpMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char == '.':
                        word = word + char
                        state = State(9)

                    elif not self.lexemas.isAsciiChar(char):
                        word = word + char
                        state = State(9)

                    elif self.lexemas.isStartDelimiter(char):
                        token = Token(word, 'OpMF', idxLine)
                        self.errors.append(token)

                        word = char
                        state = State(15)

                    elif self.lexemas.isEndDelimiter(char) and char != '.' and char != ';':
                        token = Token(word, 'OpMF', idxLine)
                        self.errors.append(token)

                        word = char
                        state = State(16)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q9 }}#########################

                #####################{{ q10 }}#########################
                elif state.getStateNumber() == 10:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'ART', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q10 }}#########################

                #####################{{ q11 }}#########################
                elif state.getStateNumber() == 11:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'ART', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif char == '+':
                        word = word + char
                        state = State(11)

                    elif self.lexemas.isCommentDelimiter(char):
                        token = Token(word, 'ART', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(17)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q11 }}#########################

                #####################{{ q12 }}#########################
                elif state.getStateNumber() == 12:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'ART', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif char == '-':
                        word = word + char
                        token = Token(word, 'ART', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif self.lexemas.isDigit(char):
                        word = word + char
                        state = State(5)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q12 }}#########################

                #####################{{ q13 }}#########################
                elif state.getStateNumber() == 13:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'OpMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char == '&':
                        word = word + char
                        state = State(99)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q13 }}#########################

                #####################{{ q14 }}#########################
                elif state.getStateNumber() == 14:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'OpMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char == '|':
                        word = word + char
                        state = State(99)

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q14 }}#########################

                #####################{{ q99 }}#########################
                elif state.getStateNumber() == 99:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'LOG', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    else:
                        word = word + char
                        state = State(9)
                #####################{{ FIM q99 }}#########################

                #####################{{ q15 }}#########################
                elif state.getStateNumber() == 15:
                    if self.lexemas.isEndDelimiter(char) or self.lexemas.isStartDelimiter(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(15)

                    elif self.lexemas.isSpace(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)
                        word = ''
                        state = State(0)

                    elif self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').islower():
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        # tamanho da palavra
                        sizePalavra += 1
                        state = State(1)
                        word = char

                    elif self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').isupper():
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        state = State(1)
                        word = char

                    elif self.lexemas.isDigit(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(2)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracter(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(20)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracters(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(21)

                    else:
                        word = char
                        state = State(22)
                #####################{{ FIM q15 }}#########################

                #####################{{ q16 }}#########################
                elif state.getStateNumber() == 16:
                    if self.lexemas.isEndDelimiter(char) or self.lexemas.isStartDelimiter(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(16)

                    elif self.lexemas.isSpace(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)
                        word = ''
                        state = State(0)

                    elif self.lexemas.isDigit(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(2)

                    else:
                        word = char
                        state = State(22)
                #####################{{ FIM q16 }}#########################

                #####################{{ q17 }}#########################
                elif state.getStateNumber() == 17:
                    if char == '\n':
                        word = ''
                        state = State(0)

                    else:
                        state = State(17)
                #####################{{ FIM q17 }}#########################

                #####################{{ q18 }}#########################
                elif state.getStateNumber() == 18:
                    if char == '#':
                        word = word + char
                        state = State(19)
                        blockComment = True

                    elif char == '\n' or self.lexemas.isSpace(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)
                        state = State(0)
                        word = ''

                    elif self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').islower():
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        # tamanho da palavra
                        sizePalavra = 1
                        state = State(1)
                        word = char

                    elif self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').isupper():
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        state = State(1)
                        word = char

                    elif self.lexemas.isDigit(char):
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        state = State(2)

                    elif char == '}':
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)

                        word = char
                        token = Token(word, 'DEL', idxLine)
                        self.states.append(token)
                        state = State(0)

                    elif self.lexemas.isLogicalOperator(char) or self.lexemas.isArithmeticOperator(char) or self.lexemas.isRelationalOperator(char):
                        word = word + char
                        state = State(9)

                    else:
                        word = word + char
                        state = State(22)

                #####################{{ FIM q18 }}#########################

                #####################{{ q19 }}#########################
                elif state.getStateNumber() == 19:
                    if char == '#':
                        word = word + char
                        state = State(24)

                    elif char == "\n":
                        word = word + char
                        token = Token(word, 'CoMF', idxLine)
                        comments.append(word)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char == " ":
                        word = word + char
                        token = Token(word, 'CoMF', idxLine)
                        comments.append(word)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    else:
                        word = word + char
                #####################{{ FIM q19 }}#########################

                #####################{{ q20 }}#########################
                elif state.getStateNumber() == 20:
                    if not self.lexemas.isAsciiChar(char):
                        word = word + char
                        state = State(20)

                    elif ((self.lexemas.isValidSimbol(char) or char == '\'') and sizePalavra < 1):
                        sizePalavra += 1
                        word = word + char

                    elif sizePalavra == 1 and self.lexemas.isCaracter(char):
                        word = word + char
                        token = Token(word, 'CAR', idxLine)
                        self.states.append(token)
                        sizePalavra = 0
                        state = State(0)
                        word = ''

                    elif self.lexemas.isCaracter(char) or char == '\n':
                        word = word + char
                        token = Token(word, 'CaMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    else:
                        word = word + char
                        sizePalavra += 1
                #####################{{ FIM q20 }}#########################

                #####################{{ q21 }}#########################
                elif state.getStateNumber() == 21:
                    sizePalavra += 1

                    if self.lexemas.isAsciiChar(char) and bytes(char, 'ascii').hex() == '5c' and (self.lexemas.isCaracter(line[idxChar+1]) or self.lexemas.isCaracters(line[idxChar+1]) or bytes(line[idxChar+1], 'ascii').hex() == '5c'):
                        word = word + char
                        state = State(21)

                    if not self.lexemas.isAsciiChar(char):
                        errou = True
                        word = word + char
                        state = State(21)

                    elif (self.lexemas.isAsciiChar(char) and self.lexemas.isValidSimbol(char)) and ((bytes(char, 'ascii').hex() == '5c' and bytes(line[idxChar-1], 'ascii').hex() == '5c') or (self.lexemas.isCaracter(char) and bytes(line[idxChar-1], 'ascii').hex() == '5c') or (self.lexemas.isCaracters(char) and bytes(line[idxChar-1], 'ascii').hex() == '5c')):
                        word = word + char

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isValidSimbol(char):
                        word = word + char
                        state = State(21)

                    elif sizePalavra == 2 and self.lexemas.isCaracters(char) and bytes(line[idxChar-1], 'ascii').hex() == '5c':
                        word = word + char
                        token = Token(word, 'CMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isCaracters(char):

                        if errou == True:
                            word = word + char
                            token = Token(word, 'CMF', idxLine)
                            self.errors.append(token)
                            state = State(0)
                            word = ''

                        else:
                            word = word + char
                            token = Token(word, 'CAD', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''

                    elif char == '\n':
                        token = Token(word, 'CMF', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif not self.lexemas.isValidSimbol(char):
                        errou = True
                        word = word + char

                #####################{{ FIM q21 }}#########################

                #####################{{ q22 }}#########################
                elif state.getStateNumber() == 22:
                    if self.lexemas.isSpace(char) or char == '\n':
                        token = Token(word, 'SII', idxLine)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif self.lexemas.isDigit(char):
                        word = word + char
                        state = State(5)

                    elif self.lexemas.isStartDelimiter(char):
                        token = Token(word, 'SII', idxLine)
                        self.errors.append(token)

                        word = char
                        state = State(15)

                    elif self.lexemas.isEndDelimiter(char) and char != '.':
                        token = Token(word, 'SII', idxLine)
                        self.errors.append(token)

                        word = char
                        state = State(16)

                    elif self.lexemas.isAsciiChar(char) and self.lexemas.isValidSimbol(char):
                        word = word + char
                        state = State(22)

                    elif not self.lexemas.isAsciiChar(char) and not self.lexemas.isValidSimbol(char):
                        word = word + char
                        state = State(25)

                    else:
                        word = word + char
                        state = State(22)
                #####################{{ FIM q22 }}#########################

                #####################{{ q23 }}#########################

                #####################{{ FIM 23 }}#########################

                #####################{{ q24 }}#########################
                elif state.getStateNumber() == 24:
                    if char == '}':
                        word = word + char
                        #token = Token(word, 'COM', idxLine)
                        # self.states.append(token)
                        blockComment = False
                        state = State(0)
                        word = ''

                    elif char == "\n":
                        word = word + char
                        token = Token(word, 'CoMF', idxLine)
                        comments.append(word)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char == " ":
                        word = word + char
                        token = Token(word, 'CoMF', idxLine)
                        comments.append(word)
                        self.errors.append(token)
                        state = State(0)
                        word = ''

                    elif char != "#":
                        word = word + char
                        state = State(19)
                #####################{{ FIM 24 }}#########################

                #####################{{ q25 }}#########################
                elif state.getStateNumber() == 25:
                    if self.lexemas.isSpace(char) or char == '\n':
                        word = word + char
                        token = Token(word, 'SII', idxLine)
                        self.errors.append(token)

                        word = ''
                        state = State(0)

                    else:
                        word = word + char
                        state = State(25)
                #####################{{ FIM 25 }}#########################
                #print('Posição:', idxChar, 'Char: ', char, 'Before:', before, 'state:', state.getStateNumber())

        return {'states': self.states, 'errors': self.errors}
