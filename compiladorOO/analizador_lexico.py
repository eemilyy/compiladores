from token_lex import TokenLex

class AnalizadorLexico:

    def __init__(self,texto):
        self.texto = texto
        self.tokens = []
    
    def tokenizar(self, texto):
        buffer = ""
        linha_atual = 1
        #inserir_prox = False
        for linha in texto:
            for i in range(len(linha)):
                if((i + 1) < len(linha)):
                    buffer += linha[i]
                    #if(inserir_prox):
                        #inserir_prox = False
                    if(self.verifica_delimitadores(buffer, linha_atual)):
                        #print("hello")
                        buffer = ""
                    elif(linha[i + 1] == " " or linha[i + 1] == "{" or linha[i + 1] == "}" or linha[i + 1] == "(" or linha[i + 1] == ")" or linha[i + 1] == ";"):
                        #inserir_prox = True
                        buffer = buffer.strip()
                        self.verifica_palavras_reservadas(buffer, linha_atual)
                        buffer = ""
                        
                    
                        
            buffer = ""
            linha_atual += 1

    
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
        elif (buffer == "int" or buffer == "boolean"):
            self.tokens.append(TokenLex("<tipo>","int,boolean",linha))
            return True
        elif (buffer == "def"):
            self.tokens.append(TokenLex("<declaracao_func>","def",linha))
            return True
        elif (buffer == "procedure"):
            self.tokens.append(TokenLex("<procedimento>","proedure",linha))
            return True
        elif (buffer == "const"):
            self.tokens.append(TokenLex("<constante>","const",linha))
            return True
        elif (buffer == "return"):
            self.tokens.append(TokenLex("<retorno>","return",linha))
            return True
        elif (buffer == "if" or buffer == "else"):
            self.tokens.append(TokenLex("<condicao>","if,else",linha))
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
        elif (buffer == "==" or buffer == "!=" or buffer == "<=" or buffer == ">=" or buffer == ">" or buffer == "<"):
            self.tokens.append(TokenLex("<booleanas>",">, <, >=, <=, ==, !=",linha))
            return True
        elif (buffer == "="):
            self.tokens.append(TokenLex("<atribuição>","=",linha))
            return True
        else:
            #print("entrou variavel")
            self.varivel(buffer, linha)
            #return False #não encontrado

    def varivel(self, buffer, linha):   
        #print(buffer)
        if((buffer[0].upper() >= 'A' and buffer[0].upper() <= 'Z')):
            # for c in buffer:
            #     #print(c)
            #     if(c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
            #         continue
            #     else:
            #         return False
            self.tokens.append(TokenLex("<varivel>",buffer,linha))
        else:
            for c in buffer:
                 #print(c)
                 if(c >= '0' and c <= '9'):
                     continue
                 else:
                     return False
            self.tokens.append(TokenLex("<numerico>",buffer,linha))

    def imprimir_lista_tokens(self):
        for t in self.tokens:
            print(t.nome + " " + t.lexema + " " + str(t.linha))