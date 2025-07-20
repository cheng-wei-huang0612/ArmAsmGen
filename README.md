# ArmAsmGen - AArch64 Assembly Generator DSL

AArch64 (Arm v8-A) assembly generator Domain Specific Language for Python.

## Installation

To use this package, install it in development mode:

```bash
pip install -e .
```

## Usage

```python
from armasmgen.builder import ASMCode, Block

# Create assembly code
f = ASMCode()

with f as asm:
    asm.equ("CONST", "0x1234")
    with Block(label="main") as m:
        m.ADD("x0", "x1", "x2")
        with Block(label="inner") as inn:
            inn.ADD_imm("x3", "x4", 7)

# Output the assembly
f.stdout()
```

## Examples

See the `examples/` directory for usage examples:
- `demo_basic.py` - Basic usage example
- `demo_complex.py` - Complex program structure example

## Development

After making changes to the source code, the package is automatically updated since it's installed in development mode with `pip install -e .`.
