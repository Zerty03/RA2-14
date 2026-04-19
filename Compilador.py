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

def gerar_assembly(lista_tokens, nome_arquivo_saida):

    global contador_ciclos

    memoria_numeros = []

    with open(nome_arquivo_saida, 'w') as f:
        f.write(".global _start\n")
        f.write(".text\n")
        f.write("_start:\n\n")

        for tipo, valor in lista_tokens:
            if tipo == "NUMERO":
                id_num = len(memoria_numeros) + 1
                memoria_numeros.append((id_num, valor))

                f.write(f" // - Numero: {valor} - \n")
                f.write(f" ldr r0, =num_{id_num} \n")
                f.write(f" vldr d0, [r0] \n")
                f.write(" vpush {d0} \n\n")
            
            elif tipo == "OPERADOR" and valor not in ['(', ')']:
                f.write(f" // - Operador: {valor} - \n")
                f.write(" vpop {d0} \n")
                f.write(" vpop {d1} \n")

                if valor == '+':
                    f.write(" vadd.f64 d2, d1, d0 \n")
                elif valor == '-':
                    f.write(" vsub.f64 d2, d1, d0 \n")
                elif valor == '*':
                    f.write(" vmul.f64 d2, d1, d0 \n")
                elif valor == '/':
                    f.write(" vdiv.f64 d2, d1, d0 \n")
                elif valor == '//':
                    f.write(" vdiv.f64 d2, d1, d0 \n")
                    f.write(" vcvt.s32.f64 s0, d2 \n")
                    f.write(" vcvt.f64.s32 d2, s0 \n")
                elif valor == '%':
                    f.write(" vdiv.f64 d2, d1, d0 \n")
                    f.write(" vcvt.s32.f64 s0, d2 \n")
                    f.write(" vcvt.f64.s32 d2, s0 \n")
                    f.write(" vmul.f64 d2, d2, d0 \n")
                    f.write(" vsub.f64 d2, d1, d2 \n")
                elif valor == '^':
                    contador_ciclos += 1
                    id_ciclo = contador_ciclos
                    f.write(" vcvt.s32.f64 s0, d0 \n")
                    f.write(" vmov r2, s0 \n")

                    id_num_const = len(memoria_numeros) + 1
                    memoria_numeros.append((id_num_const, 1.0))
                    f.write(f" ldr r0, =num_{id_num_const} \n")
                    f.write("  vldr d2, [r0] \n")

                    f.write(f"\nciclo_potencia_{id_ciclo}:\n")
                    f.write(" cmp r2, #0 \n")
                    f.write(f" ble fim_potencia_{id_ciclo} \n")
                    f.write(" vmul.f64 d2, d2, d1 \n")
                    f.write(" sub r2, r2, #1 \n")
                    f.write(f" b ciclo_potencia_{id_ciclo} \n")
                    f.write(f"\nfim_potencia_{id_ciclo}:\n")

                    f.write(" vpush {d2} \n\n")

            elif tipo == "COMANDO":
                f.write(f" // - Comando: {valor} - \n")
                if valor == "MEM":
                    f.write(" ldr r0, =variavel_mem  \n")
                    f.write(" vldr d0, [r0] \n")
                    f.write(" vpush {d0} \n\n")
                elif valor == "RES":
                    f.write(" vpop {d0} \n")
                    f.write(" vcvt.s32.f64 s0, d0 \n")
                    f.write(" vmov r1, s0 \n")
                    f.write(" mov r2, #8 \n")
                    f.write(" mul r1, r1, r2 \n")
                    f.write(" ldr r0, =historico_res \n")
                    f.write(" ldr r3, =ponteiro_res  \n")
                    f.write(" ldr r3, [r3] \n")
                    f.write(" mul r3, r3, r2 \n")
                    f.write(" add r0, r0, r3 \n")
                    f.write(" sub r0, r0, r1 \n")
                    f.write(" vldr d2, [r0] \n")
                    f.write(" vpush {d2} \n\n")

        f.write("\n_fim:\n")
        f.write(" b _fim \n")

        f.write("\n.data\n")

        for id_num, val in memoria_numeros:
            f.write(f"num_{id_num}: .double {val}\n")

        f.write("\nvariavel_mem: .space 8 \n")
        f.write("historico_res: .space 800 \n")
        f.write("ponteiro_res: .word 0 \n")

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