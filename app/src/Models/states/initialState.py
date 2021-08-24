from Lexemas import *
from states.identifierState import IdentifierState
from states.numberState import NumberState
from states.relationalOperatorState import RelationalOperatorState
from states.arithmeticOperatorState import ArithmeticOperatorState


class InitialState:
    
    def __init__(self,line):
        self.stateName = 'INIT'
        self.line = line
        self.indexChar = 0
        self.states = {}
    
    def getStateName(self):
        return self.stateName
    
    def checkChar(self):
        line = self.line
        hasEnded = False
        nextState =[]

        # for indexChar, char in enumerate(line):
        #     print('LINHA:',line)
        #     print('CHAR:' +str(indexChar),'\'',char,'\'')
            
        #     if not char.isspace():
        #         if indexChar < len(line) and char != '\\n' and indexChar+1 < len(line):
        #             if Lexemas().isLetter(char):
        #                 nextState = IdentifierState(indexChar+1,line,line[indexChar+1]).checkChar()
        #                 self.states = nextState
        #         else:
        #             return self.states
     
        #     elif indexChar >= len(line):
        #         return self.states
            
        #     else:
        #         continue
            
            # if indexChar <= len(line) and char != '\\n':
            #     if hasEnded==True:
            #         return self.states
                
            #     elif Lexemas().isNumber(char) and hasEnded==False:
            #         self.states.append('NRO')
            #         NumberState(indexChar+1,line).checkChar()
                    
            #     elif Lexemas().isLetter(char) and hasEnded==False:
            #         self.states.append('IDE')
            #         IdentifierState(indexChar+1,line).checkChar()
                    
            #     elif Lexemas().isRelationalOperator(char) and hasEnded==False:
            #         self.states.append('REL')
            #         RelationalOperatorState(indexChar+1,line).checkChar()
                    
                # elif Lexemas().isArithmeticOperator(char) and hasEnded==False:
                #     self.state = ArithmeticOperatorState(indexChar+1,line).checkChar()
                
            # elif indexChar > len(line)-1:
            #     hasEnded=True
                
            # elif hasEnded:
            #     return self.state
            
            # if indexChar <= len(line)-1 and char != '\\n':
            #     if Lexemas.isLetter(char) and hasEnded==False:
            #         alteredLine = line[indexChar+1:]
            #         self.stateFinal = IdentifierState(indexChar,alteredLine).checkChar()
            #         print(self.stateFinal)
                    
            #     elif hasEnded== True:
            #         return self.stateFinal
            
            # elif indexChar >= len(line[self.indexChar:]) or char == '\\n':
            #     hasEnded = True
            
            # else:
            #     break
            
        # for indexChar, char in enumerate(line):
        #     print('LINHA:',line)
        #     print('CHAR:' +str(indexChar),'\'',char,'\'')
            
        #     if indexChar <= len(line)-1:
        #         print('estados',self.states)
        #         if Lexemas.isLetter(char):
        #             self.states.append(['IDE',char,indexChar])
        #             # self.states.append(IdentifierState(char).getStateName())
        #             return IdentifierState(indexChar,line).checkChar()
                
        #         elif Lexemas.isNumber(char):
        #             self.states.append(['NRO',char,indexChar])
        #             # self.states.append(NumberState(char).getStateName())
                
        #         elif Lexemas.isRelationalOperator(char):
        #             self.states.append(['REL',char,indexChar])
        #             # self.states.append(RelationalOperatorState(char).getStateName())
                
        #         elif Lexemas.isArithmeticOperators(char):
        #             self.states.append(['ART',char,indexChar])
        #             # self.states.append(ArithmeticOperatorState(char).getStateName())
                
        #         elif Lexemas.isLogicalOperator(char):
        #             self.states.append(['LOG',char,indexChar])
        #             # self.states.append()
                    
        #         elif Lexemas.isDelimiter(char):
        #             self.states.append(['DEL',char,indexChar])
        #             # self.states.append()
                
        #         elif Lexemas.isCommentDelimiter(char):
        #             self.states.append(['CoDEL',char,indexChar])
        #             # self.states.append()
                    
        #         elif Lexemas.isValidSimbol(char):
        #             self.states.append(['SII',char,indexChar])
        #             # self.states.append()
        #     else:
        #         return self.states[len(self.states)-1]
