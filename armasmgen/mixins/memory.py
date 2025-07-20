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

    def STR(self, src: RegArg, addr: RegArg):
        src_str, addr_str = self._reg_to_str(src), self._reg_to_str(addr)
        self.emit(Instruction(
            template="str {src}, [{addr}]",
            dsts=[],              # 寫入記憶體
            srcs=[src_str, addr_str],
            kwargs=dict(src=src_str, addr=addr_str)
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