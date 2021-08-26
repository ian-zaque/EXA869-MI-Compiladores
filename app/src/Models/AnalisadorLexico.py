from os.path import dirname, abspath
from os import listdir
from automato import Automato

#FUNCTION TO GET ALL THE TEXTS INPUTS
def getInputFiles(dir):
    files = []
    dir = listdir(dir)

    for index,filename in enumerate(dir):
        if filename.startswith('entrada'):
            files.append([filename,index])

    return files

#FUNCTION TO READ THE FILE
def readFileInputs(path,pathOutput,filename,index):
    automato = Automato(path + '\\' + filename)
    tokens = automato.getNextToken()
    lineTxt = []
    
    file = open(pathOutput+'\\saida'+str(index)+'.txt','w')
    
    for idx, token in enumerate(tokens):
        lineTxt= str(token.getLine()+1) + ' ' + token.getType() + ' ' + token.getWord()
        file.write(lineTxt)
        file.write('\n')
    file.close()
        
    


def main():
    path = dirname(dirname(dirname(dirname(abspath(__file__)))))
    pathOutput = path + '\\output'
    path = path + '\\input'
    print('0000',path)
    print('bbbbb',pathOutput)
    inputFiles = getInputFiles(path)

    for idx, file in enumerate(inputFiles):
        readFileInputs(path, pathOutput, file[0], file[1]-1)



main()
