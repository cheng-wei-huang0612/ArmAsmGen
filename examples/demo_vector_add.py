#!/usr/bin/env python3
"""
Vector ADD Instruction Demo - ArmAsmGen

This demo showcases the vector ADD instructions for AArch64 SIMD operations.
Each ADD function performs element-wise addition with a specific arrangement.

Features demonstrated:
- Specific ADD functions: ADD_8B, ADD_16B, ADD_4H, ADD_8H, ADD_2S, ADD_4S, ADD_1D, ADD_2D
- Intuitive API: function name indicates the number and size of elements
- Vector register usage (v0, v1, v2, etc.)
- Element-wise parallel addition
- Export to assembly file

Usage:
    python examples/demo_vector_add.py
"""

from armasmgen.builder import ASMCode, Block


def demo_vector_add_basic():
    """Basic vector addition examples with different element sizes"""
    print("=== Basic Vector Addition Demo ===\n")
    
    with ASMCode() as asm:
        asm.equ("VECTOR_SIZE", "128")  # 128-bit SIMD vectors
        asm.comment("Vector ADD instruction demonstration")
        asm.comment("Performing element-wise addition on vector registers")
        
        with Block(label="vector_add_demo") as demo:
            # 32-bit elements: Add 4 x 32-bit integers
            demo.comment("4 x 32-bit elements: v0.4S = v1.4S + v2.4S")
            demo.ADD_4S("v0", "v1", "v2")
            
            # 16-bit elements: Add 8 x 16-bit integers
            demo.comment("8 x 16-bit elements: v3.8H = v4.8H + v5.8H")  
            demo.ADD_8H("v3", "v4", "v5")
            
            # 8-bit elements: Add 16 x 8-bit integers
            demo.comment("16 x 8-bit elements: v6.16B = v7.16B + v8.16B")
            demo.ADD_16B("v6", "v7", "v8")
            
            # 64-bit elements: Add 2 x 64-bit integers
            demo.comment("2 x 64-bit elements: v9.2D = v10.2D + v11.2D")
            demo.ADD_2D("v9", "v10", "v11")
            
            demo.RET()
    
    print("Generated Assembly:")
    asm.stdout(indent=True)
    print()


def demo_vector_add_comprehensive():
    """Comprehensive demo showing all supported arrangements"""
    print("=== Comprehensive Vector ADD Demo ===\n")
    
    with ASMCode() as asm:
        asm.comment("Complete demonstration of all ADD vector instructions")
        
        with Block(label="test_all_arrangements") as test:
            # Demonstrate all available ADD instructions
            test.comment("8 x 8-bit elements")
            test.ADD_8B("v0", "v1", "v2")
            
            test.comment("16 x 8-bit elements")
            test.ADD_16B("v3", "v4", "v5")
            
            test.comment("4 x 16-bit elements")
            test.ADD_4H("v6", "v7", "v8")
            
            test.comment("8 x 16-bit elements")
            test.ADD_8H("v9", "v10", "v11")
            
            test.comment("2 x 32-bit elements")
            test.ADD_2S("v12", "v13", "v14")
            
            test.comment("4 x 32-bit elements")
            test.ADD_4S("v15", "v16", "v17")
            
            test.comment("1 x 64-bit element")
            test.ADD_1D("v18", "v19", "v20")
            
            test.comment("2 x 64-bit elements")
            test.ADD_2D("v21", "v22", "v23")
            
            test.RET()
    
    print("Generated Assembly:")
    asm.stdout(indent=True)
    print()


def demo_vector_add_practical():
    """Practical example: Simple vector addition function"""
    print("=== Practical Vector Addition Example ===\n")
    
    with ASMCode() as asm:
        asm.comment("Practical example: Vector addition function")
        asm.comment("Adds corresponding elements of two SIMD vectors")
        
        with Block(label="vector_add_func") as func:
            func.comment("Function: add two 4x32-bit vectors")
            func.comment("Input: v0 and v1 contain source vectors")
            func.comment("Output: v2 contains result vector")
            
            # Perform vector addition - now much cleaner!
            func.ADD_4S("v2", "v0", "v1")  # v2 = v0 + v1 (4 x 32-bit)
            
            # Also demonstrate other element sizes
            func.comment("Demonstrate different element sizes")
            func.ADD_8H("v3", "v4", "v5")   # 8 x 16-bit
            func.ADD_16B("v6", "v7", "v8")  # 16 x 8-bit
            func.ADD_2D("v9", "v10", "v11") # 2 x 64-bit
            
            func.RET()
    
    print("Generated Assembly:")
    asm.stdout(indent=True)
    print()


