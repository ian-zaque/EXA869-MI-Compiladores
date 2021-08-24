from Lexemas import Lexemas

class ArithmeticOperatorState:
    
    def __init__(self,indexChar,line):
        self.stateName = 'ART'
        self.indexChar = indexChar
        self.line = line
        self.state = []
    
    def getStateName(self):
        return self.stateName
    
    def checkChar(self):
        line = self.line
        hasEnded = False
        
        if self.indexChar >= len(line)-1:
            return self.state
        
        else:
            char = line[self.indexChar]
            
            if self.indexChar <= len(line) and char != '\\n':
                if hasEnded == True:
                    return self.state
                    
                elif Lexemas().isArithmeticOperator(char) and hasEnded==False:
                    self.state.append('ART')
                    ArithmeticOperatorState(self.indexChar+1,line).checkChar()
                    
            elif self.indexChar > len(line)-1:
                hasEnded=True
                    
            elif hasEnded:
                return self.state