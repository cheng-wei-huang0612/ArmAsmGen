# asm_printer/mixins/arithmetic.py
from ..core import Instruction, RegArg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..register import Register

class ArithmeticMixin:
    def emit(self, inst: Instruction): ...  # 型別提示
    def _reg_to_str(self, reg: RegArg) -> str: ...  # 型別提示

    def ADD(self, dst: RegArg, src0: RegArg, src1: RegArg):
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="add {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_imm(self, dst: RegArg, src0: RegArg, imm: int):
        if not (0 <= imm <= 4095):
            raise ValueError("ADD (imm12) out of range")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="add {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def SUB(self, dst: RegArg, src0: RegArg, src1: RegArg):
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="sub {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def SUB_imm(self, dst: RegArg, src0: RegArg, imm: int):
        if not (0 <= imm <= 4095):
            raise ValueError("SUB (imm12) out of range")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="sub {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def MUL(self, dst: RegArg, src0: RegArg, src1: RegArg):
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="mul {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def MADD(self, Xd: RegArg, Xn: RegArg, Xm: RegArg, Xa: RegArg):
        """
        Multiply-add:
        This instruction multiplies two register values, adds a third register value, 
        and writes the result to the destination register.

            Xd = Xa + (Xn * Xm)

        Reference: A-profile: section C6.2.244, page C6-2100
        """
        dst_str, src0_str, src1_str, src2_str = (
            self._reg_to_str(Xd), self._reg_to_str(Xn), 
            self._reg_to_str(Xm), self._reg_to_str(Xa)
        )
        self.emit(Instruction(
            template="madd {dst}, {src0}, {src1}, {src2}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str, src2_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str, src2=src2_str)
        ))

    def MSUB(self, Xd: RegArg, Xn: RegArg, Xm: RegArg, Xa: RegArg):
        """
        Multiply-subtract:
        This instruction multiplies two register values, subtracts a third register value, 
        and writes the result to the destination register.

            Xd = Xa - (Xn * Xm)

        Reference: A-profile: section C6.2.245, page C6-2101
        """
        dst_str, src0_str, src1_str, src2_str = (
            self._reg_to_str(Xd), self._reg_to_str(Xn), 
            self._reg_to_str(Xm), self._reg_to_str(Xa)
        )
        self.emit(Instruction(
            template="msub {dst}, {src0}, {src1}, {src2}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str, src2_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str, src2=src2_str)
        ))


    def MNEG(self, Xd: RegArg, Xn: RegArg, Xm: RegArg):
        """
        Multiply-negate:
        This instruction multiplies two register values, negates the result, 
        and writes it to the destination register.

            Xd = -(Xn * Xm)

        Reference: A-profile: section C6.2.246, page C6-2102
        """
        dst_str, src0_str, src1_str = self._reg_to_str(Xd), self._reg_to_str(Xn), self._reg_to_str(Xm)
        self.emit(Instruction(
            template="mneg {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))