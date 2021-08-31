# -*- coding: utf-8 -*-
#coding: utf-8
from os.path import dirname, abspath
from FileReader import FileReader
from FileWriter import FileWriter
from automato import Automato


def readFileInputs(path, pathOutput, filename, index):
    tokens = Automato(path + '\\' + filename).getTokens()
    FileWriter.write(path, pathOutput, filename, index,tokens)

def main():
    # os.chdir(os.path.abspath(
    #         os.path.dirname(__file__)))
    path = dirname(dirname(dirname(dirname(abspath(__file__)))))
    pathOutput = path + '\\output'
    pathInput = path + '\\input'
    
    try:
        inputFiles = FileReader.getInputFiles(pathInput)
        for idx, file in enumerate(inputFiles):
            readFileInputs(pathInput, pathOutput, file[0], file[1])
        
    except OSError:
        print("Erro ao escanear e analisar um dos arquivos")

main()
