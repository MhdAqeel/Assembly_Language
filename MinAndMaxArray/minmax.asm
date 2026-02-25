.data
    array: .space 400

.text
.globl main

main:
    li   $v0, 5
    syscall
    move $t0, $v0

    la   $t1, array
    move $t2, $t1
    move $t3, $t0

read_loop:
    beqz $t3, read_done
    li   $v0, 5
    syscall
    sw   $v0, 0($t2)
    addi $t2, $t2, 4
    addi $t3, $t3, -1
    j    read_loop

read_done:
    lw   $t4, 0($t1)
    lw   $t5, 0($t1)

    addi $t2, $t1, 4
    addi $t3, $t0, -1

find_loop:
    beqz $t3, find_done
    lw   $t6, 0($t2)

    bge  $t6, $t4, check_max
    move $t4, $t6

check_max:
    ble  $t6, $t5, next_iter
    move $t5, $t6

next_iter:
    addi $t2, $t2, 4
    addi $t3, $t3, -1
    j    find_loop

find_done:
    move $a0, $t4
    li   $v0, 1
    syscall

    li   $v0, 11
    li   $a0, 10
    syscall

    move $a0, $t5
    li   $v0, 1
    syscall

    li   $v0, 11
    li   $a0, 10
    syscall

    li   $v0, 10
    syscall
