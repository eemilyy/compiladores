from token import Token

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
        for linha in texto:
            for caractere in linha:
                if(caractere != " "):
                    buffer += caractere
                    print(buffer)
                else:
                    #buffer = buffer.strip(" ")
                    if(self.palavras_reservadas.__contains__(buffer)):
                        print("achou " + buffer)
                        
                    buffer = ""
            buffer = ""
                #buffer = buffer + caractere if caractere != " " else buffer = ""
                    #print(buffer)
            #print(linha)