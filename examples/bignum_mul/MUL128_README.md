# 128×128→256 Bit Multiplication Test

This directory (`examples/bignum_mul/`) contains a focused implementation of 128×128 bit multiplication that produces a 256-bit result, along with a C test program that verifies correctness using the GMP (GNU Multiple Precision) library.

## Files

- `demo_mul128_fixed.py` - Python script that generates the assembly code
- `mul128x128_fixed.s` - Generated ARM64 assembly implementation  
- `test_mul128.c` - C test program with GMP verification
- `Makefile` - Build system for compiling and running tests

## Assembly Function

The generated assembly implements:
```c
void mul128x128(uint64_t a[2], uint64_t b[2], uint64_t result[4]);
```

**Parameters:**
- `a[2]`: 128-bit input A as `{low, high}` (little-endian)
- `b[2]`: 128-bit input B as `{low, high}` (little-endian)  
- `result[4]`: 256-bit output as `{r0, r1, r2, r3}` (little-endian)

**Algorithm:**
Uses the standard method for multi-precision multiplication:
1. Compute 4 partial products: `A_low×B_low`, `A_low×B_high`, `A_high×B_low`, `A_high×B_high`
2. Each partial product uses `MUL` (low 64 bits) and `UMULH` (high 64 bits)
3. Combine results with proper carry propagation using `ADDS`/`ADCS` instructions
4. Store the 256-bit result in memory

## Requirements

- **ARM64 processor** (Apple M1/M2, AWS Graviton, etc.)
- **GMP library** for verification
- **GCC** and **GNU assembler**

## Building and Running

### Install Dependencies (macOS with Homebrew)
```bash
brew install gmp
```

### Install Dependencies (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install libgmp-dev build-essential
```

### Build and Run
```bash
cd examples/bignum_mul
make run
```

Or manually:
```bash
# Assemble the ARM64 code
as -arch arm64 -o mul128x128_fixed.o mul128x128_fixed.s

# Compile the C test
gcc -arch arm64 -O2 -Wall -c -o test_mul128.o test_mul128.c

# Link with GMP
gcc -arch arm64 -o test_mul128 mul128x128_fixed.o test_mul128.o -lgmp

# Run the test
./test_mul128
```

## Expected Output

```
128×128→256 Multiplication Test with GMP Verification
=====================================================

=== Test 1: Small Numbers ===
A = 0x000000000000000f
B = 0x0000000000000010
Assembly Result = 0x00000000000000000000000000000000000000000000000000f0
✓ PASS: Assembly result matches GMP

=== Test 2: Medium Numbers ===
A = 0x0000000100000000
B = 0x0000000200000000
Assembly Result = 0x00000000000000000000000200000000000000000000000000000000
✓ PASS: Assembly result matches GMP

... (more tests)

=== All Tests Complete ===
```

## Algorithm Verification

The test program verifies correctness by:
1. Running the same multiplication in GMP (reference implementation)
2. Comparing bit-by-bit with our assembly result
3. Testing edge cases: small numbers, large numbers, zero operands, maximum values

## Cross-Platform Notes

- **ARM64 Native**: Works directly on Apple Silicon, AWS Graviton, etc.
- **x86_64**: Requires cross-compilation tools or emulation
- **Other architectures**: The assembly is ARM64-specific

## Implementation Details

**Register Usage:**
- `x0, x1, x2`: Function parameters (pointers)
- `x4, x5`: Input A (loaded from memory)
- `x6, x7`: Input B (loaded from memory)  
- `x10-x17`: Intermediate partial products
- `x20-x23`: Final 256-bit result
- `x8, x9, x10-x12`: Address calculations

**Key Instructions:**
- `MUL`: 64×64→64 multiplication (low part)
- `UMULH`: 64×64→64 unsigned multiply-high (upper part)
- `ADDS/ADCS`: Add with carry for proper overflow handling
- `LDR/STR`: Memory access for inputs and results

This implementation demonstrates proper multi-precision arithmetic with carry propagation, essential for cryptographic applications and big integer libraries.
