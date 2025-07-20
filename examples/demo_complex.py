#!/usr/bin/env python3
"""
Complex ARM Assembly Demo
Demonstrates advanced features of the armasmgen library including:
- Multiple constants and bit definitions
- Nested blocks with different labels
- Function-like code blocks
- Memory operations with stack management
- Complex arithmetic operations
- Multiple data processing patterns
"""

from armasmgen.builder import ASMCode, Block

def create_complex_arm_program():
    """Generate a complex ARM assembly program with multiple functions and data structures."""
    f = ASMCode()

    with f as asm:
        # Define constants and bit patterns
        asm.equ("BUFFER_SIZE", "0x1000")
        asm.equ("MAX_ITERATIONS", "100")
        asm.equ("STATUS_MASK", "0xFF00")
        asm.equ("ERROR_CODE", "0xDEAD")

        # Main program entry point
        with Block(label="start") as main:
            # Initialize stack and save registers
            main.STP_stack_offset("x29", "x30", -16)  # Save frame pointer and link register
            main.ADD_imm("x29", "sp", 0)  # Set up frame pointer
            
            # Initialize variables
            main.ADD_imm("x0", "xzr", 42)      # Load initial value
            main.ADD_imm("x1", "xzr", 1000)    # Load counter
            main.ADD_imm("x2", "xzr", 0)       # Initialize accumulator
            
            # Call data processing function
            with Block(label="data_processing") as process:
                # Save working registers
                process.STP_stack_offset("x3", "x4", -16)
                process.STP_stack_offset("x5", "x6", -32)
                
                # Complex arithmetic operations
                with Block(label="calculation_loop") as calc_loop:
                    # Multiply x0 by 3 using addition
                    calc_loop.ADD("x3", "x0", "x0")    # x3 = x0 * 2
                    calc_loop.ADD("x3", "x3", "x0")    # x3 = x0 * 3
                    
                    # Add to accumulator
                    calc_loop.ADD("x2", "x2", "x3")
                    
                    # Update counter and value
                    calc_loop.SUB("x1", "x1", "x0")    # Decrement counter by current value
                    calc_loop.ADD_imm("x0", "x0", 1)   # Increment current value
                    
                    # Nested condition check
                    with Block(label="bounds_check") as bounds:
                        # Check if we've exceeded maximum iterations
                        bounds.ADD_imm("x4", "xzr", 50)  # Load comparison value
                        bounds.SUB("x5", "x0", "x4")     # Compare current value
                        
                        # Simulate conditional branch logic preparation
                        with Block(label="continue_processing") as cont:
                            cont.ADD("x6", "x2", "x0")     # Additional processing
                            cont.SUB("x2", "x6", "x3")     # Adjust result
                
                # Restore working registers
                process.LDR("x5", "sp")    # Load from stack (simplified)
                process.LDR("x6", "sp")    # Load from stack (simplified)
                process.LDR("x3", "sp")    # Load from stack (simplified)
                process.LDR("x4", "sp")    # Load from stack (simplified)
            
            # Memory operations and data handling
            with Block(label="memory_operations") as memory:
                # Store results to memory locations
                memory.STR("x2", "x10")     # Store accumulator result
                memory.STR("x0", "x11")     # Store final counter value
                memory.STR("x1", "x12")     # Store remaining iterations
                
                # Load data for verification
                memory.LDR("x20", "x10")    # Load back result
                memory.LDR("x21", "x11")    # Load back counter
                memory.LDR("x22", "x12")    # Load back iterations
                
                # Perform verification calculations
                with Block(label="verify_results") as verify:
                    verify.ADD("x23", "x20", "x21")    # Combine results
                    verify.SUB("x24", "x23", "x22")    # Final verification value
                    verify.ADD_imm("x25", "x24", 1)    # Adjust for off-by-one
            
            # Error handling and cleanup section
            with Block(label="error_handling") as error:
                # Simulate error checking
                error.ADD_imm("x26", "xzr", 0)     # Clear error register
                error.SUB("x27", "x25", "xzr")     # Check if result is zero
                
                with Block(label="cleanup") as cleanup:
                    # Prepare return value
                    cleanup.ADD("x0", "x25", "xzr")   # Set return value
                    
                    # Restore stack frame
                    cleanup.SUB("sp", "x29", "x0")    # Restore stack pointer (simplified)
                    cleanup.LDR("x29", "sp")          # Restore frame pointer (simplified)
                    cleanup.LDR("x30", "sp")          # Restore link register (simplified)
                    
                    with Block(label="return_sequence") as ret_seq:
                        # Final operations before return
                        ret_seq.ADD_imm("x1", "x0", 0)     # Copy return value
                        ret_seq.ADD_imm("x2", "xzr", 0)    # Clear temporary register
        
        # Utility function simulation
        with Block(label="utility_functions") as utils:
            with Block(label="multiply_by_constant") as mult:
                # Simulate multiplication by repeated addition
                mult.ADD_imm("x10", "xzr", 0)   # Initialize result
                mult.ADD_imm("x11", "xzr", 7)   # Multiplier constant
                
                with Block(label="mult_loop") as mult_loop:
                    mult_loop.ADD("x10", "x10", "x0")  # Add multiplicand to result
                    mult_loop.SUB("x11", "x11", "x0")  # Decrement counter (simplified)
            
            with Block(label="data_manipulation") as data_manip:
                # Complex data manipulation patterns
                data_manip.ADD("x12", "x0", "x1")     # Combine inputs
                data_manip.SUB("x13", "x12", "x2")    # Subtract offset
                data_manip.ADD_imm("x14", "x13", 255) # Add constant
                
                # Nested data processing
                with Block(label="bit_operations") as bit_ops:
                    # Simulate bit manipulation using arithmetic
                    bit_ops.ADD("x15", "x14", "x14")   # Left shift simulation (x2)
                    bit_ops.ADD("x16", "x15", "x15")   # Left shift simulation (x4)
                    bit_ops.SUB("x17", "x16", "x14")   # Create bit pattern

    return f

