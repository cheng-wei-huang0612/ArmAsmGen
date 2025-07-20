# armasmgen/mixins/vector_arithmetic.py
from ..core import Instruction, RegArg
from ..register import Register, RegisterType, RegisterWidth
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..register import Register

class VectorArithmeticMixin:
    def emit(self, inst: Instruction): ...  # Type hint
    def _reg_to_str(self, reg: RegArg) -> str: ...  # Type hint

    def _validate_vector_register(self, reg: RegArg, param_name: str) -> str:
        """
        Validate that the register argument is appropriate for vector operations.
        Returns the string representation of the register.
        """
        # Convert to string for final output
        reg_str = self._reg_to_str(reg)
        
        # If it's a Register object, perform type checking
        if isinstance(reg, Register):
            if reg.reg_type != RegisterType.VECTOR:
                raise TypeError(
                    f"Parameter '{param_name}' must be a vector register, "
                    f"got {reg.reg_type.value} register '{reg_str}'"
                )
            
            # Check if it's the right width for vector operations
            if reg.width not in [RegisterWidth.V, RegisterWidth.D, RegisterWidth.S, RegisterWidth.H, RegisterWidth.B]:
                raise TypeError(
                    f"Parameter '{param_name}' must be a vector register width (V/D/S/H/B), "
                    f"got width '{reg.width.value}'"
                )
        
        # If it's a string, do basic validation
        elif isinstance(reg, str):
            # Check for common mistakes (general purpose registers)
            if reg.startswith('x') or reg.startswith('w'):
                raise TypeError(
                    f"Parameter '{param_name}' is a general purpose register '{reg_str}'. "
                    f"Vector ADD operations require vector registers (v0-v31)."
                )
            
            # Check for special registers
            special_regs = {'sp', 'lr', 'xzr', 'wzr', 'pc'}
            if reg.lower() in special_regs:
                raise TypeError(
                    f"Parameter '{param_name}' is a special register '{reg_str}'. "
                    f"Vector ADD operations require vector registers (v0-v31)."
                )
            
            # Check if it looks like a vector register
            if not (reg.startswith('v') or reg.startswith('d') or 
                   reg.startswith('s') or reg.startswith('h') or reg.startswith('b')):
                raise TypeError(
                    f"Parameter '{param_name}' does not appear to be a vector register '{reg_str}'. "
                    f"Vector ADD operations require vector registers (v0-v31, d0-d31, s0-s31, h0-h31, b0-b31)."
                )
        
        return reg_str

    def ADD_8B(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (8 x 8-bit elements):
        Adds 8 corresponding 8-bit elements from two vector registers.
        
            Vd.8B = Vn.8B + Vm.8B
        
        Example:
            ADD_8B("v0", "v1", "v2")  # v0.8B = v1.8B + v2.8B
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.8B, {src0}.8B, {src1}.8B",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_16B(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (16 x 8-bit elements):
        Adds 16 corresponding 8-bit elements from two vector registers.
        
            Vd.16B = Vn.16B + Vm.16B
        
        Example:
            ADD_16B("v0", "v1", "v2")  # v0.16B = v1.16B + v2.16B
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.16B, {src0}.16B, {src1}.16B",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_4H(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (4 x 16-bit elements):
        Adds 4 corresponding 16-bit elements from two vector registers.
        
            Vd.4H = Vn.4H + Vm.4H
        
        Example:
            ADD_4H("v0", "v1", "v2")  # v0.4H = v1.4H + v2.4H
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.4H, {src0}.4H, {src1}.4H",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_8H(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (8 x 16-bit elements):
        Adds 8 corresponding 16-bit elements from two vector registers.
        
            Vd.8H = Vn.8H + Vm.8H
        
        Example:
            ADD_8H("v0", "v1", "v2")  # v0.8H = v1.8H + v2.8H
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.8H, {src0}.8H, {src1}.8H",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_2S(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (2 x 32-bit elements):
        Adds 2 corresponding 32-bit elements from two vector registers.
        
            Vd.2S = Vn.2S + Vm.2S
        
        Example:
            ADD_2S("v0", "v1", "v2")  # v0.2S = v1.2S + v2.2S
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.2S, {src0}.2S, {src1}.2S",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_4S(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (4 x 32-bit elements):
        Adds 4 corresponding 32-bit elements from two vector registers.
        
            Vd.4S = Vn.4S + Vm.4S
        
        Example:
            ADD_4S("v0", "v1", "v2")  # v0.4S = v1.4S + v2.4S
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.4S, {src0}.4S, {src1}.4S",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_1D(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (1 x 64-bit element):
        Adds 1 corresponding 64-bit element from two vector registers.
        
            Vd.1D = Vn.1D + Vm.1D
        
        Example:
            ADD_1D("v0", "v1", "v2")  # v0.1D = v1.1D + v2.1D
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.1D, {src0}.1D, {src1}.1D",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))

    def ADD_2D(self, Vd: RegArg, Vn: RegArg, Vm: RegArg):
        """
        Vector Add (2 x 64-bit elements):
        Adds 2 corresponding 64-bit elements from two vector registers.
        
            Vd.2D = Vn.2D + Vm.2D
        
        Example:
            ADD_2D("v0", "v1", "v2")  # v0.2D = v1.2D + v2.2D
            
        Raises:
            TypeError: If any parameter is not a vector register
        """
        dst_str = self._validate_vector_register(Vd, "Vd")
        src0_str = self._validate_vector_register(Vn, "Vn") 
        src1_str = self._validate_vector_register(Vm, "Vm")
        
        self.emit(Instruction(
            template="add {dst}.2D, {src0}.2D, {src1}.2D",
            dsts=[dst_str],
            srcs=[src0_str, src1_str],
            kwargs=dict(dst=dst_str, src0=src0_str, src1=src1_str)
        ))
