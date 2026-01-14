.data
String1: .asciiz "Input a number: "
String2: .asciiz "Output = "
int1:    .word 0
int2:    .word 0
int3:    .word 0
ans:     .word 0

.text

main:
    la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, int1

    la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, int2

    la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, int3

    lw $t0, int1
    lw $t1, int2
    lw $t2, int3

    add $t3, $t0, $t1
    add $t3, $t3, $t2

    la $a0, String2
    li $v0, 4
    syscall

    li $v0, 1
    move $a0, $t3
    syscall

    li $v0, 10
    syscall
