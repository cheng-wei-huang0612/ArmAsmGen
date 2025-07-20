# asm_printer/mixins/arithmetic.py
from ..core import Instruction
from ..register import Register
from typing import Union

# Type alias for register arguments (can be Register object or string)
RegArg = Union[Register, str]

class ArithmeticMixin:
    def emit(self, inst: Instruction): ...  # 型別提示

    def _reg_to_str(self, reg: RegArg) -> str:
        """Convert register argument to string representation"""
        if isinstance(reg, Register):
            return str(reg)
        return str(reg)

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

