from token_lex import TokenLex
from simbolo import Simbolo

class AnalizadorLexico:

    def __init__(self,texto):
        self.texto = texto
        self.tokens = []
        self.tabela_simbolos = {}
    
    def tokenizar(self, texto):
        buffer = ""
        linha_atual = 1
        #inserir_prox = False
        for linha in texto:
            for i in range(len(linha)):
                if((i + 1) < len(linha)): #saber se a linha chegou no final
                    buffer += linha[i]
                    #if(inserir_prox):
                        #inserir_prox = False
                    if(self.verifica_delimitadores(buffer, linha_atual)):
                        #print("hello")
                        buffer = ""
                    elif(linha[i + 1] == " " or linha[i + 1] == "\n" or linha[i + 1] == "{" or linha[i + 1] == "}" or linha[i + 1] == "(" or linha[i + 1] == ")" or linha[i + 1] == ";" or linha[i + 1] == ","):
                        #inserir_prox = True
                        buffer = buffer.strip()
                        self.verifica_palavras_reservadas(buffer, linha_atual)
                        buffer = ""
                                           
                        
            buffer = ""
            linha_atual += 1
        self.tokens.append(TokenLex("<EOF>","EOF",(linha_atual + 1)))

    
    def verifica_delimitadores(self, p, linha):
        if(p == " "):
            return True
        elif(p == "{"):
            self.tokens.append(TokenLex("<abre_chaves>","{",linha))
            return True
        elif(p == "}"):
            self.tokens.append(TokenLex("<fecha_chaves>","}",linha))
            return True
        elif(p == "("):
            self.tokens.append(TokenLex("<abre_parenteses>","(",linha))
            return True
        elif(p == ")"):
            self.tokens.append(TokenLex("<fecha_parenteses>",")",linha))
            return True
        elif(p == ";"):
            self.tokens.append(TokenLex("<fim_comando>",";",linha))
            return True
        else:
            return False


    def verifica_palavras_reservadas(self, buffer, linha):
        if (buffer == "main"):
            self.tokens.append(TokenLex("<programa>","main",linha))
            return True
        elif (buffer == "int"):
            self.tokens.append(TokenLex("<tipo>","int",linha))
            return True
        elif (buffer == "boolean"):
            self.tokens.append(TokenLex("<tipo>","boolean",linha))
            return True
        elif (buffer == "$def"):
            self.tokens.append(TokenLex("<declaracao_func>","$def",linha))
            return True
        elif (buffer == "&def"):
            self.tokens.append(TokenLex("<declaracao_func>","&def",linha))
            return True
        elif (buffer == "procedure"):
            self.tokens.append(TokenLex("<procedimento>","procedure",linha))
            return True
        elif (buffer == "const"):
            self.tokens.append(TokenLex("<constante>","const",linha))
            return True
        elif (buffer == "return"):
            self.tokens.append(TokenLex("<retorno>","return",linha))
            return True
        elif (buffer == "if"):
            self.tokens.append(TokenLex("<condicao>","if",linha))
            return True
        elif (buffer == "else"):
            self.tokens.append(TokenLex("<condicao>","else",linha))
            return True
        elif (buffer == "while"):
            self.tokens.append(TokenLex("<laco>","while",linha))
            return True
        elif (buffer == "break"):
            self.tokens.append(TokenLex("<parar>","break",linha))
            return True
        elif (buffer == "continue"):
            self.tokens.append(TokenLex("<continuar>","continue",linha))
            return True
        elif (buffer == "printf"):
            self.tokens.append(TokenLex("<imprimir>","printf",linha))
            return True
        elif (buffer == "=="):
            self.tokens.append(TokenLex("<booleanas>","==",linha))
            return True
        elif (buffer == "!="):
            self.tokens.append(TokenLex("<booleanas>","!=",linha))
            return True
        elif (buffer == "<="):
            self.tokens.append(TokenLex("<booleanas>","<=",linha))
            return True
        elif (buffer == ">="):
            self.tokens.append(TokenLex("<booleanas>",">=",linha))
            return True
        elif (buffer == ">"):
            self.tokens.append(TokenLex("<booleanas>",">",linha))
            return True
        elif (buffer == "<"):
            self.tokens.append(TokenLex("<booleanas>","<",linha))
            return True

        elif (buffer == "+"):
            self.tokens.append(TokenLex("<aritmeticas>","+",linha))
            return True
        elif (buffer == "-"):
            self.tokens.append(TokenLex("<aritmeticas>","-",linha))
            return True
        elif (buffer == "*"):
            self.tokens.append(TokenLex("<aritmeticas>","*",linha))
            return True
        elif (buffer == "/"):
            self.tokens.append(TokenLex("<aritmeticas>","/",linha))
            return True
        elif (buffer == "="):
            self.tokens.append(TokenLex("<atribuicao>","=",linha))
            return True
        elif (buffer == ","):
            self.tokens.append(TokenLex("<virgula>",",",linha))
            return True
        elif (buffer == "true"):
            self.tokens.append(TokenLex("<palavraBooleana>","true",linha))
            return True
        elif(buffer == "false"):
            self.tokens.append(TokenLex("<palavraBooleana>","false",linha))
            return True
        else:
            #print("entrou variavel")
            self.varivel(buffer, linha)
            #return False #não encontrado

    def varivel(self, buffer, linha):   
        #print(buffer)
        if((buffer[0].upper() >= 'A' and buffer[0].upper() <= 'Z')):
            for c in buffer:
                #print(c)
                if((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9')):
                    continue
                else:
                    print('\033[91m' + "Error variable line: " + str(linha) + '\033[0m')
                    quit()

            last_token = self.tokens[len(self.tokens) -1] #pega o ultimo token adicionado
            if(buffer not in self.tabela_simbolos): ##### VERIFICA SE A VARIAVEL JÁ EXISTE NA LISTA
                if(last_token.nome == "<tipo>"): #adicionando na tabela de simbolos
                        if(last_token.lexema == "int"):
                            self.tabela_simbolos[buffer] = Simbolo("int",linha)
                        
                        elif(last_token.lexema == "boolean"):
                            self.tabela_simbolos[buffer] = Simbolo("boolean",linha)
                        

                elif(last_token.lexema == "$def"):
                    self.tabela_simbolos[buffer] = Simbolo("$def",linha)

                elif(last_token.lexema == "&def"):
                    self.tabela_simbolos[buffer] = Simbolo("&def",linha)   

                elif(last_token.nome == "<constante>"):
                    self.tabela_simbolos[buffer] = Simbolo("const",linha)

                self.tokens.append(TokenLex("<variavel>",buffer,linha))
            else:
                print(self.tokens[len(self.tokens) -1].nome)
                if(self.tokens[len(self.tokens) -1].nome != "<tipo>"):
                    self.tokens.append(TokenLex("<variavel>",buffer,linha))
                else:
                    print('\033[91m' + "Error variable {0} already exists: ".format(buffer) + '\033[0m')
                    quit()
        else:
            for c in buffer:
                 #print(c)
                 if(c >= '0' and c <= '9'):
                     continue
                 else:
                    print('\033[91m' + "Error line: " + str(linha) + '\033[0m')
                    quit()
                    return False
            self.tokens.append(TokenLex("<numerico>",buffer,linha))

    def imprimir_lista_tokens(self):
        #print(self.tokens[3].nome + "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        for t in self.tokens:
            print(t.nome + " " + t.lexema + " " + str(t.linha))
    
    def imprimir_tabela_simbolos(self):
        print("SIMBOLOS")
        for t in self.tabela_simbolos:
            print(self.tabela_simbolos[t].tipo + " " + t + " " + str(self.tabela_simbolos[t].linha))
