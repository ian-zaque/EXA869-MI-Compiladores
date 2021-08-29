from lexemas import Lexemas

class State:
    
    def __init__(self,numState):
        self.stateType = Lexemas().stateTypes[numState]
        self.stateNumber = numState
        print('typee',self.stateType)
        
    def getStateType(self):
        return self.stateType
    
    def getStateNumber(self):
        return self.stateNumber