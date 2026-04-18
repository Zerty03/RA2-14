# Analisador Sintático LL(1) e Árvore Sintática

## 1. Regra de Produção da Gramatica

Para seguir a notação padrão (onde Não-Terminais são letras maiusculas e Terminais são minúsculas ou símbolos), definimos que:

**Símbolos Não-Terminais (Variáveis):** `S` (Programa Raiz), `C` (Lista de Comandos), `B` (Bloco), `O` (Operações/Conteúdo), `I` (Item Único)

**Símbolos Terminais (Tokens):** `start`, `end`, `(`, `)`, `num`, `var`, `op`, `cmd`

**Produções:**
1. S $\rightarrow$ start C end
2. C $\rightarrow$ B C | $\varepsilon$
3. B $\rightarrow$ ( O )
4. O $\rightarrow$ I O | $\varepsilon$
5. I $\rightarrow$ num | var | op | cmd | B

---

## 2. Conjunto FIRST e FOLLOW

| Não-Terminal | FIRST | FOLLOW |
| :---: | :--- | :--- |
| **S** | `{ start }` | `{ $ }` |
| **C** | `{ (, ε }` | `{ end }` |
| **B** | `{ ( }` | `{ (, end }` |
| **O** | `{ num, var, op, cmd, (, ε }` | `{ ) }` |
| **I** | `{ num, var, op, cmd, ( }` | `{ num, var, op, cmd, (, ) }` |

*(Nota: o símbolo $\varepsilon$ representa a cadeia vazia e `$` representa o fim do arquivo)*

---

## 3. Tabela de Análise Sintática LL(1)

A gramática abaixo prova-se estritamente **LL(1)**, pois não há colisões (nenhuma célula possui mais de uma regra de produção), garantindo que o *Parser* não sofra de ambiguidades.

| NT \ Term | start | end | ( | ) | num | var | op | cmd | $ |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S** | S $\rightarrow$ start C end | | | | | | | | |
| **C** | | C $\rightarrow$ $\varepsilon$ | C $\rightarrow$ B C | | | | | | |
| **B** | | | B $\rightarrow$ ( O ) | | | | | | |
| **O** | | | O $\rightarrow$ I O | O $\rightarrow$ $\varepsilon$ | O $\rightarrow$ I O | O $\rightarrow$ I O | O $\rightarrow$ I O | O $\rightarrow$ I O | |
| **I** | | | I $\rightarrow$ B | | I $\rightarrow$ num | I $\rightarrow$ var | I $\rightarrow$ op | I $\rightarrow$ cmd | |