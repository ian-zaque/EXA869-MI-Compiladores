class Lexemas:
    
    def __init__(self):
        self.tokens = [
            #tokens
            'PRE', 'IDE', 'NRO', 'DEL', 'REL', 'LOG', 'ART', 'SII', 'CAR', 'CAD',
            
            #errors
            'SII', 'CMF', 'NMF', 'CaMF', 'CoMF', 'OpMF',      
        ]
        
        self.stateTypes = {
            0 : {'q0','INITIAL'},                               #INITIAL STATE, FIRST DIGIT     {{ a-z | A-Z }}
            
            #IDENTIFICADORES OU PALAVRAS_RESERVADAS
            1 : {'q1','WAITING_OR_FINAL_LETTER'},               #RETURNS TOKEN 'IDE' OR 'PRE'   {{ a-z | A-Z | 0-9 | _ }}
            
            #NÚMEROS
            2 : {'q2', 'WAITING_OR_FINAL_DIGIT'},               #RETURNS TOKEN 'NRO'        {{0-9}}
            3 : {'q3', 'WAITING_DIGITS_AFTER_POINT'},           #MANDATORY TO RECEIVE A DIGIT   {{ . }}
            4 : {'q4', 'WAITING_DIGITS_AFTER_POINT-DIGIT'},     #RETURNS TOKEN 'NRO'        {{ 0-9 }}
            5 : {'q5', 'ERROR_NMF'},                            #RETURNS ERROR 'NMF'        _other_
            
            #OPERADORES RELACIONAIS
            6 : {'q6', 'WAITING_OR_FINAL_REL'},                 #RETURNS TOKEN 'REL'       {{ = | < | > }}
            7 : {'q7', 'WAITING_EQUALS_AFTER_EXCLAMATION'},     #MANDATORY TO RECEIVE '='.  {{ ! }}
            8 : {'q8', 'FINAL_REL_AFTER_REL'},                  #RETURNS TOKEN 'REL'        {{ = }}
            9 : {'q9', 'ERROR_OpMF'},                           #RETURNS ERROR 'OpMF'       _other_
            
            #OPERADORES ARITMÉTICOS
            10 : {'q10', 'FINAL_ART'},                          #RETURNS TOKEN 'ART'     {{ * | / }}
            11 : {'q11', 'WAITING_OR_FINAL_ART'},               #RETURNS TOKEN 'ART'     {{ + | - }}
            12 : {'q12', 'ERROR_OpMF'},                         #RETURNS ERROR 'OpMF'    _other_or_not_space_before_or_after_
            
            #OPERADORES LÓGICOS
            13 : {'q13', 'WAITING_FINAL_LOG'},                  #MANDATORY TO RECEIVE '&' OR '|'.  {{ & | '|' }}
            14 : {'q14', 'FINAL_LOG'},                          #RETURNS TOKEN 'LOG' {{ & | '|' }}
            15 : {'q15', 'FINAL_EXCLAMATION'},                  #RETURNS TOKEN 'LOG'  {{ ! }}
            16 : {'q16', 'ERROR_OpMF'},                         #RETURNS ERROR 'OpMF'  {{ &! | !& | '|' | |& | &| | _othen_ }}
            
            17 : {'q17', 'LINE_COMMENT'},                       #IGNORES THE WHOLE LINE     {{ % }}
            18 : {'q18', 'WAITING_#_TO_START_BLOCK_COMMENT'},   #MANDATORY TO RECEIVE '#' {{ '#' }}  
            19 : {'q19', 'WAITING_#_TO_MIDDLE_BLOCK_COMMENT'},  #MANDATORY TO RECEIVE '#' {{ '#' }}
            20 : {'q20', 'WAITING_}_TO_END_BLOCK_COMMENT'},     #MANDATORY TO RECEIVE '}' {{ '}' }}
            21 : {'q21', 'ERROR_CoMF'},                         #RETURNS ERROR 'OpMF'      _OTHER_
            
            22 : {'q22', 'SYMBOL'},                             #RETURNS ERROR 'SII'      SIMBOLS
        }

        self.RESERVERD_WORDS = [
            'algoritmo', 'variaveis', 'constantes', 'registro','funcao', 'retorno', 
            'vazio', 'se', 'senao', 'enquanto','para', 'leia', 'escreva', 'inteiro', 
            'real', 'booleano', 'char','cadeia', 'verdadeiro', 'falso',
        ]
        
        self.NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        self.RELATIONAL_OPERATORS = ['=', '<', '>', '==', '<=', '>=', '!=']
        
        self.ARITHMETIC_OPERATORS = ['+', '-', '++', '--', '*', '/']

        self.LOGICAL_OPERATORS = ['&&', '||', '!']

        self.START_DELIMITERS = ['(', '{', '[']

        self.END_DELIMITERS = [';', ',', '.', ')', '}', ']', '\\t']
        
        self.COMMENT_DELIMMITERS = ['%', '{#', '#}']
    
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
    
    def isStartDelimiter(self,char):
        return char in self.START_DELIMITERS
    
    def isEndDelimiter(self,char):
        return char in self.END_DELIMITERS
    
    def isCommentDelimiter(self,char):
        return char in self.COMMENT_DELIMMITERS
    
    def isCaracters(self, char):
        return bytes(char, 'ascii').hex() == '22'

    def isCaracter(self, char):
        return bytes(char, 'ascii').hex() == '27'

    def isValidSimbol(self, char):
        simbol = int(bytes(char, 'ascii').hex(), 16)
        return (simbol > 31 and simbol < 127 and simbol != 34 and simbol != 39)