## 2. Conjuntos FIRST e FOLLOW

| Não-Terminal | FIRST | FOLLOW |
| :---: | :--- | :--- |
| **S** | `{ (start) }` | `{ $ }` |
| **C** | `{ (, ε }` | `{ (end) }` |
| **B** | `{ ( }` | `{ (, (end) }` |
| **O** | `{ num, var, op, cmd, (, ε }` | `{ ) }` |
| **I** | `{ num, var, op, cmd, ( }` | `{ num, var, op, cmd, (, ) }` |