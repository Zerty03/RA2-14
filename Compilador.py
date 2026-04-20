import sys
contador_ciclos = 0

def analisador_lexico(linha_texto):
    ESTADO_INICIAL = 0
    ESTADO_NUMERO_INTEIRO = 1
    ESTADO_NUMERO_DECIMAL = 2
    ESTADO_LETRA = 3 
    ESTADO_IGUAL = 4
    
    estado_atual = ESTADO_INICIAL
    lexema_atual = ""
    tokens = []
    
    linha_limpa = linha_texto.replace("(START)", " START ").replace("(END)", " END ")
    entrada = linha_texto + " "

    i = 0
    while i < len(entrada):
        caracter = entrada[i]
        
        if estado_atual == ESTADO_INICIAL:
            if caracter.isspace():
                i += 1
                continue 
            
            elif caracter.isdigit():
                estado_atual = ESTADO_NUMERO_INTEIRO
                lexema_atual += caracter
                
            elif caracter.isalpha():
                estado_atual = ESTADO_LETRA
                lexema_atual += caracter

            elif caracter == '=':
                estado_atual = ESTADO_IGUAL
                
            elif caracter in "+-*/%^()|<>":
                tokens.append(("OPERADOR", caracter))
                
            else:
                raise ValueError(f"Caractere inválido '{caracter}' na coluna {i+1}")

        elif estado_atual == ESTADO_IGUAL:
            if caracter == '=':
                tokens.append(("OPERADOR", "=="))
            else:
                raise ValueError("Erro léxico: Esperado '=' após '='. O operador de igualdade é '=='.")
            estado_atual = ESTADO_INICIAL
            continue

        elif estado_atual == ESTADO_NUMERO_INTEIRO:
            if caracter.isdigit():
                lexema_atual += caracter
                
            elif caracter == '.':
                estado_atual = ESTADO_NUMERO_DECIMAL
                lexema_atual += caracter
                
            else:
                tokens.append(("NUMERO", float(lexema_atual)))
                lexema_atual = ""
                estado_atual = ESTADO_INICIAL 
                i -= 1

        elif estado_atual == ESTADO_NUMERO_DECIMAL:
            if caracter.isdigit():
                lexema_atual += caracter
            else:
                tokens.append(("NUMERO", float(lexema_atual)))
                lexema_atual = ""
                estado_atual = ESTADO_INICIAL
                i -= 1
                    
        elif estado_atual == ESTADO_LETRA:
            if caracter.isalpha():
                lexema_atual += caracter
            else:
                # força letras serem maiusculas
                palavra = lexema_atual.upper()

                # classifica a palavra lida no seu grupo correto
                if palavra == "START":
                    tokens.append(("START", "START"))
                elif palavra == "END":
                    tokens.append(("END", "END"))
                elif palavra in ["NEM", "RES", "IF", "WHILE"]:
                    tokens.append(("COMANDO", palavra))
                else:
                    tokens.append(("VARIAVEL", palavra))

                lexema_atual = ""
                estado_atual = ESTADO_INICIAL
                i -= 1
                
        i += 1

    return tokens

# Classes da arvore sintática (AST)
class NoAST:
    #Clase base para todos os nós da árvore herdam deste
    pass

# nó raiz
class NoPrograma(NoAST):
    def __init__(self):
        # Lista para guardar todos os blocos do programa entre o START e o END
        self.comandos = []

class NoBloco(NoAST):
    def __init__(self):
        # Lista para guardar todos os Números, Variaveis, Operadores ou outros Blocos, tudo que estiver entre ()
        self.itens = []

# Decisão IF
class NoIf(NoAST):
    def __init__(self, condicao, bloco_verdadeiro):
        # guarda os teste (confição) e o bloco que vai rodar se for TRUE
        self.condicao = condicao
        self.bloco_verdadeiro = bloco_verdadeiro

# Repetição While
class NoWhile(NoAST):
    def __init__(self, condicao, bloco_loop):
        # Guarda o teste e o bloco que vai ficar repetindo
        self.condicao = condicao
        self.bloco_loop = bloco_loop

#Terminal
class NoNumero(NoAST):
    def __init__(self, valor):
        #guarda um número (float), vai virar instrução de carga(vldr)
        self.valor = valor

#Memória
class NoVariavel(NoAST):
    def __init__(self, nome):
        #Guarda o nome de uma variavel inventada pelo usuario
        self.nome = nome

#ação
class NoOperador(NoAST):
    def __init__(self, simbolo):
        # Guarda operadores matemáticos ou lógicos
        self.simbolo = simbolo

