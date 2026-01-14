#Program to print a message
.data
string1: .asciiz "Hello, this is my first Assembly Program\n" 
string2: .asciiz "Hello, this is my second Assembly Program\n" 
.text
.global _start
_start:
jal main
li $v0, 10
syscall # Use syscall 10 to stop simulation
 
main:
la $a0, string1 # load address of string to be printed into $a0 
li $v0, 4 # # code for printing string is 4
syscall # call operating system to perform print operation

la $a0, string2 # load address of string to be printed into $a0 
li $v0, 4 # # code for printing string is 4
syscall
