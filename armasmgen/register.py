# armasmgen/register.py
"""
Register management system for AArch64 assembly generation.

Provides:
- Register class for representing physical and virtual registers
- Register pools for organizing registers by type and calling convention
- Virtual register support for macro blocks and register allocation
"""

from typing import Optional, Set, List, Union
from enum import Enum


class RegisterType(Enum):
    """Types of registers in AArch64"""
    GENERAL = "general"    # x0-x30, w0-w30
    VECTOR = "vector"      # v0-v31, d0-d31, s0-s31, h0-h31, b0-b31
    SPECIAL = "special"    # sp, lr, etc.


class RegisterWidth(Enum):
    """Register width variants"""
    # General purpose registers
    X = "x"     # 64-bit
    W = "w"     # 32-bit
    
    # Vector registers  
    V = "v"     # 128-bit vector
    Q = "q"     # 128-bit vector (explicit quad-word)
    D = "d"     # 64-bit scalar
    S = "s"     # 32-bit scalar
    H = "h"     # 16-bit scalar
    B = "b"     # 8-bit scalar


class Register:
    """
    Represents a register in AArch64 architecture.
    Can be physical (x0, v1) or virtual (X<tmp>, V<local>).
    """
    
    def __init__(self, 
                 name: str,
                 reg_type: RegisterType,
                 width: RegisterWidth,
                 number: Optional[int] = None,
                 is_virtual: bool = False,
                 virtual_name: Optional[str] = None):
        self.name = name
        self.reg_type = reg_type
        self.width = width
        self.number = number
        self.is_virtual = is_virtual
        self.virtual_name = virtual_name
        
        # Validate physical register numbers
        if not is_virtual and number is not None:
            if reg_type == RegisterType.GENERAL and not (0 <= number <= 30):
                raise ValueError(f"General register number must be 0-30, got {number}")
            elif reg_type == RegisterType.VECTOR and not (0 <= number <= 31):
                raise ValueError(f"Vector register number must be 0-31, got {number}")
    
    def __str__(self) -> str:
        """String representation for assembly output"""
        if self.is_virtual:
            if self.virtual_name:
                return f"{self.width.value.upper()}<{self.virtual_name}>"
            else:
                return f"{self.width.value.upper()}<{self.name}>"
        return self.name
    
    def __repr__(self) -> str:
        return f"Register({self.name}, {self.reg_type.value}, {self.width.value}, virtual={self.is_virtual})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Register):
            return False
        return (self.name == other.name and 
                self.reg_type == other.reg_type and
                self.width == other.width and
                self.is_virtual == other.is_virtual)
    
    def __hash__(self) -> int:
        return hash((self.name, self.reg_type, self.width, self.is_virtual))
    
    def get_alias(self, new_width: RegisterWidth) -> 'Register':
        """
        Get another width view of the same physical register.
        e.g., x0.get_alias(RegisterWidth.W) -> w0
        """
        if self.is_virtual:
            return Register(
                name=f"{new_width.value}{self.number}" if self.number is not None else self.name,
                reg_type=self.reg_type,
                width=new_width,
                number=self.number,
                is_virtual=True,
                virtual_name=self.virtual_name
            )
        
        if self.number is None:
            raise ValueError("Cannot create alias for register without number")
        
        new_name = f"{new_width.value}{self.number}"
        return Register(new_name, self.reg_type, new_width, self.number, False)
    
    @classmethod
    def physical(cls, name: str, reg_type: RegisterType, width: RegisterWidth, number: int) -> 'Register':
        """Create a physical register"""
        return cls(name, reg_type, width, number, False)
    
    @classmethod
    def virtual(cls, name: str, reg_type: RegisterType, width: RegisterWidth, virtual_name: Optional[str] = None) -> 'Register':
        """Create a virtual register"""
        return cls(name, reg_type, width, None, True, virtual_name)


# Convenience functions for creating common registers
def x_reg(n: int) -> Register:
    """Create x register (64-bit general purpose)"""
    return Register.physical(f"x{n}", RegisterType.GENERAL, RegisterWidth.X, n)

def w_reg(n: int) -> Register:
    """Create w register (32-bit general purpose)"""
    return Register.physical(f"w{n}", RegisterType.GENERAL, RegisterWidth.W, n)

def v_reg(n: int) -> Register:
    """Create v register (128-bit vector)"""
    return Register.physical(f"v{n}", RegisterType.VECTOR, RegisterWidth.V, n)

def q_reg(n: int) -> Register:
    """Create q register (128-bit vector, explicit quad-word)"""
    return Register.physical(f"q{n}", RegisterType.VECTOR, RegisterWidth.Q, n)

def d_reg(n: int) -> Register:
    """Create d register (64-bit vector scalar)"""
    return Register.physical(f"d{n}", RegisterType.VECTOR, RegisterWidth.D, n)
    return Register.physical(f"d{n}", RegisterType.VECTOR, RegisterWidth.D, n)

def virtual_x(name: str) -> Register:
    """Create virtual x register"""
    return Register.virtual(f"X<{name}>", RegisterType.GENERAL, RegisterWidth.X, name)

def virtual_v(name: str) -> Register:
    """Create virtual v register"""
    return Register.virtual(f"V<{name}>", RegisterType.VECTOR, RegisterWidth.V, name)


