# asm_printer/mixins/arithmetic.py
from ..core import Instruction

class ArithmeticMixin:
    def emit(self, inst: Instruction): ...  # 型別提示

    def ADD(self, dst, src0, src1):
        self.emit(Instruction(
            template="add {dst}, {src0}, {src1}",
            dsts=[dst],
            srcs=[src0, src1],
            kwargs=dict(dst=dst, src0=src0, src1=src1)
        ))

    def ADD_imm(self, dst, src0, imm):
        if not (0 <= imm <= 4095):
            raise ValueError("ADD (imm12) out of range")
        self.emit(Instruction(
            template="add {dst}, {src0}, {imm}",
            dsts=[dst],
            srcs=[src0],
            kwargs=dict(dst=dst, src0=src0, imm=imm)
        ))

    def SUB(self, dst, src0, src1):
        self.emit(Instruction(
            template="sub {dst}, {src0}, {src1}",
            dsts=[dst],
            srcs=[src0, src1],
            kwargs=dict(dst=dst, src0=src0, src1=src1)
        ))