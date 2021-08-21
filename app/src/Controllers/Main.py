from os.path import dirname, abspath
from os import listdir

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
def readFile(path,filename):
    file = open(path + '\\' + filename, 'r')
    for line in file:
        for char in line:
            print(char)
            #CHAMAR AUTOMATO AQUI
    file.close()
############################

path = dirname(dirname(dirname(dirname(abspath(__file__)))))
path = path + '\\input'

inputFiles = getInputFiles(path)

for idx, file in enumerate(inputFiles):
    readFile(path,file[0])


