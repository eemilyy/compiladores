from analizador_semantico import *

class AnalizadorSintatico:
    def __init__(self, lista_tokens, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.lista_tokens = lista_tokens
        self.look_ahead = 0
        self.instrucoes = []

    def start(self):
        print("START")
        self.programa()
        print("Fim de compilação")
        return self.instrucoes

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

        elif(token_.nome == "<atribuicao>"):                
            self.atribuicao()
            self.bloco()
        elif(token_.nome == "<variavel>"): #Analisar com calma
            if(self.lista_tokens[self.look_ahead + 1].nome == "<abre_parenteses>"):
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
        # elif(token_.nome == "<retorno>"): #TESTANDO RETORNO APENAS DENTRO DE DEF
        #     self.retorno()
        #     self.bloco()
        elif(token_.nome == "<procedimento>"):
            self.procedimento()
            self.bloco()
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
        self.match("<tipo>")
        self.match("<variavel>")
        if(self.lista_tokens[self.look_ahead].nome != "<atribuicao>"):
            self.match("<fim_comando>")

    def declaracao_funcao(self):
        self.match("<declaracao_func>")
        self.funcao()
        self.match("<abre_chaves>")
        self.bloco()
        self.retorno()
        self.match("<fecha_chaves>")

    def atribuicao(self):
        look_ahead_aux = self.look_ahead - 1
        instrucao_aux = []
        while self.lista_tokens[look_ahead_aux].nome != "<fim_comando>":
            #if self.lista_tokens[look_ahead_aux].nome != "<palavraBooleana>" :
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])

            look_ahead_aux += 1
        self.instrucoes.append(instrucao_aux)

        if verificar_atribuicao(self.lista_tokens, self.tabela_simbolos, self.look_ahead):
            self.match("<atribuicao>")
            if(self.lista_tokens[self.look_ahead].nome == "<palavraBooleana>"):
                self.match("<palavraBooleana>")
            elif(self.lista_tokens[self.look_ahead].nome != "<variavel>"):
                self.match("<numerico>")
                if(self.lista_tokens[self.look_ahead].nome == "<aritmeticas>"):
                    while(self.lista_tokens[self.look_ahead].nome == "<aritmeticas>"):
                        self.match("<aritmeticas>")
                        if(self.lista_tokens[self.look_ahead].nome == "<numerico>"):
                            self.match("<numerico>")
                        else:
                            self.match("<variavel>")
            else:
                if(self.lista_tokens[self.look_ahead + 1].nome == "<abre_parenteses>"):
                    self.funcao()
                else:
                    self.match("<variavel>")
                    if(self.lista_tokens[self.look_ahead].nome == "<aritmeticas>"):
                        while(self.lista_tokens[self.look_ahead].nome == "<aritmeticas>"):
                            self.match("<aritmeticas>")
                            if(self.lista_tokens[self.look_ahead].nome == "<numerico>"):
                                self.match("<numerico>")
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
        #<parametros> ::= <declaracao_variavel> , <parametros> | <declaracao_variavel> | ε
        if(token_.nome == "<tipo>"):
            self.match("<tipo>")
            self.match("<variavel>")
            if(self.lista_tokens[self.look_ahead].nome == "<virgula>"):
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
        if verificar_expressao(self.lista_tokens, self.tabela_simbolos, self.look_ahead): ## VERIFICO SE A EXPRESSÃO ESTA CORRETA
            self.match(self.lista_tokens[self.look_ahead].nome) #SE ENTROU NO IF ELE ACEITA QUALQUER COISA QUE VIER
            if(self.lista_tokens[self.look_ahead].nome == "<booleanas>"):
                self.match("<booleanas>")
                if(self.lista_tokens[self.look_ahead].nome == "<variavel>"):
                    self.match("<variavel>")
                elif(self.lista_tokens[self.look_ahead].nome == "<palavraBooleana>"):
                    self.match("<palavraBooleana>")
                else:
                    self.match("<numerico>")
            else:
                self.match("<aritmeticas>")
                if(self.lista_tokens[self.look_ahead].nome == "<variavel>"):
                    self.match("<variavel>")
                elif(self.lista_tokens[self.look_ahead].nome == "<numerico>"):
                    self.match("<numerico>")

                
                if(self.lista_tokens[self.look_ahead].nome == "<booleanas>"):
                    self.match("<booleanas>")
                    if(self.lista_tokens[self.look_ahead].nome == "<variavel>"):
                        self.match("<variavel>")
                    else:
                        self.match("<numerico>")
        else:
            print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(self.lista_tokens[self.look_ahead].linha) + '\033[0m')
            exit()

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
            if(verificar_retorno_variavel(self.lista_tokens, self.tabela_simbolos, self.look_ahead)):
                self.match("<variavel>")
        else:
            self.match("<numerico>")
        self.match("<fim_comando>")
    
    def procedimento(self):
        self.match("<procedimento>")
        self.funcao()
        self.match("<abre_chaves>")
        if(verificar_procedimento(self.lista_tokens, self.tabela_simbolos, self.look_ahead)):
            self.bloco()
        self.match("<fecha_chaves>")
    
