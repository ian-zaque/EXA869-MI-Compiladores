from states.numberState import NumberState
from lexemas import *

class IdentifierState:
    
    def __init__(self,indexChar,line):
        self.stateName = 'IDE'
        self.indexChar = indexChar
        self.line = line
    
    def getStateName(self):
        return self.stateName
    
    def checkChar(self):
        line = self.line
        stateFinal = []
        hasEnded = False
        
        for idxChar, char in enumerate(line):
            print('char novo',char)
            print('liiinha',line)
            
            if idxChar <= len(line)-1 and char != '\\n':
                if Lexemas.isLetter(char) and hasEnded==False:
                    alteredLine = line[idxChar+1:]
                    self.nextState = IdentifierState(idxChar,alteredLine).checkChar()
                    print(self.nextState)
                
                elif Lexemas.isNumber(char) and hasEnded==False:
                    alteredLine = line[idxChar+1:]
                    self.nextState = NumberState(idxChar,alteredLine).checkChar()
                    print(self.nextState)
                
                elif hasEnded== True:
                    self.stateFinal = self.nextState
                    return self.stateFinal
                    
            elif idxChar > len(line[self.indexChar:]) or char == '\\n':
                hasEnded = True
            
            # if self.indexChar <= len(line):
            #     if Lexemas.isLetter(char):
            #         print('leeeeeee',char)
            #         stateFinal = IdentifierState(self.indexChar+1,line).checkChar()

            #     elif Lexemas.isNumber(char):
            #         stateFinal = NumberState(char,idxChar,line).checkChar()
                
            #     elif hasEnded == True:
            #         return stateFinal
                
            #     elif idxChar <= len(line)-1:
            #         hasEnded = True
                    
            #     else:
            #         return 'IMF'
            # else:
            #     return stateFinal
    