from lexemas import Lexemas

class RelationalOperatorState:
    
    def __init__(self,indexChar,line):
        self.stateName = 'REL'
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
                    
                elif Lexemas().isRelationalOperator(char) and hasEnded==False:
                    self.state.append('REL')
                    RelationalOperatorState(self.indexChar+1,line).checkChar()
                    
            elif self.indexChar > len(line)-1:
                hasEnded=True
                    
            elif hasEnded:
                return self.state