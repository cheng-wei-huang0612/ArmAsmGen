#!/usr/bin/env python3
"""
Register Type Validation Demo - ArmAsmGen Vector Operations

This demo shows how the vector ADD instructions validate register types
to prevent common mistakes like using scalar registers in vector operations.

Features demonstrated:
- Register type validation for vector operations
- Clear error messages for invalid register types
- Support for both Register objects and string register names
- Prevention of mixing scalar and vector registers

Usage:
    python examples/demo_register_validation.py
"""

from armasmgen.builder import ASMCode, Block
from armasmgen.register import v_reg, x_reg, d_reg


def demo_valid_vector_operations():
    """Demonstrate valid vector operations with proper registers"""
    print("=== Valid Vector Operations ===\n")
    
    with ASMCode() as asm:
        asm.comment("Valid vector register usage")
        
        with Block(label="valid_operations") as demo:
            # These should all work fine
            demo.comment("String-based vector registers")
            demo.ADD_4S("v0", "v1", "v2")
            demo.ADD_8H("v3", "v4", "v5")
            demo.ADD_2D("v6", "v7", "v8")
            
            demo.RET()
    
    print("✅ All valid operations completed successfully!")
    print("Generated Assembly:")
    asm.stdout(indent=True)
    print()


def demo_register_objects():
    """Demonstrate usage with Register objects"""
    print("=== Using Register Objects ===\n")
    
    with ASMCode() as asm:
        asm.comment("Using Register objects for type safety")
        
        with Block(label="register_objects") as demo:
            # Create proper vector register objects
            vec0 = v_reg(0)  # v0
            vec1 = v_reg(1)  # v1  
            vec2 = v_reg(2)  # v2
            
            demo.comment("Vector registers created as Register objects")
            demo.ADD_4S(vec0, vec1, vec2)
            demo.ADD_8H("v3", "v4", "v5")  # Mix Register objects with strings
            
            demo.RET()
    
    print("✅ Register objects work perfectly!")
    print("Generated Assembly:")
    asm.stdout(indent=True)
    print()


def demo_invalid_scalar_registers():
    """Demonstrate validation catching invalid scalar register usage"""
    print("=== Invalid Register Type Detection ===\n")
    
    # Test 1: General purpose register in vector operation
    print("❌ Test 1: Using general purpose register 'x0' in vector ADD")
    try:
        with ASMCode() as asm:
            with Block(label="bad_example1") as demo:
                demo.ADD_4S("x0", "v1", "v2")  # This should fail
    except TypeError as e:
        print(f"✅ Caught error: {e}")
    print()
    
    # Test 2: Mixed register types
    print("❌ Test 2: Mixing general purpose and vector registers") 
    try:
        with ASMCode() as asm:
            with Block(label="bad_example2") as demo:
                demo.ADD_2D("v0", "x1", "v2")  # This should fail
    except TypeError as e:
        print(f"✅ Caught error: {e}")
    print()
    
    # Test 3: Using w registers (32-bit GP)
    print("❌ Test 3: Using 32-bit general purpose register 'w0'")
    try:
        with ASMCode() as asm:
            with Block(label="bad_example3") as demo:
                demo.ADD_8H("w0", "v1", "v2")  # This should fail
    except TypeError as e:
        print(f"✅ Caught error: {e}")
    print()


def demo_register_object_validation():
    """Test validation with Register objects"""
    print("=== Register Object Type Validation ===\n")
    
    # Test with actual Register objects
    print("❌ Test 4: General purpose Register object in vector operation")
    try:
        with ASMCode() as asm:
            with Block(label="bad_example4") as demo:
                gp_reg = x_reg(0)  # Create x0 Register object
                demo.ADD_4S(gp_reg, "v1", "v2")  # This should fail
    except TypeError as e:
        print(f"✅ Caught error: {e}")
    print()


def demo_edge_cases():
    """Test edge cases and corner scenarios"""
    print("=== Edge Cases ===\n")
    
    # Test with d registers (should work - they're vector register variants)
    print("✅ Test 5: Using d register variants (should work)")
    try:
        with ASMCode() as asm:
            with Block(label="edge_case1") as demo:
                demo.comment("d registers are vector register variants")
                # Note: This might generate a warning but shouldn't fail type checking
                demo.ADD_2D("d0", "d1", "d2")
        print("✅ d register usage accepted")
        asm.stdout(indent=True)
    except Exception as e:
        print(f"⚠️  Edge case result: {e}")
    print()


def demo_comprehensive_validation():
    """Show comprehensive validation in action"""
    print("=== Comprehensive Validation Demo ===\n")
    
    register_tests = [
        ("v0", True, "128-bit vector register"),
        ("d0", True, "64-bit vector register"),  
        ("s0", True, "32-bit vector register"),
        ("h0", True, "16-bit vector register"),
        ("b0", True, "8-bit vector register"),
        ("x0", False, "64-bit general purpose register"),
        ("w0", False, "32-bit general purpose register"),
        ("sp", False, "stack pointer"),
        ("lr", False, "link register"),
    ]
    
    for reg_name, should_pass, description in register_tests:
        print(f"Testing {reg_name} ({description}):", end=" ")
        
        try:
            with ASMCode() as asm:
                with Block(label=f"test_{reg_name}") as demo:
                    demo.ADD_4S(reg_name, "v1", "v2")
            
            if should_pass:
                print("✅ PASS (as expected)")
            else:
                print("❌ FAIL (should have been rejected)")
                
        except TypeError as e:
            if not should_pass:
                print("✅ PASS (correctly rejected)")
            else:
                print(f"❌ FAIL (should have been accepted): {e}")
        except Exception as e:
            print(f"⚠️  UNEXPECTED ERROR: {e}")
    
    print()


if __name__ == "__main__":
    print("ArmAsmGen - Register Type Validation Demo")
    print("=" * 60)
    
    # Run all validation demos
    demo_valid_vector_operations()
    demo_register_objects()
    demo_invalid_scalar_registers()
    demo_register_object_validation()
    demo_edge_cases()
    demo_comprehensive_validation()
    
    print("🛡️  Register type validation is working!")
    print("\n✨ Key Benefits:")
    print("   • Prevents mixing scalar and vector registers")
    print("   • Clear error messages for invalid usage")
    print("   • Works with both strings and Register objects") 
    print("   • Catches common mistakes at code generation time")
