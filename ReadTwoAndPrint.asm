# Program to read two integers n1 and n2, and print sequence from n1 to n2
.data
prompt1: .asciiz "Input n1: "
prompt2: .asciiz "Input n2: "
output: .asciiz "Output: "
comma: .asciiz ", "

.text
main:
    # Print prompt for n1
    la $a0, prompt1
    li $v0, 4
    syscall
    
    # Read integer n1 from user
    li $v0, 5           # syscall 5 reads an integer
    syscall
    move $t0, $v0       # store n1 in $t0 (also our counter)
    
    # Print prompt for n2
    la $a0, prompt2
    li $v0, 4
    syscall
    
    # Read integer n2 from user
    li $v0, 5           # syscall 5 reads an integer
    syscall
    move $t1, $v0       # store n2 in $t1
    
    # Print "Output: "
    la $a0, output
    li $v0, 4
    syscall
    
loop:
    # Print the current number
    move $a0, $t0
    li $v0, 1
    syscall
    
    # Check if this is the last number
    beq $t0, $t1, end_loop   # if counter == n2, skip comma
    
    # Print comma and space
    la $a0, comma
    li $v0, 4
    syscall
    
    # Increment counter and continue
    addi $t0, $t0, 1
    ble $t0, $t1, loop       # continue if counter <= n2
    
end_loop:
    # Print newline at the end
    li $a0, 10          # ASCII code for newline
    li $v0, 11          # syscall 11 prints a character
    syscall
    
    # Exit program
    li $v0, 10
    syscall