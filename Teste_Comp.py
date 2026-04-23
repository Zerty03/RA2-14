import pytest
from Compilador import (
    analisador_lexico,
    lerTokens,
    construirGramatica,
    analisador_sintatico,
    gerarArvore,
    NoPrograma,
    NoBloco,
    NoIf,
    NoWhile,
    NoMem,
    NoRes,
    NoNumero,
    NoVariavel,
    NoOperador,
)
 
# ===========================================================================
# Helpers
# ===========================================================================
 
def tokenizar(codigo):
    """Tokeniza uma string de código linha por linha e retorna o vetor de tokens."""
    todos = []
    for linha in codigo.strip().splitlines():
        todos.extend(analisador_lexico(linha))
    return todos
 
 
def parsear(codigo):
    """Tokeniza e faz o parse de uma string de código, retornando a AST raiz."""
    tokens = tokenizar(codigo)
    tabela = construirGramatica()['tabela_ll1']
    return analisador_sintatico(tokens, tabela)
 
 
# ===========================================================================
# 1. Erros léxicos
# ===========================================================================
 
class TestErrosLexicos:
 
    def test_caractere_arroba_invalido(self):
        """@ não é um caractere válido da linguagem."""
        with pytest.raises(ValueError, match="Caractere inválido"):
            analisador_lexico("(5.0 @ 3.0 +)")
 
    def test_caractere_hash_invalido(self):
        """# não é um caractere válido da linguagem."""
        with pytest.raises(ValueError, match="Caractere inválido"):
            analisador_lexico("(# 2.0 +)")
 
    def test_operador_igual_simples_invalido(self):
        """= sozinho não é válido — o operador de igualdade é ==."""
        with pytest.raises(ValueError, match="operador de igualdade"):
            analisador_lexico("(A B =)")
 
    def test_numero_inteiro_reconhecido(self):
        tokens = analisador_lexico("(42 3 +)")
        valores = [v for _, v in tokens]
        assert 42.0 in valores
 
    def test_numero_real_reconhecido(self):
        tokens = analisador_lexico("(3.14 2.0 *)")
        valores = [v for _, v in tokens]
        assert 3.14 in valores
 
    def test_operador_igual_duplo_valido(self):
        """== deve ser reconhecido como operador válido."""
        tokens = analisador_lexico("(A B ==)")
        tipos = [t for t, _ in tokens]
        assert "OPERADOR" in tipos
 
    def test_variavel_maiuscula_reconhecida(self):
        tokens = analisador_lexico("(CONTADOR)")
        assert ("VARIAVEL", "CONTADOR") in tokens
 
    def test_variavel_minuscula_convertida_para_maiuscula(self):
        """Variáveis minúsculas devem ser convertidas para maiúsculas."""
        tokens = analisador_lexico("(valor)")
        assert ("VARIAVEL", "VALOR") in tokens
 
 
# ===========================================================================
# 2. Expressões válidas simples
# ===========================================================================
 
