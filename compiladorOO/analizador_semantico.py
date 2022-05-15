def get_tipo(variavel, tabela_simbolos):
    if variavel in tabela_simbolos:
        #print(tabela_simbolos[variavel].tipo)
        return tabela_simbolos[variavel].tipo
    return False


def verificar_atribuicao(lista_tokens, tabela_simbolos, look_ahead):
    if lista_tokens[look_ahead - 2].lexema == "boolean" and lista_tokens[look_ahead + 1].nome == "<palavraBooleana>":
        return True
    elif lista_tokens[look_ahead - 2].lexema == "int" and lista_tokens[look_ahead + 1].nome == "<numerico>":
        return True
    elif lista_tokens[look_ahead - 2].lexema == "int" and lista_tokens[look_ahead + 1].nome == "<variavel>":
        tipo = get_tipo(lista_tokens[look_ahead + 1].lexema, tabela_simbolos)
        #print(tipo)
        if(tipo == "int"):
            return True
        elif(tipo == "$def"):
            return True
        else:
            print('\033[91m' + "Semantic error in line {0}".format(lista_tokens[look_ahead - 2].linha) + '\033[0m') #DETALHAR ERRO
            return False

    elif lista_tokens[look_ahead - 2].lexema == "boolean" and lista_tokens[look_ahead + 1].nome == "<variavel>":
        tipo = get_tipo(lista_tokens[look_ahead + 1].lexema, tabela_simbolos)
        #print(tipo)
        if(tipo == "boolean"):
            return True
        elif tipo == "&def":
            return True
        else:
            print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, tipo, lista_tokens[look_ahead + 1].nome) + '\033[0m') #DETALHAR ERRO
            return False
    elif lista_tokens[look_ahead - 2].nome == "<fim_comando>": # DECLARAÇÃO SEM SER DIRETA, EX: a = b;
        print(lista_tokens[look_ahead + 1].lexema)
        tipo = get_tipo(lista_tokens[look_ahead + 1].lexema, tabela_simbolos)
        tipoAtribuicao = get_tipo(lista_tokens[look_ahead - 1].lexema, tabela_simbolos)
        if tipo and tipoAtribuicao:
            if tipo == "int":
                if tipoAtribuicao == tipo:
                    return True
                else:
                    print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, tipoAtribuicao, tipo ) + '\033[0m') #DETALHAR ERRO
                    return False
            elif tipo == "boolean":
                #tipoAtribuicao = get_tipo(lista_tokens[look_ahead - 1].lexema, tabela_simbolos)
                #print(tipoAtribuicao)
                if tipoAtribuicao == tipo:
                    return True
                else:
                    print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, tipoAtribuicao, tipo ) + '\033[0m') #DETALHAR ERRO
                    return False
        else:
            print('\033[91m' + "Semantic error in line {0}, uninitialized variable {1}".format(lista_tokens[look_ahead - 2].linha) + '\033[0m') #DETALHAR ERRO
            return False
    
    else:
        #print("semantic error {}, expected {0} <--> {1}".format(lista_tokens[look_ahead - 2].lexema, lista_tokens[look_ahead + 1].lexema))
        print("entrou")
        print('\033[91m' + "Semantic error line: {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, lista_tokens[look_ahead - 2].lexema, lista_tokens[look_ahead + 1].lexema) + '\033[0m')
        return False


def verificar_expressao(lista_tokens, tabela_simbolos, look_ahead):
    tipo = get_tipo(lista_tokens[look_ahead].lexema, tabela_simbolos)
    tipoAtribuicao = get_tipo(lista_tokens[look_ahead + 2].lexema, tabela_simbolos)
    if tipo and tipoAtribuicao:
        # print("Tipo " + str(tipo))
        # print("Nome " + str(lista_tokens[look_ahead].nome))
        if tipo == "boolean" and lista_tokens[look_ahead + 2].nome == "<palavraBooleana>":
            return True
        elif tipo == "int" and lista_tokens[look_ahead + 2].nome == "<numerico>":
            return True
        elif lista_tokens[look_ahead].nome == "<variavel>" or lista_tokens[look_ahead].nome == "<numerico>":
        #elif tipo == "int":
            if tipo == tipoAtribuicao:
                return True
        else:
            print('\033[91m' + "Semantic error line: {0}, Incompatible types".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
            return False
    else:
        print('\033[91m' + "Semantic error line: {0}, uninitialized variable".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
        return False