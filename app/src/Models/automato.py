from states.identifierState import IdentifierState
from states.numberState import NumberState
from states.reserverdWordState import ReserverdWordState
from states.relationalOperatorState import RelationalOperatorState
from states.arithmeticOperatorState import ArithmeticOperatorState

class Automato:

    def __init__(self, initialState, file):
        self.initialState = initialState
        self.currentState = {}
        self.states = {}
        self.file = open(file,'r')
        self.states['IdentifierState'] = IdentifierState()
        self.states['NumberState'] = NumberState()
        self.states['ReserverdWordState'] = ReserverdWordState()
        self.states['RelationalOperatorState'] = RelationalOperatorState()
        self.states['ArithmeticOperatorState'] = ArithmeticOperatorState()
    
    def getInitialState(self):
        return self.initialState
    
    def setInitialState(self,initialState):
        self.initialState = initialState
    
    def getStates(self):
        return self.states
    
    def setStates(self,stateName, state):
        self.states[stateName] = state
    
    def getFile(self):
        return self.file
    
    def resetAutomato(self, initialState):
        self.initialState = initialState
        self.states['IdentifierState'] = IdentifierState()
        self.states['NumberState'] = NumberState()
        self.states['ReserverdWordState'] = ReserverdWordState()
        self.states['RelationalOperatorState'] = RelationalOperatorState()
        self.states['ArithmeticOperatorState'] = ArithmeticOperatorState()
        
    def handleFile(self):
        file = self.file
        line = file.readline()
        
        for idx,char in enumerate(line):
            print('char',char,idx)
            # if idx == len(line)-1:    EOF
        
        self.file.close()
        