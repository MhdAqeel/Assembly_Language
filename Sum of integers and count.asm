# MIPS Assembly Program
# Read three integers n1, n2, n3
# Print the total sum and count of numbers from n1 to n2 incremented by n3

.data

.text
.globl main

main:
    # Read n1
    li $v0, 5               # syscall for read integer
    syscall
    move $t0, $v0           # $t0 = n1
    
    # Read n2
    li $v0, 5               # syscall for read integer
    syscall
    move $t1, $v0           # $t1 = n2
    
    # Read n3
    li $v0, 5               # syscall for read integer
    syscall
    move $t2, $v0           # $t2 = n3
    
    # Initialize variables
    move $t3, $t0           # $t3 = current number (start with n1)
    li $t4, 0               # $t4 = sum (initialize to 0)
    li $t5, 0               # $t5 = count (initialize to 0)
    
loop:
    # Check if current number <= n2
    bgt $t3, $t1, end_loop  # if current > n2, exit loop
    
    # Add current number to sum
    add $t4, $t4, $t3       # sum += current
    
    # Increment count
    addi $t5, $t5, 1        # count++
    
    # Increment current by n3
    add $t3, $t3, $t2       # current += n3
    
    # Repeat loop
    j loop

end_loop:
    # Print the sum
    li $v0, 1               # syscall for print integer
    move $a0, $t4           # load sum
    syscall
    
    # Print space
    li $a0, 32              # ASCII code for space
    li $v0, 11              # syscall for print character
    syscall
    
    # Print the count
    li $v0, 1               # syscall for print integer
    move $a0, $t5           # load count
    syscall
    
    # Exit program
    li $v0, 10              # syscall for exit
    syscall
