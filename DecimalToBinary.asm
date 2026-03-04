.data


.text
	main:
	li $v0 , 5
	syscall
	move $t0 ,$v0
	
	li $s0 , 2
	
	loop:
	beqz $t0 , exit
	
	div $t0 , $s0
	mflo $t1
	mfhi $t2
	
	li $v0 , 1
	move $a0 , $t2
	syscall
	
	move $t0 , $t1
	
	j loop
	
	
	exit:
	li $v0 , 10
	syscall