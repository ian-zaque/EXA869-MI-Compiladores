from os import listdir

class FileReader:
        
    def getInputFiles(dir):
        files = []
        try:
            dir = listdir(dir)

            for index, filename in enumerate(dir):
                if filename.startswith('entrada'):
                    idx = int(''.join(i for i in filename if i.isdigit()))
                    files.append([filename, idx])

            return files

        except:
            print("Ocorreu um erro ao listar os arquivos de Entrada")