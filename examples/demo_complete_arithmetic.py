#!/usr/bin/env python3
"""
Demo: Complete arithmetic instruction set showcase
Demonstrates all arithmetic instructions in ArmAsmGen.
"""

from armasmgen import ASMCode, Block, x_reg, virtual_x

def demo_complete_arithmetic():
    """Showcase all arithmetic instructions"""
    print("=== Complete Arithmetic Instruction Set ===")
    
    f = ASMCode()
    with f as asm:
        asm.equ("DEMO_CONSTANT", "42")
        
        with Block(label="arithmetic_showcase") as m:
            # Basic arithmetic
            print("Basic arithmetic:")
            m.ADD("x0", "x1", "x2")              # Add registers
            m.ADD_imm("x3", "x4", 100)           # Add immediate
            m.SUB("x5", "x6", "x7")              # Subtract registers  
            m.SUB_imm("x8", "x9", 50)            # Subtract immediate
            m.MUL("x10", "x11", "x12")           # Multiply
            
            print("Advanced multiply operations:")
            # Advanced multiply
            m.MADD("x13", "x14", "x15", "x16")   # Multiply-add: x13 = x16 + (x14 * x15)
            m.MSUB("x17", "x18", "x19", "x20")   # Multiply-subtract: x17 = x20 - (x18 * x19)
            m.MNEG("x21", "x22", "x23")          # Multiply-negate: x21 = -(x22 * x23)
            
            print("High multiply (for wide arithmetic):")
            # High multiply for wide arithmetic
            m.UMULH("x24", "x25", "x26")         # Unsigned multiply high
            m.SMULH("x27", "x28", "x29")         # Signed multiply high
            
            print("Flag-setting arithmetic:")
            # Flag-setting arithmetic (essential for multi-precision)
            m.ADDS("x0", "x1", "x2")             # Add and set flags
            m.ADDS_imm("x3", "x4", 200)          # Add immediate and set flags
            m.ADCS("x5", "x6", "x7")             # Add with carry and set flags
            m.ADCS_imm("x8", "x9", 0)            # Add with carry (propagate only)
            
            m.SUBS("x10", "x11", "x12")          # Subtract and set flags
            m.SUBS_imm("x13", "x14", 75)         # Subtract immediate and set flags
            m.SBCS("x15", "x16", "x17")          # Subtract with carry and set flags
    
    f.stdout()


def demo_practical_crypto_example():
    """Practical example: RSA-style big integer multiplication"""
    print("\n=== Practical Example: Cryptographic Multiplication ===")
    
    f = ASMCode()
    with f as asm:
        asm.equ("RSA_COMMENT", "// 256-bit modular multiplication core")
        
        with Block(label="crypto_multiply") as m:
            # Simulate part of Montgomery multiplication or similar
            # This is a simplified version of what might appear in cryptographic code
            
            # Load operands (in real crypto, these would come from memory)
            a0, a1 = virtual_x("a0"), virtual_x("a1")  # 128-bit A
            b0, b1 = virtual_x("b0"), virtual_x("b1")  # 128-bit B
            
            # Step 1: Partial products (A × B)
            m.MUL(a0, "x0", "x4")             # A_low * B_low -> low
            m.UMULH(a1, "x0", "x4")           # A_low * B_low -> high
            
            temp1, temp2 = virtual_x("temp1"), virtual_x("temp2")
            m.MUL(temp1, "x0", "x5")          # A_low * B_high -> low  
            m.UMULH(temp2, "x0", "x5")        # A_low * B_high -> high
            
            # Step 2: Add with carry propagation
            m.ADDS(a1, a1, temp1)            # Add cross terms
            carry = virtual_x("carry")
            m.ADCS(carry, temp2, "xzr")       # Capture carry
            
            # Step 3: Continue building full product...
            # (In real crypto, this would continue with modular reduction)
            result_low = virtual_x("result_low")
            result_high = virtual_x("result_high")
            
            m.ADD(result_low, a0, "xzr")      # Store low result
            m.ADD(result_high, a1, carry)     # Store high result
            
            # Step 4: Store results (in real code, back to memory)
            m.ADD("x20", result_low, "xzr")   # Output low 64 bits
            m.ADD("x21", result_high, "xzr")  # Output high 64 bits
    
    f.stdout()


if __name__ == "__main__":
    demo_complete_arithmetic()
    demo_practical_crypto_example()
    
    print("\n=== ArmAsmGen Arithmetic Instructions Summary ===")
    print("Basic Operations:")
    print("  ✓ ADD/ADD_imm - Addition with register/immediate")
    print("  ✓ SUB/SUB_imm - Subtraction with register/immediate")
    print("  ✓ MUL - Basic multiplication")
    print("")
    print("Advanced Multiply:")
    print("  ✓ MADD - Multiply-add (a + b×c)")
    print("  ✓ MSUB - Multiply-subtract (a - b×c)")  
    print("  ✓ MNEG - Multiply-negate (-(a×b))")
    print("")
    print("Wide Arithmetic:")
    print("  ✓ UMULH - Unsigned multiply high (upper 64 bits)")
    print("  ✓ SMULH - Signed multiply high (upper 64 bits)")
    print("")
    print("Multi-Precision Support:")
    print("  ✓ ADDS/ADDS_imm - Add and set flags")
    print("  ✓ ADCS/ADCS_imm - Add with carry")
    print("  ✓ SUBS/SUBS_imm - Subtract and set flags")
    print("  ✓ SBCS - Subtract with carry")
    print("")
    print("Applications:")
    print("  • Big integer arithmetic")
    print("  • Cryptographic operations")
    print("  • High-precision calculations")
    print("  • Multi-word operations")
    print("  • Error detection and correction")
