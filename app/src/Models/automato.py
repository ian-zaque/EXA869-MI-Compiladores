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
                numState = 0
                word = ''
                
                for idxChar,char in enumerate(line):
                    # print('Posição:',idxChar, 'Char: ',char)
                
                    #####################{{ q0 }}#########################
                    if numState == 0:
                        if self.lexemas.isLetter(char):
                            numState = 1
                            word = word + char
                        
                        elif char == '\n' or self.lexemas.isSpace(char):
                            numState = 0
                        
                        elif self.lexemas.isDigit(char):
                            numState = 2
                            word = word + char
                        
                        elif char in ['=', '<', '>']:
                            numState = 6
                            word = word + char
                            
                        elif char == '!':
                            numState = 7
                            word = word + char
                        
                        elif char in ['*','/']:
                            numState = 10
                            word = word + char
                        
                        elif char == '+':
                            numState = 11
                            word = word + char
                        
                        elif char == '-':
                            numState= 12
                            word = word + char
                        
                        else:
                            # ALGUM ERRO
                            numState = 99
                    #####################{{ FIM Q0 }}#########################
                    
                    #####################{{ q1 }}#########################
                    elif numState == 1:
                        if self.lexemas.isLetter(char) or self.lexemas.isDigit(char) or char=='_':
                            numState = 1
                            word = word + char
                        
                        elif self.lexemas.isSpace(char) or self.lexemas.isDelimiter(char) or char == '\n':
                            if self.lexemas.isReservedWord(word):
                                token = Token(word,'PRE',idxLine)
                            else:
                                token = Token(word,'IDE',idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0
                            #TRATAR ESPAÇO AQUI
                            
                        else:               # TRATAR ERROS OU OUTRA OCASIOES AQUI
                            numState = 0
                    #####################{{ FIM q1 }}#########################
                    
                    #####################{{ q2 }}#########################
                    elif numState == 2:
                        if self.lexemas.isDigit(char):
                            numState = 2
                            word = word + char

                        elif char == '.':
                            numState = 3
                            word = word + char
                        
                        elif self.lexemas.isSpace(char) or self.lexemas.isDelimiter(char) or char == '\n':
                            token = Token(word, 'NRO', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                        
                        else:
                            #q5
                            word = word + char
                            token = Token(word, 'NMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                    #####################{{ FIM q2 }}#########################
                    
                    #####################{{ q3 }}#########################
                    elif numState == 3:
                        if self.lexemas.isDigit(char):
                            numState = 4
                            word = word + char
                        
                        else:
                            word = word + char
                            token = Token(word, 'NMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                    #####################{{ FIM q3 }}#########################
                    
                    #####################{{ q4 }}#########################
                    elif numState == 4:
                        if self.lexemas.isDigit(char):
                            numState = 4
                            word = word + char
                        
                        elif self.lexemas.isSpace(char) or self.lexemas.isDelimiter(char) or char == '\n':
                            token = Token(word, 'NRO', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                        
                        else:
                            word = word + char
                            token = Token(word, 'NMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                    #####################{{ FIM q4 }}#########################
                    
                    #####################{{ q6 }}#########################
                    elif numState == 6:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'REL', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                        
                        elif char == '=':
                            word = word + char
                            token = Token(word, 'REL', idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0
                    #####################{{ FIM q6 }}#########################
                    
                    #####################{{ q7 }}#########################
                    elif numState == 7:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                        
                        elif char == '=':
                            word = word + char
                            token = Token(word, 'REL', idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0
                        
                        elif self.lexemas.isLetter(char):
                            token = Token(word, 'LOG', idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0                   
                         
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0
                    #####################{{ FIM q7 }}#########################
                    
                    #####################{{ q10 }}#########################
                    elif numState == 10:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'ART', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            word =''
                            numState = 0
                    #####################{{ FIM q10 }}#########################
                    
                    #####################{{ q11 }}#########################
                    elif numState == 11:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                            
                        elif char == '+':
                            word = word + char
                            token = Token(word, 'ART', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                     #####################{{ FIM q11 }}#########################
                    
                    
                    #####################{{ q12 }}#########################
                    elif numState == 12:
                        if self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                            
                        elif char == '-':
                            word = word + char
                            token = Token(word, 'ART', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                            
                        else:
                            word = word + char
                            token = Token(word, 'OpMF', idxLine)
                            self.states.append(token)
                            numState = 0
                            word = ''
                     #####################{{ FIM q12 }}#########################
                    
            return self.states