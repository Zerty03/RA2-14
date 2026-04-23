## 1. Regras de Produção da Gramática

**Símbolos Não-Terminais (Variáveis):** `S` (Programa Raiz), `C` (Lista de Comandos), `B` (Bloco), `O` (Operações/Conteúdo), `I` (Item Único)

**Símbolos Terminais (Tokens Únicos):** `(start)`, `(end)`, `(`, `)`, `num`, `var`, `op`, `cmd`

**Produções:**
1. S $\rightarrow$ (start) C (end)
2. C $\rightarrow$ B C | $\varepsilon$
3. B $\rightarrow$ ( O )
4. O $\rightarrow$ I O | $\varepsilon$
5. I $\rightarrow$ num | var | op | cmd | B