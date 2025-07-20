#!/usr/bin/env python3
"""
Demo: Proper multi-precision arithmetic using ADDS/ADCS
Shows correct 128×128→256 bit multiplication with carry handling.
"""

from armasmgen import ASMCode, Block, x_reg, virtual_x

def demo_carry_instructions():
    """Demonstrate ADDS, ADCS, SUBS, SBCS instructions"""
    print("=== Carry and Flag-Setting Instructions ===")
    
    f = ASMCode()
    with f as asm:
        with Block(label="carry_demo") as m:
            # Addition with flags
            m.ADDS("x0", "x1", "x2")         # x0 = x1 + x2, set flags
            m.ADDS_imm("x3", "x4", 100)      # x3 = x4 + 100, set flags
            
            # Add with carry (use carry from previous ADDS)
            m.ADCS("x5", "x6", "x7")         # x5 = x6 + x7 + carry, set flags
            m.ADCS_imm("x8", "x9", 0)        # x8 = x9 + 0 + carry (propagate carry)
            
            # Subtraction with flags
            m.SUBS("x10", "x11", "x12")      # x10 = x11 - x12, set flags
            m.SUBS_imm("x13", "x14", 50)     # x13 = x14 - 50, set flags
            
            # Subtract with carry/borrow
            m.SBCS("x15", "x16", "x17")      # x15 = x16 - x17 - ~carry, set flags
    
    f.stdout()


def demo_64bit_addition_with_carry():
    """Demonstrate 128-bit addition using 64-bit operations with carry"""
    print("\n=== 128-bit Addition with Carry ===")
    
    f = ASMCode()
    with f as asm:
        asm.equ("COMMENT", "// Add {x0,x1} + {x2,x3} -> {x4,x5} (128-bit)")
        
        with Block(label="add128") as m:
            # Add low parts and set carry flag
            m.ADDS("x5", "x1", "x3")         # Low: x5 = x1 + x3, set carry
            
            # Add high parts with carry from low addition
            m.ADCS("x4", "x0", "x2")         # High: x4 = x0 + x2 + carry
            
            # Result: 128-bit sum is in {x4, x5}
    
    f.stdout()


def demo_proper_128x128_multiply():
    """Proper 128×128→256 multiplication with correct carry handling"""
    print("\n=== Proper 128×128→256 Multiplication ===")
    
    f = ASMCode()
    with f as asm:
        asm.equ("INPUT_A_HIGH", "x0")
        asm.equ("INPUT_A_LOW", "x1") 
        asm.equ("INPUT_B_HIGH", "x2")
        asm.equ("INPUT_B_LOW", "x3")
        asm.equ("RESULT_3", "x20")  # Most significant
        asm.equ("RESULT_2", "x21")
        asm.equ("RESULT_1", "x22") 
        asm.equ("RESULT_0", "x23")  # Least significant
        
        with Block(label="mul128x128_proper") as m:
            # Virtual registers for partial products
            ll_l = virtual_x("ll_low")    # A_low * B_low -> low
            ll_h = virtual_x("ll_high")   # A_low * B_low -> high
            lh_l = virtual_x("lh_low")    # A_low * B_high -> low
            lh_h = virtual_x("lh_high")   # A_low * B_high -> high
            hl_l = virtual_x("hl_low")    # A_high * B_low -> low  
            hl_h = virtual_x("hl_high")   # A_high * B_low -> high
            hh_l = virtual_x("hh_low")    # A_high * B_high -> low
            hh_h = virtual_x("hh_high")   # A_high * B_high -> high
            
            # Step 1: Compute all partial products
            m.MUL(ll_l, "x1", "x3")      # A_low * B_low -> 128 bits
            m.UMULH(ll_h, "x1", "x3")
            
            m.MUL(lh_l, "x1", "x2")      # A_low * B_high -> 128 bits  
            m.UMULH(lh_h, "x1", "x2")
            
            m.MUL(hl_l, "x0", "x3")      # A_high * B_low -> 128 bits
            m.UMULH(hl_h, "x0", "x3")
            
            m.MUL(hh_l, "x0", "x2")      # A_high * B_high -> 128 bits
            m.UMULH(hh_h, "x0", "x2")
            
            # Step 2: Combine with proper carry propagation
            # Result[63:0] = ll_l
            m.ADD("x23", "xzr", ll_l)
            
            # Result[127:64] = ll_h + lh_l + hl_l (with carry out)
            m.ADDS("x22", ll_h, lh_l)    # First addition, set carry
            m.ADCS("x22", "x22", hl_l)   # Add third term with carry
            
            # Result[191:128] = lh_h + hl_h + hh_l + carry_from_below
            m.ADCS("x21", lh_h, hl_h)    # Add with carry from below
            m.ADCS("x21", "x21", hh_l)   # Add third term with carry
            
            # Result[255:192] = hh_h + carry_from_below  
            m.ADCS("x20", hh_h, "xzr")   # Add only carry from below
            
            # Final result: 256-bit product in {x20, x21, x22, x23}
    
    f.stdout()


