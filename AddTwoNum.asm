.data
int1: .word 0       
int2: .word 0          
ans:  .word 0         

.text

main:
   
    li $v0, 5     
    syscall
    sw $v0, int1      


    li $v0, 5      
    syscall
    sw $v0, int2      

    lw $t0, int1     
    lw $t1, int2  

    add $t2, $t0, $t1  
    sw $t2, ans       
	
         
    move $a0, $t2 
	li $v0, 1     
    syscall

    li $v0, 10   
    syscall
