# ============================================================
# MIPS Program: Read N numbers into an array, find Min & Max
# ============================================================

.data
    prompt_n:    .asciiz "Enter the number of elements (n): "
    prompt_val:  .asciiz "Enter number: "
    msg_min:     .asciiz "Minimum value: "
    msg_max:     .asciiz "Maximum value: "
    newline:     .asciiz "\n"
    array:       .space 400        # Reserve space for up to 100 integers (4 bytes each)

.text
.globl main

main:
    # -------------------------------------------------------
    # Step 1: Read n (number of elements)
    # -------------------------------------------------------
    li   $v0, 4                    # syscall: print string
    la   $a0, prompt_n
    syscall

    li   $v0, 5                    # syscall: read integer
    syscall
    move $s0, $v0                  # $s0 = n

    # -------------------------------------------------------
    # Step 2: Read n integers and store them in the array
    # -------------------------------------------------------
    la   $s1, array                # $s1 = base address of array
    li   $t0, 0                    # $t0 = loop counter i = 0

read_loop:
    bge  $t0, $s0, read_done       # if i >= n, exit loop

    li   $v0, 4                    # print prompt
    la   $a0, prompt_val
    syscall

    li   $v0, 5                    # read integer
    syscall                        # $v0 = input value

    sll  $t1, $t0, 2               # offset = i * 4
    add  $t2, $s1, $t1             # address = base + offset
    sw   $v0, 0($t2)               # store value in array[i]

    addi $t0, $t0, 1               # i++
    j    read_loop

read_done:

    # -------------------------------------------------------
    # Step 3: Initialize min and max with array[0]
    # -------------------------------------------------------
    lw   $s2, 0($s1)               # $s2 = min = array[0]
    lw   $s3, 0($s1)               # $s3 = max = array[0]
    li   $t0, 1                    # start loop from index 1

    # -------------------------------------------------------
    # Step 4: Loop through the array to find min and max
    # -------------------------------------------------------
find_loop:
    bge  $t0, $s0, find_done       # if i >= n, exit loop

    sll  $t1, $t0, 2               # offset = i * 4
    add  $t2, $s1, $t1             # address = base + offset
    lw   $t3, 0($t2)               # $t3 = array[i]

    # Check for new minimum
    bge  $t3, $s2, check_max       # if array[i] >= min, skip
    move $s2, $t3                  # update min

check_max:
    # Check for new maximum
    ble  $t3, $s3, next_iteration  # if array[i] <= max, skip
    move $s3, $t3                  # update max

next_iteration:
    addi $t0, $t0, 1               # i++
    j    find_loop

find_done:

    # -------------------------------------------------------
    # Step 5: Print the Minimum value
    # -------------------------------------------------------
    li   $v0, 4
    la   $a0, msg_min
    syscall

    li   $v0, 1                    # syscall: print integer
    move $a0, $s2                  # print min
    syscall

    li   $v0, 4
    la   $a0, newline
    syscall

    # -------------------------------------------------------
    # Step 6: Print the Maximum value
    # -------------------------------------------------------
    li   $v0, 4
    la   $a0, msg_max
    syscall

    li   $v0, 1                    # syscall: print integer
    move $a0, $s3                  # print max
    syscall

    li   $v0, 4
    la   $a0, newline
    syscall

    # -------------------------------------------------------
    # Exit program
    # -------------------------------------------------------
    li   $v0, 10
    syscall
