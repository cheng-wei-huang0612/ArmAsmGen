# armasmgen/__init__.py
"""
armasmgen ── AArch64 (Arm v8-A) assembly generator DSL.

核心構件：
    Instruction   ── 記錄指令結構化資訊
    BaseAsm       ── 最簡容器，僅存指令序列
    Block         ── 可巢狀的區塊（with 句法）
    ASMCode       ── 整份組合檔（最外層 Block）
    mixins.*      ── 指令糖衣（算術、記憶體、SIMD…）

常見用法：
    from armasmgen import ASMCode, Block
    with ASMCode() as asm:
        with Block(label="main") as m:
            m.ADD("x0", "x1", "x2")
    print(asm.encode())
"""

from .core import Instruction, BaseAsm, RegArg
from .builder import ASMCode, Block
from .register import (
    Register, RegisterType, RegisterWidth, RegisterPool,
    AArch64RegisterPools, aarch64_pools,
    x_reg, w_reg, v_reg, d_reg, virtual_x, virtual_v
)

# Import mixins for direct access
from .mixins import ArithmeticMixin, MemoryMixin, LogicMixin

# 如果你想提供「全部 mixin 都已注入」的便利類別，可加：
from .mixins import arithmetic, memory, logic  # 依需求匯入更多

class AsmFunc(Block,                      # Block already inherits mixins
              arithmetic.ArithmeticMixin,
              memory.MemoryMixin,
              logic.LogicMixin):
    """預組合：最常用指令集一次到位"""
    pass

__all__ = [
    "Instruction",
    "BaseAsm",
    "ASMCode",
    "Block",
    "AsmFunc",
    "RegArg",
    # Register system
    "Register",
    "RegisterType",
    "RegisterWidth", 
    "RegisterPool",
    "AArch64RegisterPools",
    "aarch64_pools",
    "x_reg",
    "w_reg", 
    "v_reg",
    "d_reg",
    "virtual_x",
    "virtual_v",
    # Mixins
    "ArithmeticMixin",
    "MemoryMixin", 
    "LogicMixin",
]