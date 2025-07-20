#!/usr/bin/env python3
"""
Demo: Register management system with virtual registers and pools.
Shows physical registers, virtual registers, and register allocation.
"""

from armasmgen import (
    ASMCode, Block, 
    aarch64_pools, x_reg, v_reg, virtual_x, virtual_v,
    RegisterType, RegisterWidth
)

def demo_basic_registers():
    """Basic register usage"""
    print("=== Basic Register Usage ===")
    
    f = ASMCode()
    with f as asm:
        # Using physical registers
        reg_x0 = x_reg(0)
        reg_x1 = x_reg(1)
        reg_x2 = x_reg(2)
        
        with Block(label="physical_regs") as m:
            m.ADD(reg_x0, reg_x1, reg_x2)  # add x0, x1, x2
            m.SUB("x3", "x4", "x5")        # Still works with strings
    
    f.stdout()


def demo_virtual_registers():
    """Virtual register demonstration"""
    print("\n=== Virtual Register Usage ===")
    
    f = ASMCode()
    with f as asm:
        # Create virtual registers
        tmp1 = virtual_x("tmp1")
        tmp2 = virtual_x("tmp2") 
        result = virtual_x("result")
        
        vec_tmp = virtual_v("vec_data")
        
        with Block(label="virtual_demo") as m:
            m.ADD(tmp1, "x0", "x1")        # add X<tmp1>, x0, x1
            m.MUL(tmp2, tmp1, "x2")        # mul X<tmp2>, X<tmp1>, x2  
            m.SUB(result, tmp2, "x3")      # sub X<result>, X<tmp2>, x3
    
    f.stdout()


def demo_register_pools():
    """Register pool allocation demo"""
    print("\n=== Register Pool Management ===")
    
    # Get some registers from pools
    scratch_pool = aarch64_pools.x_caller_saved
    callee_pool = aarch64_pools.x_callee_saved
    
    print(f"Caller-saved pool: {scratch_pool}")
    print(f"Available registers: {len(scratch_pool.get_available())}")
    
    # Allocate some registers
    reg1 = scratch_pool.allocate()  # Get any available
    
    # Find an available register for specific allocation
    available_regs = list(scratch_pool.get_available())
    if len(available_regs) > 1:
        reg2 = scratch_pool.allocate(available_regs[1])  # Get second available
    else:
        reg2 = scratch_pool.allocate()  # Get any available
    
    print(f"Allocated: {reg1}, {reg2}")
    print(f"Remaining available: {len(scratch_pool.get_available())}")
    
    # Generate code with allocated registers
    f = ASMCode()
    with f as asm:
        with Block(label="pool_demo") as m:
            m.ADD(reg1, "x10", "x11")
            m.SUB(reg2, reg1, "x12")
    
    f.stdout()
    
    # Clean up
    scratch_pool.free(reg1)
    scratch_pool.free(reg2)


def demo_macro_block():
    """Macro block with mixed virtual and physical registers"""
    print("\n=== Macro Block with Mixed Registers ===")
    
    # Create virtual registers for the macro
    pools = aarch64_pools
    local1 = pools.create_virtual_register("local1", RegisterType.GENERAL, RegisterWidth.X)
    local2 = pools.create_virtual_register("local2", RegisterType.GENERAL, RegisterWidth.X)
    temp = pools.create_virtual_register("temp", RegisterType.GENERAL, RegisterWidth.X)
    
    f = ASMCode()
    with f as asm:
        asm.equ("MACRO_CONST", "42")
        
        with Block(label="vector_add_macro") as macro:
            # Mix of virtual and physical registers
            macro.ADD(local1, "x0", "x1")      # x0, x1 are inputs
            macro.ADD_imm(temp, local1, 10)    # Add constant
            macro.MUL(local2, temp, "x2")      # x2 is another input  
            macro.SUB("x0", local2, temp)      # x0 is output
    
    f.stdout()


if __name__ == "__main__":
    demo_basic_registers()
    demo_virtual_registers() 
    demo_register_pools()
    demo_macro_block()
    
    print("\n=== Summary ===")
    print("✓ Physical register objects (x_reg, v_reg)")
    print("✓ Virtual register support (X<name>, V<name>)") 
    print("✓ Register pools with calling convention classification")
    print("✓ Register allocation and tracking")
    print("✓ Mixed register usage in macro blocks")
    print("✓ SLOTHY-style virtual register syntax")
