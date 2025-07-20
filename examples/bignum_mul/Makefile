# Makefile for 128×128→256 multiplication test
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

TARGET = test_mul128
ASM_OBJ = mul128x128_fixed.o
C_OBJ = test_mul128.o

.PHONY: all clean run install-deps

all: $(TARGET)

$(TARGET): $(ASM_OBJ) $(C_OBJ)
	$(CC) $(ARCH_FLAGS) -o $@ $^ $(LDFLAGS)

$(ASM_OBJ): mul128x128_fixed.s
	$(AS) $(ARCH_FLAGS) -o $@ $<

$(C_OBJ): test_mul128.c
	$(CC) $(ARCH_FLAGS) $(CFLAGS) -c -o $@ $<

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) $(ASM_OBJ) $(C_OBJ)

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
	@echo "Available targets:"
	@echo "  all         - Build the test program"
	@echo "  run         - Build and run the test"
	@echo "  clean       - Remove build files"
	@echo "  install-deps- Install GMP library"
	@echo "  help        - Show this help"
