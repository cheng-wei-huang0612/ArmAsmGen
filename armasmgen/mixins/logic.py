# asm_printer/mixins/logic.py
from ..core import Instruction, RegArg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..register import Register

class LogicMixin:
    def emit(self, inst: Instruction): ...  # 型別提示
    def _reg_to_str(self, reg: RegArg) -> str: ...  # 型別提示

    def AND(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Bitwise AND (register):
        Performs a bitwise AND of the values in two registers, 
        and writes the result to the destination register.

            dst = src0 & src1

        Reference: A-profile: section C6.2.11, page C6-1816
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="and {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def AND_imm(self, dst: RegArg, src0: RegArg, imm: int):
        """
        Bitwise AND (immediate):
        Performs a bitwise AND of a register value and an immediate value,
        and writes the result to the destination register.

            dst = src0 & imm

        Reference: A-profile: section C6.2.11, page C6-1816
        """
        if not (0 <= imm <= 0xFFFF):  # 16-bit immediate for logical operations
            raise ValueError("AND immediate out of range (0-65535)")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="and {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def ORR(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Bitwise OR (register):
        Performs a bitwise inclusive OR of the values in two registers,
        and writes the result to the destination register.

            dst = src0 | src1

        Reference: A-profile: section C6.2.180, page C6-2024
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="orr {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ORR_imm(self, dst: RegArg, src0: RegArg, imm: int):
        """
        Bitwise OR (immediate):
        Performs a bitwise inclusive OR of a register value and an immediate value,
        and writes the result to the destination register.

            dst = src0 | imm

        Reference: A-profile: section C6.2.180, page C6-2024
        """
        if not (0 <= imm <= 0xFFFF):
            raise ValueError("ORR immediate out of range (0-65535)")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="orr {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def EOR(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Bitwise Exclusive OR (register):
        Performs a bitwise exclusive OR of the values in two registers,
        and writes the result to the destination register.

            dst = src0 ^ src1

        Reference: A-profile: section C6.2.112, page C6-1938
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="eor {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def EOR_imm(self, dst: RegArg, src0: RegArg, imm: int):
        """
        Bitwise Exclusive OR (immediate):
        Performs a bitwise exclusive OR of a register value and an immediate value,
        and writes the result to the destination register.

            dst = src0 ^ imm

        Reference: A-profile: section C6.2.112, page C6-1938
        """
        if not (0 <= imm <= 0xFFFF):
            raise ValueError("EOR immediate out of range (0-65535)")
        dst_str, src0_str = self._reg_to_str(dst), self._reg_to_str(src0)
        self.emit(Instruction(
            template="eor {dst}, {src0}, #{imm}",
            dsts=[dst_str],
            srcs=[src0_str],
            kwargs=dict(dst=dst_str, src0=src0_str, imm=imm)
        ))

    def BIC(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Bitwise Bit Clear (register):
        Performs a bitwise AND of one register value with the complement of another register value,
        and writes the result to the destination register.

            dst = src0 & (~src1)

        Reference: A-profile: section C6.2.24, page C6-1836
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="bic {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ORN(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Bitwise OR NOT (register):
        Performs a bitwise inclusive OR of one register value with the complement of another register value,
        and writes the result to the destination register.

            dst = src0 | (~src1)

        Reference: A-profile: section C6.2.179, page C6-2023
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="orn {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def EON(self, dst: RegArg, src0: RegArg, src1: RegArg):
        """
        Bitwise Exclusive OR NOT (register):
        Performs a bitwise exclusive OR of one register value with the complement of another register value,
        and writes the result to the destination register.

            dst = src0 ^ (~src1)

        Reference: A-profile: section C6.2.111, page C6-1937
        """
        dst_str, src0_str, src1_str = self._reg_to_str(dst), self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="eon {dst}, {src0}, {src1}",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def MVN(self, dst: RegArg, src: RegArg):
        """
        Move NOT (register):
        Performs a bitwise inversion of a register value,
        and writes the result to the destination register.

            dst = ~src

        Reference: A-profile: section C6.2.168, page C6-2007
        """
        dst_str, src_str = self._reg_to_str(dst), self._reg_to_str(src)
        self.emit(Instruction(
            template="mvn {dst}, {src}",
            dsts=[dst_str],
            srcs=[src_str],
            kwargs=dict(dst=dst_str, src=src_str)
        ))

    # Shift operations (logical shifts)
    def LSL(self, dst: RegArg, src: RegArg, shift: int):
        """
        Logical Shift Left (immediate):
        Performs a logical left shift of a register value by an immediate amount,
        and writes the result to the destination register.

            dst = src << shift

        Reference: Part of MOV instruction with LSL shift
        """
        if not (0 <= shift <= 63):
            raise ValueError("LSL shift amount must be 0-63")
        dst_str, src_str = self._reg_to_str(dst), self._reg_to_str(src)
        self.emit(Instruction(
            template="lsl {dst}, {src}, #{shift}",
            dsts=[dst_str],
            srcs=[src_str],
            kwargs=dict(dst=dst_str, src=src_str, shift=shift)
        ))

    def LSR(self, dst: RegArg, src: RegArg, shift: int):
        """
        Logical Shift Right (immediate):
        Performs a logical right shift of a register value by an immediate amount,
        and writes the result to the destination register.

            dst = src >> shift (logical)

        Reference: Part of MOV instruction with LSR shift
        """
        if not (0 <= shift <= 63):
            raise ValueError("LSR shift amount must be 0-63")
        dst_str, src_str = self._reg_to_str(dst), self._reg_to_str(src)
        self.emit(Instruction(
            template="lsr {dst}, {src}, #{shift}",
            dsts=[dst_str],
            srcs=[src_str],
            kwargs=dict(dst=dst_str, src=src_str, shift=shift)
        ))

    def ASR(self, dst: RegArg, src: RegArg, shift: int):
        """
        Arithmetic Shift Right (immediate):
        Performs an arithmetic right shift of a register value by an immediate amount,
        and writes the result to the destination register.

            dst = src >> shift (arithmetic, sign-extended)

        Reference: Part of MOV instruction with ASR shift
        """
        if not (0 <= shift <= 63):
            raise ValueError("ASR shift amount must be 0-63")
        dst_str, src_str = self._reg_to_str(dst), self._reg_to_str(src)
        self.emit(Instruction(
            template="asr {dst}, {src}, #{shift}",
            dsts=[dst_str],
            srcs=[src_str],
            kwargs=dict(dst=dst_str, src=src_str, shift=shift)
        ))

    # MOV instructions - data movement operations (logically related to bit manipulation)
    def MOV(self, dst: RegArg, src: RegArg):
        """
        Move register:
        This instruction copies the value from the source register to the destination register.

            dst = src

        Reference: A-profile: section C6.2.159, page C6-1990
        """
        dst_str, src_str = self._reg_to_str(dst), self._reg_to_str(src)
        self.emit(Instruction(
            template="mov {dst}, {src}",
            dsts=[dst_str],
            srcs=[src_str],
            kwargs=dict(dst=dst_str, src=src_str)
        ))

    def MOV_imm(self, dst: RegArg, imm: int):
        """
        Move immediate:
        This instruction moves a 16-bit immediate value to the destination register.

            dst = imm (16-bit immediate)

        For 64-bit values, use MOVZ/MOVK or multiple MOV instructions.
        Reference: A-profile: section C6.2.159, page C6-1990
        """
        if not (0 <= imm <= 65535):
            raise ValueError("MOV immediate must be 16-bit (0-65535)")
        dst_str = self._reg_to_str(dst)
        self.emit(Instruction(
            template="mov {dst}, #{imm}",
            dsts=[dst_str],
            srcs=[],
            kwargs=dict(dst=dst_str, imm=imm)
        ))

    def MOVZ(self, dst: RegArg, imm: int, shift: int = 0):
        """
        Move wide with zero:
        This instruction moves a 16-bit immediate value to the destination register,
        shifting it left by 0, 16, 32, or 48 bits, and zeroing the other bits.

            dst = imm << shift (with zero extension)

        Useful for loading large constants.
        Reference: A-profile: section C6.2.170, page C6-2015
        """
        if not (0 <= imm <= 65535):
            raise ValueError("MOVZ immediate must be 16-bit (0-65535)")
        if shift not in [0, 16, 32, 48]:
            raise ValueError("MOVZ shift must be 0, 16, 32, or 48")
        dst_str = self._reg_to_str(dst)
        if shift == 0:
            template = "movz {dst}, #{imm}"
            kwargs = dict(dst=dst_str, imm=imm)
        else:
            template = "movz {dst}, #{imm}, lsl #{shift}"
            kwargs = dict(dst=dst_str, imm=imm, shift=shift)
        self.emit(Instruction(
            template=template,
            dsts=[dst_str],
            srcs=[],
            kwargs=kwargs
        ))

    def MOVK(self, dst: RegArg, imm: int, shift: int):
        """
        Move wide with keep:
        This instruction moves a 16-bit immediate value to the destination register,
        shifting it left by 0, 16, 32, or 48 bits, and keeping the other bits unchanged.

            dst[shift+15:shift] = imm (keep other bits)

        Used with MOVZ to build large 64-bit constants.
        Reference: A-profile: section C6.2.169, page C6-2013
        """
        if not (0 <= imm <= 65535):
            raise ValueError("MOVK immediate must be 16-bit (0-65535)")
        if shift not in [0, 16, 32, 48]:
            raise ValueError("MOVK shift must be 0, 16, 32, or 48")
        dst_str = self._reg_to_str(dst)
        self.emit(Instruction(
            template="movk {dst}, #{imm}, lsl #{shift}",
            dsts=[dst_str],
            srcs=[dst_str],  # dst is also a source (keeping some bits)
            kwargs=dict(dst=dst_str, imm=imm, shift=shift)
        ))
