class Lexemas:
    RESERVERD_WORDS = [
        'algoritmo', 'variaveis', 'constantes', 'registro','funcao', 
        'retorno', 'vazio', 'se', 'senao', 'enquanto','para', 'leia', 'escreva', 'inteiro', 'real', 'booleano', 
        'char','cadeia', 'verdadeiro', 'falso'
    ]
    
    NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    RELATIONAL_OPERATORS = ['=', '<', '>', '==', '<=', ' >=', '!=']
    
    ARITHMETIC_OPERATORS = ['+', '-', '++', '--', '*', '/']

    LOGICAL_OPERATORS = ['&&', '||', '!']

    DELIMITERS = [';', ',', '.', '(', ')', '{', '}', '[', ']', ' ', '\\n', '\\t']
    
    COMMENT_DELIMMITERS = ['#', '{#', '#}']
    
    def isReservedWord(self,word):
        return word in self.RESERVERD_WORDS
    
    def isNumber(word):
        return word.isnumeric()

    def isLetter(word):
        return word.isalpha()

    def isRelationalOperator(self,word):
        return word in self.RELATIONAL_OPERATORS
    
    def isArithmeticOperators(self,word):
        return word in self.ARITHMETIC_OPERATORS
    
    def isLogicalOperator(self,word):
        return word in self.LOGICAL_OPERATORS
    
    def isDelimiter(self,word):
        return word in self.DELIMITERS
    
    def isCommentDelimiter(self,word):
        return word in self.COMMENT_DELIMMITERS
    
    def isValidSimbol(word):
        asciiValue = ord(word)
        return asciiValue not in ['"', '\'', 34, 39] and asciiValue.isacii()