def create_sorting_algorithm_demo():
    """Create a demo that simulates a simple sorting algorithm structure."""
    f = ASMCode()
    
    with f as asm:
        # Constants for array processing
        asm.equ("ARRAY_SIZE", "10")
        asm.equ("ELEMENT_SIZE", "8")
        asm.equ("BASE_ADDRESS", "0x10000")
        
        with Block(label="bubble_sort") as sort:
            # Initialize array processing
            sort.ADD_imm("x0", "xzr", 0)    # i = 0 (outer loop counter)
            sort.ADD_imm("x1", "xzr", 10)   # array size
            
            with Block(label="outer_loop") as outer:
                outer.ADD_imm("x2", "xzr", 0)  # j = 0 (inner loop counter)
                outer.SUB("x3", "x1", "x0")    # inner limit = size - i
                
                with Block(label="inner_loop") as inner:
                    # Load array elements for comparison
                    inner.ADD("x4", "x2", "x2")      # Calculate offset (j * 2)
                    inner.LDR("x5", "x4")            # Load array[j]
                    inner.ADD_imm("x6", "x4", 8)     # Next element offset
                    inner.LDR("x7", "x6")            # Load array[j+1]
                    
                    # Compare and potentially swap
                    with Block(label="compare_swap") as swap:
                        swap.SUB("x8", "x5", "x7")    # Compare elements
                        
                        # Simulate conditional swap
                        with Block(label="perform_swap") as do_swap:
                            do_swap.STR("x7", "x4")     # Store smaller element first
                            do_swap.STR("x5", "x6")     # Store larger element second
                    
                    # Increment inner loop counter
                    inner.ADD_imm("x2", "x2", 1)
                
                # Increment outer loop counter
                outer.ADD_imm("x0", "x0", 1)
    
    return f

if __name__ == "__main__":
    print("=== Complex ARM Assembly Demo ===\n")
    
    print("1. Complex Program with Multiple Functions:")
    print("-" * 50)
    complex_program = create_complex_arm_program()
    complex_program.stdout()
    
    print("\n\n2. Sorting Algorithm Structure:")
    print("-" * 50)
    sorting_demo = create_sorting_algorithm_demo()
    sorting_demo.stdout()
    
    print("\n=== Demo Complete ===")
