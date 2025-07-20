#!/usr/bin/env python3

"""
Demo of vector memory operations with register type validation.
This demonstrates load/store operations for vector registers.
"""

from armasmgen.builder import ASMCode, Block
from armasmgen.register import v_reg, x_reg

def demo_basic_vector_memory():
    """Demonstrate basic vector memory operations."""
    print("=== Basic Vector Memory Operations ===")
    
    with ASMCode() as asm:
        asm.comment("Vector memory operations demonstration")
        asm.comment("Load and store operations for 128-bit SIMD registers")
        
        with Block(label="vector_memory_basic") as demo:
            # Create register objects
            v0 = v_reg(0)  # Vector register v0
            v1 = v_reg(1)  # Vector register v1
            x0 = x_reg(0)  # Address register x0
            x1 = x_reg(1)  # Address register x1
            x2 = x_reg(2)  # Address register x2
            
            # Basic vector load/store
            demo.comment("Basic vector load/store operations")
            demo.LDR_vector(v0, x0)  # Load 128-bit vector from [x0] -> q0
            demo.STR_vector(v1, x1)  # Store 128-bit vector to [x1] -> q1
            
            # Vector load/store with offset
            demo.comment("Vector operations with offset")
            demo.LDR_vector_offset(v0, x0, 16)   # Load from [x0 + 16] -> q0
            demo.STR_vector_offset(v1, x1, 32)   # Store to [x1 + 32] -> q1
            
            # 128-bit register operations
            demo.comment("Explicit 128-bit Q register operations")
            demo.LDR_Q(v0, x2)      # Load 128-bit Q register -> q0
            demo.STR_Q(v1, x2)      # Store 128-bit Q register -> q1
        
        print("Generated Assembly:")
        print(asm.encode())

def demo_vector_pair_operations():
    """Demonstrate vector load/store pair operations."""
    print("=== Vector Load/Store Pair Operations ===")
    
    with ASMCode() as asm:
        asm.comment("Vector load/store pair operations")
        asm.comment("Efficient loading and storing of register pairs")
        
        with Block(label="vector_pairs") as demo:
            # Create register objects
            v0 = v_reg(0)
            v1 = v_reg(1)
            v2 = v_reg(2)
            v3 = v_reg(3)
            x0 = x_reg(0)
            
            # Load/store pair operations
            demo.comment("Load/store pair operations")
            demo.LDP_vector(v0, v1, x0)         # Load pair: q0, q1 from [x0]
            demo.STP_vector(v2, v3, x0)         # Store pair: q2, q3 to [x0]
            
            # With offsets
            demo.comment("Pair operations with offsets")
            demo.LDP_vector_offset(v0, v1, x0, 32)   # Load from [x0 + 32]
            demo.STP_vector_offset(v2, v3, x0, 64)   # Store to [x0 + 64]
        
        print("Generated Assembly:")
        print(asm.encode())

def demo_mixed_register_usage():
    """Demonstrate mixing scalar and vector operations safely."""
    print("=== Mixed Register Usage (Safe) ===")
    
    with ASMCode() as asm:
        asm.comment("Mixed scalar and vector memory operations")
        asm.comment("Different register types used appropriately")
        
        with Block(label="mixed_usage") as demo:
            # Create register objects
            x0 = x_reg(0)
            x1 = x_reg(1)
            v0 = v_reg(0)
            v1 = v_reg(1)
            
            # Scalar memory operations
            demo.comment("Scalar memory operations")
            demo.LDR(x0, x1)          # Load 64-bit scalar
            demo.STR(x0, x1)          # Store 64-bit scalar
            
            # Vector memory operations  
            demo.comment("Vector memory operations")
            demo.LDR_vector(v0, x1)   # Load 128-bit vector -> q0
            demo.STR_vector(v1, x1)   # Store 128-bit vector -> q1
            demo.LDR_Q(v0, x1)        # Load Q register (explicit 128-bit) -> q0
        
        print("Generated Assembly:")
        print(asm.encode())

def demo_comprehensive_vector_memory():
    """Comprehensive demonstration of all vector memory operations."""
    print("=== Comprehensive Vector Memory Operations ===")
    
    with ASMCode() as asm:
        asm.comment("Comprehensive vector memory operation showcase")
        asm.comment("All available vector load/store operations")
        
        with Block(label="comprehensive_vector") as demo:
            # Create register objects
            v0 = v_reg(0)
            v1 = v_reg(1)
            v2 = v_reg(2)
            v3 = v_reg(3)
            x0 = x_reg(0)
            x1 = x_reg(1)
            
            demo.comment("Vector Load Operations")
            demo.LDR_vector(v0, x0)              # Basic load -> q0
            demo.LDR_vector_offset(v1, x0, 16)   # With offset -> q1
            demo.LDR_Q(v0, x1)                   # Q register load -> q0
            demo.LDP_vector(v2, v3, x0)          # Load pair -> q2, q3
            demo.LDP_vector_offset(v0, v1, x0, 32)  # Pair with offset -> q0, q1
            
            demo.comment("")  # Empty line for readability
            
            demo.comment("Vector Store Operations")
            demo.STR_vector(v0, x0)              # Basic store q0
            demo.STR_vector_offset(v1, x0, 16)   # With offset q1
            demo.STR_Q(v1, x1)                   # Q register store q1
            demo.STP_vector(v2, v3, x0)          # Store pair q2, q3
            demo.STP_vector_offset(v0, v1, x0, 32)  # Pair with offset q0, q1
        
        print("Generated Assembly:")
        print(asm.encode())

def demo_register_validation_explanation():
    """Explain register validation without actually causing errors."""
    print("=== Register Validation System ===")
    print("""
The vector memory operations now include comprehensive register validation:

1. Vector Load/Store Operations:
   - LDR_vector, STR_vector: Require VECTOR registers for data, GENERAL for address
   - LDR_Q, STR_Q: Require VECTOR registers (Q width preferred)
   - LDP_vector, STP_vector: Require VECTOR registers for both data registers

2. Register Type Checking:
   - VECTOR registers: v0-v31, d0-d31, s0-s31, h0-h31, b0-b31, q0-q31
   - GENERAL registers: x0-x30, w0-w30 (for addresses)
   - Mixing types inappropriately will raise clear error messages

3. Benefits:
   - Prevents runtime assembly errors
   - Clear error messages for debugging
   - Self-documenting code with type safety
   - Consistent API across all operations

Example error: Using x0 as vector register will show:
"Expected VECTOR register for dst, but got GENERAL register x0"
""")

if __name__ == "__main__":
    demo_basic_vector_memory()
    print()
    demo_vector_pair_operations() 
    print()
    demo_mixed_register_usage()
    print()
    demo_comprehensive_vector_memory()
    print()
    demo_register_validation_explanation()
