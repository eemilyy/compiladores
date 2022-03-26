from analizador_lexico import AnalizadorLexico
arq = open("code.txt","r")
texto = arq.readlines()


#print(texto)
arq.close()

parser = AnalizadorLexico(texto)
parser.tokenizar(texto)