class TestExpressoesSimples:
 
    def test_adicao(self):
        ast = parsear("(START)\n(3.0 2.0 +)\n(END)")
        assert isinstance(ast, NoPrograma)
        assert len(ast.comandos) == 1
        bloco = ast.comandos[0]
        assert isinstance(bloco, NoBloco)
        assert any(isinstance(i, NoOperador) and i.simbolo == '+' for i in bloco.itens)
 
    def test_subtracao(self):
        ast = parsear("(START)\n(10.0 4.0 -)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoOperador) and i.simbolo == '-' for i in bloco.itens)
 
    def test_multiplicacao(self):
        ast = parsear("(START)\n(3.0 2.0 *)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoOperador) and i.simbolo == '*' for i in bloco.itens)
 
    def test_divisao_real(self):
        ast = parsear("(START)\n(9.0 2.0 |)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoOperador) and i.simbolo == '|' for i in bloco.itens)
 
    def test_divisao_inteira(self):
        ast = parsear("(START)\n(10 3 /)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoOperador) and i.simbolo == '/' for i in bloco.itens)
 
    def test_resto(self):
        ast = parsear("(START)\n(10 3 %)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoOperador) and i.simbolo == '%' for i in bloco.itens)
 
    def test_potenciacao(self):
        ast = parsear("(START)\n(2.0 8 ^)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoOperador) and i.simbolo == '^' for i in bloco.itens)
 
    def test_multiplos_blocos(self):
        """Programa com várias operações deve gerar um comando por bloco."""
        ast = parsear("(START)\n(1.0 2.0 +)\n(3.0 4.0 -)\n(END)")
        assert len(ast.comandos) == 2
 
    def test_programa_vazio(self):
        """Programa sem nenhum comando entre START e END deve ser aceito."""
        ast = parsear("(START)\n(END)")
        assert isinstance(ast, NoPrograma)
        assert len(ast.comandos) == 0
 
 
# ===========================================================================
# 3. Expressões aninhadas
# ===========================================================================
 
class TestExpressoesAninhadas:
 
    def test_aninhamento_simples(self):
        """(A (C D *) +) — soma A com o produto de C e D."""
        ast = parsear("(START)\n(2.0 (3.0 4.0 *) +)\n(END)")
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoBloco) for i in bloco.itens)
 
    def test_aninhamento_duplo(self):
        """((A B +) (C D *) |) — divisão real de dois subblocos."""
        ast = parsear("(START)\n((2.0 3.0 +) (4.0 5.0 *) |)\n(END)")
        bloco = ast.comandos[0]
        subblocos = [i for i in bloco.itens if isinstance(i, NoBloco)]
        assert len(subblocos) == 2
 
    def test_aninhamento_profundo(self):
        """Três níveis de aninhamento."""
        ast = parsear("(START)\n(((1.0 2.0 +) 3.0 *) 4.0 -)\n(END)")
        assert isinstance(ast, NoPrograma)
        bloco = ast.comandos[0]
        assert any(isinstance(i, NoBloco) for i in bloco.itens)
 
    def test_todas_operacoes_aninhadas(self):
        """Cada operação usada em um subbloco aninhado."""
        codigo = """(START)
((4.0 2.0 +) (3.0 1.0 -) *)
((7 3 %) (2 4 ^) +)
((9.0 3.0 /) (2.0 5.0 *) |)
(END)"""
        ast = parsear(codigo)
        assert len(ast.comandos) == 3
 
 
# ===========================================================================
# 4. Estruturas de controle
# ===========================================================================
 
class TestEstruturasControle:
 
    def test_if_gera_no_correto(self):
        """IF deve gerar um NoIf com condição e bloco verdadeiro."""
        ast = parsear("(START)\n(1.0 2.0 < (3.0 4.0 +) IF)\n(END)")
        no = ast.comandos[0]
        assert isinstance(no, NoIf)
 
    def test_if_tem_condicao(self):
        ast = parsear("(START)\n(1.0 2.0 < (3.0 4.0 +) IF)\n(END)")
        no = ast.comandos[0]
        assert no.condicao is not None
 
    def test_if_tem_bloco_verdadeiro(self):
        ast = parsear("(START)\n(1.0 2.0 < (3.0 4.0 +) IF)\n(END)")
        no = ast.comandos[0]
        assert no.bloco_verdadeiro is not None
 
    def test_while_gera_no_correto(self):
        """WHILE deve gerar um NoWhile com condição e bloco loop."""
        ast = parsear("(START)\n(1.0 5.0 < (1.0 1.0 +) WHILE)\n(END)")
        no = ast.comandos[0]
        assert isinstance(no, NoWhile)
 
    def test_while_tem_condicao(self):
        ast = parsear("(START)\n(1.0 5.0 < (1.0 1.0 +) WHILE)\n(END)")
        no = ast.comandos[0]
        assert no.condicao is not None
 
    def test_while_tem_bloco_loop(self):
        ast = parsear("(START)\n(1.0 5.0 < (1.0 1.0 +) WHILE)\n(END)")
        no = ast.comandos[0]
        assert no.bloco_loop is not None
 
    def test_operadores_relacionais(self):
        """Todos os operadores relacionais devem ser aceitos em condições."""
        for op in ['<', '>', '==']:
            ast = parsear(f"(START)\n(1.0 2.0 {op} (3.0) IF)\n(END)")
            assert isinstance(ast.comandos[0], NoIf)
 
 
# ===========================================================================
# 5. Comandos especiais
# ===========================================================================
 
class TestComandosEspeciais:
 
    def test_mem_armazena_valor(self):
        """(V NOME MEM) deve gerar NoMem com nome e valor corretos."""
        ast = parsear("(START)\n(3.14 PI MEM)\n(END)")
        no = ast.comandos[0]
        assert isinstance(no, NoMem)
        assert no.nome_mem == "PI"
        assert isinstance(no.valor, NoNumero)
 
    def test_mem_leitura_variavel(self):
        """(NOME) deve gerar um bloco com uma variável dentro."""
        ast = parsear("(START)\n(3.14 PI MEM)\n(PI)\n(END)")
        no = ast.comandos[1]
        assert isinstance(no, NoBloco)
        assert isinstance(no.itens[0], NoVariavel)
        assert no.itens[0].nome == "PI"
 
    def test_res_gera_no_correto(self):
        """(N RES) deve gerar NoRes com o índice correto."""
        ast = parsear("(START)\n(2.0 3.0 +)\n(1 RES)\n(END)")
        no = ast.comandos[1]
        assert isinstance(no, NoRes)
        assert no.n == 1
 
    def test_res_indice_zero(self):
        """(0 RES) deve ser aceito — N é inteiro não negativo."""
        ast = parsear("(START)\n(2.0 3.0 +)\n(0 RES)\n(END)")
        no = ast.comandos[1]
        assert isinstance(no, NoRes)
        assert no.n == 0
 
 
# ===========================================================================
# 6. Entradas inválidas (erros sintáticos)
# ===========================================================================
 
class TestErrosSintaticos:
 
    def test_parentese_fechamento_faltando(self):
        """Bloco sem ')' deve lançar SyntaxError."""
        with pytest.raises(SyntaxError):
            parsear("(START)\n(3.0 2.0 +\n(END)")
 
    def test_sem_start(self):
        """Programa sem (START) deve lançar SyntaxError."""
        with pytest.raises(SyntaxError):
            parsear("(3.0 2.0 +)\n(END)")
 
    def test_sem_end(self):
        """Programa sem (END) deve lançar SyntaxError."""
        with pytest.raises(SyntaxError):
            parsear("(START)\n(3.0 2.0 +)")
 
    def test_res_com_variavel_invalido(self):
        """(X RES) onde X não é número deve lançar SyntaxError."""
        with pytest.raises(SyntaxError):
            parsear("(START)\n(X RES)\n(END)")
 
 
# ===========================================================================
# 7. Casos extremos
# ===========================================================================
 
class TestCasosExtremos:
 
    def test_aninhamento_cinco_niveis(self):
        """Cinco níveis de aninhamento devem ser aceitos sem erro."""
        ast = parsear("(START)\n((((1.0 2.0 +) 3.0 *) 4.0 -) 5.0 |)\n(END)")
        assert isinstance(ast, NoPrograma)
 
    def test_muitos_blocos_sequenciais(self):
        """20 blocos sequenciais devem todos ser parseados."""
        linhas = ["(START)"] + ["(1.0 2.0 +)"] * 20 + ["(END)"]
        ast = parsear("\n".join(linhas))
        assert len(ast.comandos) == 20
 
    def test_numero_inteiro_e_real_no_mesmo_bloco(self):
        """Inteiros e reais podem coexistir no mesmo bloco."""
        ast = parsear("(START)\n(3 2.5 +)\n(END)")
        bloco = ast.comandos[0]
        valores = [i.valor for i in bloco.itens if isinstance(i, NoNumero)]
        assert 3.0 in valores
        assert 2.5 in valores
 
    def test_construir_gramatica_retorna_estrutura_completa(self):
        """construirGramatica() deve retornar as 4 chaves obrigatórias."""
        estrutura = construirGramatica()
        assert 'gramatica'  in estrutura
        assert 'first'      in estrutura
        assert 'follow'     in estrutura
        assert 'tabela_ll1' in estrutura
 
    def test_first_nao_terminais_corretos(self):
        """FIRST de cada não-terminal deve conter os terminais esperados."""
        first = construirGramatica()['first']
        assert '(start)' in first['S']
        assert '('        in first['B']
        assert 'num'      in first['I']
        assert 'ε'        in first['C']
 
    def test_follow_nao_terminais_corretos(self):
        """FOLLOW de cada não-terminal deve conter os terminais esperados."""
        follow = construirGramatica()['follow']
        assert '$'      in follow['S']
        assert '(end)'  in follow['C']
        assert ')'      in follow['O']
 
    def test_tabela_ll1_sem_conflitos(self):
        """Cada célula da tabela deve ter no máximo uma produção (sem conflitos)."""
        tabela = construirGramatica()['tabela_ll1']
        for nt, entradas in tabela.items():
            for terminal, producao in entradas.items():
                # Produção deve ser uma lista de símbolos, não uma lista de listas
                assert isinstance(producao, list), \
                    f"Conflito em tabela[{nt}][{terminal}]: mais de uma produção"
                assert not isinstance(producao[0], list), \
                    f"Conflito em tabela[{nt}][{terminal}]: produção aninhada"