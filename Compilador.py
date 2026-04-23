# Integrantes do grupo:
# Eugenio Polistchuk Berendsen - Zerty03

# Nome do grupo no Canvas: RA2-14

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
    entrada = linha_limpa + " "

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

#Comando (V MEN): Armazena valor em variável de memória
class NoMem(NoAST):
    def __init__(self, valor, nome_mem):
        # valor = expressão/número a guardar; nome_mem = nome da variável
        self.valor = valor
        self.nome_mem = nome_mem
 
# Comando (N RES): retorna resultado de N linhas atrás
class NoRes(NoAST):
    def __init__(self, n):
        # n = quantas linhas atrás buscar o resultado
        self.n = n

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
            
            elif comando_nome == "MEM":
                if len(itens) >= 3 and isinstance(itens[-2], NoVariavel):
                    nome_mem = itens[-2].nome
                    valor_mem = itens[-3]
                    return NoMem(valor_mem, nome_mem)
                else:
                    raise SyntaxError(f"Erro Sintático: Formato inválido para MEM. Use (valor NOME MEM)")

        # (N RES): dois itens — o número N e o comando RES
        if len(itens) == 2 and isinstance(itens[-1], NoComando) and itens[-1].nome == "RES":
            if isinstance(itens[0], NoNumero):
                return NoRes(int(itens[0].valor))
            else:
                raise SyntaxError("Erro Sintático: RES requer um número inteiro. Use (N RES)")
            
        if len(itens) == 1 and isinstance(itens[0], NoVariavel):
            no_bloco = NoBloco()
            no_bloco.itens = itens
            return no_bloco

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
        self.resultado_linhas = []

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

        # Espaços para armazenar resultados de cada linha (usado pelo RES)
        for label in self.resultado_linhas:
            self.codigo.append(f"{label}: .space 8")
            self.codigo.append(f"var_{var}: .space 8") # 8 bytes = 64 bits para FPU

        # Salva tudo no disco
        with open(nome_arquivo, "w") as f:
            f.write("\n".join(self.codigo))


    # Navegadores da Arvore Sintática
    def visitar_programa(self, no_prog):
        # Cada comando no programa corresponde a uma "linha".
        # Após executar cada bloco, salvamos o topo da pilha FPU em res_N
        # para que (N RES) possa recuperá-lo.
        total = len(no_prog.comandos)
        for idx, cmd in enumerate(no_prog.comandos):
            self.visitar_no(cmd, profundidade_pilha=0)
            # Salva resultado do topo da pilha (se houver) como resultado desta linha
            label_resultado = f"res_linha_{idx + 1}"
            self.resultado_linhas.append(label_resultado)
            self.add_inst(f"// Salvando resultado da linha {idx + 1}")
            self.add_inst("vpop {d0}")
            self.add_inst(f"ldr r0, =res_linha_{idx + 1}")
            self.add_inst("vstr d0, [r0]")

    def visitar_no(self, no, profundidade_pilha=0):
        if isinstance(no, NoBloco):
            prof = profundidade_pilha
            for item in no.itens:
                prof = self.visitar_item(item, prof)

        elif isinstance(no, NoNumero):
            # Número solto tratado como bloco de um item só
            self.visitar_item(no, profundidade_pilha)

        elif isinstance(no, NoVariavel):
            # Variável solta tratada como bloco de um item só
            self.visitar_item(no, profundidade_pilha)

        elif isinstance(no, NoMem):
            # (V NOME MEM): avalia o valor e salva na variável de memória
            self.add_inst(f"\n// COMANDO MEM: Guardando resultado em '{no.nome_mem}'")
            self.variaveis.add(no.nome_mem)
            self.visitar_no(no.valor, profundidade_pilha) # empilha o valor
            self.add_inst("vpop {d0}") # pega da pilha FPU
            self.add_inst(f"ldr r0, =var_{no.nome_mem}")
            self.add_inst("vstr d0, [r0]") # salva na RAM

        elif isinstance(no, NoRes):
            # (N RES): busca o resultado salvo N linhas atrás no histórico
            self.add_inst(f"\n// COMANDO RES: Lendo resultado de {no.n} linha(s) atrás")
            self.add_inst(f"ldr r0, =res_linha_{no.n}")
            self.add_inst("vldr d0, [r0]")
            self.add_inst("vpush {d0}")

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

            # Operações matemáticas
            if item.simbolo == '+':
                self.add_inst("vadd.f64 d2, d1, d0")
            elif item.simbolo == '-':
                self.add_inst("vsub.f64 d2, d1, d0")
            elif item.simbolo == '*':
                self.add_inst("vmul.f64 d2, d1, d0")
            elif item.simbolo == '|':
                # Divisão real
                self.add_inst("vdiv.f64 d2, d1, d0")
            elif item.simbolo == '/':
                # Divisão inteira: divide, trunca para int32 e volta para f64
                self.add_inst("vdiv.f64 d2, d1, d0")
                self.add_inst("vcvt.s32.f64 s4, d2  // Trunca para inteiro")
                self.add_inst("vcvt.f64.s32 d2, s4  // Volta para double")
            elif item.simbolo == '%':
                # Resto da divisão inteira: A % B = A - (int(A/B) * B)
                self.add_inst("// Resto: A mod B = A - trunc(A/B)*B")
                self.add_inst("vdiv.f64 d2, d1, d0          // d2 = A / B")
                self.add_inst("vcvt.s32.f64 s4, d2           // Trunca para int")
                self.add_inst("vcvt.f64.s32 d2, s4           // Volta para double")
                self.add_inst("vmul.f64 d2, d2, d0           // d2 = trunc(A/B) * B")
                self.add_inst("vsub.f64 d2, d1, d2           // d2 = A - resultado")
            elif item.simbolo == '^':
                # Potenciação: implementada como loop de multiplicações
                # Converte o expoente (B) para inteiro no registrador r1
                lbl_loop  = self.gerar_label("pow_loop")
                lbl_fim_p = self.gerar_label("pow_fim")
                self.add_inst("// Potenciação A^B via loop")
                self.add_inst("vcvt.s32.f64 s4, d0     // B inteiro em s4")
                self.add_inst("vmov r1, s4              // r1 = B (contador)")
                self.add_inst("vmov.f64 d2, d1         // d2 = A (acumulador)")
                self.add_inst("subs r1, r1, #1         // já contamos 1 multiplicação")
                self.add_inst(f"ble {lbl_fim_p}        // se B<=1, resultado já é A")
                self.codigo.append(f"    {lbl_loop}:")
                self.add_inst("vmul.f64 d2, d2, d1    // d2 = d2 * A")
                self.add_inst("subs r1, r1, #1")
                self.add_inst(f"bgt {lbl_loop}")
                self.codigo.append(f"    {lbl_fim_p}:")

            # Operações Lógicas
            elif item.simbolo in ['<', '>', '==']:
                self.add_inst("vcmp.f64 d1, d0")
                self.add_inst("vmrs APSR_nzcv, fpscr")
                lbl_true = self.gerar_label("op_true")
                lbl_end  = self.gerar_label("op_end")

                if item.simbolo == '<':  self.add_inst(f"blt {lbl_true}")
                elif item.simbolo == '>': self.add_inst(f"bgt {lbl_true}")
                elif item.simbolo == '==': self.add_inst(f"beq {lbl_true}")

                # Falso → empilha 0.0
                self.add_inst("ldr r0, =const_0")
                self.add_inst("vldr d2, [r0]")
                self.add_inst(f"b {lbl_end}")
                self.codigo.append(f"{lbl_true}:")
                # Verdadeiro → empilha 1.0
                self.add_inst("ldr r0, =const_1")
                self.add_inst("vldr d2, [r0]")
                self.codigo.append(f"{lbl_end}:")

            self.add_inst("vpush {d2} // Empilha resultado")
            return prof - 1

        return prof

