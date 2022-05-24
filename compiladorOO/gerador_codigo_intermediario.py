from token_lex import TokenLex

class GeradorCodigoIntermediario:
    
    def __init__(self, lista_instrucoes):
        self.lista_instrucoes = lista_instrucoes
        self.labels = 0
        self.lastLabelWhile = []
        self.labelsElse = []

    def imprimirListainstrucoes(self):
        for i in range(len(self.lista_instrucoes)):
            for j in range(len(self.lista_instrucoes[i])):
                print(self.lista_instrucoes[i][j].lexema, end=" ")
            print("")

    def start(self):
        arq = open("output.txt", 'w')

        print('\033[4m' + "CODIGO INTERMEDIARIO:" + '\033[0m')
        for i in range(len(self.lista_instrucoes)):
            print("")
            arq.write("\n")

            if(self.lista_instrucoes[i][1].nome) == "<atribuicao>": 
                #print(self.lista_instrucoes[i][1].lexema)
                self.gen_attr(self.lista_instrucoes[i], arq) #chamando funcao para gerar codigo para atribuicao

            elif(self.lista_instrucoes[i][0].nome) == "<condicao>":
                #print(self.lista_instrucoes[i][0].lexema)
                self.gen_if(self.lista_instrucoes[i], arq)

            elif(self.lista_instrucoes[i][0].nome) == "<laco>" or self.lista_instrucoes[i][0].nome == "<fecha_chaves>":
                self.gen_while(self.lista_instrucoes[i], arq)
            
            elif(self.lista_instrucoes[i][0].nome) == "<variavel>": #chamada procedure
                self.gen_call_proc(self.lista_instrucoes[i], arq)

            elif(self.lista_instrucoes[i][0].nome) == "<declaracao_func>":
                #print("declaracaoooo funcao ---- gen <<<<<<<<<<<<")
                self.gen_func(self.lista_instrucoes[i], arq)
            
            elif(self.lista_instrucoes[i][0].nome) == "<end_func>":
                print("end_func")
                arq.write("end_func" + "\n")
                #print("declaracaoooo funcao ---- gen <<<<<<<<<<<<")
                #self.gen_func(self.lista_instrucoes[i])

            elif(self.lista_instrucoes[i][0].nome == "<procedimento>"):
                #print("declaracao procedimento <-------------------------------------")
                self.gen_proc(self.lista_instrucoes[i], arq)

            elif(self.lista_instrucoes[i][0].nome) == "<end_proc>":
                print("end_proc")
                arq.write("end_proc" + "\n")

            elif(self.lista_instrucoes[i][0].nome) == "<retorno>":
                print("{0} {1}".format(self.lista_instrucoes[i][0].lexema, self.lista_instrucoes[i][1].lexema))
                arq.write("{0} {1}".format(self.lista_instrucoes[i][0].lexema, self.lista_instrucoes[i][1].lexema) + "\n")

            elif(self.lista_instrucoes[i][0].nome) == "<imprimir>":
                 #print("{0} {1}".format(self.lista_instrucoes[i][0].lexema, self.lista_instrucoes[i][1].lexema))
                 a = print("print({0})".format(self.lista_instrucoes[i][2].lexema))
                 arq.write("print({0})".format(self.lista_instrucoes[i][2].lexema) + "\n")
        
        arq.close()

    def gen_if(self, instrucao, arq):
        if(instrucao[0].lexema == "if"):
            listAux = []
            # listAux.append(TokenLex("_c0","_c0",0))
            # listAux.append(TokenLex("<atribuicao>","=",0))
            for item in instrucao:
                if item.lexema not in ["if","(",")"]:
                    listAux.append(item)

            #self.gen_attr(listAux, arq)

            self.labels += 1
            print("ifFalse",end=" ")
            arq.write("ifFalse ")

            for item in listAux:
                print(item.lexema, end="")
                arq.write(item.lexema + "")

            if len(self.lastLabelWhile) != 0:
                self.labels += 1 
            print(" goto: L{0}".format(self.labels))
            arq.write(" goto: L{0}".format(self.labels) + "\n")
            
            self.labelsElse.append(self.labels)

        else:
            pop = self.labelsElse.pop()
            print("L{0}:".format(pop))
            arq.write("L{0}:".format(pop) + "\n")
            #print("else")


    def gen_while(self, instrucao, arq):
        if(instrucao[0].lexema == "while"):
            listAux = []
            # listAux.append(TokenLex("_c0","_c0",0))
            # listAux.append(TokenLex("<atribuicao>","=",0))
            for item in instrucao:
                if item.lexema not in ["while","(",")"]:
                    listAux.append(item)


            self.labels += 1
            #self.lastLabelWhile = self.labels
            self.lastLabelWhile.append(self.labels)
            print("L{0}:".format(self.labels))
            arq.write("L{0}:".format(self.labels) + "\n")
            
            #self.gen_attr(listAux, arq)
            print("whileFalse",end=" ")
            arq.write("whileFalse ")
            for item in listAux:
                print(item.lexema, end="")
                arq.write(item.lexema + "")

            print(" goto: L{0}".format(self.labels + 1))
            arq.write(" goto: L{0}".format(self.labels + 1) + "\n")

            #self.labelsElse.append(self.labels)
        else:
            #self.labels += 1 <<<<<<<<<<<<<<<<,,------------------
            pop = self.lastLabelWhile.pop()
            arq.write("goto: L{0}".format(pop) + "\n")
            arq.write("L{0}:".format(pop + 1) + "\n")
            print("goto: L{0}".format(pop))
            print("L{0}:".format(pop + 1))

    def gen_attr(self, instrucao, arq):
        if(len(instrucao) == 3):
            for item in instrucao:
                print(item.lexema,end=" ")
                arq.write(item.lexema + " ")
            print("")
            arq.write("\n")
        else:
            #instrucao.reverse()
            if(instrucao[3].nome == "<abre_parenteses>"): #chamada de funcao
                contParam = 0
                i = 4
                if len(instrucao) > 5:
                    while(instrucao[i + 1].nome != "<fecha_parenteses>"):
                        i += 1
                    while(instrucao[i].nome != "<abre_parenteses>"):
                        if instrucao[i].lexema != ",":
                            print("_param = {0} ".format(instrucao[i].lexema))
                            arq.write("_param = {0} ".format(instrucao[i].lexema) + "\n")
                            contParam += 1
                        i -= 1
                
                print("{0} = call {1},{2}".format(instrucao[0].lexema, instrucao[2].lexema, contParam))
                arq.write("{0} = call {1},{2}".format(instrucao[0].lexema, instrucao[2].lexema, contParam) + "\n")

            else:
                print("_t0 = {0} {1} {2}".format(instrucao[2].lexema, instrucao[3].lexema, instrucao[4].lexema))
                arq.write("_t0 = {0} {1} {2}".format(instrucao[2].lexema, instrucao[3].lexema, instrucao[4].lexema) + "\n")
                anterior = 0
                i = 5
                while(i < len(instrucao)):
                    print("_t{0} = _t{1} {2} {3}".format(anterior + 1,anterior,instrucao[i].lexema,instrucao[i+1].lexema))
                    arq.write("_t{0} = _t{1} {2} {3}".format(anterior + 1,anterior,instrucao[i].lexema,instrucao[i+1].lexema) + "\n")

                    anterior += 1

                    i += 2
            
                print("{0} = _t{1}".format(instrucao[0].lexema,anterior))
                arq.write("{0} = _t{1}".format(instrucao[0].lexema,anterior) + "\n")

    def gen_call_proc(self, instrucao, arq):
        # for item in instrucao:
        #     print(item.lexema,end=" ")
        # print("->>>>>>>>>>>>>> chamada de procedimento")

        contParam = 0
        i = 2
        if len(instrucao) > 3:
            while(instrucao[i + 1].nome != "<fecha_parenteses>"):
                i += 1
            while(instrucao[i].nome != "<abre_parenteses>"):
                if instrucao[i].lexema != ",":
                    print("_param = {0} ".format(instrucao[i].lexema))
                    arq.write("_param = {0} ".format(instrucao[i].lexema) + "\n")
                    contParam += 1
                i -= 1
        
        print("call {0},{1}".format(instrucao[0].lexema, contParam))
        arq.write("call {0},{1}".format(instrucao[0].lexema, contParam) + "\n")

    def gen_func(self, instrucao, arq):
        # for item in instrucao:
        #     print(item.lexema,end=" ")
        # print("")

        # contParam = 0
        # i = 2
        # if len(instrucao) > 3:
        #     while(instrucao[i + 1].nome != "<fecha_parenteses>"):
        #         i += 1
        #     while(instrucao[i].nome != "<abre_parenteses>"):
        #         if instrucao[i].lexema not in  [",","int","boolean"]:
        #             print("_p{0} = {1} ".format(contParam,instrucao[i].lexema))
        #             arq.write("_p{0} = {1} ".format(contParam,instrucao[i].lexema) + "\n")
        #             contParam += 1
        #         i -= 1
        print("func {0}:\nbegin_func:".format(instrucao[1].lexema))
        arq.write("func {0}:\nbegin_func:".format(instrucao[1].lexema) + "\n")
        

    def gen_proc(self, instrucao, arq):
        
        # contParam = 0
        # i = 2
        # if len(instrucao) > 3:
        #     while(instrucao[i + 1].nome != "<fecha_parenteses>"):
        #         i += 1
        #     while(instrucao[i].nome != "<abre_parenteses>"):
        #         if instrucao[i].lexema not in  [",","int","boolean"]:
        #             print("_p{0} = {1} ".format(contParam,instrucao[i].lexema))
        #             arq.write("_p{0} = {1} ".format(contParam,instrucao[i].lexema) + "\n")
        #             contParam += 1
        #         i -= 1
        print("proc {0}:\nbegin_proc:".format(instrucao[1].lexema))
        arq.write("proc {0}:\nbegin_proc:".format(instrucao[1].lexema) + "\n")