class Lexemas:
    reserverdWords = [
        'algoritmo', 'variaveis', 'constantes', 'registro','funcao', 
        'retorno', 'vazio', 'se', 'senao', 'enquanto','para', 'leia', 'escreva', 'inteiro', 'real', 'booleano', 
        'char','cadeia', 'verdadeiro', 'falso'
    ]
    
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    relationalOperators = ['=', '<', '>', '==', '<=', ' >=', '!=']
    
    arithmeticOperators = ['+', '-', '++', '--', '*', '/']

    logicalOperators = ['&&', '||', '!']

    delimiters = [';', ',', '.', '(', ')', '{', '}', '[', ']', ' ', '\\n', '\\t']
    
    commentDelimiters = ['#', '{#', '#}']
    
    def isReservedWord(self,word):
        return word in self.reserverdWords
    
    def isNumber(self,word):
        return word.isnumeric()

    def isLetter(self, word):
        return word.isalpha()

    def isRelationalOperator(self,word):
        return word in self.relationalOperators
    
    def isArithmeticOperators(self,word):
        return word in self.arithmeticOperators
    
    def isLogicalOperator(self,word):
        return word in self.logicalOperators
    
    def isDelimiter(self,word):
        return word in self.delimiters
    
    def isCommentDelimiters(self,word):
        return word in self.commentDelimiters
    
    def isValidSimbol(self,word):
        asciiValue = ord(word)
        return asciiValue not in ['"', '\'', 34, 39] and asciiValue.isacii()