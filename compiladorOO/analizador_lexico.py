from token_lex import TokenLex

class AnalizadorLexico:

    def __init__(self,texto):
        self.texto = texto
        self.tokens = []
        self.palavras_reservadas= ["main",
                                    "int",
                                    "boolean",
                                    "const",
                                    "def",
                                    "procedure",
                                    "return",
                                    "if",
                                    "else",
                                    "while",
                                    "break",
                                    "continue", 
                                    "printf"]
    
    def tokenizar(self, texto):
        buffer = ""
        linha_atual = 1
        for linha in texto:
            for caractere in linha:
                if(caractere != " "):
                    buffer += caractere
                    print(buffer)
                else:
                    #buffer = buffer.strip(" ")
                    if(self.palavras_reservadas.__contains__(buffer)):
                        print("achou " + buffer + " "+ str(linha_atual))
                        self.verifica_palavras_reservadas(buffer, linha_atual)

                    buffer = ""
            buffer = ""
                #buffer = buffer + caractere if caractere != " " else buffer = ""
                    #print(buffer)
            #print(linha)
            linha_atual += 1


        for t in self.tokens:
            print(t.nome + " " + t.lexema + " " + str(t.linha))

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
        elif (buffer == "return"):
            self.tokens.append(TokenLex("<retorno>","return",linha))
            return True
        elif (buffer == "if" or buffer == "else"):
            self.tokens.append(TokenLex("<if>","if,else",linha))
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
        else:
            return False #não encontrado