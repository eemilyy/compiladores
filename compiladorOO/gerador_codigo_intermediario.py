
class GeradorCodigoIntermediario:
    
    def __init__(self, lista_instrucoes):
        self.lista_instrucoes = lista_instrucoes


    def start(self):
        for i in range(len(self.lista_instrucoes)):
            if self.lista_instrucoes[i].nome == "atribuicao":
                self.gen_attr(self, self.list_instrucoes[i]) #atribuicao

            elif self.lista_instrucoes[i].nome == "condicional":
                self.gen_if(self, self.list_instrucoes[i])

    def gen_if(self, instrucao):
        print("funcao para printar if")

    def gen_attr(self, instrucao):
        print("funcao para printar atribuicoes")
