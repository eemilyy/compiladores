from token_lex import TokenLex

class GeradorCodigoIntermediario:
    
    def __init__(self, lista_instrucoes):
        self.lista_instrucoes = lista_instrucoes
        self.labels = 0
        self.labelsElse = []

    def imprimirListainstrucoes(self):
        for i in range(len(self.lista_instrucoes)):
            for j in range(len(self.lista_instrucoes[i])):
                print(self.lista_instrucoes[i][j].lexema, end=" ")
            print("")

    def start(self):

        print("CODIGO INTERMEDIARIO:")
        for i in range(len(self.lista_instrucoes)):
            print("")
            if(self.lista_instrucoes[i][1].nome) == "<atribuicao>": 
                #print(self.lista_instrucoes[i][1].lexema)
                self.gen_attr(self.lista_instrucoes[i]) #chamando funcao para gerar codigo para atribuicao

            elif(self.lista_instrucoes[i][0].nome) == "<condicao>":
                #print(self.lista_instrucoes[i][0].lexema)
                self.gen_if(self.lista_instrucoes[i])



    def gen_if(self, instrucao):
        if(instrucao[0].lexema == "if"):
            listAux = []
            listAux.append(TokenLex("_c0","_c0",0))
            listAux.append(TokenLex("<atribuicao>","=",0))
            for item in instrucao:
                if item.lexema not in ["if","(",")"]:
                    listAux.append(item)

            self.gen_attr(listAux)

            self.labels += 1
            print("ifFalse _c0 goto: L{0}".format(self.labels))
            self.labelsElse.append(self.labels)

        else:
            print("L{0}:".format(self.labelsElse.pop()))
            #print("else")

    def gen_attr(self, instrucao):
        if(len(instrucao) == 3):
            for item in instrucao:
                print(item.lexema,end=" ")
            print("")
        else:
            #instrucao.reverse()
            if(instrucao[3].nome == "<abre_parenteses>"):
                contParam = 0
                i = 4
                while(instrucao[i + 1].nome != "<fecha_parenteses>"):
                    i += 1
                while(instrucao[i].nome != "<abre_parenteses>"):
                    print("_p{0} = {1} ".format(contParam,instrucao[i].lexema))
                    i -= 1
                    contParam += 1
                
                print("{0} = call {1},{2}".format(instrucao[0].lexema, instrucao[2].lexema, contParam))

            else:
                print("_t0 = {0} {1} {2}".format(instrucao[2].lexema, instrucao[3].lexema, instrucao[4].lexema))
                anterior = 0
                i = 5
                while(i < len(instrucao)):
                    print("_t{0} = _t{1} {2} {3}".format(anterior + 1,anterior,instrucao[i].lexema,instrucao[i+1].lexema))

                    anterior += 1

                    i += 2
            
                print("{0} = _t{1}".format(instrucao[0].lexema,anterior))
