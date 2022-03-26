class Token:
    def __init__(self, nome, lexema, linha):
        self.nome = nome
        self.lexema = lexema
        self.linha = linha

    def imprimir(self):
        print(self.nome + " " + self.lexema + " " + self.linha)
