.data
	newline: .asciz "\n"
.text
	main:
	
	li $v0 , 5
	syscall
	move $t0 , $v0
	
	li $t1 , 0   	#total of comsoc
	li $t2 , 0		#total of ieee
	
	loop:
	
	beqz $t0 , exit
	
	li $v0 , 5
	syscall					#add comsoc
	add $t1 , $v0 , $t1
	
	li $v0 , 5
	syscall					#add ieee
	add $t2 , $t2 , $v0
	
	addi $t0 , $t0 , -1
	
	j loop
	
	
	exit:
	move $a0 , $t1
	li $v0 , 1		#print comsoc
	syscall
	
	la $a0 , newline
	li $v0 , 4
	syscall
	
	move $a0 , $t2
	li $v0 , 1		#print ieee
	syscall
	
	la $a0 , newline
	li $v0 , 4
	syscall
	
	
	li $v0 , 10
	syscall
