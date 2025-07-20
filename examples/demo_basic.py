from armasmgen.builder import ASMCode, Block

f = ASMCode()

with f as asm:
    asm.equ("CONST","0x1234")
    with Block(label="main") as m:
        m.ADD("x0","x1","x2")
        with Block(label="inner") as inn:
            inn.ADD_imm("x3","x4",7)

f.stdout()