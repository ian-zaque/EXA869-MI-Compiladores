# -*- coding: utf-8 -*-
#coding: utf-8
from os.path import dirname, abspath
from os import listdir
from automato import Automato

# FUNCTION TO GET ALL THE TEXTS INPUTS


def getInputFiles(dir):
    files = []
    dir = listdir(dir)

    for index, filename in enumerate(dir):
        if filename.startswith('entrada'):
            idx = int(''.join(i for i in filename if i.isdigit()))
            files.append([filename, idx])

    return files

# FUNCTION TO READ THE FILE


def readFileInputs(path, pathOutput, filename, index):
    automato = Automato(path + '\\' + filename)
    #automato = Automato(path + '/' + filename)
    tokens = automato.getTokens()
    lineTxt = []

    file = open(pathOutput+'\\saida'+str(index)+'.txt', 'w')
    #file = open(pathOutput+'/saida'+str(index)+'.txt', 'w')

    for idx, token in enumerate(tokens['states']):
        lineTxt = str(token.getLine()+1) + ' ' + \
            token.getType() + ' ' + token.getWord()
        file.write(lineTxt)
        file.write('\n')

    for idx, token in enumerate(tokens['errors']):
        file.write('\n')
        lineTxt = str(token.getLine()+1) + ' ' + \
            token.getType() + ' ' + token.getWord()
        file.write(lineTxt)
    file.close()


def main():
    path = dirname(dirname(dirname(dirname(abspath(__file__)))))
    pathOutput = path + '\\output'
    pathInput = path + '\\input'
    #pathOutput = path + '/output'
    #pathInput = path + '/input'
    inputFiles = getInputFiles(pathInput)

    for idx, file in enumerate(inputFiles):
        readFileInputs(pathInput, pathOutput, file[0], file[1])


main()
