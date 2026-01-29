# Program to read an integer n and print sequence from 0 to n
.data
prompt: .asciiz "Input: "
output: .asciiz "Output: "
comma: .asciiz ", "

.text
main:
    # Print prompt
    la $a0, prompt
    li $v0, 4
    syscall
    
    # Read integer n from user
    li $v0, 5           # syscall 5 reads an integer
    syscall
    move $t1, $v0       # store n in $t1
    
    # Print "Output: "
    la $a0, output
    li $v0, 4
    syscall
    
    # Initialize loop counter
    move $t0, $zero     # counter starts at 0
    
loop:
    # Print the current number
    move $a0, $t0
    li $v0, 1
    syscall
    
    # Check if this is the last number
    beq $t0, $t1, end_loop   # if counter == n, skip comma
    
    # Print comma and space
    la $a0, comma
    li $v0, 4
    syscall
    
    # Increment counter and continue
    addi $t0, $t0, 1
    ble $t0, $t1, loop       # continue if counter <= n
    
end_loop:
    # Print newline at the end
    li $a0, 10          # ASCII code for newline
    li $v0, 11          # syscall 11 prints a character
    syscall
    
    # Exit program
    li $v0, 10
    syscall