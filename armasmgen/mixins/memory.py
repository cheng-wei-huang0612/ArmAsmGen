# asm_printer/mixins/memory.py
from ..core import Instruction

class MemoryMixin:
    def emit(self, inst: Instruction): ...

    def LDR(self, dst, addr):
        self.emit(Instruction(
            template="ldr {dst}, [{addr}]",
            dsts=[dst],
            srcs=[addr],
            kwargs=dict(dst=dst, addr=addr)
        ))

    def STR(self, src, addr):
        self.emit(Instruction(
            template="str {src}, [{addr}]",
            dsts=[],              # 寫入記憶體
            srcs=[src, addr],
            kwargs=dict(src=src, addr=addr)
        ))

    def STP_stack_offset(self, src0, src1, imm):
        if imm % 16:
            raise ValueError("stack offset must be 16-byte aligned")
        self.emit(Instruction(
            template="stp {src0}, {src1}, [sp, #{imm}]",
            dsts=["stack"],
            srcs=[src0, src1],
            kwargs=dict(src0=src0, src1=src1, imm=imm)
        ))