from token import Token

class AnalizadorLexico:

    def __init__(self,texto):
        self.texto = texto
        self.tokens = []
        self.palavras_reservadas= ["main"]
    
    def tokenizar(self, texto):
        buffer = ""
        for linha in texto:
            for caractere in linha:
                print(caractere)
            #print(linha)