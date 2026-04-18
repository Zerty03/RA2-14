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

