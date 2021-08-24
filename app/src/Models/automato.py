from states.initialState import *
from states.identifierState import IdentifierState
from states.numberState import NumberState
from states.reserverdWordState import ReserverdWordState
from states.relationalOperatorState import RelationalOperatorState
from states.arithmeticOperatorState import ArithmeticOperatorState
from Token import Token

class Automato:

    def __init__(self, file):
        self.file = open(file,'r')
        self.fileContent = self.file.readlines()
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
        if self.isEOF():
            return
        
        state = 0
        word = ''
        index = -1
        
        file = self.fileContent
        print('-----------',file)
        for indexLine, line in enumerate(file):
            if indexLine == len(file):
                return self.states
            
            else:
                for indexChar, char in enumerate(line):
                    print('LINE',word)
                    if indexLine == len(line):
                        return self.states
                    
                    else:
                        if state == 0:
                            if Lexemas().isLetter(char):
                                word = word+char
                                print('CHAR 1',char)
                                print('STATE 1',self.states)
                                state = 1
                                
                            elif Lexemas().isSpace(char):
                                state = 0
                                print('CHAR 0',char)
                                print('STATE 0',self.states)
                                break
                            #
                            #OUTROS IFS PARA OUTRAS ENTRADAS
                            #
                            
                            else:
                                print('ERRO')
                                self.states.append(Token(word,'IDE').toString())
                                print('STATES RETURN 1',self.states)
                                return self.states
                            
                        elif state == 1:
                            if Lexemas().isLetter(char):
                                word = word+char
                                state = 1
                                print('CHAR 2',char)
                                print('STATE WAITING LETTER',state)
                                
                            else:
                                state = Token(word, 'IDE')
                                print('STATE IDE',state.getType())
                                
                        elif state.getType() == 'IDE':
                            self.states.append(Token(word,'IDE').toString())
                            print('STATES RETURN 2',self.states)
                            
                            
        print('eeeestados',self.states)       
        return self.states
        # state = 0      #initial
        # word = ''
        # index = -1
        # while True:
        #     if self.isEOF():
        #         break
            
        #     currentLine = self.nextChar()
        #     print('aaaaaaaaa',currentLine)
        #     for idx, letra in enumerate(currentLine):              
        #         if state==0:        #initial
        #             if self.lexemas.isLetter(letra):
        #                 state = 1
        #                 break
        #             #
        #             # OUTROS IFS PARA OUTRAS ENTRADAS
        #             #
        #             elif self.lexemas.isSpace(letra):
        #                 state = 0
        #                 break
                    
        #             else:
        #                 print('current',letra)
        #                 print('state',state)
        #                 return 'ERRRROOO'

        #         elif state == 1:      #IDE OU PRE
        #             if self.lexemas.isLetter(letra) or self.lexemas.isDigit(letra) or letra == '_':
        #                 state =1
        #                 break
        #             else:
        #                 state = 'IDE'
        #                 break
                
        #         elif state == 'IDE':
        #             self.back()
        #             self.states[idx] = Token(letra,'IDE').getType()
        #             return self.states
        # print('oisdafn',state)
            
    
    def handleFile(self):
        file = self.file
        # for indexLine, line in enumerate(file):
        #     # for indexChar, char in enumerate(line):
        #     #     print('CHAR:' +str(indexChar),char)
        #     self.states = InitialState(line).checkChar()
        #     # print('LINHA:'+str(indexLine),line)
        #     print('ESTADOS',self.states)
        # file.close()
        
        
        # while True:
        #     for idx,char in enumerate(line):
        #         i = idx
        #         if idx >= len(line)-1:      #EOLINE
        #             break
                
        #         print('char',char,idx)
        #         self.states[i] = InitialState(char)
        #         state = self.states[i].checkChar()
        #         self.currentState = state
        #         self.states[i] = state
                
        #         while True:
        #             i += 1

        #             if i >= len(line)-1:
        #                 break
            # if END OF FILE BREAK AND CLOSE FILE
        