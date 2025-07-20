# ArmAsmGen Examples Directory

This directory contains demonstration files showing various features of the ArmAsmGen library for generating AArch64 assembly code.

## 🚀 Getting Started

### Basic Usage
- **`demo_basic.py`** - Introduction to basic assembly generation with simple arithmetic and memory operations

### Vector Operations (SIMD)
- **`demo_vector_add.py`** - Vector ADD instructions for SIMD operations with different element arrangements (ADD_4S, ADD_8H, etc.)
- **`demo_vector_memory.py`** - Vector memory operations (LDR_vector, STR_vector, LDP_vector, STP_vector) with proper q-register conversion

### Register Management & Validation
- **`demo_register_validation.py`** - Register type validation system showing how to prevent mixing scalar and vector registers

## 🧮 Advanced Examples

### Arithmetic Operations
- **`demo_complete_arithmetic.py`** - Comprehensive arithmetic operations including multiply-accumulate and carry operations
- **`demo_multiprecision.py`** - Multi-precision arithmetic using ADDS/ADCS with proper carry handling for large number operations
- **`demo_wide_multiply.py`** - Wide multiplication (128-bit × 128-bit → 256-bit) using UMULH and SMULH instructions

### Export & Integration
- **`demo_comprehensive.py`** - Custom mixin combinations and comprehensive instruction usage patterns
- **`demo_export_formats.py`** - Different output formats and file export capabilities

### Specialized Applications
- **`bignum_mul/`** - Complete bignum multiplication example with Makefile, C test harness, and optimized assembly

## 📋 Generated Files

The examples directory also contains generated assembly files (`.s`) from running the demos:
- `exported_assembly.s`
- `matrix_multiply_*.s`
- `vector_add_demo*.s`
- `mul128x128_fixed.s`

## 🔧 Running the Examples

Each Python file can be run independently:

```bash
# Basic usage
python examples/demo_basic.py

# Vector operations
python examples/demo_vector_add.py
python examples/demo_vector_memory.py

# Register validation
python examples/demo_register_validation.py

# Advanced features
python examples/demo_multiprecision.py
python examples/demo_wide_multiply.py
```

## 🎯 Use Cases by Domain

### **Game/Graphics Programming**
- Vector operations: `demo_vector_add.py`, `demo_vector_memory.py`
- Matrix operations: Generated `matrix_multiply_*.s` files

### **Cryptography/Security**
- Large number arithmetic: `demo_multiprecision.py`, `bignum_mul/`
- Wide multiplication: `demo_wide_multiply.py`

### **Systems Programming**
- Basic operations: `demo_basic.py`, `demo_complete_arithmetic.py`
- Register management: `demo_register_validation.py`

### **Compiler/Code Generation**
- Export formats: `demo_export_formats.py`
- Custom mixins: `demo_comprehensive.py`

## 💡 Key Features Demonstrated

- **Type Safety**: Register validation prevents mixing scalar/vector registers
- **Correct Assembly Syntax**: Vector operations properly use q-register format
- **Register Objects**: Prefer `v_reg(0)` over string `"v0"` for better type safety
- **SIMD Support**: Comprehensive vector arithmetic and memory operations
- **Export Flexibility**: Multiple output formats and file generation options
- **Real-World Applications**: Complete examples like bignum multiplication

## 🔍 Understanding the Output

Vector memory operations automatically convert register names for correct ARM64 syntax:
```python
# Input (using Register objects):
demo.LDR_vector(v_reg(0), x_reg(0))

# Generated Assembly:
ldr q0, [x0]  # Correct q-register format, not v0
```

This ensures the generated assembly works with standard ARM64 assemblers and toolchains.
