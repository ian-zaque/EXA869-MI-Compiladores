from lexemas import Lexemas

class State:
    
    def __init__(self,numState,word,line,char):
        self.name = Lexemas().stateTypes[numState]
        self.word = word
        self.line = line
        self.char = char
        
    def setSigla(self,sigla):
        self.sigla = sigla
        
    def getSigla(self):
        return self.sigla       
        
    def setWord(self,word):
        self.word = word
        
    def getWord(self):
        return self.word 
        
    def setLine(self,line):
        self.line = line
    
    def getLine(self):
        return self.line 
        
    def setChar(self,char):
        self.char = char
        
    def getChar(self):
        return self.char 