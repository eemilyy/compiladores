class AnalizadorSintatico:
    def __init__(self, lista_tokens):
        self.lista_tokens
        look_ahead = 0

    def start(self):
        pass

    def match(self, terminal):
        if(self.lista_tokens[self.look_ahead].nome == terminal):
            self.look_ahead += 1
        else:
            print("Syntax error line: " + str(self.lista_tokens[self.look_ahead].linha))
#----------------------------------------------------------------------------------------------------
    def programa(self):
        #look_ahead = self.lista_tokens[self.look_ahead] #busca o token que look_ahead esta apontando
        self.match("main")
        self.match("{")
        self.bloco()
        self.match("}")

    
    
    def bloco(self):
        pass