from armasmgen import *


f = BackgroundCode("constant_demo")

with f as asm:
    with DataBlock(label="my_constants", ) as m:
        m.add_data("word", 12345678)
    with ASMCode(label="my_add") as main:
        main.ADD("x0", "x1", "x2")


f.export_to_file("demo_constant.s")