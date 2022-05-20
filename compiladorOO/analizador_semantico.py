
def get_tipo(variavel, tabela_simbolos):
    if variavel.lexema in tabela_simbolos:
        if(tabela_simbolos[variavel.lexema].linha < variavel.linha):
            return tabela_simbolos[variavel.lexema].tipo
        else:
            return False
    return False


def verificar_atribuicao(lista_tokens, tabela_simbolos, look_ahead):
    if lista_tokens[look_ahead - 2].lexema == "boolean" and lista_tokens[look_ahead + 1].nome == "<palavraBooleana>":
        return True
    elif lista_tokens[look_ahead - 2].lexema == "int" and lista_tokens[look_ahead + 1].nome == "<variavel>":
        tipo = get_tipo(lista_tokens[look_ahead + 1], tabela_simbolos)
        if(tipo == "int"):
            return True
        elif(tipo == "$def"):
            return True
        else:
            print('\033[91m' + "Semantic error in line {0}".format(lista_tokens[look_ahead - 2].linha) + '\033[0m') #DETALHAR ERRO
            return False
    elif lista_tokens[look_ahead - 2].lexema == "int" and lista_tokens[look_ahead + 1].nome == "<numerico>":
        if lista_tokens[look_ahead + 2].nome == "<aritmeticas>":
            if(get_tipo(lista_tokens[look_ahead + 3], tabela_simbolos) == "int"):
                return True
            elif(lista_tokens[look_ahead + 3].nome == "<numerico>"):
                return True
            else:
                print('\033[91m' + "Semantic error in line {0}".format(lista_tokens[look_ahead - 2].linha) + '\033[0m') #DETALHAR ERRO
                return False
        return True

    elif lista_tokens[look_ahead - 2].lexema == "boolean" and lista_tokens[look_ahead + 1].nome == "<variavel>":
        tipo = get_tipo(lista_tokens[look_ahead + 1], tabela_simbolos)
        if(tipo == "boolean"):
            return True
        elif tipo == "&def":
            return True
        else:
            print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, tipo, lista_tokens[look_ahead + 1].nome) + '\033[0m') #DETALHAR ERRO
            return False
    elif lista_tokens[look_ahead - 2].nome == "<fim_comando>" or lista_tokens[look_ahead - 2].nome == "<abre_chaves>" or lista_tokens[look_ahead - 2].nome == "<fecha_chaves>": # DECLARAÇÃO SEM SER DIRETA, EX: a = b;
        tipo = get_tipo(lista_tokens[look_ahead + 1], tabela_simbolos)
        tipoAtribuicao = get_tipo(lista_tokens[look_ahead - 1], tabela_simbolos)
        if tipo and tipoAtribuicao:
            if tipo == "int":
                if tipoAtribuicao == tipo:
                    return True
                else:
                    print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, tipoAtribuicao, tipo ) + '\033[0m') #DETALHAR ERRO
                    return False
            elif tipo == "boolean":
                if tipoAtribuicao == tipo:
                    return True
                else:
                    print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, tipoAtribuicao, tipo ) + '\033[0m') #DETALHAR ERRO
                    return False
        else:
            if not tipoAtribuicao or not tipo: ################# verificaarrr com calma
                print('\033[91m' + "Semantic error in line {0}, uninitialized variable".format(lista_tokens[look_ahead - 2].linha) + '\033[0m') #DETALHAR ERRO
                return False
            elif lista_tokens[look_ahead + 1].nome == "<numerico>": #AGORA ACEITA SER UMA DECLARAÇÇÃO DO TIPO a = 10;
                return True
            else:
                print('\033[91m' + "Semantic error in line {0}, uninitialized variable".format(lista_tokens[look_ahead - 2].linha) + '\033[0m') #DETALHAR ERRO
                return False

    else:
        print('\033[91m' + "Semantic error line: {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 2].linha, lista_tokens[look_ahead - 2].lexema, lista_tokens[look_ahead + 1].lexema) + '\033[0m')
        return False


def verificar_expressao(lista_tokens, tabela_simbolos, look_ahead):
    tipo = get_tipo(lista_tokens[look_ahead], tabela_simbolos)
    tipoAtribuicao = get_tipo(lista_tokens[look_ahead + 2], tabela_simbolos)
    if tipo and tipoAtribuicao:
        if tipo == "boolean" and lista_tokens[look_ahead + 2].nome == "<palavraBooleana>":
            if lista_tokens[look_ahead + 3].nome == "<booleanas>":
                resultado = get_tipo(lista_tokens[look_ahead + 4], tabela_simbolos)
                if resultado == tipo:
                    return True
                else:
                    print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
                    return False
            return True
        elif (tipo == "int" and lista_tokens[look_ahead + 2].nome == "<numerico>") or (tipo == "int" and tipoAtribuicao == "int"):
            if lista_tokens[look_ahead + 3].nome == "<booleanas>":
                resultado = get_tipo(lista_tokens[look_ahead + 4], tabela_simbolos)
                if resultado:
                    if resultado == tipo:
                        return True
                    else:
                        print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
                        return False
                else:
                    if lista_tokens[look_ahead + 4].nome == "<numerico>":
                        return True
                    else:
                        print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
                        return False
            return True
        elif lista_tokens[look_ahead].nome == "<variavel>" or lista_tokens[look_ahead].nome == "<numerico>":
            if tipo == tipoAtribuicao:
                return True
        else:
            print('\033[91m' + "Semantic error line: {0}, Incompatible types".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
            return False
    elif (not tipo and not tipoAtribuicao) or (not tipo and tipoAtribuicao) or (tipo and not tipoAtribuicao):
        if lista_tokens[look_ahead + 2].nome == "<numerico>" or lista_tokens[look_ahead].nome == "<numerico>":
            
            return True
        else:
            print('\033[91m' + "Semantic error line: {0}, uninitialized variable".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
            return False
    else:
        print('\033[91m' + "Semantic error line: {0}, uninitialized variable".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
        return False

def verificar_procedimento(lista_tokens, tabela_simbolos, look_ahead):
    while(lista_tokens[look_ahead].nome != "<fecha_chaves>"):
        if(lista_tokens[look_ahead].nome == "<retorno>"):
            print('\033[91m' + "Semantic error line: {0}, procedure must have no return".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
            return False
        look_ahead += 1
    return True

def verificar_retorno_variavel(lista_tokens, tabela_simbolos, look_ahead):
    if(get_tipo(lista_tokens[look_ahead], tabela_simbolos)):
        return True
    else:
        print('\033[91m' + "Semantic error line: {0}, uninitialized variable".format(lista_tokens[look_ahead - 2].linha) + '\033[0m')
        return False