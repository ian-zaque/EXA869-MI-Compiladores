class Token:
    def __init__(self,word,type):
        self.tokens = [
            'PRE', 'IDE', 'NRO', 'DEL', 'REL', 'LOG', 'ART', 'SII', 'CAR', 'CAD'
            'SII', 'CMF', 'NMF', 'CaMF', 'CoMF', 'OpMF',      
        ]
        
        self.word = word
        self.type = type
        
    def getType(self):
        return self.type
    
    def setType(self,type):
        self.type = type
        
    def getWord(self):
        return self.word
    
    def setWord(self,word):
        self.word = word
        
    def toString(self):
        return {self.word, self.type}