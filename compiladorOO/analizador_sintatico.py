class AnalizadorSintatico:
    def __init__(self, lista_tokens):
        self.lista_tokens = lista_tokens
        self.look_ahead = 0

    def start(self):
        print("START")
        self.programa()
        print("Fim de compilação")

    def match(self, terminal):
        if(self.lista_tokens[self.look_ahead].nome == terminal):
            print("match!: "+ terminal)
            self.look_ahead += 1
        else:
            print("nao match!: "+ terminal)
            print("Syntax error line: " + str(self.lista_tokens[self.look_ahead].linha))
#----------------------------------------------------------------------------------------------------
    def programa(self):
        #look_ahead = self.lista_tokens[self.look_ahead] #busca o token que look_ahead esta apontando
        self.match("<programa>")
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")

               
    def bloco(self):
        token_ = self.lista_tokens[self.look_ahead]
        #print(token_.nome)
        if(token_.nome == "<tipo>"):
            self.declaracao_variavel()
            self.bloco()
        elif(token_.nome == "<declaracao_func>"):
            self.declaracao_funcao()
        elif(token_.nome == "<condicao>"):
            self.condicao()
        elif(token_.nome == "<laco>"):
            self.laco()
        elif(token_.nome == "<imprimir>"):
            self.imprimir()
        elif(token_.nome == "<retorno>"):
            self.retorno()
        elif(token_.nome == "<procedimento>"):
            self.procedimento()
        elif(token_.nome == "<parar>"):
            self.match("<parar>")
        elif(token_.nome == "<continuar>"):
            self.match("<continuar>")
        else:
            #print("BLOCO Syntax error line: " + str(token_.linha))
            return

    
    def declaracao_variavel(self):
        self.match("<tipo>")
        self.match("<variavel>")
        self.match("<fim_comando>")

    def declaracao_funcao(self):
        self.match("<declaracao_func>")
        self.funcao()
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")

    def funcao(self):
        self.match("<variavel>")
        self.match("<abre_parenteses>")
        self.parametros()
        self.match("<fecha_parenteses>")

    def parametros(self): # FAZER
        #<parametros> ::= <declaracao_variavel> , <parametros> | <declaracao_variavel> | ε
        pass

    def expressao_simples(self): #*
        self.match("<variavel>")
        self.match("<booleanas>")
        self.match("<variavel>")
        pass
    
    def condicao(self):
        self.match("<condicao>")
        self.match("<abre_parenteses>")
        #self.expressao_simples()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")
        self.match("<condicao>")
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")
    
    def laco(self):
        self.match("<laco>")
        self.match("<abre_parenteses>")
        self.expressao_simples() #*
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")
    
    def imprimir(self):
        self.match("<imprimir>")
        self.match("<abre_parenteses>")
        self.match("<variavel>") # Falta constante
        self.match("<fecha_parenteses>")
        self.match("<fim_comando>")
    
    def retorno(self):
        self.match("<retorno>")
        self.match("<variavel>")
        self.match("<fim_comando>")
    
    def procedimento(self):
        self.match("<procedimento>")
        self.match("<variavel>")
        self.match("<fim_comando>")
    
