.data
newline: .asciiz "\n"
.text

main:

li $v0 , 5
syscall
move $t0 , $v0		# t0 = A

li $v0 , 5
syscall
move $t1 , $v0		# t1 = B

li $v0 , 5
syscall
move $t2 , $v0		# t2 = Base

li $v0 , 12
syscall
move $t3 , $v0		#t3 = ascii

li $t4 , 0          #t4 used for result

mul $t5 , $t0 , $t3
add $t6 , $t5 , $t1

div $t6 , $t2
mfhi $t7

la $a0 , newline
li $v0 , 4
syscall

move $a0 , $t7
li $v0 , 1
syscall

li $v0 , 10
syscall
