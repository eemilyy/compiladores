from token_lex import TokenLex

class AnalizadorLexico:

    def __init__(self,texto):
        self.texto = texto
        self.tokens = []
    
    def tokenizar(self, texto):
        buffer = ""
        linha_atual = 1
        for linha in texto:
            for caractere in linha:
                if(self.look_ahead(caractere, linha_atual)):
                    #print(caractere != " " and caractere != "{")
                    buffer += caractere
                    #print(buffer)
                else:
                    #print(buffer)
                    self.verifica_palavras_reservadas(buffer, linha_atual)
                    buffer = ""

            buffer = ""
            linha_atual += 1

        for t in self.tokens:
            print(t.nome + " " + t.lexema + " " + str(t.linha))
    
    def look_ahead(self, p, linha):
        if(p == " "):
            return False
        elif(p == "{"):
            self.tokens.append(TokenLex("<abre_chaves>","{",linha))
            return False
        elif(p == "}"):
            self.tokens.append(TokenLex("<fecha_chaves>","}",linha))
            return False
        elif(p == "("):
            self.tokens.append(TokenLex("<abre_parenteses>","(",linha))
            return False
        elif(p == ")"):
            self.tokens.append(TokenLex("<fecha_parenteses>",")",linha))
            return False
        elif(p == ";"):
            self.tokens.append(TokenLex("<fim_comando>",";",linha))
            return False
        else:
            return True


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