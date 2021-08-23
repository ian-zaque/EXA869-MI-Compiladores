from lexemas import *
from states.identifierState import IdentifierState
from states.numberState import NumberState
from states.relationalOperatorState import RelationalOperatorState
from states.arithmeticOperatorState import ArithmeticOperatorState


class InitialState:
    
    def __init__(self,line):
        self.stateName = 'INIT'
        self.line = line
        self.stateFinal = []
    
    def getStateName(self):
        return self.stateName
    
    def checkChar(self):
        line = self.line
        hasEnded = False

        for indexChar, char in enumerate(line):
            print('LINHA:',line)
            print('CHAR:' +str(indexChar),'\'',char,'\'')
            
            if indexChar <= len(line)-1 and char != '\\n':
                if Lexemas.isLetter(char) and hasEnded==False:
                    alteredLine = line[indexChar+1:]
                    self.stateFinal = IdentifierState(indexChar,alteredLine).checkChar()
                    print(self.stateFinal)
                    
                elif hasEnded== True:
                    return self.stateFinal
            
            elif indexChar >= len(line[self.indexChar:]) or char == '\\n':
                hasEnded = True
            
            else:
                return 'CARACTER INVALIDO'
            
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