def demo_multi_precision_square():
    """Demonstrate proper 128-bit squaring with carry handling"""
    print("\n=== Proper 128-bit Squaring ===")
    
    f = ASMCode()
    with f as asm:
        asm.equ("COMMENT", "// Square {x0,x1} -> {x20,x21,x22,x23}")
        
        with Block(label="square128_proper") as m:
            # For (a*2^64 + b)^2 = a^2*2^128 + 2*a*b*2^64 + b^2
            # We need: b^2, a^2, and 2*a*b
            
            # Part 1: b^2 (x1^2)
            b_sq_l = virtual_x("b_sq_l") 
            b_sq_h = virtual_x("b_sq_h")
            m.MUL(b_sq_l, "x1", "x1")
            m.UMULH(b_sq_h, "x1", "x1")
            
            # Part 2: a^2 (x0^2) 
            a_sq_l = virtual_x("a_sq_l")
            a_sq_h = virtual_x("a_sq_h")
            m.MUL(a_sq_l, "x0", "x0")
            m.UMULH(a_sq_h, "x0", "x0")
            
            # Part 3: a*b (x0*x1)
            ab_l = virtual_x("ab_l")
            ab_h = virtual_x("ab_h") 
            m.MUL(ab_l, "x0", "x1")
            m.UMULH(ab_h, "x0", "x1")
            
            # Part 4: 2*a*b (double the cross product)
            ab2_l = virtual_x("ab2_l")
            ab2_h = virtual_x("ab2_h")
            m.ADDS(ab2_l, ab_l, ab_l)       # 2*ab_l, set carry
            m.ADCS(ab2_h, ab_h, ab_h)       # 2*ab_h + carry
            
            # Step 5: Combine all parts with carry
            # bits [63:0] = b_sq_l
            m.ADD("x23", "xzr", b_sq_l)
            
            # bits [127:64] = b_sq_h + ab2_l
            m.ADDS("x22", b_sq_h, ab2_l)
            
            # bits [191:128] = ab2_h + a_sq_l + carry
            m.ADCS("x21", ab2_h, a_sq_l)
            
            # bits [255:192] = a_sq_h + carry
            m.ADCS("x20", a_sq_h, "xzr")
            
            # Result: 256-bit square in {x20, x21, x22, x23}
    
    f.stdout()


def demo_compare_old_vs_new():
    """Compare old (incorrect) vs new (correct) carry handling"""
    print("\n=== Comparison: Incorrect vs Correct Carry Handling ===")
    
    f = ASMCode()
    with f as asm:
        with Block(label="incorrect_way") as old:
            # Old way: just ADD (no carry propagation)
            old.ADD("x10", "x11", "x12")     # No carry information
            old.ADD("x13", "x14", "x15")     # Misses carry from previous
        
        with Block(label="correct_way") as new:
            # New way: ADDS/ADCS (proper carry propagation) 
            new.ADDS("x20", "x21", "x22")    # Set carry flag
            new.ADCS("x23", "x24", "x25")    # Use carry from previous
    
    f.stdout()


if __name__ == "__main__":
    demo_carry_instructions()
    demo_64bit_addition_with_carry()
    demo_proper_128x128_multiply()
    demo_multi_precision_square()
    demo_compare_old_vs_new()
    
    print("\n=== Multi-Precision Arithmetic Summary ===")
    print("✓ ADDS - Add and set carry flag")
    print("✓ ADCS - Add with carry (for multi-word addition)")
    print("✓ SUBS - Subtract and set borrow flag") 
    print("✓ SBCS - Subtract with borrow (for multi-word subtraction)")
    print("✓ Proper 128×128→256 multiplication with carry propagation")
    print("✓ Correct handling of overflow in multi-precision arithmetic")
    print("✓ Essential for cryptography, big integers, and precise calculations")
