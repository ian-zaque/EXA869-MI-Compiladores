class Token:
    def __init__(self,word,type,line):        
        self.word = word
        self.type = type
        self.line = line
        
    def getType(self):
        return self.type
    
    def setType(self,type):
        self.type = type
        
    def getWord(self):
        return self.word
    
    def setWord(self,word):
        self.word = word
        
    def toString(self):
        line = self.line
        typeToken = self.type
        word = self.word
        return [line, typeToken, word]