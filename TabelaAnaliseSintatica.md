## 3. Tabela de Análise Sintática LL(1)

| NT \ Term | (start) | (end) | ( | ) | num | var | op | cmd | $ |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S** | S $\rightarrow$ (start) C (end) | | | | | | | | |
| **C** | | C $\rightarrow$ $\varepsilon$ | C $\rightarrow$ B C | | | | | | |
| **B** | | | B $\rightarrow$ ( O ) | | | | | | |
| **O** | | | O $\rightarrow$ I O | O $\rightarrow$ $\varepsilon$ | O $\rightarrow$ I O | O $\rightarrow$ I O | O $\rightarrow$ I O | O $\rightarrow$ I O | |
| **I** | | | I $\rightarrow$ B | | I $\rightarrow$ num | I $\rightarrow$ var | I $\rightarrow$ op | I $\rightarrow$ cmd | |