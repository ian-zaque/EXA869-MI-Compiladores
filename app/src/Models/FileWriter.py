class FileWriter:
    
    def write(path, pathOutput, filename, index,tokens):
        try:
            file = open(pathOutput+'\\saida'+str(index)+'.txt', 'w')
            # file = open(pathOutput+'/saida'+str(index)+'.txt', 'w')
            lineTxt = []

            for idx, token in enumerate(tokens['states']):
                lineTxt = str(token.getLine()+1) + ' ' + \
                    token.getType() + ' ' + token.getWord()
                file.write(lineTxt)
                file.write('\n')

            if len(tokens['errors']) >= 1:
                print(len(tokens['errors']), "erro(s) detectados no arquivo: entrada" + str(index) + '.txt')
                
                for idx, token in enumerate(tokens['errors']):
                    file.write('\n')
                    lineTxt = str(token.getLine()+1) + ' ' + \
                        token.getType() + ' ' + token.getWord()
                    file.write(lineTxt)
                    
            else:
                print("Sucesso! Arquivo:",'\'saida'+str(index)+'.txt\'', "sem erros léxicos!")
                file.write('\n')
                file.write("Sucesso!")
            file.close()
            
        except:
            print("Ocorreu um erro ao escrever a saída do arquivo:",'entrada'+str(index)+'.txt')