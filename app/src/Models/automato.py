from Token import Token
from lexemas import Lexemas
from State import State

class Automato:

    def __init__(self, file):
        self.file = open(file,'r')
        self.lexemas = Lexemas()
        self.states = []
    
    def getNextToken(self):
            file = self.file.readlines()
            for idxLine, line in enumerate(file):
                sizePalavra = 0
                state = State(0)
                word = ''
                
                for idxChar,char in enumerate(line):
                    # print('Posição:',idxChar, 'Char: ',char)
                
                    #####################{{ q0 }}#########################
                    if state.getStateNumber() == 0:                    
                        if char == '\n' or char == '\t' or self.lexemas.isSpace(char):
                            state = State(0)
                        
                        elif bytes(char, 'ascii').islower():
                            # tamanho da palavra
                            sizePalavra += 1
                            state = State(1)
                            word = word + char
                        
                        elif bytes(char, 'ascii').isupper():
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
                        
                        elif char in ['*','/']:
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
                        
                        elif char in self.lexemas.START_DELIMITERS:
                            state = State(15)
                            word = word + char
                        
                        elif char in self.lexemas.END_DELIMITERS:
                            state = State(16)
                            word = word + char
                        
                        else:
                            # ALGUM ERRO
                            print('ERRO 1',word)
                            print('ERRO 2',state.getStateNumber())
                            state = State(0)
                    #####################{{ FIM Q0 }}#########################
                    
                    
                    #####################{{ q1 }}#########################
                    elif state.getStateNumber() == 1:
                        if ((sizePalavra == 1 or sizePalavra < 10) and bytes(char, 'ascii').islower()):
                            sizePalavra += 1
                            word = word + char

                        elif self.lexemas.isSpace(char) or char == '\n':
                            if (sizePalavra >= 2 and sizePalavra <= 10 and sizePalavra != 3) and self.lexemas.isReservedWord(word):
                                token = Token(word, 'PRE', idxLine)

                            else:
                                token = Token(word, 'IDE', idxLine)
                                self.states.append(token)
                                word = ''
                                state = State(0)

                        elif self.lexemas.isLetter(char) or self.lexemas.isDigit(char) or char == '_':
                            word = word + char
                        
                        elif self.lexemas.isEndDelimiter(char):
                            token = Token(word, 'IDE', idxLine)
                            self.states.append(token)
                            
                            token = Token(char, 'DEL', idxLine)
                            self.states.append(token)
                            
                            word = ''
                            state = State(0)
                        
                        else:
                            state = State(0)
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
                        
                        else:
                            #q5
                            word = word + char
                            token = Token(word, 'NMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                    #####################{{ FIM q2 }}#########################
                    
                    
                    #####################{{ q3 }}#########################
                    elif state.getStateNumber() == 3:
                        if self.lexemas.isDigit(char):
                            state = State(4)
                            word = word + char
                        
                        else:
                            word = word + char
                            token = Token(word, 'NMF', idxLine)
                            self.states.append(token)
                            state = State(5)
                            word = ''
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
                        
                        else:
                            word = word + char
                            token = Token(word, 'NMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                    #####################{{ FIM q4 }}#########################
                    
                    
                    #####################{{ q6 }}#########################
                    elif state.getStateNumber() == 6:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'REL', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                        
                        elif char == '=':
                            word = word + char
                            token = Token(word, 'REL', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                    #####################{{ FIM q6 }}#########################
                    
                    
                    #####################{{ q7 }}#########################
                    elif state.getStateNumber() == 7:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                        
                        elif char == '=':                   # !=
                            word = word + char
                            token = Token(word, 'REL', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                        
                        elif self.lexemas.isLetter(char) or char =='!':             # ! or !! or !!! ...
                            token = Token(word, 'LOG', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)      
                         
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                    #####################{{ FIM q7 }}#########################
                    
                    
                    #####################{{ q10 }}#########################
                    elif state.getStateNumber() == 10:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'ART', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
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
                            token = Token(word, 'ART', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
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
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                    #####################{{ FIM q12 }}#########################
                    
                    #####################{{ q13 }}#########################
                    elif state.getStateNumber() == 13:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                            
                        elif char == '&':
                            token = Token(word, 'LOG', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                            
                        else:
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                    #####################{{ FIM q13 }}#########################
                    
                    #####################{{ q14 }}#########################
                    elif state.getStateNumber() == 14:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                            
                        elif char == '|':
                            token = Token(word, 'LOG', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                            
                        else:
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            state = State(0)
                            word = ''
                    #####################{{ FIM q14 }}#########################
                    
                    
                    #####################{{ q15 }}#########################
                    elif state.getStateNumber() == 15:
                        if self.lexemas.isSpace(char):
                            token = Token(word, 'DEL', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                    #####################{{ FIM q15 }}#########################
                    
                    #####################{{ q16 }}#########################
                    elif state.getStateNumber() == 16:
                        if self.lexemas.isSpace(char):
                            token = Token(word, 'DEL', idxLine)
                            self.states.append(token)
                            word =''
                            state = State(0)
                    #####################{{ FIM q16 }}#########################
                    
            return self.states