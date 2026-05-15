# Árvore Sintática

**Arquivo de entrada:** `Teste2.txt`

```
**Programa**
    ├── Bloco
    │   ├── Número: `3.0`
    │   ├── Número: `2.0`
    │   ├── Operador: `+`
    │   ├── Número: `5.0`
    │   └── Operador: `*`
    ├── Bloco
    │   ├── Bloco
    │   │   ├── Número: `4.0`
    │   │   ├── Número: `2.0`
    │   │   └── Operador: `+`
    │   ├── Bloco
    │   │   ├── Número: `3.0`
    │   │   ├── Número: `1.0`
    │   │   └── Operador: `-`
    │   └── Operador: `*`
    ├── Bloco
    │   ├── Bloco
    │   │   ├── Número: `10.0`
    │   │   ├── Número: `2.0`
    │   │   └── Operador: `|`
    │   ├── Bloco
    │   │   ├── Número: `3.0`
    │   │   ├── Número: `1.0`
    │   │   └── Operador: `+`
    │   └── Operador: `-`
    ├── Bloco
    │   ├── Bloco
    │   │   ├── Número: `7.0`
    │   │   ├── Número: `3.0`
    │   │   └── Operador: `%`
    │   ├── Bloco
    │   │   ├── Número: `2.0`
    │   │   ├── Número: `4.0`
    │   │   └── Operador: `^`
    │   └── Operador: `+`
    ├── Bloco
    │   ├── Bloco
    │   │   ├── Número: `9.0`
    │   │   ├── Número: `3.0`
    │   │   └── Operador: `/`
    │   ├── Bloco
    │   │   ├── Número: `2.0`
    │   │   ├── Número: `5.0`
    │   │   └── Operador: `*`
    │   └── Operador: `|`
    ├── **MEM** → `TOTAL`
    │   └── Bloco
    │       └── Número: `100.0`
    ├── **MEM** → `TOTAL`
    │   └── Bloco
    │       ├── Variável: `TOTAL`
    │       ├── Número: `20.0`
    │       └── Operador: `-`
    ├── **RES** ← linha `1`
    ├── **RES** ← linha `2`
    ├── **WHILE**
    │   ├── Condição:
    │   │   ├── Bloco
    │   │   │   ├── Variável: `TOTAL`
    │   │   │   ├── Número: `0.0`
    │   │   │   └── Operador: `>`
    │   └── Bloco Loop:
    │       └── **MEM** → `TOTAL`
    │           └── Bloco
    │               ├── Variável: `TOTAL`
    │               ├── Número: `10.0`
    │               └── Operador: `-`
    ├── **MEM** → `LIMITE`
    │   └── Bloco
    │       └── Número: `50.0`
    ├── **IF**
    │   ├── Condição:
    │   │   ├── Bloco
    │   │   │   ├── Variável: `TOTAL`
    │   │   │   ├── Variável: `LIMITE`
    │   │   │   └── Operador: `<`
    │   └── Bloco Verdadeiro:
    │       └── **MEM** → `TOTAL`
    │           └── Bloco
    │               ├── Variável: `TOTAL`
    │               ├── Número: `2.0`
    │               └── Operador: `*`
    ├── Bloco
    │   └── Variável: `TOTAL`
    └── **RES** ← linha `3`
```
