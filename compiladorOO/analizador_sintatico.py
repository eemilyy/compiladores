from analizador_semantico import *

class AnalizadorSintatico:
    def __init__(self, lista_tokens, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.lista_tokens = lista_tokens
        self.look_ahead = 0

    def start(self):
        print("START")
        self.programa()
        print("Fim de compilação")

    def match(self, terminal):
        if(self.lista_tokens[self.look_ahead].nome == terminal):
            print("match!: "+ terminal)
            if(self.look_ahead < len(self.lista_tokens)):
                self.look_ahead += 1
        else:
            print('\033[91m' + "Not Found: "+ terminal + '\033[0m')
            print('\033[91m' + "Syntax error line: " + str(self.lista_tokens[self.look_ahead].linha) + '\033[0m')
            #self.look_ahead += 1
#----------------------------------------------------------------------------------------------------
    def programa(self):
        #look_ahead = self.lista_tokens[self.look_ahead] #busca o token que look_ahead esta apontando
        self.match("<programa>")
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")

               
    def bloco(self):
        token_ = self.lista_tokens[self.look_ahead]
        if(token_.nome == "<tipo>"):
            self.declaracao_variavel()
            self.bloco()
            # token_ = self.lista_tokens[self.look_ahead]
            # print("VOLTOU" + token_.nome)
            # if(token_.nome != "<fim_comando>"):
            #     self.match("<fim_comando>")
            # elif(token_.nome == "<atribuicao>"):                
            #     self.atribuicao()

            # self.bloco()
        # elif(token_.lexema == "boolean"):
        #     print("entrou boolean")
        #     self.declaracao_variavelBooleana()
        #     self.bloco()
        elif(token_.nome == "<atribuicao>"):                
            self.atribuicao()
            self.bloco()
        elif(token_.nome == "<variavel>"): #Analisar com calma
            #print("variavel" + self.lista_tokens[self.look_ahead + 1].nome)
            if(self.lista_tokens[self.look_ahead + 1].nome == "<abre_parenteses>"):
                #print("funcao")
                self.funcao()
                self.match("<fim_comando>")
            else:
                self.match("<variavel>")
                self.atribuicao()
            self.bloco()
        elif(token_.nome == "<declaracao_func>"):
            self.declaracao_funcao()
            self.bloco()
        elif(token_.nome == "<condicao>"):
            self.condicao()
            self.bloco()
        elif(token_.nome == "<laco>"):
            self.laco()
            self.bloco()
        elif(token_.nome == "<imprimir>"):
            self.imprimir()
            self.bloco()
        elif(token_.nome == "<retorno>"):
            self.retorno()
            self.bloco()
        elif(token_.nome == "<procedimento>"):
            self.procedimento()
            self.bloco()
        # elif(token_.nome == "<parar>"):
        #     self.match("<parar>")
        #     self.match("<fim_comando>")
        #     self.bloco()
        # elif(token_.nome == "<continuar>"):
        #     self.match("<continuar>")
        #     self.match("<fim_comando>")
        #     self.bloco()
        elif(token_.nome == "<variavel>"):
            self.funcao()
            self.match("<fim_comando>")
            self.bloco()
        elif(token_.nome == "<constante>"):
            self.match("<constante>")
            self.match("<variavel>")
            self.match("<fim_comando>")
            self.bloco()
        else:
            #print('\033[93m' + "BLOCO Syntax error line: " + str(token_.linha) + '\033[0m')
            return

    def declaracao_variavelBooleana(self):
        self.match("<tipo>")
        self.match("<variavel>")
        #self.match("<fim_comando>")

    def declaracao_variavel(self):
        # if(self.lista_tokens[self.look_ahead].lexema == "boolean"):
        #     self.declaracao_variavelBooleana()
        # else:
        self.match("<tipo>")
        self.match("<variavel>")
        # elif(self.lista_tokens[self.look_ahead].lexema == "boolean"):
        #     self.match("<tipo>")
        #     self.match("<palavraBooleana>")

        #print("DV:  "+ str((self.lista_tokens[self.look_ahead]).nome))
        if(self.lista_tokens[self.look_ahead].nome != "<atribuicao>"):
            self.match("<fim_comando>")

    def declaracao_funcao(self):
        self.match("<declaracao_func>")
        self.funcao()
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")

    def atribuicao(self):
        if verificar_atribuicao(self.lista_tokens, self.tabela_simbolos, self.look_ahead):
            self.match("<atribuicao>")
            #print(self.lista_tokens[self.look_ahead - 3].lexema)
            if(self.lista_tokens[self.look_ahead - 3].lexema == "boolean"):
                self.match("<palavraBooleana>")
            elif(self.lista_tokens[self.look_ahead].nome != "<variavel>"):
                self.match("<numerico>")
                if(self.lista_tokens[self.look_ahead].nome == "<aritmeticas>"):
                    self.match("<aritmeticas>")
                    self.match("<numerico>")
            else:
                print(self.lista_tokens[self.look_ahead + 1].nome)
                if(self.lista_tokens[self.look_ahead + 1].nome == "<abre_parenteses>"):
                    print("entrou funcc!")
                    self.funcao()
                else:
                    self.match("<variavel>")
            self.match("<fim_comando>")
        else:
            exit()

    def funcao(self):
        self.match("<variavel>")
        self.match("<abre_parenteses>")
        self.parametros()
        self.match("<fecha_parenteses>")

    def parametros(self):
        token_ = self.lista_tokens[self.look_ahead]
        print(self.lista_tokens[self.look_ahead].nome)
        #<parametros> ::= <declaracao_variavel> , <parametros> | <declaracao_variavel> | ε
        if(token_.nome == "<tipo>"):
            self.match("<tipo>")
            self.match("<variavel>")
            if(self.lista_tokens[self.look_ahead].nome == "<virgula>"):
                #self.match("<virgula>")
                #self.match("<tipo>")
                #self.match("<variavel>")
                self.parametros()
            else:
                return
        elif(token_.nome == "<virgula>"):
            self.match("<virgula>")
            if(self.lista_tokens[self.look_ahead].nome != "<variavel>" and self.lista_tokens[self.look_ahead].nome != "<numerico>"):
                self.match("<tipo>")
                self.match("<variavel>")
                self.parametros()
            else:
                self.parametros()
                
        elif(token_.nome == "<variavel>"):
            self.match("<variavel>")
            self.parametros()
        elif(token_.nome == "<numerico>"):
            self.match("<numerico>")
            self.parametros()
        else:
            return

    def expressao_simples(self): #*
        self.match("<variavel>")
        #print(self.lista_tokens[self.look_ahead].nome)
        if(self.lista_tokens[self.look_ahead].nome == "<booleanas>"):
            self.match("<booleanas>")
            if(self.lista_tokens[self.look_ahead].nome == "<variavel>"):
                self.match("<variavel>")
            else:
                self.match("<numerico>")
        #elif(self.lista_tokens[self.look_ahead].nome == "<aritmeticas>"):
        else:
            self.match("<aritmeticas>")
            self.match("<variavel>")
            if(self.lista_tokens[self.look_ahead].nome == "<booleanas>"):
                self.match("<booleanas>")
                if(self.lista_tokens[self.look_ahead].nome == "<variavel>"):
                    self.match("<variavel>")
                else:
                    self.match("<numerico>")
        #self.match("<variavel>")
    
    def condicao(self):
        self.match("<condicao>")
        self.match("<abre_parenteses>")
        self.expressao_simples()
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
        if(self.lista_tokens[self.look_ahead].nome == "<continuar>"):
            self.match("<continuar>")
            self.match("<fim_comando>")
        elif(self.lista_tokens[self.look_ahead].nome == "<parar>"):
            self.match("<parar>")
            self.match("<fim_comando>")
        self.match("<fecha_chaves>")
    
    def imprimir(self):
        self.match("<imprimir>")
        self.match("<abre_parenteses>")
        self.match("<variavel>") # Falta constante
        self.match("<fecha_parenteses>")
        self.match("<fim_comando>")
    
    def retorno(self):
        self.match("<retorno>")
        if(self.lista_tokens[self.look_ahead].nome == "<variavel>"):
            self.match("<variavel>")
        #elif(self.lista_tokens[self.look_ahead].nome == "<numerico>"):
        else:
            self.match("<numerico>")
        self.match("<fim_comando>")
    
    def procedimento(self):
        self.match("<procedimento>")
        self.funcao()
        self.match("<abre_chaves>")
        self.bloco()
        self.match("<fecha_chaves>")
    