#Temporario
class NoComando(NoAST):
    def __init__(self, nome):
        #Ajuda a identificar as palavras IF e WHILE
        self.nome = nome

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 #aponta para o token atual

    def token_atual(self):
        # Retorna o token atual ou um marcador de fim de arquivo
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")
    
    def avancar(self):
        #avançar proximo token
        self.pos += 1

    def erro(self, esperado):
        #leanta um erro sintático e para a compilação
        tipo, valor = self.token_atual()
        raise SyntaxError(f"Erro Sintatico: Esperado '{esperado}', mas encontrou '{valor}' na posição {self.pos + 1} ")
    
    def match(self, tipo_esperado, valor_esperado = None):
        #verifica se o token atual é o esperado
        tipo, valor = self.token_atual()
        if tipo == tipo_esperado and (valor_esperado is None or valor == valor_esperado):
            self.avancar()
            return valor
        self.erro(valor_esperado if valor_esperado else tipo_esperado)

    #regra 1: S -> START C END
    def parse_programa(self):
        no_prog = NoPrograma()
        self.match("START", "START")
        no_prog.comandos = self.parse_comandos()
        self.match("END", "END")
        return no_prog
    
    #Regra 2: C -> B C | ε
    def parse_comandos(self):
        comandos = []
        tipo, valor = self.token_atual()
        #Quando encontrar um '(' sabemos que vem um bloco novo
        while tipo == "OPERADOR" and valor == "(":
            comandos.append(self.parse_bloco())
            tipo, valor = self.token_atual()
        return comandos
    
    #Regra 3: B -> ( O )
    def parse_bloco(self):
        self.match("OPERADOR", "(")
        itens = self.parse_conteudo() #Le tudo o que está dentro
        self.match("OPERADOR", ")")

        if len(itens) >= 3 and isinstance(itens[-1],NoComando):
            comando_nome = itens[-1].nome

            if comando_nome == "IF":
                bloco_verdadeiro = itens[-2]
                condicao = itens[-3]
                return NoIf(condicao, bloco_verdadeiro)
            
            elif comando_nome == "WHILE":
                bloco_loop = itens[-2]
                condicao = itens[-3]
                return NoWhile(condicao, bloco_loop)

        # Se não for IF nem WHILE é um bloco matemático normal    
        no_bloco = NoBloco()
        no_bloco.itens = itens
        return no_bloco
    
    #Regra 4 e 5: O -> I O | ε e I -> num | var | op | cmd | B
    def parse_conteudo(self):
        itens = []
        tipo, valor = self.token_atual()

        # Enquanto não encontrar o ), continua a ler os itens
        while tipo != "EOF" and not (tipo == "OPERADOR" and valor == ")"):
            if tipo == "OPERADOR" and valor == "(":
                #Encontrou um ( então é um subbloco
                itens.append(self.parse_bloco())
            elif tipo == "NUMERO":
                itens.append(NoNumero(valor))
                self.avancar()
            elif tipo == "VARIAVEL":
                itens.append(NoVariavel(valor))
                self.avancar()
            elif tipo == "OPERADOR":
                itens.append(NoOperador(valor))
                self.avancar()
            elif tipo == "COMANDO":
                itens.append(NoComando(valor))
                self.avancar()
            else:
                self.erro("Item válido (Número, Variável, Operador ou Bloco)")
            
            tipo, valor = self.token_atual()
        return itens
    
    def analisador_sintatico(tokens):
        parser = Parser(tokens)
        return parser.parse_programa()

class GeradorAssembly:
    def __init__(self, arvore):
        self.arvore = arvore
        self.codigo = []
        self.variaveis = set()
        self.numeros_memoria = []
        self.contador_labels = 0

    def gerar_label(self, prefixo):
        self.contador_labels += 1
        return f"{prefixo}_{self.contador_labels}"
    
    def add_inst(self, instrucao):
        self.codigo.append("    " + instrucao)

    def registrar_numero(self, valor):
        id_num = len(self.numeros_memoria) + 1
        self.numeros_memoria.append((id_num, valor))
        return id_num
    
    def compilar(self, nome_arquivo):
        # Cabeçalho arquivo assembly
        self.codigo.append(".global _start")
        self.codigo.append(".text")
        self.codigo.append("_start:\n")

        # inicia a travesia na arvore sintatica (raiz)
        self.visitar_programa(self.arvore)

        #fim execução
        self.codigo.append("\n_fim:")
        self.codigo.append("    b _fim\n")

        # Seção de Memória RAM
        self.codigo.append(".data")
        for id_num, val in self.numeros_memoria:
            self.codigo.append(f"num_{id_num}: .double {val}")

        # Constantes para IF e WHILE
        self.codigo.append("const_1: .double 1.0")
        self.codigo.append("const_0: .double 0.0")

        # Cria um espaço dinâmico na RAM para cada variável inventada pelo usuário!
        for var in self.variaveis:
            self.codigo.append(f"var_{var}: .space 8") # 8 bytes = 64 bits para FPU

        # Salva tudo no disco
        with open(nome_arquivo, "w") as f:
            f.write("\n".join(self.codigo))

        

def salvar_tokens(lista_tokens, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for tipo, valor in lista_tokens:
            f.write(f"<{tipo}, {valor}>\n")

def main():
    if len(sys.argv) < 2:
        print("Uso correto: python Compilador.py <arquivo_de_teste.txt>")
        return
    
    nome_arquivo_entrada = sys.argv[1]

    nome_arquivo_assembly = "saida_assembly.s"
    nome_arquivo_tokens = "tokens_gerados.txt"
    todos_tokens = []

    try:
        print(f"Lendo o arquivo: {nome_arquivo_entrada} ...")

        with open(nome_arquivo_entrada, 'r') as arquivo:
            linhas = arquivo.readlines()

            numero_linha = 1
            for linha in linhas:
                try:
                    tokens_da_linha = analisador_lexico(linha)
                    todos_tokens.extend(tokens_da_linha)
                except ValueError as erro:
                    print(f"\n Erro de compilação")
                    print(f"Erro Lexico na linha {numero_linha}: {erro}")
                    sys.exit(1)

                numero_linha += 1

        salvar_tokens(todos_tokens, nome_arquivo_tokens)
        print(f"Sucesso! Arquivo de tokens gerado: {nome_arquivo_tokens}")

        gerar_assembly(todos_tokens, nome_arquivo_assembly)
        print(f"Sucesso! Arquivo Assembly gerado: {nome_arquivo_assembly}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo_entrada}' não foi encontrado na pasta atual")

if __name__ == "__main__":
    main()