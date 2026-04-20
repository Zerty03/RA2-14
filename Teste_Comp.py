import unittest
import os
from Compilador import analisador_lexico, analisador_sintatico, GeradorAssembly

class TestFase2Lexico(unittest.TestCase):
    
    # Testa se o Lexer reconhece as palavras reservadas da Fase 2.
    def test_delimitadores_e_comandos(self):
        tokens = analisador_lexico("START IF WHILE MEM END")
        esperado = [
            ("START", "START"),
            ("COMANDO", "IF"),
            ("COMANDO", "WHILE"),
            ("COMANDO", "MEM"),
            ("END", "END")
        ]
        self.assertEqual(tokens, esperado)

    # Testa se variáveis criadas pelo usuário e novos operadores lógicos são lidos.
    def test_variaveis_e_operadores_novos(self):
        tokens = analisador_lexico("X CONTADOR < > == |")
        esperado = [
            ("VARIAVEL", "X"),
            ("VARIAVEL", "CONTADOR"),
            ("OPERADOR", "<"),
            ("OPERADOR", ">"),
            ("OPERADOR", "=="),
            ("OPERADOR", "|")
        ]
        self.assertEqual(tokens, esperado)

class TestFase2Integracao(unittest.TestCase):
    
    # Prepara um arquivo de teste temporário com START, matemática, variável e END.
    def setUp(self):
        self.arq_in = "temp_teste_fase2.txt"
        self.arq_out = "temp_saida_fase2.s"
        with open(self.arq_in, "w") as f:
            f.write("START\n")
            f.write("( 10.0 5.0 + )\n")
            f.write("( 20.0 MINHAVAR )\n")
            f.write("END\n")

    # Limpa os arquivos temporários após o teste.
    def tearDown(self):
        if os.path.exists(self.arq_in): os.remove(self.arq_in)
        if os.path.exists(self.arq_out): os.remove(self.arq_out)

    # Testa o pipeline completo: Lexer -> Parser (AST) -> Gerador de Assembly.
    def test_compilacao_completa(self):
        # 1. Lexer
        todos_tokens = []
        with open(self.arq_in, 'r') as f:
            for linha in f:
                todos_tokens.extend(analisador_lexico(linha))

        # 2. Parser (Gera a Árvore)
        arvore = analisador_sintatico(todos_tokens)
        self.assertIsNotNone(arvore, "A Árvore Sintática não foi gerada!")

        # 3. Gerador
        gerador = GeradorAssembly(arvore)
        gerador.compilar(self.arq_out)

        # 4. Validação do Arquivo Assembly
        self.assertTrue(os.path.exists(self.arq_out), "O arquivo Assembly não foi criado!")
        with open(self.arq_out, 'r') as f:
            asm = f.read()
        
        # Verifica se gerou soma e se alocou dinamicamente o espaço para a variável inventada
        self.assertIn("vadd.f64", asm)
        self.assertIn("var_MINHAVAR: .space 8", asm)

if __name__ == '__main__':
    unittest.main(verbosity=2)