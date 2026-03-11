.data
array: .space 100
.text
main:
la $t0 , array

li $v0 , 5
syscall
move $t1 , $v0		#lenth

move $t2 , $t1	#counter
loop:
beqz $t2 , base

li $v0 , 5
syscall
sw $v0 , 0($t0)

addi $t0 , $t0 , 4
addi $t2 , $t2 , -1

j loop

base:
li $v0 , 5
syscall
move $t3 , $v0		#t3 = base

li $t4,0	#result
la $t5 , array
move $t6 , $t1	#counter

calculate:
beqz $t6 , exit
lw $t8 , 0($t5)

mul $t7 , $t4 , $t3
add $t4 , $t7 ,$t8

addi $t5 , $t5 , 4
addi $t6 , $t6 , -1

j calculate

exit:
li $v0 , 1
move $a0 , $t4
syscall

li $v0 , 10
syscall

	