def arvore_para_dict(no):
    # Converte recursivamente qualquer nó da AST em um dicionário
    # serializável para JSON. Cada nó recebe um campo 'tipo' para
    # identificação, mais os campos específicos de cada classe.
    if no is None:
        return None
 
    if isinstance(no, NoPrograma):
        return {
            "tipo": "Programa",
            "comandos": [arvore_para_dict(c) for c in no.comandos]
        }
 
    if isinstance(no, NoBloco):
        return {
            "tipo": "Bloco",
            "itens": [arvore_para_dict(i) for i in no.itens]
        }
 
    if isinstance(no, NoIf):
        return {
            "tipo": "If",
            "condicao": arvore_para_dict(no.condicao),
            "bloco_verdadeiro": arvore_para_dict(no.bloco_verdadeiro)
        }
 
    if isinstance(no, NoWhile):
        return {
            "tipo": "While",
            "condicao": arvore_para_dict(no.condicao),
            "bloco_loop": arvore_para_dict(no.bloco_loop)
        }
 
    if isinstance(no, NoMem):
        return {
            "tipo": "Mem",
            "nome_mem": no.nome_mem,
            "valor": arvore_para_dict(no.valor)
        }
 
    if isinstance(no, NoRes):
        return {
            "tipo": "Res",
            "n": no.n
        }
 
    if isinstance(no, NoNumero):
        return {
            "tipo": "Numero",
            "valor": no.valor
        }
 
    if isinstance(no, NoVariavel):
        return {
            "tipo": "Variavel",
            "nome": no.nome
        }
 
    if isinstance(no, NoOperador):
        return {
            "tipo": "Operador",
            "simbolo": no.simbolo
        }
 
    if isinstance(no, NoComando):
        return {
            "tipo": "Comando",
            "nome": no.nome
        }
 
    # Fallback para nós desconhecidos
    return {"tipo": "Desconhecido", "repr": str(no)}
 
 
def salvar_arvore_json(arvore, nome_arquivo):
    # Serializa a AST para JSON e salva no arquivo especificado.
    dicionario = arvore_para_dict(arvore)
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dicionario, f, indent=2, ensure_ascii=False)

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
    nome_arquivo_ast = "arvore_sintatica.json"
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

            salvar_arvore_json(arvore_ast, nome_arquivo_ast)
            print(f"Sucesso! Arvore Sintatica salva em: {nome_arquivo_ast}")
    
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