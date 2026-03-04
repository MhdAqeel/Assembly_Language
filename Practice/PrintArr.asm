.data
input: .word 10,20,30,40,50
newline: .asciiz "\n"

.text
	main:
	la $s0 , input
	li $s1 , 5
	
	loop:
	beq $s1 , $0 , exit
	
	li $v0 , 1 
	lw $a0 , 0($s0)
	syscall
	
	li $v0 , 4
	la $a0 , newline
	syscall
	
	addi $s0, $s0, 4   
    addi $s1, $s1, -1  
    j loop
	
	exit:
	
	li $v0 , 10
	syscal
