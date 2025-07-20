# Combined Makefile for 128×128→256, 256×256→512, and 512×512→1024 multiplication tests
# Requires GMP library: brew install gmp (on macOS) or apt-get install libgmp-dev (on Linux)

CC = gcc
AS = as
CFLAGS = -O2 -Wall -Wextra
LDFLAGS = -lgmp

# Detect architecture
UNAME_M := $(shell uname -m)
ifeq ($(UNAME_M),arm64)
    ARCH_FLAGS = -arch arm64
else ifeq ($(UNAME_M),x86_64)
    # Cross-compile for ARM64 on x86_64 (requires cross-compiler)
    CC = aarch64-linux-gnu-gcc
    AS = aarch64-linux-gnu-as
    ARCH_FLAGS = 
else
    ARCH_FLAGS = 
endif

# Combined targets
TARGET_COMBINED = test_mul_combined
ASM_OBJ_128 = mul128x128_fixed.o
ASM_OBJ_256 = mul256x256_fixed.o
ASM_OBJ_512 = mul512x512_fixed.o
C_OBJ_COMBINED = test_mul_combined.o

# 512×512 specific targets
TARGET_512 = test_mul512
C_OBJ_512 = test_mul512.o

# Legacy individual targets (keeping for compatibility)
TARGET_128 = test_mul128
TARGET_256 = test_mul256
C_OBJ_128 = test_mul128.o
C_OBJ_256 = test_mul256.o

.PHONY: all clean run run-128 run-256 run-512 run-combined install-deps gen-all gen-128 gen-256 gen-512 help

# Default target builds combined version
all: $(TARGET_COMBINED)

# Combined targets
$(TARGET_COMBINED): $(ASM_OBJ_128) $(ASM_OBJ_256) $(ASM_OBJ_512) $(C_OBJ_COMBINED)
	$(CC) $(ARCH_FLAGS) -o $@ $^ $(LDFLAGS)

$(C_OBJ_COMBINED): test_mul_combined.c
	$(CC) $(ARCH_FLAGS) $(CFLAGS) -c -o $@ $<

# Legacy individual targets (128-bit)
$(TARGET_128): $(ASM_OBJ_128) $(C_OBJ_128)
	$(CC) $(ARCH_FLAGS) -o $@ $^ $(LDFLAGS)

$(C_OBJ_128): test_mul128.c
	$(CC) $(ARCH_FLAGS) $(CFLAGS) -c -o $@ $<

# Legacy individual targets (256-bit)
$(TARGET_256): $(ASM_OBJ_256) $(C_OBJ_256)
	$(CC) $(ARCH_FLAGS) -o $@ $^ $(LDFLAGS)

$(C_OBJ_256): test_mul256.c
	$(CC) $(ARCH_FLAGS) $(CFLAGS) -c -o $@ $<

# Assembly object files
$(ASM_OBJ_128): mul128x128_fixed.s
	$(AS) $(ARCH_FLAGS) -o $@ $<

$(ASM_OBJ_256): mul256x256_fixed.s
	$(AS) $(ARCH_FLAGS) -o $@ $<

# 512×512 specific targets
$(TARGET_512): $(ASM_OBJ_512) $(C_OBJ_512)
	$(CC) $(ARCH_FLAGS) -o $@ $^

$(C_OBJ_512): test_mul512.c
	$(CC) $(ARCH_FLAGS) $(CFLAGS) -c -o $@ $<

$(ASM_OBJ_512): mul512x512_fixed.s
	$(AS) $(ARCH_FLAGS) -o $@ $<

# Generate assembly code using Python scripts
gen-all: gen-128 gen-256 gen-512

gen-combined:
	python3 demo_mul_fixed.py

gen-512:
	python3 demo_mul_fixed.py

gen-128:
	@if [ -f "demo_mul128_fixed.py" ]; then \
		python3 demo_mul128_fixed.py; \
	else \
		python3 demo_mul_fixed.py; \
	fi

gen-256:
	@if [ -f "demo_mul256_fixed.py" ]; then \
		python3 demo_mul256_fixed.py; \
	else \
		python3 demo_mul_fixed.py; \
	fi

# Run targets
run: $(TARGET_COMBINED)
	./$(TARGET_COMBINED)

run-combined: $(TARGET_COMBINED)
	./$(TARGET_COMBINED)

run-128: $(TARGET_128)
	./$(TARGET_128)

run-256: $(TARGET_256)
	./$(TARGET_256)

run-512: $(TARGET_512)
	./$(TARGET_512)

# Build individual targets
build-128: $(TARGET_128)

build-256: $(TARGET_256)

build-512: $(TARGET_512)

build-combined: $(TARGET_COMBINED)

clean:
	rm -f $(TARGET_128) $(ASM_OBJ_128) $(C_OBJ_128)
	rm -f $(TARGET_256) $(ASM_OBJ_256) $(C_OBJ_256)
	rm -f $(TARGET_512) $(ASM_OBJ_512) $(C_OBJ_512)
	rm -f $(TARGET_COMBINED) $(C_OBJ_COMBINED)
	rm -f mul128x128_fixed.s mul256x256_fixed.s mul512x512_fixed.s

clean-asm:
	rm -f mul128x128_fixed.s mul256x256_fixed.s mul512x512_fixed.s

install-deps:
	@echo "Installing GMP library..."
	@if command -v brew >/dev/null 2>&1; then \
		echo "Using Homebrew (macOS)..."; \
		brew install gmp; \
	elif command -v apt-get >/dev/null 2>&1; then \
		echo "Using apt-get (Ubuntu/Debian)..."; \
		sudo apt-get update && sudo apt-get install -y libgmp-dev; \
	elif command -v yum >/dev/null 2>&1; then \
		echo "Using yum (RedHat/CentOS)..."; \
		sudo yum install -y gmp-devel; \
	else \
		echo "Please install GMP library manually for your system"; \
		exit 1; \
	fi

help:
	@echo "Combined Bignum Multiplication Makefile"
	@echo "========================================"
	@echo ""
	@echo "Main targets:"
	@echo "  all         - Build the combined test program (default)"
	@echo "  run         - Build and run the combined test program"
	@echo "  clean       - Remove all build files"
	@echo "  install-deps- Install GMP library"
	@echo ""
	@echo "Generation targets:"
	@echo "  gen-combined- Generate both assembly files using combined script"
	@echo "  gen-all     - Generate both assembly files (alias for gen-combined)"
	@echo "  gen-128     - Generate 128-bit assembly"
	@echo "  gen-256     - Generate 256-bit assembly"
	@echo ""
	@echo "Individual targets (legacy):"
	@echo "  build-128   - Build 128-bit test program only"
	@echo "  build-256   - Build 256-bit test program only"
	@echo "  run-128     - Run 128-bit test program only"
	@echo "  run-256     - Run 256-bit test program only"
	@echo ""
	@echo "Utility targets:"
	@echo "  clean-asm   - Remove generated assembly files only"
	@echo "  help        - Show this help"
