# Program to print a numbered sequence
.data
string1: .asciiz "Sequence:\n"
space: .asciiz " "
count: .word 20

.text
main:
    # Print the header string
    la $a0, string1
    li $v0, 4
    syscall

    # Initialize loop counter and limit
    move $t0, $zero      # counter starts at 0
    lw $t1, count        # load count value (20) from memory
    
loop:
    # Print the current number
    move $a0, $t0
    li $v0, 1
    syscall
    
    # Print a space
    la $a0, space
    li $v0, 4
    syscall
    
    # Increment counter and check condition
    addi $t0, $t0, 1
    blt $t0, $t1, loop   # continue if $t0 < count
    
    # Print newline at the end
    li $a0, 10           # ASCII code for newline
    li $v0, 11           # syscall 11 prints a character
    syscall

    # Exit program
    li $v0, 10
    syscall