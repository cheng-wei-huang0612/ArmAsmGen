#!/usr/bin/env python3
"""
Test the refactored _reg_to_str method in BaseAsm
"""

from armasmgen import ASMCode, x_reg, virtual_x

def test_mixin_methods():
    """Test that all mixins can use the shared _reg_to_str method"""
    
    f = ASMCode()
    
    # Test with mixed register types
    physical_reg = x_reg(0)
    virtual_reg = virtual_x("temp")
    string_reg = "x1"
    
    with f as asm:
        print("Testing arithmetic mixin:")
        asm.ADD(physical_reg, virtual_reg, string_reg)
        asm.SUB_imm(virtual_reg, physical_reg, 42)
        asm.MUL("x2", physical_reg, virtual_reg)
        asm.MADD("x3", string_reg, physical_reg, virtual_reg)
        
        print("Testing memory mixin:")
        asm.LDR(physical_reg, "x10")
        asm.STR(virtual_reg, physical_reg)
        asm.STP_stack_offset(string_reg, virtual_reg, -16)
    
    print("Generated assembly:")
    f.stdout()

if __name__ == "__main__":
    test_mixin_methods()
