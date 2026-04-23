import sys
import json
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
                estado_atual = ESTADO_INICIAL
            else:
                raise ValueError("Erro léxico: Esperado '=' após '='. O operador de igualdade é '=='.")

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
            if caracter.isalpha() or caracter == '_':
                lexema_atual += caracter
            else:
                # força letras serem maiusculas
                palavra = lexema_atual.upper()

                # classifica a palavra lida no seu grupo correto
                if palavra == "START":
                    tokens.append(("START", "START"))
                elif palavra == "END":
                    tokens.append(("END", "END"))
                elif palavra in ["MEM", "RES", "IF", "WHILE"]:
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
        self.numeros_memoria = [] #Guarda variáveis únicas para criar espaço na RAM depois
        self.contador_labels = 0 # Guarda os números fixos para colocar na RAM

    def gerar_label(self, prefixo):
        # Cria nomes únicos para os pulos no codigo
        self.contador_labels += 1
        return f"{prefixo}_{self.contador_labels}"
    
    def add_inst(self, instrucao):
        # Apenas formata o código Assembly com recuo para ficar legivel
        self.codigo.append("    " + instrucao)

    def registrar_numero(self, valor):
        # Associa cada número a um ID único para ser criado na seção .data
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

        #Cria as variáveis estáticas para os números que apareceram no código
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


    # Navegadores da Arvore Sintática
    def visitar_programa(self, no_prog):
        for cmd in no_prog.comandos:
            self.visitar_no(cmd, profundidade_pilha=0)

    def visitar_no(self, no, profundidade_pilha=0):
        if isinstance(no, NoBloco):
            prof = profundidade_pilha
            for item in no.itens:
                prof = self.visitar_item(item, prof)

        elif isinstance(no, NoIf):
            lbl_fim = self.gerar_label("fim_if")

            self.add_inst("\n// INICIO IF (Avaliando Condicao) \n")
            self.visitar_no(no.condicao, profundidade_pilha)

            self.add_inst("vpop {d0}") # Pega o resultado (1.0 ou 0.0)
            self.add_inst("ldr r0, =const_0")
            self.add_inst("vldr d1, [r0]")
            self.add_inst("vcmp.f64 d0, d1") # Compara com 0.0 (Falso)
            self.add_inst("vmrs APSR_nzcv, fpscr")
            self.add_inst(f"beq {lbl_fim} // Se for Falso, pula o bloco inteiro!")

            self.add_inst("\n// BLOCO VERDADEIRO \n")
            self.visitar_no(no.bloco_verdadeiro, profundidade_pilha)
            self.codigo.append(f"{lbl_fim}:")

        elif isinstance(no, NoWhile):
            lbl_inicio = self.gerar_label("inicio_while")
            lbl_fim = self.gerar_label("fim_while")

            self.codigo.append(f"\n{lbl_inicio}:")
            self.add_inst("\n// INICIO WHILE (Avaliando Condicao) \n")
            self.visitar_no(no.condicao, profundidade_pilha)

            # Mesma logica do IF, avalia se o resultado da condição é 0.0
            self.add_inst("vpop {d0}")
            self.add_inst("ldr r0, =const_0")
            self.add_inst("vldr d1, [r0]")
            self.add_inst("vcmp.f64 d0, d1")
            self.add_inst("vmrs APSR_nzcv, fpscr")
            self.add_inst(f"beq {lbl_fim} // Se Falso, Quebra o Loop!")

            self.add_inst("\n// BLOCO WHILE \n")
            self.visitar_no(no.bloco_loop, profundidade_pilha)
            self.add_inst(f"b {lbl_inicio} // Volta lá para cima!")
            self.codigo.append(f"{lbl_fim}:")

    def visitar_item(self, item, prof):
        if isinstance(item, NoNumero):
            # Busca numero na memória RAM usando um ponteiro (r0) e empilha na FPU
            id_num = self.registrar_numero(item.valor)
            self.add_inst(f"ldr r0, =num_{id_num}")
            self.add_inst("vldr d0, [r0]")
            self.add_inst("vpush {d0}")
            return prof + 1

        elif isinstance(item, NoVariavel):
            self.variaveis.add(item.nome)
            # Se a pilha tem algo, é uma ATRIBUIÇÃO. Se está vazia, é uma LEITURA.
            if prof > 0:
                self.add_inst(f"// Guardando valor na variavel {item.nome}")
                self.add_inst("vpop {d0}")
                self.add_inst(f"ldr r0, =var_{item.nome}")
                self.add_inst("vstr d0, [r0]")
                return prof - 1
            else:
                self.add_inst(f"// Lendo valor da variavel {item.nome}")
                self.add_inst(f"ldr r0, =var_{item.nome}")
                self.add_inst("vldr d0, [r0]") # Load: Memória -> Registrador
                self.add_inst("vpush {d0}")
                return prof + 1

        elif isinstance(item, NoOperador):
            self.add_inst(f"// Operador {item.simbolo}")
            self.add_inst("vpop {d0} // Operando B")
            self.add_inst("vpop {d1} // Operando A")

            # operações matematicas
            if item.simbolo == '+': self.add_inst("vadd.f64 d2, d1, d0")
            elif item.simbolo == '-': self.add_inst("vsub.f64 d2, d1, d0")
            elif item.simbolo == '*': self.add_inst("vmul.f64 d2, d1, d0")
            elif item.simbolo == '|': self.add_inst("vdiv.f64 d2, d1, d0") # Div Real
            elif item.simbolo == '/': # Div Inteira 
                # divisão inteira ele arranca as casa decimais e volta para float
                self.add_inst("vdiv.f64 d2, d1, d0")
                self.add_inst("vcvt.s32.f64 s0, d2")
                self.add_inst("vcvt.f64.s32 d2, s0")

            # Operações Lógicas
            elif item.simbolo in ['<', '>', '==']:
                self.add_inst("vcmp.f64 d1, d0")
                self.add_inst("vmrs APSR_nzcv, fpscr")
                lbl_true = self.gerar_label("op_true")
                lbl_end = self.gerar_label("op_end")

                #Compara e pula de acordo com a condição
                if item.simbolo == '<': self.add_inst(f"blt {lbl_true}")
                elif item.simbolo == '>': self.add_inst(f"bgt {lbl_true}")
                elif item.simbolo == '==': self.add_inst(f"beq {lbl_true}")

                # Se for falso, empilha 0.0
                self.add_inst("ldr r0, =const_0")
                self.add_inst("vldr d2, [r0]")
                self.add_inst(f"b {lbl_end}")
                self.codigo.append(f"{lbl_true}:")
                # Se for verdadeiro, empilha 1.0
                self.add_inst("ldr r0, =const_1")
                self.add_inst("vldr d2, [r0]")
                self.codigo.append(f"{lbl_end}:")

            self.add_inst("vpush {d2}") # Empilha o resultado final de volta
            return prof - 1 

        return prof

