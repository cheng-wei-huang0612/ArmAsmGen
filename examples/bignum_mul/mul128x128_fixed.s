
.global mul128x128
.global _mul128x128
mul128x128:
_mul128x128:
    main:
    ldp x4, x5, [x0]
    ldp x6, x7, [x1]
    mul x10, x4, x6
    umulh x11, x4, x6
    mul x12, x4, x7
    umulh x13, x4, x7
    mul x14, x5, x6
    umulh x15, x5, x6
    mul x16, x5, x7
    umulh x17, x5, x7
    mov x3, x10
    adds x4, x11, x12
    adcs x4, x4, x14
    adcs x5, x13, x15
    adcs x5, x5, x16
    adcs x6, x17, xzr
    stp x3, x4, [x2]
    stp x5, x6, [x2, #16]
    ret