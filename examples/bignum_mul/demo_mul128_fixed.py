#!/usr/bin/env python3
"""
Focused Demo: 128×128→256 bit multiplication using only physical registers
Generates clean assembly for C interop and testing with GMP.
Uses advanced ARM64 addressing modes and instruction optimizations.
"""

from armasmgen.builder import ASMCode, Block
from armasmgen.mixins.arithmetic import ArithmeticMixin
from armasmgen.mixins.memory import MemoryMixin
from armasmgen.mixins.control import ControlFlowMixin

# Combined instruction set for 128-bit multiplication
class AArch64MultiplicationISA(ArithmeticMixin, MemoryMixin, ControlFlowMixin):
    pass

def create_mul128x128():
    """Create 128×128→256 multiplication function using only physical registers and advanced addressing modes"""
    
    f = ASMCode(label="mul128x128")
    with f as asm:
        # Function signature: mul128x128(uint64_t a[2], uint64_t b[2], uint64_t result[4])
        # x0 = pointer to a[2] (128-bit input A)
        # x1 = pointer to b[2] (128-bit input B) 
        # x2 = pointer to result[4] (256-bit output)
        
        with Block(label="main") as m:
            # ✨ OPTIMIZATION 1: Use LDP for efficient 128-bit loading
            # Load both parts of A and B with single instructions
            m.LDP("x4", "x5", "x0")     # x4=a[0] (low), x5=a[1] (high)
            m.LDP("x6", "x7", "x1")     # x6=b[0] (low), x7=b[1] (high)
            
            # ✨ OPTIMIZATION 2: Compute all partial products
            # Standard 128×128→256 multiplication algorithm
            # ll = A_low × B_low, lh = A_low × B_high, hl = A_high × B_low, hh = A_high × B_high
            
            # ll = A_low * B_low (x4 * x6)
            m.MUL("x10", "x4", "x6")     # ll_low
            m.UMULH("x11", "x4", "x6")   # ll_high
            
            # lh = A_low * B_high (x4 * x7)
            m.MUL("x12", "x4", "x7")     # lh_low
            m.UMULH("x13", "x4", "x7")   # lh_high
            
            # hl = A_high * B_low (x5 * x6)
            m.MUL("x14", "x5", "x6")     # hl_low
            m.UMULH("x15", "x5", "x6")   # hl_high
            
            # hh = A_high * B_high (x5 * x7)
            m.MUL("x16", "x5", "x7")     # hh_low  
            m.UMULH("x17", "x5", "x7")   # hh_high
            
            # ✨ OPTIMIZATION 3: Efficient carry propagation with register reuse
            # Reuse x3-x6 to avoid callee-saved registers and minimize register pressure
            
            # Result[63:0] = ll_low (direct copy)
            m.MOV("x3", "x10")           # result[0] = ll_low
            
            # Result[127:64] = ll_high + lh_low + hl_low (with carry)
            m.ADDS("x4", "x11", "x12")   # ll_high + lh_low (set carry)
            m.ADCS("x4", "x4", "x14")    # + hl_low (with carry)
            
            # Result[191:128] = lh_high + hl_high + hh_low + carry
            m.ADCS("x5", "x13", "x15")   # lh_high + hl_high + previous carry
            m.ADCS("x5", "x5", "x16")    # + hh_low + carry
            
            # Result[255:192] = hh_high + final carry
            m.ADCS("x6", "x17", "xzr")   # hh_high + carry from previous
            
            # ✨ OPTIMIZATION 4: Use STP for efficient 256-bit storing
            # Store result in two 128-bit chunks
            m.STP("x3", "x4", "x2")       # Store result[0], result[1] at [x2, x2+8]
            m.STP_offset("x5", "x6", "x2", 16)  # Store result[2], result[3] at [x2+16, x2+24]
            
            # ✨ OPTIMIZATION 5: Clean function return
            m.RET()  # Standard ARM64 function return
    
    return f

def main():
    """Generate the multiplication function and export to assembly file"""
    print("=== Generating 128×128→256 Multiplication (Physical Registers Only) ===")
    
    asm_code = create_mul128x128()
    
    # Export to file
    output_file = "mul128x128_fixed.s"  # Fixed: relative path since we're in examples/
    asm_code.export_to_file(output_file)
    print(f"✓ Assembly exported to: {output_file}")
    print("✓ Uses only caller-saved registers (x0-x17)")
    print("✓ Avoids callee-saved registers (x19-x30) to prevent segfaults")
    
    # Also show on console
    print("\n=== Generated Assembly ===")
    asm_code.stdout()

if __name__ == "__main__":
    main()
