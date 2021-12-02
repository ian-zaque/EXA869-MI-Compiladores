# -*- coding: utf-8 -*-
#coding: utf-8

from os.path import dirname, abspath
from AnalisadorSintatico import *
from FileReader import FileReader
from FileWriter import FileWriter
from automato import Automato

class AnalisadorLexico:
    
    def __init__(self) -> None:
        pass
    
    def readFileInputs(self,path, pathOutput, filename, index):
        #tokens = Automato(path + '\\' + filename).getTokens()
        tokens = Automato(path + '/' + filename).getTokens()

        sintatico = AnalisadorSintatico(tokens).parse(index)
        sintatico = list(dict.fromkeys(sintatico))
        
        FileWriter.write(path, pathOutput, filename, index, sintatico)
        #FileWriter.write(path, pathOutput, filename, index, tokens)


    def main(self):
        path = dirname(dirname(dirname(dirname(abspath(__file__)))))
        pathOutput = path + '\\output'
        pathInput = path + '\\input'
        pathOutput = path + '/output'
        pathInput = path + '/input'

        try:
            inputFiles = FileReader.getInputFiles(pathInput)
            for idx, file in enumerate(inputFiles):
                self.readFileInputs(pathInput, pathOutput, file[0], file[1])

        except OSError:
            print("Erro ao escanear e analisar um dos arquivos")

