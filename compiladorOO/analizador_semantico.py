def get_tipo():
    print("sj")
def verificar_atribuicao(lista_tokens, tabela_simbolos, look_ahead):
    if lista_tokens[look_ahead - 2].lexema == "boolean" and lista_tokens[look_ahead + 1].nome == "<palavraBooleana>":
        return True
    elif lista_tokens[look_ahead - 2].lexema == "int" and lista_tokens[look_ahead + 1].nome == "<numerico>":
        return True
    else:
        #print("semantic error {}, expected {0} <--> {1}".format(lista_tokens[look_ahead - 2].lexema, lista_tokens[look_ahead + 1].lexema))
        print("entrou")
        print('\033[91m' + "Semantic error line: {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, lista_tokens[look_ahead - 2].lexema, lista_tokens[look_ahead + 1].lexema) + '\033[0m')
        return False