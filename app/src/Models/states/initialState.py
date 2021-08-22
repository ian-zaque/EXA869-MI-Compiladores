from lexemas import Lexemas
from states.identifierState import IdentifierState
from states.numberState import NumberState
from states.relationalOperatorState import RelationalOperatorState
from states.arithmeticOperatorState import ArithmeticOperatorState


class InitialState:
    
    def __init__(self,char):
        self.stateName = 'INIT'
        self.char = char
    
    def getStateName(self):
        return self.stateName
    
    def checkChar(self):
        word = self.char
        print('aoeifnaidfníaf',self.char)
        if Lexemas.isLetter(word):
            return IdentifierState(word)
        
        elif Lexemas.isNumber(word):
            return NumberState(word)
        
        elif Lexemas.isRelationalOperator(word):
            return RelationalOperatorState(word)
        
        elif Lexemas.isArithmeticOperators(word):
            return ArithmeticOperatorState(word)
