from states.initialState import InitialState
from states.identifierState import IdentifierState
from states.numberState import NumberState
from states.reserverdWordState import ReserverdWordState
from states.relationalOperatorState import RelationalOperatorState
from states.arithmeticOperatorState import ArithmeticOperatorState

class Automato:

    def __init__(self, file):
        self.currentState = {}
        self.states = {}
        self.file = open(file,'r')
        # self.states['InitialState'] = InitialState()
        # self.states['IdentifierState'] = IdentifierState()
        # self.states['NumberState'] = NumberState()
        # self.states['ReserverdWordState'] = ReserverdWordState()
        # self.states['RelationalOperatorState'] = RelationalOperatorState()
        # self.states['ArithmeticOperatorState'] = ArithmeticOperatorState()
    
    def getInitialState(self):
        return self.state.initialState
    
    def setInitialState(self,initialState):
        self.state.initialState = initialState
    
    def getStates(self):
        return self.states
    
    def setStates(self,stateName, state):
        self.states[stateName] = state
    
    def getFile(self):
        return self.file
        
    def handleFile(self):
        file = self.file
        line = file.readline()
        print(line)
        
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
                    
                    
        line = file.readline()
            # if END OF FILE BREAK AND CLOSE FILE
        
            
        
        self.file.close()
        