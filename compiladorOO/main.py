from analizador_lexico import AnalizadorLexico
arq = open("code.txt","r")
texto = arq.readlines()


#print(texto)
arq.close()

lexer = AnalizadorLexico(texto)
lexer.tokenizar(texto)
lexer.imprimir_lista_tokens()
