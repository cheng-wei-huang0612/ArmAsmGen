# asm_printer/mixins/memory.py
from ..core import Instruction, RegArg
from ..register import Register, RegisterType, RegisterWidth
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..register import Register

class MemoryMixin:
    def emit(self, inst: Instruction): ...
    def _reg_to_str(self, reg: RegArg) -> str: ...  # 型別提示
    
    def _convert_to_q_register(self, reg_str: str) -> str:
        """Convert v register to q register for 128-bit memory operations"""
        if reg_str.startswith('v') and reg_str[1:].isdigit():
            return 'q' + reg_str[1:]
        return reg_str

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

    # Vector Memory Operations with Register Validation
    def _validate_vector_register(self, reg: RegArg, param_name: str) -> str:
        """Validate vector register and return string representation"""
        reg_str = self._reg_to_str(reg)
        
        # If it's a Register object, check type
        if isinstance(reg, Register):
            if reg.reg_type != RegisterType.VECTOR:
                raise ValueError(f"Parameter '{param_name}' must be a vector register, got {reg.reg_type.value} register '{reg_str}'")
        
        # If it's a string, validate format
        elif isinstance(reg, str):
            if not (reg_str.startswith('v') or reg_str.startswith('q') or reg_str.startswith('d') or 
                   reg_str.startswith('s') or reg_str.startswith('h') or reg_str.startswith('b')):
                raise ValueError(f"Parameter '{param_name}' should be a vector register (v/q/d/s/h/b), got '{reg_str}'")
        
        return reg_str
    
    def _validate_general_register(self, reg: RegArg, param_name: str) -> str:
        """Validate general register and return string representation"""
        reg_str = self._reg_to_str(reg)
        
        # If it's a Register object, check type
        if isinstance(reg, Register):
            if reg.reg_type != RegisterType.GENERAL:
                raise ValueError(f"Parameter '{param_name}' must be a general register, got {reg.reg_type.value} register '{reg_str}'")
        
        # If it's a string, validate format
        elif isinstance(reg, str):
            if not (reg_str.startswith('x') or reg_str.startswith('w') or reg_str in {'sp', 'lr'}):
                raise ValueError(f"Parameter '{param_name}' should be a general register (x/w), got '{reg_str}'")
        
        return reg_str

    def LDR_vector(self, dst: RegArg, addr: RegArg):
        """Load vector register: ldr qN, [addr] (128-bit vector load)"""
        dst_str = self._validate_vector_register(dst, "dst")
        addr_str = self._validate_general_register(addr, "addr")
        # Convert to q register for 128-bit loads
        dst_str = self._convert_to_q_register(dst_str)
        self.emit(Instruction(
            template="ldr {dst}, [{addr}]",
            dsts=[dst_str],
            srcs=[addr_str],
            kwargs=dict(dst=dst_str, addr=addr_str)
        ))

    def STR_vector(self, src: RegArg, addr: RegArg):
        """Store vector register: str qN, [addr] (128-bit vector store)"""
        src_str = self._validate_vector_register(src, "src")
        addr_str = self._validate_general_register(addr, "addr")
        # Convert to q register for 128-bit stores
        src_str = self._convert_to_q_register(src_str)
        self.emit(Instruction(
            template="str {src}, [{addr}]",
            dsts=[],
            srcs=[src_str, addr_str],
            kwargs=dict(src=src_str, addr=addr_str)
        ))

    def LDR_vector_offset(self, dst: RegArg, base: RegArg, offset: int):
        """Load vector with offset: ldr qN, [base, #offset]"""
        if not (-256 <= offset <= 255):
            raise ValueError("LDR vector offset must be in range [-256, 255]")
        dst_str = self._validate_vector_register(dst, "dst")
        base_str = self._validate_general_register(base, "base")
        # Convert to q register for 128-bit loads
        dst_str = self._convert_to_q_register(dst_str)
        self.emit(Instruction(
            template="ldr {dst}, [{base}, #{offset}]",
            dsts=[dst_str],
            srcs=[base_str],
            kwargs=dict(dst=dst_str, base=base_str, offset=offset)
        ))

    def STR_vector_offset(self, src: RegArg, base: RegArg, offset: int):
        """Store vector with offset: str qN, [base, #offset]"""
        if not (-256 <= offset <= 255):
            raise ValueError("STR vector offset must be in range [-256, 255]")
        src_str = self._validate_vector_register(src, "src")
        base_str = self._validate_general_register(base, "base")
        # Convert to q register for 128-bit stores
        src_str = self._convert_to_q_register(src_str)
        self.emit(Instruction(
            template="str {src}, [{base}, #{offset}]",
            dsts=[],
            srcs=[src_str, base_str],
            kwargs=dict(src=src_str, base=base_str, offset=offset)
        ))

    def LDP_vector(self, dst1: RegArg, dst2: RegArg, addr: RegArg):
        """Load pair of vector registers: ldp qN1, qN2, [addr]"""
        dst1_str = self._validate_vector_register(dst1, "dst1")
        dst2_str = self._validate_vector_register(dst2, "dst2")
        addr_str = self._validate_general_register(addr, "addr")
        # Convert to q registers for 128-bit loads
        dst1_str = self._convert_to_q_register(dst1_str)
        dst2_str = self._convert_to_q_register(dst2_str)
        self.emit(Instruction(
            template="ldp {dst1}, {dst2}, [{addr}]",
            dsts=[dst1_str, dst2_str],
            srcs=[addr_str],
            kwargs=dict(dst1=dst1_str, dst2=dst2_str, addr=addr_str)
        ))

    def STP_vector(self, src1: RegArg, src2: RegArg, addr: RegArg):
        """Store pair of vector registers: stp qN1, qN2, [addr]"""
        src1_str = self._validate_vector_register(src1, "src1")
        src2_str = self._validate_vector_register(src2, "src2")
        addr_str = self._validate_general_register(addr, "addr")
        # Convert to q registers for 128-bit stores
        src1_str = self._convert_to_q_register(src1_str)
        src2_str = self._convert_to_q_register(src2_str)
        self.emit(Instruction(
            template="stp {src1}, {src2}, [{addr}]",
            dsts=[],
            srcs=[src1_str, src2_str, addr_str],
            kwargs=dict(src1=src1_str, src2=src2_str, addr=addr_str)
        ))

    def LDP_vector_offset(self, dst1: RegArg, dst2: RegArg, base: RegArg, offset: int):
        """Load pair of vectors with offset: ldp qN1, qN2, [base, #offset]"""
        if offset % 16 != 0 or not (-1024 <= offset <= 1008):
            raise ValueError("LDP vector offset must be 16-byte aligned and in range [-1024, 1008]")
        dst1_str = self._validate_vector_register(dst1, "dst1")
        dst2_str = self._validate_vector_register(dst2, "dst2")
        base_str = self._validate_general_register(base, "base")
        # Convert to q registers for 128-bit loads
        dst1_str = self._convert_to_q_register(dst1_str)
        dst2_str = self._convert_to_q_register(dst2_str)
        self.emit(Instruction(
            template="ldp {dst1}, {dst2}, [{base}, #{offset}]",
            dsts=[dst1_str, dst2_str],
            srcs=[base_str],
            kwargs=dict(dst1=dst1_str, dst2=dst2_str, base=base_str, offset=offset)
        ))

    def STP_vector_offset(self, src1: RegArg, src2: RegArg, base: RegArg, offset: int):
        """Store pair of vectors with offset: stp qN1, qN2, [base, #offset]"""
        if offset % 16 != 0 or not (-1024 <= offset <= 1008):
            raise ValueError("STP vector offset must be 16-byte aligned and in range [-1024, 1008]")
        src1_str = self._validate_vector_register(src1, "src1")
        src2_str = self._validate_vector_register(src2, "src2")
        base_str = self._validate_general_register(base, "base")
        # Convert to q registers for 128-bit stores
        src1_str = self._convert_to_q_register(src1_str)
        src2_str = self._convert_to_q_register(src2_str)
        self.emit(Instruction(
            template="stp {src1}, {src2}, [{base}, #{offset}]",
            dsts=[],
            srcs=[src1_str, src2_str, base_str],
            kwargs=dict(src1=src1_str, src2=src2_str, base=base_str, offset=offset)
        ))

    def LDR_Q(self, dst: RegArg, addr: RegArg):
        """Load Q register (explicit 128-bit): ldr qN, [addr]"""
        dst_str = self._validate_vector_register(dst, "dst")
        addr_str = self._validate_general_register(addr, "addr")
        # Always convert to q register for explicit Q operations
        dst_str = self._convert_to_q_register(dst_str)
        self.emit(Instruction(
            template="ldr {dst}, [{addr}]",
            dsts=[dst_str],
            srcs=[addr_str],
            kwargs=dict(dst=dst_str, addr=addr_str)
        ))

    def STR_Q(self, src: RegArg, addr: RegArg):
        """Store Q register (explicit 128-bit): str qN, [addr]"""
        src_str = self._validate_vector_register(src, "src")
        addr_str = self._validate_general_register(addr, "addr")
        # Always convert to q register for explicit Q operations
        src_str = self._convert_to_q_register(src_str)
        self.emit(Instruction(
            template="str {src}, [{addr}]",
            dsts=[],
            srcs=[src_str, addr_str],
            kwargs=dict(src=src_str, addr=addr_str)
        ))