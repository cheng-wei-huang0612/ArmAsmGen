
my_constants:
.align 4
.word 12345678

.global my_add
.global _my_add
my_add:
_my_add:
add x0, x1, x2
ret