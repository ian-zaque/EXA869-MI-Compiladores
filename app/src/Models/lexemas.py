class Lexemas:
    
    def __init__(self):
        self.tokens = [
            'PRE', 'IDE', 'NRO', 'DEL', 'REL', 'LOG', 'ART', 'SII', 'CAR', 'CAD'
            'SII', 'CMF', 'NMF', 'CaMF', 'CoMF', 'OpMF',      
        ]
             
        self.RESERVERD_WORDS = [
            'algoritmo', 'variaveis', 'constantes', 'registro','funcao', 
            'retorno', 'vazio', 'se', 'senao', 'enquanto','para', 'leia', 'escreva', 'inteiro', 'real', 'booleano', 
            'char','cadeia', 'verdadeiro', 'falso'
        ]
        
        self.NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        self.RELATIONAL_OPERATORS = ['=', '<', '>', '==', '<=', ' >=', '!=']
        
        self.ARITHMETIC_OPERATORS = ['+', '-', '++', '--', '*', '/']

        self.LOGICAL_OPERATORS = ['&&', '||', '!']

        self.DELIMITERS = [';', ',', '.', '(', ')', '{', '}', '[', ']', ' ', '\\n', '\\t']
        
        self.COMMENT_DELIMMITERS = ['#', '{#', '#}']
    
    def isReservedWord(self,char):
        return char in self.RESERVERD_WORDS
    
    def isDigit(self,char):
        return char.isnumeric()

    def isLetter(self,char):
        return char.isalpha()

    def isSpace(self,char):
        return char.isspace()

    def isRelationalOperator(self,char):
        return char in self.RELATIONAL_OPERATORS
    
    def isArithmeticOperator(self,char):
        return char in self.ARITHMETIC_OPERATORS
    
    def isLogicalOperator(self,char):
        return char in self.LOGICAL_OPERATORS
    
    def isDelimiter(self,char):
        return char in self.DELIMITERS
    
    def isCommentDelimiter(self,char):
        return char in self.COMMENT_DELIMMITERS
    
    def isValidSimbol(char):
        asciiValue = ord(char)
        return asciiValue not in [34, 39] and asciiValue.isacii()
    
    st = ' '
    print(st.isspace())