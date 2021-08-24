from Token import Token
from lexemas import Lexemas
from State import State

class Automato:

    def __init__(self, file):
        self.file = open(file,'r')
        self.index = -1
        self.lexemas = Lexemas()
        self.states = []
    
    def getNextToken(self):
            file = self.file.readlines()
            for idxLine, line in enumerate(file):
                print('Linha:',idxLine, 'Valor: ',line)
                print(self.file.readlines())
                numState = 0
                word = ''
                # state = State(numState,word,line,line[idxLine])
                
                # if idxLine >= len(line):
                #     break
                
                for idxChar,char in enumerate(line):
                    print('Posição:',idxChar, 'Char: ',char)
                
                    if numState == 0:                   #WAITING
                        if self.lexemas.isLetter(char):
                            numState = 1
                            word = word + char
                            state = State(numState,word,line,char)
                        # 
                        # AQUI OUTROS IFS
                        
                        
                        elif char == '\n' or self.lexemas.isSpace(char):
                            numState = 0
                        
                        else:
                            # ALGUM ERRO
                            numState = 99
                    
                    elif numState ==1:              #RECEIVED char
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
                            
                            # TRATAR ERROS OU OUTRA OCASIOES AQUI
                        else:
                            numState = 0
                                    
            return self.states