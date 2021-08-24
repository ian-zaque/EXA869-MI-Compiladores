from Token import Token
from lexemas import Lexemas

class Automato:

    def __init__(self, file):
        self.file = open(file,'r')
        self.index = -1
        self.lexemas = Lexemas()
        self.states = []
    
    def getFile(self):
        return self.file
    
    def nextChar(self):
        self.index = self.index+1
        return self.fileContent[self.index]
    
    def back(self):
        self.index = self.index-1
    
    def isEOF(self):
        return self.index == len(self.file.readlines())
    
    def getNextToken(self):
            file = self.file.readlines()
            for idxLine, line in enumerate(file):
                print('Linha:',idxLine, 'Valor: ',line)
                print(self.file.readlines())
                numState = 0
                word = ''
                
                # if idxLine >= len(line):
                #     break
                
                for idxChar,char in enumerate(line):
                    print('Posição:',idxChar, 'Char: ',char)
                
                    if numState == 0:
                        if self.lexemas.isLetter(char):
                            numState = 1
                            word = word + char
                        # 
                        # AQUI OUTROS IFS
                        
                        
                        elif char == '\n' or self.lexemas.isSpace(char):
                            numState = 0
                        
                        else:
                            # ALGUM ERRO
                            numState = 99
                    
                    elif numState ==1:
                        if self.lexemas.isLetter(char) or self.lexemas.isDigit(char) or char=='_':
                            numState = 1
                            word = word + char
                        
                        elif self.lexemas.isSpace(char) or char == '\n':
                            token = Token(word,'IDE',idxLine)
                            self.states.append(token.toString())
                            word =''
                            numState = 0
                            #TRATAR ESPAÇO AQUI
                            
                            # TRATAR ERROS OU OUTRA OCASIOES AQUI
                        else:
                            numState = 0           
            return self.states
        # if self.isEOF():
        #     return
        
        # state = 0
        # word = ''
        # index = -1
        
        # file = self.fileContent
        # for indexLine, line in enumerate(file):
        #     index = indexLine
        #     if self.isEOF():
        #         return self.states
            
        #     else:
        #         word = ''
        #         state = 0
        #         for indexChar, char in enumerate(line):
        #             if indexChar == len(line):
        #                 return self.states
                    
        #             else:
        #                 if state == 0:
        #                     if Lexemas().isLetter(char):
        #                         word = word+char
        #                         state = 1
                                
        #                     elif Lexemas().isSpace(char):
        #                         state = 0
        #                         word = ''
        #                     #
        #                     #OUTROS IFS PARA OUTRAS ENTRADAS
        #                     #
                            
        #                     else:
        #                         print('ERRO')
        #                         return self.states
                            
        #                 elif state == 1:
        #                     if Lexemas().isLetter(char):
        #                         word = word+char
        #                         state = 1
                                
        #                     else:
        #                         state = Token(word, 'IDE')
        #                         self.states.append(state.toString())
                                
        #                 elif state.getType() == 'IDE':
        #                     self.states.append(state.toString())
        # return self.states