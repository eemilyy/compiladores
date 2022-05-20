
class GeradorCodigoIntermediario:
    
    def __init__(self, lista_instrucoes):
        self.lista_instrucoes = lista_instrucoes

    def imprimirListainstrucoes(self):
        for i in range(len(self.lista_instrucoes)):
            for j in range(len(self.lista_instrucoes[i])):
                print(self.lista_instrucoes[i][j].lexema, end=" ")
            print("")

    def start(self):

        print("hello")

    def gen_if(self, instrucao):
        print("funcao para printar if")

    def gen_attr(self, instrucao):
        print("funcao para printar atribuicoes")
