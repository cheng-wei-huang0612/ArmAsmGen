#!/usr/bin/env python3
"""
Demo: Custom mixin combinations and comprehensive instruction usage
"""

from armasmgen import (
    ASMCode, Block, 
    ArithmeticMixin, MemoryMixin, LogicMixin,
    x_reg, virtual_x
)
from armasmgen.core import BaseAsm

# Create a custom class with only specific mixins
class CustomLogicBlock(BaseAsm, LogicMixin, ArithmeticMixin):
    """Custom block with only logic and arithmetic operations"""
    def __init__(self, label=None):
        super().__init__()
        self.label = label

def demo_comprehensive_usage():
    """Comprehensive demo using all instruction types"""
    print("=== Comprehensive Instruction Usage ===")
    
    f = ASMCode()
    
    with f as asm:
        asm.equ("DATA_MASK", "0xFF")
        asm.equ("SHIFT_AMOUNT", "4")
        
        with Block(label="comprehensive_demo") as m:
            # Physical and virtual registers
            input_reg = x_reg(0)
            temp_reg = virtual_x("temp")
            mask_reg = virtual_x("mask")
            result_reg = virtual_x("result")
            
            # 1. Arithmetic operations
            print("1. Arithmetic operations")
            m.ADD(temp_reg, input_reg, "x1")      # temp = input + x1
            m.MUL(result_reg, temp_reg, "x2")     # result = temp * x2  
            m.SUB_imm("x3", result_reg, 10)       # x3 = result - 10
            
            # 2. Logic operations  
            print("2. Logic operations")
            m.AND_imm(mask_reg, "x4", 0xFF)       # mask = x4 & 0xFF
            m.ORR(temp_reg, result_reg, mask_reg) # temp = result | mask
            m.EOR_imm("x5", temp_reg, 0xAA)       # x5 = temp ^ 0xAA
            
            # 3. Bit manipulation
            print("3. Bit manipulation")
            m.LSL(temp_reg, "x6", 4)              # temp = x6 << 4
            m.LSR("x7", temp_reg, 2)              # x7 = temp >> 2
            m.BIC("x8", "x9", temp_reg)           # x8 = x9 & (~temp)
            
            # 4. Memory operations
            print("4. Memory operations")
            m.LDR("x10", "x11")                   # Load from memory
            m.STR(result_reg, "x12")              # Store to memory
            m.STP_stack_offset("x13", mask_reg, -16)  # Store pair on stack
            
            # 5. Complex operations combining all types
            print("5. Complex combined operations")
            final_result = virtual_x("final")
            
            # Load, manipulate, and store pattern
            m.LDR(temp_reg, "x20")                # Load input
            m.AND_imm(temp_reg, temp_reg, 0xFFF0) # Clear lower 4 bits
            m.ADD_imm(temp_reg, temp_reg, 0x8)    # Add constant
            m.LSL(final_result, temp_reg, 1)      # Shift left by 1
            m.STR(final_result, "x21")            # Store result
    
    f.stdout()

def demo_custom_mixin_class():
    """Demo using custom mixin combination"""
    print("\n=== Custom Mixin Class Demo ===")
    
    f = ASMCode()
    
    with f as asm:
        # Use our custom class that only has Logic and Arithmetic mixins
        custom_block = CustomLogicBlock("custom_operations")
        
        # Only arithmetic and logic operations available
        custom_block.ADD("x0", "x1", "x2")
        custom_block.AND_imm("x3", "x0", 0xFF)
        custom_block.LSL("x4", "x3", 8)
        custom_block.ORR("x5", "x4", "x2")
        
        # Add the custom block to our main assembly
        for inst in custom_block._inst:
            asm.emit(inst)
    
    f.stdout()

if __name__ == "__main__":
    demo_comprehensive_usage()
    demo_custom_mixin_class()
    
    print("\n=== Complete ArmAsmGen Capabilities ===")
    print("✓ Arithmetic: ADD, SUB, MUL, MADD, MSUB, MNEG (register & immediate)")
    print("✓ Logic: AND, ORR, EOR, BIC, ORN, EON, MVN (register & immediate)")
    print("✓ Shifts: LSL, LSR, ASR with immediate amounts")
    print("✓ Memory: LDR, STR, STP with various addressing modes")
    print("✓ Registers: Physical (x0-x30), Virtual (X<name>), Mixed usage")
    print("✓ Architecture: Modular mixins, extensible design")
    print("✓ Integration: Register pools, calling conventions, type safety")