def salvar_tokens(lista_tokens, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for tipo, valor in lista_tokens:
            f.write(f"<{tipo}, {valor}>\n")

def ast_para_dict(no):
    #Converte os objetos Python da AST em um Dicionário padrão.
    if isinstance(no, NoPrograma):
        return {
            "tipo": "ProgramaRaiz",
            "comandos": [ast_para_dict(cmd) for cmd in no.comandos]
        }
    elif isinstance(no, NoBloco):
        return {
            "tipo": "Bloco",
            "itens": [ast_para_dict(item) for item in no.itens]
        }
    elif isinstance(no, NoIf):
        return {
            "tipo": "DecisaoIF",
            "condicao": ast_para_dict(no.condicao),
            "bloco_verdadeiro": ast_para_dict(no.bloco_verdadeiro)
        }
    elif isinstance(no, NoWhile):
        return {
            "tipo": "LacoWHILE",
            "condicao": ast_para_dict(no.condicao),
            "bloco_loop": ast_para_dict(no.bloco_loop)
        }
    elif isinstance(no, NoNumero):
        return {"tipo": "Numero", "valor": no.valor}
    elif isinstance(no, NoVariavel):
        return {"tipo": "Variavel", "nome": no.nome}
    elif isinstance(no, NoOperador):
        return {"tipo": "Operador", "simbolo": no.simbolo}
    elif isinstance(no, NoComando):
        return {"tipo": "Comando", "nome": no.nome}
    else:
        return {"tipo": "Desconhecido"}

def salvar_ast_json(arvore, nome_arquivo="arvore.json"):
    #Salva o dicionário gerado em um arquivo .json perfeitamente formatado.
    dicionario_ast = ast_para_dict(arvore)
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        # Formata o arquivo para uma melhor visualização
        json.dump(dicionario_ast, f, indent=4, ensure_ascii=False)

def salvar_arvore_markdown(no_raiz, nome_arquivo="arvore.md"):
    """Gera a árvore em formato de texto e salva em um arquivo Markdown."""
    linhas_md = ["# Representação da Árvore Sintática (AST)\n", "```text"]

    def varrer_arvore(no, nivel=0):
        espaco = "    " * nivel
        if isinstance(no, NoPrograma):
            linhas_md.append(f"{espaco}└── [S] Programa Raiz")
            for cmd in no.comandos: varrer_arvore(cmd, nivel + 1)
                
        elif isinstance(no, NoBloco):
            linhas_md.append(f"{espaco}├── [B] Bloco de Comandos")
            for item in no.itens: varrer_arvore(item, nivel + 1)
                
        elif isinstance(no, NoIf):
            linhas_md.append(f"{espaco}├── [IF] Estrutura de Decisão")
            linhas_md.append(f"{espaco}│   ├── Condição:")
            varrer_arvore(no.condicao, nivel + 2)
            linhas_md.append(f"{espaco}│   └── Bloco Verdadeiro:")
            varrer_arvore(no.bloco_verdadeiro, nivel + 2)
            
        elif isinstance(no, NoWhile):
            linhas_md.append(f"{espaco}├── [WHILE] Laço de Repetição")
            linhas_md.append(f"{espaco}│   ├── Condição:")
            varrer_arvore(no.condicao, nivel + 2)
            linhas_md.append(f"{espaco}│   └── Bloco do Laço:")
            varrer_arvore(no.bloco_loop, nivel + 2)
            
        elif isinstance(no, NoNumero):
            linhas_md.append(f"{espaco}└── (num) Número: {no.valor}")
        elif isinstance(no, NoVariavel):
            linhas_md.append(f"{espaco}└── (var) Variável: {no.nome}")
        elif isinstance(no, NoOperador):
            linhas_md.append(f"{espaco}└── (op) Operador: {no.simbolo}")

    varrer_arvore(no_raiz)
    linhas_md.append("```\n")

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_md))

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

        try:
            print("Iniciando a Analise Sintatica...")
            arvore_ast = analisador_sintatico(todos_tokens)
            print("Sucesso! Arvore Sintatica (AST) gerada sem erros.")

            salvar_ast_json(arvore_ast, "arvore_sintatica.json")
            salvar_arvore_markdown(arvore_ast, "arvore.md") 
            print("Arquivos da arvore salvos: 'arvore.json' e 'arvore.md'")
    
            gerador = GeradorAssembly(arvore_ast)
            gerador.compilar(nome_arquivo_assembly)
            print(f"Sucesso Total! Arquivo Assembly da Fase 2 gerado: {nome_arquivo_assembly}")
    
        except SyntaxError as erro:
            print(f"\n Erro de Compilacao Sintatica:")
            print(erro)
            sys.exit(1)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo_entrada}' não foi encontrado na pasta atual")

if __name__ == "__main__":
    main()