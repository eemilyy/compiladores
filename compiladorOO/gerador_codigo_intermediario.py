
class GeradorCodigoIntermediario:
    
    def __init__(self, lista_instrucoes):
        self.lista_instrucoes = lista_instrucoes

    def imprimirListainstrucoes(self):
        for i in range(len(self.lista_instrucoes)):
            for j in range(len(self.lista_instrucoes[i])):
                print(self.lista_instrucoes[i][j].lexema, end=" ")
            print("")

    def start(self):

        print("CODIGO INTERMEDIARIO:")
        for i in range(len(self.lista_instrucoes)):
            if(self.lista_instrucoes[i][1].nome) == "<atribuicao>": 
                #print(self.lista_instrucoes[i][1].lexema, end=" ")
                self.gen_attr(self.lista_instrucoes[i]) #chamando funcao para gerar codigo para atribuicao



    def gen_if(self, instrucao):
        print("funcao para printar if")

    def gen_attr(self, instrucao):
        if(len(instrucao) == 3):
            for item in instrucao:
                print(item.lexema,end=" ")
            print("")
        else:
            #instrucao.reverse()
            print("_t0 = {0} {1} {2}".format(instrucao[2].lexema, instrucao[3].lexema, instrucao[4].lexema))

            i = 5
            while(i < len(instrucao)-1):
                print("_t{0} = _t{1} {2} {3}".format(i-4,i-5,instrucao[i].lexema,instrucao[i+1].lexema))
                i += 2
            
            print("{0} = _t{1}".format(instrucao[0].lexema,i-6))
