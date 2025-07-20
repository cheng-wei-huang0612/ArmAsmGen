# asm_printer/mixins/memory.py
from ..core import Instruction, RegArg

class MemoryMixin:
    def emit(self, inst: Instruction): ...
    def _reg_to_str(self, reg: RegArg) -> str: ...  # 型別提示

    def LDR(self, dst: RegArg, addr: RegArg):
        dst_str, addr_str = self._reg_to_str(dst), self._reg_to_str(addr)
        self.emit(Instruction(
            template="ldr {dst}, [{addr}]",
            dsts=[dst_str],
            srcs=[addr_str],
            kwargs=dict(dst=dst_str, addr=addr_str)
        ))

    def LDR_offset(self, dst: RegArg, base: RegArg, offset: int):
        """Load with immediate offset: ldr dst, [base, #offset]"""
        if not (-256 <= offset <= 255):
            raise ValueError("LDR offset must be in range [-256, 255]")
        dst_str, base_str = self._reg_to_str(dst), self._reg_to_str(base)
        self.emit(Instruction(
            template="ldr {dst}, [{base}, #{offset}]",
            dsts=[dst_str],
            srcs=[base_str],
            kwargs=dict(dst=dst_str, base=base_str, offset=offset)
        ))

    def LDR_pre(self, dst: RegArg, base: RegArg, offset: int):
        """Load with pre-indexed addressing: ldr dst, [base, #offset]! (base = base + offset first)"""
        if not (-256 <= offset <= 255):
            raise ValueError("LDR pre-index offset must be in range [-256, 255]")
        dst_str, base_str = self._reg_to_str(dst), self._reg_to_str(base)
        self.emit(Instruction(
            template="ldr {dst}, [{base}, #{offset}]!",
            dsts=[dst_str, base_str],  # base register is modified
            srcs=[base_str],
            kwargs=dict(dst=dst_str, base=base_str, offset=offset)
        ))

    def LDR_post(self, dst: RegArg, base: RegArg, offset: int):
        """Load with post-indexed addressing: ldr dst, [base], #offset (load first, then base = base + offset)"""
        if not (-256 <= offset <= 255):
            raise ValueError("LDR post-index offset must be in range [-256, 255]")
        dst_str, base_str = self._reg_to_str(dst), self._reg_to_str(base)
        self.emit(Instruction(
            template="ldr {dst}, [{base}], #{offset}",
            dsts=[dst_str, base_str],  # base register is modified
            srcs=[base_str],
            kwargs=dict(dst=dst_str, base=base_str, offset=offset)
        ))

    def LDP(self, dst1: RegArg, dst2: RegArg, addr: RegArg):
        """Load pair of registers: ldp dst1, dst2, [addr]"""
        dst1_str, dst2_str, addr_str = self._reg_to_str(dst1), self._reg_to_str(dst2), self._reg_to_str(addr)
        self.emit(Instruction(
            template="ldp {dst1}, {dst2}, [{addr}]",
            dsts=[dst1_str, dst2_str],
            srcs=[addr_str],
            kwargs=dict(dst1=dst1_str, dst2=dst2_str, addr=addr_str)
        ))

    def LDP_offset(self, dst1: RegArg, dst2: RegArg, base: RegArg, offset: int):
        """Load pair with offset: ldp dst1, dst2, [base, #offset]"""
        if offset % 8 != 0 or not (-512 <= offset <= 504):
            raise ValueError("LDP offset must be 8-byte aligned and in range [-512, 504]")
        dst1_str, dst2_str, base_str = self._reg_to_str(dst1), self._reg_to_str(dst2), self._reg_to_str(base)
        self.emit(Instruction(
            template="ldp {dst1}, {dst2}, [{base}, #{offset}]",
            dsts=[dst1_str, dst2_str],
            srcs=[base_str],
            kwargs=dict(dst1=dst1_str, dst2=dst2_str, base=base_str, offset=offset)
        ))

    def STR(self, src: RegArg, addr: RegArg):
        src_str, addr_str = self._reg_to_str(src), self._reg_to_str(addr)
        self.emit(Instruction(
            template="str {src}, [{addr}]",
            dsts=[],              # 寫入記憶體
            srcs=[src_str, addr_str],
            kwargs=dict(src=src_str, addr=addr_str)
        ))

    def STR_offset(self, src: RegArg, base: RegArg, offset: int):
        """Store with immediate offset: str src, [base, #offset]"""
        if not (-256 <= offset <= 255):
            raise ValueError("STR offset must be in range [-256, 255]")
        src_str, base_str = self._reg_to_str(src), self._reg_to_str(base)
        self.emit(Instruction(
            template="str {src}, [{base}, #{offset}]",
            dsts=[],
            srcs=[src_str, base_str],
            kwargs=dict(src=src_str, base=base_str, offset=offset)
        ))

    def STR_pre(self, src: RegArg, base: RegArg, offset: int):
        """Store with pre-indexed addressing: str src, [base, #offset]!"""
        if not (-256 <= offset <= 255):
            raise ValueError("STR pre-index offset must be in range [-256, 255]")
        src_str, base_str = self._reg_to_str(src), self._reg_to_str(base)
        self.emit(Instruction(
            template="str {src}, [{base}, #{offset}]!",
            dsts=[base_str],  # base register is modified
            srcs=[src_str, base_str],
            kwargs=dict(src=src_str, base=base_str, offset=offset)
        ))

    def STR_post(self, src: RegArg, base: RegArg, offset: int):
        """Store with post-indexed addressing: str src, [base], #offset"""
        if not (-256 <= offset <= 255):
            raise ValueError("STR post-index offset must be in range [-256, 255]")
        src_str, base_str = self._reg_to_str(src), self._reg_to_str(base)
        self.emit(Instruction(
            template="str {src}, [{base}], #{offset}",
            dsts=[base_str],  # base register is modified
            srcs=[src_str, base_str],
            kwargs=dict(src=src_str, base=base_str, offset=offset)
        ))

    def STP(self, src1: RegArg, src2: RegArg, addr: RegArg):
        """Store pair of registers: stp src1, src2, [addr]"""
        src1_str, src2_str, addr_str = self._reg_to_str(src1), self._reg_to_str(src2), self._reg_to_str(addr)
        self.emit(Instruction(
            template="stp {src1}, {src2}, [{addr}]",
            dsts=[],
            srcs=[src1_str, src2_str, addr_str],
            kwargs=dict(src1=src1_str, src2=src2_str, addr=addr_str)
        ))

    def STP_offset(self, src1: RegArg, src2: RegArg, base: RegArg, offset: int):
        """Store pair with offset: stp src1, src2, [base, #offset]"""
        if offset % 8 != 0 or not (-512 <= offset <= 504):
            raise ValueError("STP offset must be 8-byte aligned and in range [-512, 504]")
        src1_str, src2_str, base_str = self._reg_to_str(src1), self._reg_to_str(src2), self._reg_to_str(base)
        self.emit(Instruction(
            template="stp {src1}, {src2}, [{base}, #{offset}]",
            dsts=[],
            srcs=[src1_str, src2_str, base_str],
            kwargs=dict(src1=src1_str, src2=src2_str, base=base_str, offset=offset)
        ))

    def STP_stack_offset(self, src0: RegArg, src1: RegArg, imm: int):
        if imm % 16:
            raise ValueError("stack offset must be 16-byte aligned")
        src0_str, src1_str = self._reg_to_str(src0), self._reg_to_str(src1)
        self.emit(Instruction(
            template="stp {src0}, {src1}, [sp, #{imm}]",
            dsts=["stack"],
            srcs=[src0_str, src1_str],
            kwargs=dict(src0=src0_str, src1=src1_str, imm=imm)
        ))