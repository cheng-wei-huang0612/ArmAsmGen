#!/usr/bin/env python3

"""
ArmAsmGen Examples Index
Run this to see all available examples and what they demonstrate.
"""

import os
import sys
from pathlib import Path

def show_examples_menu():
    """Display a menu of all available examples"""
    examples = {
        "1": {
            "name": "Basic Usage",
            "file": "demo_basic.py", 
            "description": "Introduction to basic assembly generation"
        },
        "2": {
            "name": "Vector ADD Operations", 
            "file": "demo_vector_add.py",
            "description": "SIMD vector ADD with different element arrangements"
        },
        "3": {
            "name": "Vector Memory Operations",
            "file": "demo_vector_memory.py", 
            "description": "Vector load/store with proper q-register conversion"
        },
        "4": {
            "name": "Register Validation",
            "file": "demo_register_validation.py",
            "description": "Type safety and register validation examples"
        },
        "5": {
            "name": "Complete Arithmetic",
            "file": "demo_complete_arithmetic.py",
            "description": "Comprehensive arithmetic operations"
        },
        "6": {
            "name": "Multi-precision Arithmetic", 
            "file": "demo_multiprecision.py",
            "description": "Large number operations with carry handling"
        },
        "7": {
            "name": "Wide Multiplication",
            "file": "demo_wide_multiply.py", 
            "description": "128×128→256 bit multiplication using UMULH/SMULH"
        },
        "8": {
            "name": "Export Formats",
            "file": "demo_export_formats.py",
            "description": "Different output formats and file export"
        },
        "9": {
            "name": "Custom Mixins",
            "file": "demo_comprehensive.py",
            "description": "Advanced mixin combinations and patterns"
        },
        "10": {
            "name": "Bignum Multiplication (Complete)",
            "file": "bignum_mul/demo_mul128_fixed.py",
            "description": "Complete bignum example with C test harness"
        }
    }
    
    print("🚀 ArmAsmGen Examples")
    print("=" * 50)
    print()
    
    for key, example in examples.items():
        print(f"{key:2}. {example['name']}")
        print(f"    File: {example['file']}")
        print(f"    {example['description']}")
        print()
    
    print("Enter a number to run an example, or 'q' to quit:")
    
    while True:
        choice = input("> ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            break
        elif choice in examples:
            example = examples[choice]
            file_path = Path(__file__).parent / example['file']
            
            if file_path.exists():
                print(f"\n🔄 Running {example['name']}...")
                print("=" * 50)
                os.system(f"python {file_path}")
                print("\n" + "=" * 50)
                print("Example completed. Enter another number or 'q' to quit:")
            else:
                print(f"❌ File {example['file']} not found!")
        else:
            print("Invalid choice. Please enter a number 1-10 or 'q' to quit.")

if __name__ == "__main__":
    try:
        show_examples_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
