# Program to read three integers n1, n2, n3 and print sequence from n1 to n2 incremented by n3
.data
prompt1: .asciiz "Input n1: "
prompt2: .asciiz "Input n2: "
prompt3: .asciiz "Input n3: "
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
    move $t0, $v0       # store n1 in $t0 (our counter)
    
    # Print prompt for n2
    la $a0, prompt2
    li $v0, 4
    syscall
    
    # Read integer n2 from user
    li $v0, 5           # syscall 5 reads an integer
    syscall
    move $t1, $v0       # store n2 in $t1
    
    # Print prompt for n3
    la $a0, prompt3
    li $v0, 4
    syscall
    
    # Read integer n3 from user
    li $v0, 5           # syscall 5 reads an integer
    syscall
    move $t2, $v0       # store n3 in $t2 (increment value)
    
    # Print "Output: "
    la $a0, output
    li $v0, 4
    syscall
    
    # Flag to track if we've printed at least one number
    li $t3, 0           # $t3 = 0 means first number, 1 means not first
    
loop:
    # Check if current counter exceeds n2
    bgt $t0, $t1, end_loop   # if counter > n2, exit loop
    
    # If not the first number, print comma and space
    beq $t3, $zero, skip_comma
    la $a0, comma
    li $v0, 4
    syscall
    
skip_comma:
    # Print the current number
    move $a0, $t0
    li $v0, 1
    syscall
    
    # Mark that we've printed at least one number
    li $t3, 1
    
    # Increment counter by n3
    add $t0, $t0, $t2
    j loop              # continue loop
    
end_loop:
    # Print newline at the end
    li $a0, 10          # ASCII code for newline
    li $v0, 11          # syscall 11 prints a character
    syscall
    
    # Exit program
    li $v0, 10
    syscall