def demo_export_to_file():
    """Export vector addition demo to assembly file"""
    print("=== Exporting to File ===\n")
    
    with ASMCode() as asm:
        asm.comment("Vector Addition Export Demo")
        
        with Block(label="vector_demo") as main:
            main.comment("Initialize and perform vector additions")
            main.ADD_4S("v0", "v1", "v2")    # 4 x 32-bit addition
            main.ADD_8H("v3", "v4", "v5")    # 8 x 16-bit addition  
            main.ADD_16B("v6", "v7", "v8")   # 16 x 8-bit addition
            main.ADD_2D("v9", "v10", "v11")  # 2 x 64-bit addition
            
            main.comment("Return from function")
            main.RET()
    
    # Export with indentation
    filename_indented = "vector_add_demo.s"
    asm.export_to_file(filename_indented, indent=True)
    print(f"✅ Exported indented assembly to: {filename_indented}")
    
    # Export compact format
    filename_compact = "vector_add_demo_compact.s" 
    asm.export_to_file(filename_compact, indent=False)
    print(f"✅ Exported compact assembly to: {filename_compact}")


def demo_usability_comparison():
    """Show the improved usability of the new API"""
    print("=== API Usability Comparison ===\n")
    
    print("❌ Old API (confusing):")
    print('   demo.ADD_vector("v0", "v1", "v2", "4S")  # What does "4S" mean?')
    print('   demo.ADD_vector("v3", "v4", "v5", "8H")  # Hard to remember arrangements')
    print()
    
    print("✅ New API (intuitive):")
    print('   demo.ADD_4S("v0", "v1", "v2")  # Obviously adds 4 x 32-bit elements')  
    print('   demo.ADD_8H("v3", "v4", "v5")  # Obviously adds 8 x 16-bit elements')
    print('   demo.ADD_2D("v6", "v7", "v8")  # Obviously adds 2 x 64-bit elements')
    print()
    
    with ASMCode() as asm:
        with Block(label="usability_demo") as demo:
            demo.comment("Crystal clear what each instruction does!")
            demo.ADD_4S("v0", "v1", "v2")   # 4 Singles (32-bit)
            demo.ADD_8H("v3", "v4", "v5")   # 8 Halfwords (16-bit)
            demo.ADD_16B("v6", "v7", "v8")  # 16 Bytes (8-bit)
            demo.ADD_2D("v9", "v10", "v11") # 2 Doubles (64-bit)
    
    print("Generated Assembly:")
    asm.stdout(indent=True)
    print()


def demo_register_type_safety():
    """Demonstrate the register type validation system"""
    print("=== Register Type Safety Demo ===\n")
    
    print("✅ Valid vector registers work fine:")
    try:
        with ASMCode() as asm:
            with Block(label="valid_test") as test:
                test.ADD_4S("v0", "v1", "v2")  # Should work
        print("   ADD_4S('v0', 'v1', 'v2') ✓")
    except Exception as e:
        print(f"   Unexpected error: {e}")
    
    print("\n❌ Invalid scalar registers are caught:")
    
    # Test scalar register rejection
    test_cases = [
        ("x0", "general purpose register"),
        ("w5", "32-bit general purpose register"), 
        ("sp", "stack pointer")
    ]
    
    for bad_reg, desc in test_cases:
        try:
            with ASMCode() as asm:
                with Block(label="invalid_test") as test:
                    test.ADD_4S(bad_reg, "v1", "v2")
            print(f"   ADD_4S('{bad_reg}', 'v1', 'v2') - ERROR: Should have failed!")
        except TypeError as e:
            print(f"   ADD_4S('{bad_reg}', 'v1', 'v2') ✓ - Correctly rejected ({desc})")
        except Exception as e:
            print(f"   ADD_4S('{bad_reg}', 'v1', 'v2') - Unexpected error: {e}")
    
    print("\n🛡️  Register validation prevents common mistakes!")
    print()


if __name__ == "__main__":
    print("ArmAsmGen - Vector ADD Instruction Demo (Improved API)")
    print("=" * 60)
    
    # Run all demos
    demo_vector_add_basic()
    demo_vector_add_comprehensive()
    demo_vector_add_practical()
    demo_register_type_safety()  # Add the new demo
    demo_export_to_file()
    demo_usability_comparison()
    
    print("Demo completed! 🎉")
    print("\nGenerated files:")
    print("- examples/vector_add_demo.s (indented)")
    print("- examples/vector_add_demo_compact.s (compact)")
    print("\n✨ Key Improvements:")
    print("   • Function names clearly indicate the operation!")
    print("     ADD_4S = Add 4 x 32-bit elements (Singles)")
    print("     ADD_8H = Add 8 x 16-bit elements (Halfwords)")  
    print("     ADD_2D = Add 2 x 64-bit elements (Doubles)")
    print("   • Register type validation prevents mistakes!")
    print("     Catches scalar registers in vector operations at compile time")
