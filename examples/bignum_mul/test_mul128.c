#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <gmp.h>

// Declare the external assembly function
extern void mul128x128(uint64_t a[2], uint64_t b[2], uint64_t result[4]);

// Helper function to print a 128-bit number
void print_uint128(const char* name, uint64_t high, uint64_t low) {
    printf("%s = 0x%016llx%016llx\n", name, high, low);
}

// Helper function to print a 256-bit number  
void print_uint256(const char* name, uint64_t result[4]) {
    printf("%s = 0x%016llx%016llx%016llx%016llx\n", name, 
           result[3], result[2], result[1], result[0]);
}

// Convert 128-bit number to GMP mpz_t
void uint128_to_mpz(mpz_t dest, uint64_t high, uint64_t low) {
    mpz_set_ui(dest, high);
    mpz_mul_2exp(dest, dest, 64);  // Shift left by 64 bits
    mpz_add_ui(dest, dest, low);
}

// Convert 256-bit array to GMP mpz_t (little endian)
void uint256_to_mpz(mpz_t dest, uint64_t result[4]) {
    mpz_set_ui(dest, 0);
    for (int i = 3; i >= 0; i--) {
        mpz_mul_2exp(dest, dest, 64);  // Shift left by 64 bits
        mpz_add_ui(dest, dest, result[i]);
    }
}

void test_multiplication(const char* test_name, uint64_t a_high, uint64_t a_low, 
                        uint64_t b_high, uint64_t b_low) {
    printf("\n=== %s ===\n", test_name);
    
    // Prepare inputs
    uint64_t a[2] = {a_low, a_high};  // Little endian: [low, high]
    uint64_t b[2] = {b_low, b_high};
    uint64_t result[4] = {0, 0, 0, 0}; // Will store 256-bit result
    
    // Print inputs
    print_uint128("A", a_high, a_low);
    print_uint128("B", b_high, b_low);
    
    // Call our assembly function
    mul128x128(a, b, result);
    
    // Print assembly result
    print_uint256("Assembly Result", result);
    
    // Verify with GMP
    mpz_t gmp_a, gmp_b, gmp_result, asm_result;
    mpz_inits(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    
    // Convert inputs to GMP
    uint128_to_mpz(gmp_a, a_high, a_low);
    uint128_to_mpz(gmp_b, b_high, b_low);
    
    // Compute reference result with GMP
    mpz_mul(gmp_result, gmp_a, gmp_b);
    
    // Convert assembly result to GMP for comparison
    uint256_to_mpz(asm_result, result);
    
    // Compare results
    if (mpz_cmp(gmp_result, asm_result) == 0) {
        printf("✓ PASS: Assembly result matches GMP\n");
    } else {
        printf("✗ FAIL: Results differ!\n");
        gmp_printf("GMP Result     = 0x%Zx\n", gmp_result);
        gmp_printf("Assembly Result= 0x%Zx\n", asm_result);
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
}

int main() {
    printf("128×128→256 Multiplication Test with GMP Verification\n");
    printf("=====================================================\n");
    
    // Test 1: Small numbers
    test_multiplication("Test 1: Small Numbers",
                       0x0000000000000000ULL, 0x000000000000000FULL,  // A = 15
                       0x0000000000000000ULL, 0x0000000000000010ULL); // B = 16
    
    // Test 2: Medium numbers
    test_multiplication("Test 2: Medium Numbers", 
                       0x0000000000000001ULL, 0x0000000000000000ULL,  // A = 2^64
                       0x0000000000000002ULL, 0x0000000000000000ULL); // B = 2^65
    
    // Test 3: Large numbers
    test_multiplication("Test 3: Large Numbers",
                       0x123456789ABCDEFULL, 0xFEDCBA9876543210ULL,  // A = large
                       0x0FEDCBA987654321ULL, 0x123456789ABCDEFULL); // B = large
    
    // Test 4: Maximum values
    test_multiplication("Test 4: Maximum Values",
                       0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,  // A = 2^128 - 1
                       0x0000000000000000ULL, 0x0000000000000002ULL); // B = 2
    
    // Test 5: Edge case - one operand is zero
    test_multiplication("Test 5: Zero Operand",
                       0x0000000000000000ULL, 0x0000000000000000ULL,  // A = 0
                       0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL); // B = max
    
    printf("\n=== All Tests Complete ===\n");
    return 0;
}
