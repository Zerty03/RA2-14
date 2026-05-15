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
    // Salvando resultado da linha 1
    ldr r0, =res_linha_1
    vpop {d0}
    vstr d0, [r0]
    ldr r0, =num_3
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_4
    vldr d0, [r0]
    vpush {d0}
    // Operador -
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vsub.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 2
    ldr r0, =res_linha_2
    vpop {d0}
    vstr d0, [r0]
    ldr r0, =num_5
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_6
    vldr d0, [r0]
    vpush {d0}
    // Operador *
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vmul.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 3
    ldr r0, =res_linha_3
    vpop {d0}
    vstr d0, [r0]
    ldr r0, =num_7
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_8
    vldr d0, [r0]
    vpush {d0}
    // Operador |
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vdiv.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 4
    ldr r0, =res_linha_4
    vpop {d0}
    vstr d0, [r0]
    ldr r0, =num_9
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_10
    vldr d0, [r0]
    vpush {d0}
    // Operador /
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vdiv.f64 d2, d1, d0
    vcvt.s32.f64 s4, d2  // Trunca para inteiro
    vcvt.f64.s32 d2, s4  // Volta para double
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 5
    ldr r0, =res_linha_5
    vpop {d0}
    vstr d0, [r0]
    ldr r0, =num_11
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_12
    vldr d0, [r0]
    vpush {d0}
    // Operador %
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    // Resto: A mod B = A - trunc(A/B)*B
    vdiv.f64 d2, d1, d0          // d2 = A / B
    vcvt.s32.f64 s4, d2           // Trunca para int
    vcvt.f64.s32 d2, s4           // Volta para double
    vmul.f64 d2, d2, d0           // d2 = trunc(A/B) * B
    vsub.f64 d2, d1, d2           // d2 = A - resultado
    vpush {d2} // Empilha resultado
    // Salvando resultado da linha 6
    ldr r0, =res_linha_6
    vpop {d0}
    vstr d0, [r0]
    ldr r0, =num_13
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_14
    vldr d0, [r0]
    vpush {d0}
    // Operador ^
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    // Potenciação A^B via loop
    vcvt.s32.f64 s4, d0     // B inteiro em s4
    vmov r1, s4              // r1 = B (contador)
    vmov.f64 d2, d1         // d2 = A (acumulador)
    subs r1, r1, #1         // já contamos 1 multiplicação
    ble pow_fim_2        // se B<=1, resultado já é A
    pow_loop_1:
    vmul.f64 d2, d2, d1    // d2 = d2 * A
    subs r1, r1, #1
    bgt pow_loop_1
    pow_fim_2:
    vpush {d2} // Empilha resultado
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
    
// COMANDO MEM: Guardando resultado em 'PI'
    ldr r0, =num_15
    vldr d0, [r0]
    vpush {d0}
    vpop {d0}
    ldr r0, =var_PI
    vstr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 9
    ldr r0, =res_linha_9
    vpop {d0}
    vstr d0, [r0]
    // Lendo valor da variavel PI
    ldr r0, =var_PI
    vldr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 10
    ldr r0, =res_linha_10
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO RES: Lendo resultado de 2 linha(s) atrás
    ldr r0, =res_linha_2
    vldr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 11
    ldr r0, =res_linha_11
    vpop {d0}
    vstr d0, [r0]
    
// COMANDO MEM: Guardando resultado em 'LIMITE'
    ldr r0, =num_16
    vldr d0, [r0]
    vpush {d0}
    vpop {d0}
    ldr r0, =var_LIMITE
    vstr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 12
    ldr r0, =res_linha_12
    vpop {d0}
    vstr d0, [r0]
    
// INICIO IF (Avaliando Condicao) 

    // Lendo valor da variavel LIMITE
    ldr r0, =var_LIMITE
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_17
    vldr d0, [r0]
    vpush {d0}
    // Operador >
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    bgt op_true_4
    ldr r0, =const_0
    vldr d2, [r0]
    b op_end_5
op_true_4:
    ldr r0, =const_1
    vldr d2, [r0]
op_end_5:
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =const_0
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq fim_if_3 // Se for Falso, pula o bloco inteiro!
    
// BLOCO VERDADEIRO 

    // Lendo valor da variavel LIMITE
    ldr r0, =var_LIMITE
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_18
    vldr d0, [r0]
    vpush {d0}
    // Operador -
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vsub.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    vpop {d0} // Descarta resultado do bloco IF
fim_if_3:
    // Salvando resultado da linha 13
    ldr r0, =res_linha_13
    ldr r1, =const_0
    vldr d0, [r1]
    vstr d0, [r0]
    
// COMANDO MEM: Guardando resultado em 'I'
    ldr r0, =num_19
    vldr d0, [r0]
    vpush {d0}
    vpop {d0}
    ldr r0, =var_I
    vstr d0, [r0]
    vpush {d0}
    // Salvando resultado da linha 14
    ldr r0, =res_linha_14
    vpop {d0}
    vstr d0, [r0]

inicio_while_6:
    
// INICIO WHILE (Avaliando Condicao) 

    // Lendo valor da variavel I
    ldr r0, =var_I
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_20
    vldr d0, [r0]
    vpush {d0}
    // Operador <
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    blt op_true_8
    ldr r0, =const_0
    vldr d2, [r0]
    b op_end_9
op_true_8:
    ldr r0, =const_1
    vldr d2, [r0]
op_end_9:
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =const_0
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq fim_while_7 // Se Falso, Quebra o Loop!
    
// BLOCO WHILE 

    
// COMANDO MEM: Guardando resultado em 'I'
    // Lendo valor da variavel I
    ldr r0, =var_I
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_21
    vldr d0, [r0]
    vpush {d0}
    // Operador +
    vpop {d0} // Operando B
    vpop {d1} // Operando A
    vadd.f64 d2, d1, d0
    vpush {d2} // Empilha resultado
    vpop {d0}
    ldr r0, =var_I
    vstr d0, [r0]
    vpush {d0}
    vpop {d0} // Descarta resultado do corpo do WHILE
    b inicio_while_6 // Volta lá para cima!
fim_while_7:
    // Salvando resultado da linha 15
    ldr r0, =res_linha_15
    ldr r1, =const_0
    vldr d0, [r1]
    vstr d0, [r0]

_fim:
    b _fim

.data
num_1: .double 10.0
num_2: .double 3.0
num_3: .double 10.0
num_4: .double 3.0
num_5: .double 4.0
num_6: .double 2.5
num_7: .double 9.0
num_8: .double 4.0
num_9: .double 10.0
num_10: .double 3.0
num_11: .double 10.0
num_12: .double 3.0
num_13: .double 2.0
num_14: .double 8.0
num_15: .double 3.14
num_16: .double 10.0
num_17: .double 5.0
num_18: .double 2.0
num_19: .double 1.0
num_20: .double 5.0
num_21: .double 1.0
const_1: .double 1.0
const_0: .double 0.0
var_PI: .space 8
var_I: .space 8
var_LIMITE: .space 8
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
res_linha_15: .space 8