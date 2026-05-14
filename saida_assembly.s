.global _start
.text
_start:

    ldr r0, =num_1
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_2
    vldr d0, [r0]
    vpush {d0}
    // Operador +
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vadd.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    ldr r0, =num_3
    vldr d0, [r0]
    vpush {d0}
    // Operador *
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vmul.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 1
    ldr r0, =res_linha_1
    vpop {d0}
    vstr d0, [r0]
    // Operador *
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vmul.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 2
    ldr r0, =res_linha_2
    vpop {d0}
    vstr d0, [r0]
    // Operador -
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vsub.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 3
    ldr r0, =res_linha_3
    vpop {d0}
    vstr d0, [r0]
    // Operador +
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vadd.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 4
    ldr r0, =res_linha_4
    vpop {d0}
    vstr d0, [r0]
    // Operador |
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vdiv.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 5
    ldr r0, =res_linha_5
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO MEM: Guardando resultado em 'TOTAL'
    ldr r0, =num_4
    vldr d0, [r0]
    vpush {d0}
    vpop {d0}
    ldr r0, =var_TOTAL
    vstr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 6
    ldr r0, =res_linha_6
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO MEM: Guardando resultado em 'TOTAL'
    // Lendo valor da variavel TOTAL
    ldr r0, =var_TOTAL
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_5
    vldr d0, [r0]
    vpush {d0}
    // Operador -
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vsub.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =var_TOTAL
    vstr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 7
    ldr r0, =res_linha_7
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO RES: Lendo resultado de 1 linha(s) atrás
    ldr r0, =res_linha_1
    vldr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 8
    ldr r0, =res_linha_8
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO RES: Lendo resultado de 2 linha(s) atrás
    ldr r0, =res_linha_2
    vldr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 9
    ldr r0, =res_linha_9
    vpop {d0}
    vstr d0, [r0]

inicio_while_1:
    
// INICIO WHILE (Avaliando Condicao) 

    // Lendo valor da variavel TOTAL
    ldr r0, =var_TOTAL
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_6
    vldr d0, [r0]
    vpush {d0}
    // Operador >
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    bgt op_true_3
    ldr r0, =const_0
    vldr d2, [r0]
    b op_end_4
op_true_3:
    ldr r0, =const_1
    vldr d2, [r0]
op_end_4:
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =const_0
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq fim_while_2 // Se Falso, Quebra o Loop!
    
// BLOCO WHILE 

    
// COMANDO MEM: Guardando resultado em 'TOTAL'
    // Lendo valor da variavel TOTAL
    ldr r0, =var_TOTAL
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_7
    vldr d0, [r0]
    vpush {d0}
    // Operador -
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vsub.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =var_TOTAL
    vstr d0, [r0]
    vpush {d0}
    vpop {d0} // Descarta resultado do corpo do WHILE
    b inicio_while_1 // Volta lá para cima!
fim_while_2:
    // Salvando resultado da linha 10
    ldr r0, =res_linha_10
    ldr r1, =const_0
    vldr d0, [r1]
    vstr d0, [r0]
    
// COMANDO MEM: Guardando resultado em 'LIMITE'
    ldr r0, =num_8
    vldr d0, [r0]
    vpush {d0}
    vpop {d0}
    ldr r0, =var_LIMITE
    vstr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 11
    ldr r0, =res_linha_11
    vpop {d0}
    vstr d0, [r0]
    
// INICIO IF (Avaliando Condicao) 

    // Lendo valor da variavel TOTAL
    ldr r0, =var_TOTAL
    vldr d0, [r0]
    vpush {d0}
    // Guardando valor na variavel LIMITE
    vpop {d0}
    ldr r0, =var_LIMITE
    vstr d0, [r0]
    // Operador <
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    blt op_true_6
    ldr r0, =const_0
    vldr d2, [r0]
    b op_end_7
op_true_6:
    ldr r0, =const_1
    vldr d2, [r0]
op_end_7:
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =const_0
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq fim_if_5 // Se for Falso, pula o bloco inteiro!
    
// BLOCO VERDADEIRO 

    
// COMANDO MEM: Guardando resultado em 'TOTAL'
    // Lendo valor da variavel TOTAL
    ldr r0, =var_TOTAL
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_9
    vldr d0, [r0]
    vpush {d0}
    // Operador *
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vmul.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =var_TOTAL
    vstr d0, [r0]
    vpush {d0}
    vpop {d0} // Descarta resultado do bloco IF
fim_if_5:
    // Salvando resultado da linha 12
    ldr r0, =res_linha_12
    ldr r1, =const_0
    vldr d0, [r1]
    vstr d0, [r0]
    // Lendo valor da variavel TOTAL
    ldr r0, =var_TOTAL
    vldr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 13
    ldr r0, =res_linha_13
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO RES: Lendo resultado de 3 linha(s) atrás
    ldr r0, =res_linha_3
    vldr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 14
    ldr r0, =res_linha_14
    vpop {d0}
    vstr d0, [r0]

_fim:
    b _fim

.data
num_1: .double 3.0
num_2: .double 2.0
num_3: .double 5.0
num_4: .double 100.0
num_5: .double 20.0
num_6: .double 0.0
num_7: .double 10.0
num_8: .double 50.0
num_9: .double 2.0
const_1: .double 1.0
const_0: .double 0.0
var_LIMITE: .space 8
var_TOTAL: .space 8
res_linha_1: .space 8
res_linha_2: .space 8
res_linha_3: .space 8
res_linha_4: .space 8
res_linha_5: .space 8
res_linha_6: .space 8
res_linha_7: .space 8
res_linha_8: .space 8
res_linha_9: .space 8
res_linha_10: .space 8
res_linha_11: .space 8
res_linha_12: .space 8
res_linha_13: .space 8
res_linha_14: .space 8