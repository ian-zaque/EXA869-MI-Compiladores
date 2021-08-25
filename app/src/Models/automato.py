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
                # print('Linha:',idxLine, 'Valor: ',line)
                numState = 0
                word = ''
                
                for idxChar,char in enumerate(line):
                    # print('Posição:',idxChar, 'Char: ',char)
                
                    #####################{{ q0 }}#########################
                    if numState == 0:
                        if self.lexemas.isLetter(char):
                            numState = 1
                            word = word + char
                            # state = State(numState,word,line,char)
                        # 
                        # AQUI OUTROS IFS
                        # if char in ['&','|']:
                        #     numState = 3
                        
                        elif char == '\n' or self.lexemas.isSpace(char):
                            numState = 0
                        
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
                            self.states.append(token.toString())
                            word =''
                            numState = 0
                            #TRATAR ESPAÇO AQUI
                            
                        else:               # TRATAR ERROS OU OUTRA OCASIOES AQUI
                            numState = 0
                    #####################{{ FIM q1 }}#########################
                                    
            return self.states