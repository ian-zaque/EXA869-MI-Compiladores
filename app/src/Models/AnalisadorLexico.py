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
###################################

#FUNCTION TO READ THE FILE
def readFileInputs(path,filename):
    #CHAMAR AUTOMATO AQUI. PASSAR {{file}}
    # file[0] -> file.txt, file[1] -> file index
    automato = Automato([],path + '\\' + filename)
    automato.handleFile()
############################

path = dirname(dirname(dirname(dirname(abspath(__file__)))))
path = path + '\\input'

inputFiles = getInputFiles(path)

for idx, file in enumerate(inputFiles):
    readFileInputs(path,file[0])


