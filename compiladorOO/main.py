from analizador_lexico import AnalizadorLexico
from analizador_sintatico import AnalizadorSintatico
arq = open("code.txt","r")
texto = arq.readlines()


#print(texto)
arq.close()

lexer = AnalizadorLexico(texto)
lexer.tokenizar(texto)
lexer.imprimir_lista_tokens()
lexer.imprimir_tabela_simbolos()
parser = AnalizadorSintatico(lexer.tokens)
parser.start()
