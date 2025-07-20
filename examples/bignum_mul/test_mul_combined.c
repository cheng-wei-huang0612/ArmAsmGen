#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <gmp.h>

// Global test counters
int total_tests = 0;
int passed_tests = 0;

// Declare the external assembly functions
extern void mul128x128(uint64_t a[2], uint64_t b[2], uint64_t result[4]);
extern void mul256x256(uint64_t a[4], uint64_t b[4], uint64_t result[8]);
extern void mul512x512(uint64_t a[8], uint64_t b[8], uint64_t result[16]);

// Helper function to print a 128-bit number
void print_uint128(const char* name, uint64_t high, uint64_t low) {
    printf("%s = 0x%016llx%016llx\n", name, high, low);
}

// Helper function to print a 256-bit number  
void print_uint256_from_array(const char* name, uint64_t result[4]) {
    printf("%s = 0x%016llx%016llx%016llx%016llx\n", name, 
           result[3], result[2], result[1], result[0]);
}

// Helper function to print a 256-bit number from individual values
void print_uint256(const char* name, uint64_t data[4]) {
    printf("%s = 0x%016llx%016llx%016llx%016llx\n", name, 
           data[3], data[2], data[1], data[0]);
}

// Helper function to print a 512-bit number  
void print_uint512(const char* name, uint64_t result[8]) {
    printf("%s = 0x%016llx%016llx%016llx%016llx%016llx%016llx%016llx%016llx\n", name, 
           result[7], result[6], result[5], result[4], result[3], result[2], result[1], result[0]);
}

