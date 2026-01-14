.text

main:
    li $v0, 5
    syscall
    move $t0, $v0

    li $v0, 5
    syscall
    move $t1, $v0

    li $v0, 5
    syscall
    move $t2, $v0

    add $t3, $t0, $t1
    add $t3, $t3, $t2

    li $v0, 1
    move $a0, $t3
    syscall

    li $v0, 10
    syscall
    
