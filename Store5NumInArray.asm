.data
String1: .asciiz "Input a number: "
String2: .asciiz "Output = "
numarray:     .word 0

.text

main:
	la $a1, numarray
	
    la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, 0($a1)

    la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, 4($a1)

    la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, 8($a1)
	
	la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, 12($a1)
	
	 la $a0, String1
    li $v0, 4
    syscall

    li $v0, 5
    syscall
    sw $v0, 16($a1)
	
	
    la $a0, String2
    li $v0, 4
    syscall

    lw $t0, 0($a1)             # Load and print first value
    move $a0, $t0
    li $v0, 1
    syscall

    lw $t1, 4($a1)             # Load and print second value
    move $a0, $t1
    li $v0, 1
    syscall

    lw $t2, 8($a1)             # Load and print third value
    move $a0, $t2
    li $v0, 1
    syscall

    lw $t3, 12($a1)            # Load and print fourth value
    move $a0, $t3
    li $v0, 1
    syscall

    lw $t4, 16($a1)            # Load and print fifth value
    move $a0, $t4
    li $v0, 1
    syscall

    li $v0, 10
    syscall
