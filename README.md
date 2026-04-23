# Analisador Sintático LL(1)
 
**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
**Disciplina:** Linguagens Formais e Autômatos
**Professor:** Frank de Alcantara
**Ano:** 2026
 
---
 
## Integrantes
 
* **Eugênio Polistchuk Berendsen** - [@Zerty03](https://github.com/Zerty03)
**Grupo no Canvas:** RA1-14
 
---
 
## Descrição do Projeto
 
Este projeto implementa um compilador completo para uma linguagem de programação simplificada baseada em **Notação Polonesa Reversa (RPN)**. O compilador é dividido em duas fases:
 
- **Fase 1:** Analisador Léxico (Autômato Finito Determinístico)
- **Fase 2:** Analisador Sintático LL(1) com geração de código Assembly ARMv7
---
 
## Como Funciona (Resumo Técnico)
 
### 1. Analisador Léxico
Implementado na função `analisador_lexico()`, lê a entrada caractere por caractere transitando entre estados (`ESTADO_NUMERO_INTEIRO`, `ESTADO_NUMERO_DECIMAL`, `ESTADO_LETRA`, `ESTADO_IGUAL`) para classificar os tokens sem uso de Regex.
 
### 2. Analisador Sintático LL(1)
Implementado como um **parser descendente recursivo** guiado pela tabela LL(1) construída por `construirGramatica()`. A gramática possui 5 não-terminais (S, C, B, O, I) e valida expressões RPN, comandos especiais e estruturas de controle.
 
### 3. Árvore Sintática (AST)
Gerada pelo parser e salva em dois formatos pela função `gerarArvore()`:
- `arvore_sintatica.json` — estrutura para uso nas próximas fases
- `arvore_sintatica.md` — representação visual para documentação
### 4. Gerador de Assembly ARMv7
A função `gerarAssembly()` percorre a AST e gera código para o ambiente **Cpulator-ARMv7 DEC1-SOC (v16.1)** usando a pilha da FPU:
- **Números:** declarados na seção `.data`, carregados com `vldr` e empilhados com `vpush`
- **Operadores:** desempilha dois operandos com `vpop`, opera com instruções `vadd.f64`, `vsub.f64`, `vmul.f64`, `vdiv.f64` e empilha o resultado
- **Potenciação (`^`):** laço de multiplicações com labels únicos gerados dinamicamente
- **IF/WHILE:** comparação via `vcmp.f64` + `vmrs APSR_nzcv, fpscr` + salto condicional (`beq`, `blt`, `bgt`)
---
 
## Sintaxe da Linguagem
 
Todo programa deve começar com `(START)` e terminar com `(END)`.
 
### Operações Aritméticas (RPN)
```
(A B +)   → adição
(A B -)   → subtração
(A B *)   → multiplicação
(A B |)   → divisão real (double)
(A B /)   → divisão inteira
(A B %)   → resto da divisão inteira
(A B ^)   → potenciação (B deve ser inteiro positivo)
```
 
### Expressões Aninhadas
```
(A (C D *) +)          → soma A com o produto de C e D
((A B +) (C D *) |)    → divide a soma de A e B pelo produto de C e D
```
 
### Comandos Especiais
```
(V NOME MEM)   → armazena o valor V na variável NOME
(NOME)         → lê o valor armazenado em NOME (retorna 0 se não inicializada)
(N RES)        → retorna o resultado de N linhas anteriores (N inteiro >= 0)
```
 
### Estruturas de Controle
 
**Tomada de Decisão (IF):**
```
(condição bloco IF)
```
A condição é uma expressão que resulta em `1.0` (verdadeiro) ou `0.0` (falso) usando operadores relacionais `<`, `>`, `==`. O bloco é executado apenas se a condição for verdadeira.
 
Exemplo:
```
(LIMITE 5.0 > (LIMITE 2.0 -) IF)
```
 
**Laço de Repetição (WHILE):**
```
(condição bloco WHILE)
```
O bloco é executado repetidamente enquanto a condição for verdadeira.
 
Exemplo:
```
(I 5.0 < (I 1.0 + I MEM) WHILE)
```
 
---
 
## Estrutura de Arquivos
 
| Arquivo | Descrição |
|---|---|
| `Compilador.py` | Código-fonte principal com léxico, parser, AST e gerador de Assembly |
| `test_compilador.py` | Suíte de testes com pytest (33 casos) |
| `teste1.txt` | Arquivo de teste — operações aritméticas e comandos especiais |
| `teste2.txt` | Arquivo de teste — expressões aninhadas e uso intenso de memória |
| `teste3_erro_lexico.txt` | Arquivo de teste — caso com erro léxico |
| `teste3_erro_sintatico.txt` | Arquivo de teste — caso com erro sintático |
| `tokens_gerados.txt` | Gerado automaticamente — lista de tokens classificados |
| `arvore_sintatica.json` | Gerado automaticamente — AST em JSON |
| `arvore_sintatica.md` | Gerado automaticamente — AST em formato visual |
| `saida_assembly.s` | Gerado automaticamente — código Assembly ARMv7 |
 
---
 
## Como Compilar e Executar

### Executando o compilador
```bash
python Compilador.py teste1.txt
python Compilador.py teste2.txt
python Compilador.py teste3_erro_lexico.txt
python Compilador.py teste3_erro_sintatico.txt
```
 
Ao executar, o compilador gera automaticamente na mesma pasta:
- `tokens_gerados.txt`
- `arvore_sintatica.json`
- `arvore_sintatica.md`
- `saida_assembly.s`
### Executando os testes automáticos
```bash
pip install pytest
pytest test_compilador.py -v
```
 
---
 
## Depuração
 
Se ocorrer um **erro léxico**, o compilador indica a linha e coluna do caractere inválido:
```
Erro Léxico na linha 2: Caractere inválido '@' na coluna 6
```
 
Se ocorrer um **erro sintático**, o compilador indica a posição do token inesperado:
```
Erro Sintático: Esperado ')', mas encontrou 'END' na posição 6
```