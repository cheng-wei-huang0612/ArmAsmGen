VERSION EQU 1
MAX_SIZE EQU 0x800

matrix_multiply:
add x19, xzr, #0
add x20, xzr, #0
add x21, xzr, #0
inner_loop:
mul x22, x1, x2
add x0, x0, x22
add x21, x21, #1
add x20, x20, #1
add x19, x19, #1