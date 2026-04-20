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