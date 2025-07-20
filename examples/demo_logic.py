#!/usr/bin/env python3
"""
Demo: Logic instructions (AND, ORR, EOR, shifts, etc.)
Shows bitwise operations and logical shifts.
"""

from armasmgen import ASMCode, Block, x_reg, virtual_x

def demo_basic_logic():
    """Basic logical operations"""
    print("=== Basic Logical Operations ===")
    
    f = ASMCode()
    with f as asm:
        with Block(label="logic_demo") as m:
            # Basic bitwise operations
            m.AND("x0", "x1", "x2")          # x0 = x1 & x2
            m.ORR("x3", "x4", "x5")          # x3 = x4 | x5
            m.EOR("x6", "x7", "x8")          # x6 = x7 ^ x8
            
            # Bitwise operations with immediates
            m.AND_imm("x9", "x10", 0xFF)     # x9 = x10 & 0xFF (mask lower 8 bits)
            m.ORR_imm("x11", "x12", 0x100)   # x11 = x12 | 0x100 (set bit 8)
            m.EOR_imm("x13", "x14", 0xFFFF)  # x13 = x14 ^ 0xFFFF (invert lower 16 bits)
    
    f.stdout()


def demo_advanced_logic():
    """Advanced logical operations"""
    print("\n=== Advanced Logical Operations ===")
    
    f = ASMCode()
    with f as asm:
        with Block(label="advanced_logic") as m:
            # NOT variants
            m.BIC("x0", "x1", "x2")    # x0 = x1 & (~x2) - bit clear
            m.ORN("x3", "x4", "x5")    # x3 = x4 | (~x5) - OR NOT
            m.EON("x6", "x7", "x8")    # x6 = x7 ^ (~x8) - XOR NOT
            m.MVN("x9", "x10")         # x9 = ~x10 - move NOT
    
    f.stdout()


def demo_shifts():
    """Shift operations"""
    print("\n=== Shift Operations ===")
    
    f = ASMCode()
    with f as asm:
        with Block(label="shifts") as m:
            # Logical shifts
            m.LSL("x0", "x1", 4)      # x0 = x1 << 4 (multiply by 16)
            m.LSR("x2", "x3", 8)      # x2 = x3 >> 8 (divide by 256, unsigned)
            m.ASR("x4", "x5", 2)      # x4 = x5 >> 2 (divide by 4, signed)
            
            # Combining with virtual registers
            temp = virtual_x("shifted")
            m.LSL(temp, "x6", 1)      # temp = x6 << 1 (multiply by 2)
            m.ORR("x7", temp, "x8")   # x7 = (x6 << 1) | x8
    
    f.stdout()


def demo_bit_manipulation():
    """Bit manipulation patterns"""
    print("\n=== Bit Manipulation Patterns ===")
    
    f = ASMCode()
    with f as asm:
        asm.equ("MASK_LOWER_8", "0xFF")
        asm.equ("MASK_UPPER_8", "0xFF00")
        asm.equ("BIT_FLAG", "0x80")
        
        with Block(label="bit_ops") as m:
            # Extract lower 8 bits
            m.AND_imm("x0", "x1", 0xFF)
            
            # Set specific bits
            m.ORR_imm("x2", "x3", 0x80)  # Set bit 7
            
            # Clear specific bits  
            m.BIC("x4", "x5", "x6")       # Clear bits specified in x6
            
            # Toggle bits
            m.EOR_imm("x7", "x8", 0xAA)   # Toggle alternating bits
            
            # Combine operations for complex manipulations
            temp1 = virtual_x("masked")
            temp2 = virtual_x("shifted")
            
            m.AND_imm(temp1, "x9", 0xFF)    # Extract lower byte
            m.LSL(temp2, temp1, 8)          # Shift to upper byte position
            m.ORR("x10", "x11", temp2)      # Combine with existing value
    
    f.stdout()


def demo_mixed_operations():
    """Mixed register types with logic operations"""
    print("\n=== Mixed Register Types ===")
    
    f = ASMCode()
    with f as asm:
        # Use both physical and virtual registers
        reg_x0 = x_reg(0)
        virt_tmp = virtual_x("temp")
        virt_result = virtual_x("result")
        
        with Block(label="mixed_logic") as m:
            # Mix physical, virtual, and string registers
            m.AND(virt_tmp, reg_x0, "x1")
            m.ORR(virt_result, virt_tmp, "x2") 
            m.EOR("x3", virt_result, reg_x0)
            
            # Shifts with mixed types
            m.LSL(virt_tmp, reg_x0, 4)
            m.LSR("x4", virt_tmp, 2)
    
    f.stdout()


if __name__ == "__main__":
    demo_basic_logic()
    demo_advanced_logic()
    demo_shifts()
    demo_bit_manipulation()
    demo_mixed_operations()
    
    print("\n=== Logic Mixin Summary ===")
    print("✓ Basic bitwise operations (AND, ORR, EOR)")
    print("✓ Immediate value variants")
    print("✓ Advanced operations (BIC, ORN, EON, MVN)")
    print("✓ Shift operations (LSL, LSR, ASR)")
    print("✓ Bit manipulation patterns")
    print("✓ Mixed register type support")
    print("✓ Virtual register integration")
