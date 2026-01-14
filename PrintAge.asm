.data
string1: .asciiz "Name: " 
string2: .asciiz "Mohanathas\n"
string3: .asciiz "Address: "
string4: .asciiz "Jaffna\n"
string5: .asciiz "Age: "
age: .word 20  

.text
 
main:
    # Print "Name: "
    la $a0, string1 
    li $v0, 4        
    syscall       

    # Print "Mohanathas"
    la $a0, string2 
    li $v0, 4     
    syscall          

    # Print "Address: "
    la $a0, string3  
    li $v0, 4        
    syscall          

    # Print "Jaffna"
    la $a0, string4 
    li $v0, 4       
    syscall          

    # Print "Age: "
    la $a0, string5  
    li $v0, 4       
    syscall         

    # Print the age (xx)
    lw $a0, age      
    li $v0, 1       
    syscall
    
    li $v0, 10
    syscall
