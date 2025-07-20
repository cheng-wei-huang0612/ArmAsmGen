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

    def UMULH(self, Xd: RegArg, Xn: RegArg, Xm: RegArg):
        """
        Unsigned Multiply High:
        This instruction multiplies two 64-bit unsigned register values,
        and writes the upper 64 bits of the 128-bit result to the destination register.

            Xd = (Xn * Xm)[127:64] (unsigned)

        This is used for implementing wide multiplication (128-bit results from 64-bit operands).
        Reference: A-profile: section C6.2.341, page C6-2239
        """
        dst_str, src0_str, src1_str = self._reg_to_str(Xd), self._reg_to_str(Xn), self._reg_to_str(Xm)
        self.emit(Instruction(
            template="umulh {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def SMULH(self, Xd: RegArg, Xn: RegArg, Xm: RegArg):
        """
        Signed Multiply High:
        This instruction multiplies two 64-bit signed register values,
        and writes the upper 64 bits of the 128-bit result to the destination register.

            Xd = (Xn * Xm)[127:64] (signed)

        This is used for implementing wide multiplication (128-bit results from 64-bit operands).
        Reference: A-profile: section C6.2.285, page C6-2167
        """
        dst_str, src0_str, src1_str = self._reg_to_str(Xd), self._reg_to_str(Xn), self._reg_to_str(Xm)
        self.emit(Instruction(
            template="smulh {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADDS(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Add and set flags (register):
        This instruction adds two register values, writes the result to the destination register,
        and updates the condition flags (NZCV) based on the result.

            dst = src0 + src1 (and set flags)

        Sets carry flag for multi-precision arithmetic.
        Reference: A-profile: section C6.2.4, page C6-1799
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="adds {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADDS_imm(self, dst: RegArg, src0: RegArg, imm: int):
        """
        Add and set flags (immediate):
        This instruction adds a register value and an immediate value, writes the result 
        to the destination register, and updates the condition flags.

            dst = src0 + imm (and set flags)

        Reference: A-profile: section C6.2.4, page C6-1799
        """
        if not (0 <= imm <= 4095):
            raise ValueError("ADDS immediate out of range (0-4095)")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="adds {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def ADCS(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Add with carry and set flags (register):
        This instruction adds two register values plus the carry flag, writes the result
        to the destination register, and updates the condition flags.

            dst = src0 + src1 + carry_flag (and set flags)

        Essential for multi-precision arithmetic where carry must be propagated.
        Reference: A-profile: section C6.2.2, page C6-1795
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="adcs {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADCS_imm(self, dst: RegArg, src0: RegArg, imm: int):
        """
        Add with carry and set flags (immediate):
        This instruction adds a register value, an immediate value, and the carry flag,
        writes the result to the destination register, and updates the condition flags.

            dst = src0 + imm + carry_flag (and set flags)

        Reference: A-profile: section C6.2.2, page C6-1795
        """
        if not (0 <= imm <= 4095):
            raise ValueError("ADCS immediate out of range (0-4095)")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="adcs {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def SUBS(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Subtract and set flags (register):
        This instruction subtracts one register value from another, writes the result
        to the destination register, and updates the condition flags.

            dst = src0 - src1 (and set flags)

        Sets carry flag (borrow) for multi-precision arithmetic.
        Reference: A-profile: section C6.2.299, page C6-2194
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="subs {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def SUBS_imm(self, dst: RegArg, src0: RegArg, imm: int):
        """
        Subtract and set flags (immediate):
        This instruction subtracts an immediate value from a register value,
        writes the result to the destination register, and updates the condition flags.

            dst = src0 - imm (and set flags)

        Reference: A-profile: section C6.2.299, page C6-2194
        """
        if not (0 <= imm <= 4095):
            raise ValueError("SUBS immediate out of range (0-4095)")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="subs {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def SBCS(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Subtract with carry and set flags (register):
        This instruction subtracts one register value and the NOT of the carry flag
        from another register value, writes the result to the destination register,
        and updates the condition flags.

            dst = src0 - src1 - ~carry_flag (and set flags)

        Used for multi-precision subtraction where borrow must be propagated.
        Reference: A-profile: section C6.2.251, page C6-2132
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="sbcs {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))