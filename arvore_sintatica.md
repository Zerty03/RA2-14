# Árvore Sintática

**Arquivo de entrada:** `Teste1.txt`

```
**Programa**
    ├── Bloco
    │   ├── Número: `10.0`
    │   ├── Número: `3.0`
    │   └── Operador: `+`
    ├── Bloco
    │   ├── Número: `10.0`
    │   ├── Número: `3.0`
    │   └── Operador: `-`
    ├── Bloco
    │   ├── Número: `4.0`
    │   ├── Número: `2.5`
    │   └── Operador: `*`
    ├── Bloco
    │   ├── Número: `9.0`
    │   ├── Número: `4.0`
    │   └── Operador: `|`
    ├── Bloco
    │   ├── Número: `10.0`
    │   ├── Número: `3.0`
    │   └── Operador: `/`
    ├── Bloco
    │   ├── Número: `10.0`
    │   ├── Número: `3.0`
    │   └── Operador: `%`
    ├── Bloco
    │   ├── Número: `2.0`
    │   ├── Número: `8.0`
    │   └── Operador: `^`
    ├── **RES** ← linha `1`
    ├── **MEM** → `PI`
    │   └── Bloco
    │       └── Número: `3.14`
    ├── Bloco
    │   └── Variável: `PI`
    ├── **RES** ← linha `2`
    ├── **MEM** → `LIMITE`
    │   └── Bloco
    │       └── Número: `10.0`
    ├── **IF**
    │   ├── Condição:
    │   │   ├── Bloco
    │   │   │   ├── Variável: `LIMITE`
    │   │   │   ├── Número: `5.0`
    │   │   │   └── Operador: `>`
    │   └── Bloco Verdadeiro:
    │       └── Bloco
    │           ├── Variável: `LIMITE`
    │           ├── Número: `2.0`
    │           └── Operador: `-`
    ├── **MEM** → `I`
    │   └── Bloco
    │       └── Número: `1.0`
    └── **WHILE**
        ├── Condição:
        │   ├── Bloco
        │   │   ├── Variável: `I`
        │   │   ├── Número: `5.0`
        │   │   └── Operador: `<`
        └── Bloco Loop:
            └── **MEM** → `I`
                └── Bloco
                    ├── Variável: `I`
                    ├── Número: `1.0`
                    └── Operador: `+`
```
