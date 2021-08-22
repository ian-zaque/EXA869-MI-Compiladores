from lexemas import Lexemas

class IdentifierState:
    
    def __init__(self,char):
        self.stateName = 'IDE'
        self.char = char
    
    def getStateName(self):
        return self.stateName
    
    