class RegisterPool:
    """
    Manages a collection of registers with allocation and tracking capabilities.
    """
    
    def __init__(self, name: str, registers: List[Register]):
        self.name = name
        self.registers = set(registers)
        self.allocated = set()  # Currently allocated registers
        self.reserved = set()   # Reserved registers (never allocated)
    
    def reserve(self, reg: Register) -> None:
        """Reserve a register so it won't be allocated"""
        if reg not in self.registers:
            raise ValueError(f"Register {reg} not in pool {self.name}")
        self.reserved.add(reg)
    
    def unreserve(self, reg: Register) -> None:
        """Remove reservation from a register"""
        self.reserved.discard(reg)
    
    def allocate(self, reg: Optional[Register] = None) -> Register:
        """
        Allocate a register. If reg is None, allocate any available register.
        """
        if reg is not None:
            if reg not in self.registers:
                raise ValueError(f"Register {reg} not in pool {self.name}")
            if reg in self.reserved:
                raise ValueError(f"Register {reg} is reserved")
            if reg in self.allocated:
                raise ValueError(f"Register {reg} is already allocated")
            self.allocated.add(reg)
            return reg
        
        # Find first available register
        available = self.registers - self.allocated - self.reserved
        if not available:
            raise RuntimeError(f"No available registers in pool {self.name}")
        
        reg = next(iter(available))
        self.allocated.add(reg)
        return reg
    
    def free(self, reg: Register) -> None:
        """Free an allocated register"""
        self.allocated.discard(reg)
    
    def free_all(self) -> None:
        """Free all allocated registers"""
        self.allocated.clear()
    
    def get_available(self) -> Set[Register]:
        """Get all available (unallocated, unreserved) registers"""
        return self.registers - self.allocated - self.reserved
    
    def get_allocated(self) -> Set[Register]:
        """Get all currently allocated registers"""
        return self.allocated.copy()
    
    def __len__(self) -> int:
        return len(self.registers)
    
    def __contains__(self, reg: Register) -> bool:
        return reg in self.registers
    
    def __str__(self) -> str:
        return f"RegisterPool({self.name}: {len(self.registers)} registers)"


class AArch64RegisterPools:
    """
    Standard AArch64 register pools with calling convention classifications.
    """
    
    def __init__(self):
        # Create all physical registers
        self.all_x_regs = [x_reg(i) for i in range(31)]  # x0-x30
        self.all_w_regs = [w_reg(i) for i in range(31)]  # w0-w30
        self.all_v_regs = [v_reg(i) for i in range(32)]  # v0-v31
        
        # General purpose register pools
        self.x_pool = RegisterPool("x_registers", self.all_x_regs)
        self.w_pool = RegisterPool("w_registers", self.all_w_regs)
        
        # Vector register pool
        self.v_pool = RegisterPool("v_registers", self.all_v_regs)
        
        # Calling convention pools (AArch64 AAPCS)
        # Caller-saved (scratch) registers
        self.x_caller_saved = RegisterPool("x_caller_saved", [x_reg(i) for i in range(18)])  # x0-x17
        self.v_caller_saved = RegisterPool("v_caller_saved", [v_reg(i) for i in range(8)])   # v0-v7
        
        # Callee-saved registers  
        self.x_callee_saved = RegisterPool("x_callee_saved", [x_reg(i) for i in range(19, 29)])  # x19-x28
        self.v_callee_saved = RegisterPool("v_callee_saved", [v_reg(i) for i in range(8, 16)])   # v8-v15
        
        # Parameter/return registers
        self.x_param_regs = RegisterPool("x_parameters", [x_reg(i) for i in range(8)])      # x0-x7
        self.v_param_regs = RegisterPool("v_parameters", [v_reg(i) for i in range(8)])      # v0-v7
        
        # Special registers (reserved by default)
        self.x_pool.reserve(x_reg(29))  # x29 = frame pointer
        self.x_pool.reserve(x_reg(30))  # x30 = link register
        
        # Virtual register pools
        self.virtual_x_pool = RegisterPool("virtual_x", [])
        self.virtual_v_pool = RegisterPool("virtual_v", [])
    
    def create_virtual_register(self, name: str, reg_type: RegisterType, width: RegisterWidth) -> Register:
        """Create and add a virtual register to appropriate pool"""
        virtual_reg = Register.virtual(f"{width.value.upper()}<{name}>", reg_type, width, name)
        
        if reg_type == RegisterType.GENERAL:
            self.virtual_x_pool.registers.add(virtual_reg)
        elif reg_type == RegisterType.VECTOR:
            self.virtual_v_pool.registers.add(virtual_reg)
        
        return virtual_reg
    
    def get_pool_by_type(self, reg_type: RegisterType, width: RegisterWidth, virtual: bool = False) -> RegisterPool:
        """Get appropriate register pool for given type and width"""
        if virtual:
            if reg_type == RegisterType.GENERAL:
                return self.virtual_x_pool
            elif reg_type == RegisterType.VECTOR:
                return self.virtual_v_pool
            else:
                raise ValueError(f"Unsupported virtual register type: {reg_type}")
        else:
            if reg_type == RegisterType.GENERAL:
                return self.x_pool if width == RegisterWidth.X else self.w_pool
            elif reg_type == RegisterType.VECTOR:
                return self.v_pool
            else:
                raise ValueError(f"Unsupported register type: {reg_type}")


# Global instance for convenience
aarch64_pools = AArch64RegisterPools()
