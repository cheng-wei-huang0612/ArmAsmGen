# armasmgen/mixins/control.py
from ..core import Instruction, RegArg

class ControlFlowMixin:
    def emit(self, inst: Instruction): ...  # Type hint
    def _reg_to_str(self, reg: RegArg) -> str: ...  # Type hint

    def RET(self, reg: RegArg = "x30"):
        """
        Return from subroutine:
        This instruction returns from a subroutine by branching to the address in the specified register.
        
            PC = reg (default: x30 link register)
            
        Standard ARM64 function return.
        Reference: A-profile: section C6.2.245, page C6-2122
        """
        reg_str = self._reg_to_str(reg) if reg != "x30" else "x30"
        if reg == "x30":
            # Standard return - no operand needed
            self.emit(Instruction(
                template="ret",
                dsts=[],
                srcs=["x30"],
                kwargs={}
            ))
        else:
            # Return to specific register
            self.emit(Instruction(
                template="ret {reg}",
                dsts=[],
                srcs=[reg_str],
                kwargs=dict(reg=reg_str)
            ))

    def BR(self, reg: RegArg):
        """
        Branch to register:
        This instruction branches to the address in the specified register.
        
            PC = reg
            
        Reference: A-profile: section C6.2.37, page C6-1858
        """
        reg_str = self._reg_to_str(reg)
        self.emit(Instruction(
            template="br {reg}",
            dsts=[],
            srcs=[reg_str],
            kwargs=dict(reg=reg_str)
        ))

    def BLR(self, reg: RegArg):
        """
        Branch with link to register:
        This instruction branches to the address in the specified register and saves the return address.
        
            x30 = PC + 4; PC = reg
            
        Used for calling functions through function pointers.
        Reference: A-profile: section C6.2.36, page C6-1856
        """
        reg_str = self._reg_to_str(reg)
        self.emit(Instruction(
            template="blr {reg}",
            dsts=["x30"],
            srcs=[reg_str],
            kwargs=dict(reg=reg_str)
        ))

    def B(self, label: str):
        """
        Branch (unconditional):
        This instruction branches unconditionally to the specified label.
        
            PC = label
            
        Reference: A-profile: section C6.2.31, page C6-1845
        """
        self.emit(Instruction(
            template="b {label}",
            dsts=[],
            srcs=[],
            kwargs=dict(label=label)
        ))

    def BL(self, label: str):
        """
        Branch with link:
        This instruction branches to the specified label and saves the return address.
        
            x30 = PC + 4; PC = label
            
        Used for calling functions.
        Reference: A-profile: section C6.2.35, page C6-1854
        """
        self.emit(Instruction(
            template="bl {label}",
            dsts=["x30"],
            srcs=[],
            kwargs=dict(label=label)
        ))

    def NOP(self):
        """
        No operation:
        This instruction does nothing but consume one instruction cycle.
        
        Used for alignment, timing, or as placeholder.
        Reference: A-profile: section C6.2.182, page C6-2039
        """
        self.emit(Instruction(
            template="nop",
            dsts=[],
            srcs=[],
            kwargs={}
        ))