// Helper function to print a 1024-bit number  
void print_uint1024(const char* name, uint64_t result[16]) {
    printf("%s = 0x", name);
    for (int i = 15; i >= 0; i--) {
        printf("%016llx", result[i]);
        if (i > 0 && i % 4 == 0) printf(" ");
    }
    printf("\n");
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

// Convert 512-bit array to GMP mpz_t (little endian)
void uint512_to_mpz(mpz_t dest, uint64_t result[8]) {
    mpz_set_ui(dest, 0);
    for (int i = 7; i >= 0; i--) {
        mpz_mul_2exp(dest, dest, 64);  // Shift left by 64 bits
        mpz_add_ui(dest, dest, result[i]);
    }
}

// Convert 1024-bit array to GMP mpz_t (little endian)
void uint1024_to_mpz(mpz_t dest, uint64_t result[16]) {
    mpz_set_ui(dest, 0);
    for (int i = 15; i >= 0; i--) {
        mpz_mul_2exp(dest, dest, 64);  // Shift left by 64 bits
        mpz_add_ui(dest, dest, result[i]);
    }
}

void test_128_multiplication(const char* test_name, uint64_t a_high, uint64_t a_low, 
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
    print_uint256_from_array("Assembly Result", result);
    
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
    total_tests++;
    if (mpz_cmp(gmp_result, asm_result) == 0) {
        printf("✓ PASS: Assembly result matches GMP\n");
        passed_tests++;
    } else {
        printf("✗ FAIL: Results differ!\n");
        gmp_printf("GMP Result     = 0x%Zx\n", gmp_result);
        gmp_printf("Assembly Result= 0x%Zx\n", asm_result);
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
}

void test_512_multiplication(const char* test_name, 
                            uint64_t a[8], uint64_t b[8]) {
    printf("\n=== %s ===\n", test_name);
    
    // Prepare result array
    uint64_t result[16] = {0}; // Will store 1024-bit result
    
    // Print inputs
    print_uint512("A", a);
    print_uint512("B", b);
    
    // Call our assembly function
    mul512x512(a, b, result);
    
    // Print assembly result
    print_uint1024("Assembly Result", result);
    
    // Verify with GMP
    mpz_t gmp_a, gmp_b, gmp_result, asm_result;
    mpz_inits(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    
    // Convert inputs to GMP
    uint512_to_mpz(gmp_a, a);
    uint512_to_mpz(gmp_b, b);
    
    // Compute reference result with GMP
    mpz_mul(gmp_result, gmp_a, gmp_b);
    
    // Convert assembly result to GMP for comparison
    uint1024_to_mpz(asm_result, result);
    
    // Compare results
    total_tests++;
    if (mpz_cmp(gmp_result, asm_result) == 0) {
        printf("✓ PASS: Assembly result matches GMP\n");
        passed_tests++;
    } else {
        printf("✗ FAIL: Results differ!\n");
        gmp_printf("GMP Result     = 0x%Zx\n", gmp_result);
        gmp_printf("Assembly Result= 0x%Zx\n", asm_result);
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
}

void test_256_multiplication(const char* test_name, 
                            uint64_t a[4], uint64_t b[4]) {
    printf("\n=== %s ===\n", test_name);
    
    // Prepare result array
    uint64_t result[8] = {0, 0, 0, 0, 0, 0, 0, 0}; // Will store 512-bit result
    
    // Print inputs
    print_uint256("A", a);
    print_uint256("B", b);
    
    // Call our assembly function
    mul256x256(a, b, result);
    
    // Print assembly result
    print_uint512("Assembly Result", result);
    
    // Verify with GMP
    mpz_t gmp_a, gmp_b, gmp_result, asm_result;
    mpz_inits(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    
    // Convert inputs to GMP
    uint256_to_mpz(gmp_a, a);
    uint256_to_mpz(gmp_b, b);
    
    // Compute reference result with GMP
    mpz_mul(gmp_result, gmp_a, gmp_b);
    
    // Convert assembly result to GMP for comparison
    uint512_to_mpz(asm_result, result);
    
    // Compare results
    total_tests++;
    if (mpz_cmp(gmp_result, asm_result) == 0) {
        printf("✓ PASS: Assembly result matches GMP\n");
        passed_tests++;
    } else {
        printf("✗ FAIL: Results differ!\n");
        gmp_printf("GMP Result     = 0x%Zx\n", gmp_result);
        gmp_printf("Assembly Result= 0x%Zx\n", asm_result);
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
}

// Generate random 64-bit value
uint64_t random_uint64() {
    return ((uint64_t)rand() << 32) | rand();
}

// Silent version of test_128_multiplication for bulk testing
int test_128_multiplication_silent(uint64_t a_high, uint64_t a_low, 
                                  uint64_t b_high, uint64_t b_low) {
    uint64_t a[2] = {a_low, a_high};
    uint64_t b[2] = {b_low, b_high};
    uint64_t result[4] = {0, 0, 0, 0};
    
    mul128x128(a, b, result);
    
    mpz_t gmp_a, gmp_b, gmp_result, asm_result;
    mpz_inits(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    
    uint128_to_mpz(gmp_a, a_high, a_low);
    uint128_to_mpz(gmp_b, b_high, b_low);
    mpz_mul(gmp_result, gmp_a, gmp_b);
    uint256_to_mpz(asm_result, result);
    
    total_tests++;
    int passed = (mpz_cmp(gmp_result, asm_result) == 0);
    if (passed) {
        passed_tests++;
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    return passed;
}

// Silent version of test_256_multiplication for bulk testing
int test_256_multiplication_silent(uint64_t a[4], uint64_t b[4]) {
    uint64_t result[8] = {0, 0, 0, 0, 0, 0, 0, 0};
    
    mul256x256(a, b, result);
    
    mpz_t gmp_a, gmp_b, gmp_result, asm_result;
    mpz_inits(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    
    uint256_to_mpz(gmp_a, a);
    uint256_to_mpz(gmp_b, b);
    mpz_mul(gmp_result, gmp_a, gmp_b);
    uint512_to_mpz(asm_result, result);
    
    total_tests++;
    int passed = (mpz_cmp(gmp_result, asm_result) == 0);
    if (passed) {
        passed_tests++;
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    return passed;
}

// Silent version of test_512_multiplication for bulk testing
int test_512_multiplication_silent(uint64_t a[8], uint64_t b[8]) {
    uint64_t result[16] = {0};
    
    mul512x512(a, b, result);
    
    mpz_t gmp_a, gmp_b, gmp_result, asm_result;
    mpz_inits(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    
    uint512_to_mpz(gmp_a, a);
    uint512_to_mpz(gmp_b, b);
    mpz_mul(gmp_result, gmp_a, gmp_b);
    uint1024_to_mpz(asm_result, result);
    
    total_tests++;
    int passed = (mpz_cmp(gmp_result, asm_result) == 0);
    if (passed) {
        passed_tests++;
    }
    
    mpz_clears(gmp_a, gmp_b, gmp_result, asm_result, NULL);
    return passed;
}

void run_128_bit_edge_cases() {
    printf("\n========================================\n");
    printf("128×128→256 Edge Case Tests (20 tests)\n");
    printf("========================================\n");
    
    int edge_passed = 0;
    int edge_total = 0;
    
    // Edge case 1: Both zero
    edge_total++; if (test_128_multiplication_silent(0, 0, 0, 0)) edge_passed++;
    
    // Edge case 2: One zero, other max
    edge_total++; if (test_128_multiplication_silent(0, 0, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL)) edge_passed++;
    edge_total++; if (test_128_multiplication_silent(0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 0)) edge_passed++;
    
    // Edge case 3: Both 1
    edge_total++; if (test_128_multiplication_silent(0, 1, 0, 1)) edge_passed++;
    
    // Edge case 4: Powers of 2
    edge_total++; if (test_128_multiplication_silent(0, 1, 0, 2)) edge_passed++; // 1 * 2
    edge_total++; if (test_128_multiplication_silent(0, 4, 0, 8)) edge_passed++; // 4 * 8
    edge_total++; if (test_128_multiplication_silent(1, 0, 2, 0)) edge_passed++; // 2^64 * 2^65
    
    // Edge case 5: Maximum 64-bit values
    edge_total++; if (test_128_multiplication_silent(0, 0xFFFFFFFFFFFFFFFFULL, 0, 0xFFFFFFFFFFFFFFFFULL)) edge_passed++;
    
    // Edge case 6: High bit set in one operand
    edge_total++; if (test_128_multiplication_silent(0x8000000000000000ULL, 0, 0, 1)) edge_passed++;
    edge_total++; if (test_128_multiplication_silent(0, 1, 0x8000000000000000ULL, 0)) edge_passed++;
    
    // Edge case 7: All bits set in low word
    edge_total++; if (test_128_multiplication_silent(0, 0xFFFFFFFFFFFFFFFFULL, 0, 2)) edge_passed++;
    
    // Edge case 8: Alternating bit patterns
    edge_total++; if (test_128_multiplication_silent(0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL)) edge_passed++;
    
    // Edge case 9: Single bit set in each word
    edge_total++; if (test_128_multiplication_silent(1, 1, 1, 1)) edge_passed++;
    edge_total++; if (test_128_multiplication_silent(0x8000000000000000ULL, 0x8000000000000000ULL, 1, 1)) edge_passed++;
    
    // Edge case 10: Prime-like numbers
    edge_total++; if (test_128_multiplication_silent(0, 0xFFFFFFFFFFFFFFC5ULL, 0, 0xFFFFFFFFFFFFFFC5ULL)) edge_passed++; // Large prime
    
    // Edge case 11: Mersenne-like numbers
    edge_total++; if (test_128_multiplication_silent(0, 0x7FFFFFFFFFFFFFFFULL, 0, 0x7FFFFFFFFFFFFFFFULL)) edge_passed++; // 2^63-1
    edge_total++; if (test_128_multiplication_silent(0x7FFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 2)) edge_passed++; // (2^127-1) * 2
    
    // Edge case 12: Carry propagation stress tests
    edge_total++; if (test_128_multiplication_silent(0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 0xFFFFFFFFFFFFFFFFULL)) edge_passed++;
    edge_total++; if (test_128_multiplication_silent(0xFFFFFFFFFFFFFFFFULL, 0, 0xFFFFFFFFFFFFFFFFULL, 0)) edge_passed++;
    
    // Edge case 13: One operand is power of 2, other is max
    edge_total++; if (test_128_multiplication_silent(0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 0x8000000000000000ULL)) edge_passed++;
    
    printf("Edge cases: %d/%d passed\n", edge_passed, edge_total);
}

void run_256_bit_edge_cases() {
    printf("\n========================================\n");
    printf("256×256→512 Edge Case Tests (20 tests)\n");
    printf("========================================\n");
    
    int edge_passed = 0;
    int edge_total = 0;
    
    // Edge case 1: Both zero
    uint64_t zero[4] = {0, 0, 0, 0};
    edge_total++; if (test_256_multiplication_silent(zero, zero)) edge_passed++;
    
    // Edge case 2: One zero, other max
    uint64_t max[4] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL};
    edge_total++; if (test_256_multiplication_silent(zero, max)) edge_passed++;
    edge_total++; if (test_256_multiplication_silent(max, zero)) edge_passed++;
    
    // Edge case 3: Both 1
    uint64_t one[4] = {1, 0, 0, 0};
    edge_total++; if (test_256_multiplication_silent(one, one)) edge_passed++;
    
    // Edge case 4: Powers of 2
    uint64_t two[4] = {2, 0, 0, 0};
    uint64_t four[4] = {4, 0, 0, 0};
    uint64_t pow64[4] = {0, 1, 0, 0};  // 2^64
    uint64_t pow128[4] = {0, 0, 1, 0}; // 2^128
    
    edge_total++; if (test_256_multiplication_silent(one, two)) edge_passed++;
    edge_total++; if (test_256_multiplication_silent(two, four)) edge_passed++;
    edge_total++; if (test_256_multiplication_silent(pow64, pow64)) edge_passed++;
    edge_total++; if (test_256_multiplication_silent(pow128, pow128)) edge_passed++;
    
    // Edge case 5: Maximum 64-bit value in each position
    uint64_t max_low[4] = {0xFFFFFFFFFFFFFFFFULL, 0, 0, 0};
    uint64_t max_high[4] = {0, 0, 0, 0xFFFFFFFFFFFFFFFFULL};
    
    edge_total++; if (test_256_multiplication_silent(max_low, max_low)) edge_passed++;
    edge_total++; if (test_256_multiplication_silent(max_high, max_high)) edge_passed++;
    
    // Edge case 6: High bit set
    uint64_t high_bit[4] = {0, 0, 0, 0x8000000000000000ULL};
    edge_total++; if (test_256_multiplication_silent(high_bit, one)) edge_passed++;
    edge_total++; if (test_256_multiplication_silent(high_bit, two)) edge_passed++;
    
    // Edge case 7: Alternating patterns
    uint64_t alt1[4] = {0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL};
    uint64_t alt2[4] = {0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL};
    edge_total++; if (test_256_multiplication_silent(alt1, alt2)) edge_passed++;
    
    // Edge case 8: Mersenne-like numbers
    uint64_t mersenne[4] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 0x7FFFFFFFFFFFFFFFULL}; // 2^191-1
    edge_total++; if (test_256_multiplication_silent(mersenne, two)) edge_passed++;
    
    // Edge case 9: Carry propagation stress
    uint64_t carry_test1[4] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 0};
    uint64_t carry_test2[4] = {0xFFFFFFFFFFFFFFFFULL, 0, 0, 0};
    edge_total++; if (test_256_multiplication_silent(carry_test1, carry_test2)) edge_passed++;
    
    // Edge case 10: Single bit in each word
    uint64_t bits[4] = {1, 1, 1, 1};
    edge_total++; if (test_256_multiplication_silent(bits, bits)) edge_passed++;
    
    // Edge case 11: Large prime-like numbers
    uint64_t prime_like[4] = {0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL};
    edge_total++; if (test_256_multiplication_silent(prime_like, one)) edge_passed++;
    
    // Edge case 12: Sequential patterns
    uint64_t seq1[4] = {0x0123456789ABCDEFULL, 0x123456789ABCDEF0ULL, 0x23456789ABCDEF01ULL, 0x3456789ABCDEF012ULL};
    uint64_t seq2[4] = {0xFEDCBA9876543210ULL, 0xEDCBA9876543210FULL, 0xDCBA9876543210FEULL, 0xCBA9876543210FEDULL};
    edge_total++; if (test_256_multiplication_silent(seq1, seq2)) edge_passed++;
    
    printf("Edge cases: %d/%d passed\n", edge_passed, edge_total);
}

void run_512_bit_edge_cases() {
    printf("\n========================================\n");
    printf("512×512→1024 Edge Case Tests (20 tests)\n");
    printf("========================================\n");
    
    int edge_passed = 0;
    int edge_total = 0;
    
    // Edge case 1: Both zero
    uint64_t zero[8] = {0, 0, 0, 0, 0, 0, 0, 0};
    edge_total++; if (test_512_multiplication_silent(zero, zero)) edge_passed++;
    
    // Edge case 2: One zero, other max
    uint64_t max[8] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,
                       0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL};
    edge_total++; if (test_512_multiplication_silent(zero, max)) edge_passed++;
    edge_total++; if (test_512_multiplication_silent(max, zero)) edge_passed++;
    
    // Edge case 3: Both 1
    uint64_t one[8] = {1, 0, 0, 0, 0, 0, 0, 0};
    edge_total++; if (test_512_multiplication_silent(one, one)) edge_passed++;
    
    // Edge case 4: Powers of 2
    uint64_t two[8] = {2, 0, 0, 0, 0, 0, 0, 0};
    uint64_t four[8] = {4, 0, 0, 0, 0, 0, 0, 0};
    uint64_t pow64[8] = {0, 1, 0, 0, 0, 0, 0, 0};   // 2^64
    uint64_t pow256[8] = {0, 0, 0, 0, 1, 0, 0, 0};  // 2^256
    
    edge_total++; if (test_512_multiplication_silent(one, two)) edge_passed++;
    edge_total++; if (test_512_multiplication_silent(two, four)) edge_passed++;
    edge_total++; if (test_512_multiplication_silent(pow64, pow64)) edge_passed++;
    edge_total++; if (test_512_multiplication_silent(pow256, pow256)) edge_passed++;
    
    // Edge case 5: Maximum 64-bit value in each position
    uint64_t max_low[8] = {0xFFFFFFFFFFFFFFFFULL, 0, 0, 0, 0, 0, 0, 0};
    uint64_t max_high[8] = {0, 0, 0, 0, 0, 0, 0, 0xFFFFFFFFFFFFFFFFULL};
    
    edge_total++; if (test_512_multiplication_silent(max_low, max_low)) edge_passed++;
    edge_total++; if (test_512_multiplication_silent(max_high, max_high)) edge_passed++;
    
    // Edge case 6: High bit set
    uint64_t high_bit[8] = {0, 0, 0, 0, 0, 0, 0, 0x8000000000000000ULL};
    edge_total++; if (test_512_multiplication_silent(high_bit, one)) edge_passed++;
    edge_total++; if (test_512_multiplication_silent(high_bit, two)) edge_passed++;
    
    // Edge case 7: Alternating patterns
    uint64_t alt1[8] = {0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL,
                        0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL};
    uint64_t alt2[8] = {0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL,
                        0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL, 0x5555555555555555ULL, 0xAAAAAAAAAAAAAAAAULL};
    edge_total++; if (test_512_multiplication_silent(alt1, alt2)) edge_passed++;
    
    // Edge case 8: Mersenne-like numbers
    uint64_t mersenne[8] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,
                           0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0x7FFFFFFFFFFFFFFFULL}; // 2^511-1
    edge_total++; if (test_512_multiplication_silent(mersenne, two)) edge_passed++;
    
    // Edge case 9: Carry propagation stress
    uint64_t carry_test1[8] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0, 0, 0, 0};
    uint64_t carry_test2[8] = {0xFFFFFFFFFFFFFFFFULL, 0, 0, 0, 0, 0, 0, 0};
    edge_total++; if (test_512_multiplication_silent(carry_test1, carry_test2)) edge_passed++;
    
    // Edge case 10: Single bit in each word
    uint64_t bits[8] = {1, 1, 1, 1, 1, 1, 1, 1};
    edge_total++; if (test_512_multiplication_silent(bits, bits)) edge_passed++;
    
    // Edge case 11: Large prime-like numbers
    uint64_t prime_like[8] = {0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL,
                             0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL, 0xFFFFFFFFFFFFFFC5ULL};
    edge_total++; if (test_512_multiplication_silent(prime_like, one)) edge_passed++;
    
    // Edge case 12: Sequential patterns
    uint64_t seq1[8] = {0x0123456789ABCDEFULL, 0x123456789ABCDEF0ULL, 0x23456789ABCDEF01ULL, 0x3456789ABCDEF012ULL,
                       0x456789ABCDEF0123ULL, 0x56789ABCDEF01234ULL, 0x6789ABCDEF012345ULL, 0x789ABCDEF0123456ULL};
    uint64_t seq2[8] = {0xFEDCBA9876543210ULL, 0xEDCBA9876543210FULL, 0xDCBA9876543210FEULL, 0xCBA9876543210FEDULL,
                       0xBA9876543210FEDCULL, 0xA9876543210FEDCBULL, 0x9876543210FEDCBAULL, 0x876543210FEDCBA9ULL};
    edge_total++; if (test_512_multiplication_silent(seq1, seq2)) edge_passed++;
    
    printf("Edge cases: %d/%d passed\n", edge_passed, edge_total);
}

void run_128_bit_random_tests() {
    printf("\n========================================\n");
    printf("128×128→256 Random Tests (100 tests)\n");
    printf("========================================\n");
    
    int random_passed = 0;
    for (int i = 0; i < 100; i++) {
        uint64_t a_high = random_uint64();
        uint64_t a_low = random_uint64();
        uint64_t b_high = random_uint64();
        uint64_t b_low = random_uint64();
        
        if (test_128_multiplication_silent(a_high, a_low, b_high, b_low)) {
            random_passed++;
        }
        
        if ((i + 1) % 20 == 0) {
            printf("Completed %d/100 random tests\n", i + 1);
        }
    }
    
    printf("Random tests: %d/100 passed\n", random_passed);
}

void run_256_bit_random_tests() {
    printf("\n========================================\n");
    printf("256×256→512 Random Tests (100 tests)\n");
    printf("========================================\n");
    
    int random_passed = 0;
    for (int i = 0; i < 100; i++) {
        uint64_t a[4] = {random_uint64(), random_uint64(), random_uint64(), random_uint64()};
        uint64_t b[4] = {random_uint64(), random_uint64(), random_uint64(), random_uint64()};
        
        if (test_256_multiplication_silent(a, b)) {
            random_passed++;
        }
        
        if ((i + 1) % 20 == 0) {
            printf("Completed %d/100 random tests\n", i + 1);
        }
    }
    
    printf("Random tests: %d/100 random tests passed\n", random_passed);
}

void run_512_bit_random_tests() {
    printf("\n========================================\n");
    printf("512×512→1024 Random Tests (100 tests)\n");
    printf("========================================\n");
    
    int random_passed = 0;
    for (int i = 0; i < 100; i++) {
        uint64_t a[8] = {random_uint64(), random_uint64(), random_uint64(), random_uint64(),
                         random_uint64(), random_uint64(), random_uint64(), random_uint64()};
        uint64_t b[8] = {random_uint64(), random_uint64(), random_uint64(), random_uint64(),
                         random_uint64(), random_uint64(), random_uint64(), random_uint64()};
        
        if (test_512_multiplication_silent(a, b)) {
            random_passed++;
        }
        
        if ((i + 1) % 20 == 0) {
            printf("Completed %d/100 random tests\n", i + 1);
        }
    }
    
    printf("Random tests: %d/100 random tests passed\n", random_passed);
}

void run_128_bit_tests() {
    printf("========================================\n");
    printf("128×128→256 Multiplication Tests\n");
    printf("========================================\n");
    
    // Test 1: Small numbers
    test_128_multiplication("128-bit Test 1: Small Numbers",
                           0x0000000000000000ULL, 0x000000000000000FULL,  // A = 15
                           0x0000000000000000ULL, 0x0000000000000010ULL); // B = 16
    
    // Test 2: Medium numbers
    test_128_multiplication("128-bit Test 2: Medium Numbers", 
                           0x0000000000000001ULL, 0x0000000000000000ULL,  // A = 2^64
                           0x0000000000000002ULL, 0x0000000000000000ULL); // B = 2^65
    
    // Test 3: Large numbers
    test_128_multiplication("128-bit Test 3: Large Numbers",
                           0x123456789ABCDEFULL, 0xFEDCBA9876543210ULL,  // A = large
                           0x0FEDCBA987654321ULL, 0x123456789ABCDEFULL); // B = large
    
    // Test 4: Maximum values
    test_128_multiplication("128-bit Test 4: Maximum Values",
                           0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,  // A = 2^128 - 1
                           0x0000000000000000ULL, 0x0000000000000002ULL); // B = 2
    
    // Test 5: Edge case - one operand is zero
    test_128_multiplication("128-bit Test 5: Zero Operand",
                           0x0000000000000000ULL, 0x0000000000000000ULL,  // A = 0
                           0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL); // B = max
}

void run_256_bit_tests() {
    printf("\n\n========================================\n");
    printf("256×256→512 Multiplication Tests\n");
    printf("========================================\n");
    
    // Test 1: Small numbers
    uint64_t a1[4] = {0x000000000000000FULL, 0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000000ULL};  // A = 15
    uint64_t b1[4] = {0x0000000000000010ULL, 0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000000ULL};  // B = 16
    test_256_multiplication("256-bit Test 1: Small Numbers", a1, b1);
    
    // Test 2: Medium numbers with carry propagation
    uint64_t a2[4] = {0x0000000000000000ULL, 0x0000000000000001ULL, 0x0000000000000000ULL, 0x0000000000000000ULL};  // A = 2^64
    uint64_t b2[4] = {0x0000000000000000ULL, 0x0000000000000002ULL, 0x0000000000000000ULL, 0x0000000000000000ULL};  // B = 2^65
    test_256_multiplication("256-bit Test 2: Medium Numbers", a2, b2);
    
    // Test 3: Large numbers using all 256 bits
    uint64_t a3[4] = {0xFEDCBA9876543210ULL, 0x123456789ABCDEFULL, 0x0FEDCBA987654321ULL, 0x123456789ABCDEFULL};
    uint64_t b3[4] = {0x123456789ABCDEFULL, 0xFEDCBA9876543210ULL, 0x123456789ABCDEFULL, 0x0FEDCBA987654321ULL}; 
    test_256_multiplication("256-bit Test 3: Large Numbers", a3, b3);
    
    // Test 4: Maximum 256-bit values
    uint64_t a4[4] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL};  // A = 2^256 - 1
    uint64_t b4[4] = {0x0000000000000002ULL, 0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000000ULL};  // B = 2
    test_256_multiplication("256-bit Test 4: Maximum × Small", a4, b4);
    
    // Test 5: Edge case - one operand is zero
    uint64_t a5[4] = {0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000000ULL};  // A = 0
    uint64_t b5[4] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL};  // B = max
    test_256_multiplication("256-bit Test 5: Zero Operand", a5, b5);
    
    // Test 6: Powers of 2
    uint64_t a6[4] = {0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000001ULL, 0x0000000000000000ULL};  // A = 2^128
    uint64_t b6[4] = {0x0000000000000000ULL, 0x0000000000000000ULL, 0x0000000000000001ULL, 0x0000000000000000ULL};  // B = 2^128
    test_256_multiplication("256-bit Test 6: Powers of 2", a6, b6);
    
    // Test 7: High bit set in both operands
    uint64_t a7[4] = {0x0000000000000001ULL, 0x0000000000000000ULL, 0x0000000000000000ULL, 0x8000000000000000ULL};  // A = 2^255 + 1
    uint64_t b7[4] = {0x0000000000000001ULL, 0x0000000000000000ULL, 0x0000000000000000ULL, 0x8000000000000000ULL};  // B = 2^255 + 1
    test_256_multiplication("256-bit Test 7: High Bits Set", a7, b7);
}

void run_512_bit_tests() {
    printf("\n\n========================================\n");
    printf("512×512→1024 Multiplication Tests\n");
    printf("========================================\n");
    
    // Test 1: Small numbers
    uint64_t a1[8] = {0x000000000000000FULL, 0, 0, 0, 0, 0, 0, 0};  // A = 15
    uint64_t b1[8] = {0x0000000000000010ULL, 0, 0, 0, 0, 0, 0, 0};  // B = 16
    test_512_multiplication("512-bit Test 1: Small Numbers", a1, b1);
    
    // Test 2: Medium numbers with carry propagation
    uint64_t a2[8] = {0, 0, 0, 0, 0x0000000000000001ULL, 0, 0, 0};  // A = 2^256
    uint64_t b2[8] = {0, 0, 0, 0, 0x0000000000000002ULL, 0, 0, 0};  // B = 2^257
    test_512_multiplication("512-bit Test 2: Medium Numbers", a2, b2);
    
    // Test 3: Large numbers using all 512 bits
    uint64_t a3[8] = {0xFEDCBA9876543210ULL, 0x123456789ABCDEFULL, 0x0FEDCBA987654321ULL, 0x123456789ABCDEFULL,
                      0xFEDCBA9876543210ULL, 0x123456789ABCDEFULL, 0x0FEDCBA987654321ULL, 0x123456789ABCDEFULL};
    uint64_t b3[8] = {0x123456789ABCDEFULL, 0xFEDCBA9876543210ULL, 0x123456789ABCDEFULL, 0x0FEDCBA987654321ULL,
                      0x123456789ABCDEFULL, 0xFEDCBA9876543210ULL, 0x123456789ABCDEFULL, 0x0FEDCBA987654321ULL}; 
    test_512_multiplication("512-bit Test 3: Large Numbers", a3, b3);
    
    // Test 4: Maximum 512-bit values
    uint64_t a4[8] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,
                      0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL};  // A = 2^512 - 1
    uint64_t b4[8] = {0x0000000000000002ULL, 0, 0, 0, 0, 0, 0, 0};  // B = 2
    test_512_multiplication("512-bit Test 4: Maximum × Small", a4, b4);
    
    // Test 5: Edge case - one operand is zero
    uint64_t a5[8] = {0, 0, 0, 0, 0, 0, 0, 0};  // A = 0
    uint64_t b5[8] = {0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,
                      0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL};  // B = max
    test_512_multiplication("512-bit Test 5: Zero Operand", a5, b5);
    
    // Test 6: Powers of 2
    uint64_t a6[8] = {0, 0, 0, 0, 0, 0, 0x0000000000000001ULL, 0};  // A = 2^384
    uint64_t b6[8] = {0, 0, 0, 0, 0, 0, 0x0000000000000001ULL, 0};  // B = 2^384
    test_512_multiplication("512-bit Test 6: Powers of 2", a6, b6);
    
    // Test 7: High bit set in both operands
    uint64_t a7[8] = {0x0000000000000001ULL, 0, 0, 0, 0, 0, 0, 0x8000000000000000ULL};  // A = 2^511 + 1
    uint64_t b7[8] = {0x0000000000000001ULL, 0, 0, 0, 0, 0, 0, 0x8000000000000000ULL};  // B = 2^511 + 1
    test_512_multiplication("512-bit Test 7: High Bits Set", a7, b7);
}

int main() {
    printf("Combined Bignum Multiplication Test Suite with GMP Verification\n");
    printf("==============================================================\n");
    
    // Initialize random seed
    srand((unsigned int)time(NULL));
    
    // Initialize counters
    total_tests = 0;
    passed_tests = 0;
    
    // Run original basic tests
    run_128_bit_tests();
    run_256_bit_tests();
    run_512_bit_tests();
    
    // Run comprehensive edge case tests
    run_128_bit_edge_cases();
    run_256_bit_edge_cases();
    run_512_bit_edge_cases();
    
    // Run random tests
    run_128_bit_random_tests();
    run_256_bit_random_tests();
    run_512_bit_random_tests();
    
    printf("\n=== Final Test Summary ===\n");
    printf("Total tests run: %d\n", total_tests);
    printf("Tests passed:    %d\n", passed_tests);
    printf("Tests failed:    %d\n", total_tests - passed_tests);
    printf("Success rate:    %.2f%%\n", (double)passed_tests / total_tests * 100.0);
    
    if (passed_tests == total_tests) {
        printf("🎉 ALL TESTS PASSED! 🎉\n");
        return 0;
    } else {
        printf("❌ SOME TESTS FAILED ❌\n");
        return 1;
    }
}
