from states.numberState import *
from states.relationalOperatorState import *
from states.arithmeticOperatorState import *
from Lexemas import *

class IdentifierState:
    
    def __init__(self,indexChar,line,char):
        self.stateName = 'IDE'
        self.indexChar = indexChar
        self.line = line
        self.char = char
        self.state = {}
    
    def getStateName(self):
        return self.stateName
    
    def checkChar(self):
        line = self.line
        hasEnded = False
        
        if not self.char.isspace():
            if self.indexChar <= len(self.line):
                if self.char != '\\n' and self.indexChar+1 < len(line):
                    if Lexemas().isLetter(self.char) or self.char == '_':
                        nextState = IdentifierState(self.indexChar+1,line,line[self.indexChar+1]).checkChar()
                        self.state= nextState
                else:
                    return self.state
                
                if self.indexChar >= len(self.line) or self.line[self.indexChar] == '\\n' or self.line[self.indexChar].isspace():
                    return self.state
            else:
                return self.state
        else:
            return self.state
        
        # if self.indexChar >= len(line)-1:
        #     return self.state
        
        # else:
        #     char = line[self.indexChar]
        #     if self.indexChar <= len(line):
        #         if hasEnded == True or line[self.indexChar+1]== ' ':
        #             return self.state
                
        #         elif Lexemas().isNumber(char) and hasEnded==False:
        #             self.state.append('IDE')
        #             NumberState(self.indexChar+1,line).checkChar()
                    
        #         elif (Lexemas().isLetter(char) or char == '_') and hasEnded==False:
        #             self.state.append('IDE')
        #             IdentifierState(self.indexChar+1,line).checkChar()        
                    
        #     elif self.indexChar > len(line)-1:
        #         hasEnded=True
        #         return self.state
                    
        #     elif hasEnded:
        #         return self.state
        
        # if self.indexChar <= len(line)-1 and line[self.indexChar] != '\\n':
        #     if (Lexemas.isLetter(line[self.indexChar]) or line[self.indexChar]=='_') and hasEnded==False:
        #         alteredLine = line[self.indexChar+1:]
        #         self.nextState = IdentifierState(self.indexChar+1,alteredLine).checkChar()
        #         # print(self.nextState)
            
        #     elif Lexemas.isNumber(line[self.indexChar]) and hasEnded==False:
        #         alteredLine = line[self.indexChar+1:]
        #         self.nextState = NumberState(self.indexChar+1,alteredLine).checkChar()
        #         # print(self.nextState)
            
        #     elif hasEnded== True:
        #         self.stateFinal = self.nextState
        #         return self.stateFinal
            
        # elif hasEnded:
        #     self.stateFinal = self.nextState
        #     return self.stateFinal
        
        # else:
        #     hasEnded = True
            
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
    