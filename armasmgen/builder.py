# armasmgen/builder.py
from contextvars import ContextVar
from .core import BaseAsm, Instruction
from .mixins import arithmetic, memory

_current: ContextVar["Block"] = ContextVar("_current")

class Block(BaseAsm,
            arithmetic.ArithmeticMixin,
            memory.MemoryMixin):
    def __init__(self, label: str | None = None):
        super().__init__()
        self.label = label
        self.depth = _current.get().depth + 1 if _current.get(None) else 0

    # ---------- context ----------
    def __enter__(self):
        # 進入區塊前把自己推進 context
        self._token = _current.set(self)

        # 若有 label，先 emit 1 行 label 指令（附層級）
        if self.label:
            self.emit(Instruction(
                template=f"{self.label}:",
                dsts=[], srcs=[], kwargs={},
                depth=self.depth, block=self.label
            ))
        return self

    def __exit__(self, exc_type, exc, tb):
        # pop context，取得父層
        _current.reset(self._token)
        parent = _current.get(None)

        # 把自己累積的 inst 串接到父層
        if parent is not None:
            parent._inst.extend(self._inst)
        # 如果 parent 為 None → 代表這是 ASMCode，本身已在頂層

# --------------------------------------------------------------------
class ASMCode(Block):
    def __init__(self):
        super().__init__(label=None)
        self._equs: list[str] = []
        self._bits: list[str] = []
        self._labels: set[str] = set()

    # ----- pseudo-op -----
    def equ(self, name, value): self._equs.append(f"{name} EQU {value}")

    # ---------- context ----------
    def __enter__(self):
        # ASMCode 當頂層：先把自己推進 context，depth 保持 0
        self._token = _current.set(self)
        return self

    def __exit__(self, exc_type, exc, tb):
        _current.reset(self._token)
        # 不自動列印；由使用者手動呼叫 stdout()/encode()

    # ---------- export ----------
    def encode(self, *, indent: bool = True) -> str:
        parts = self._equs + self._bits + [""]
        parts += [inst.render(indent=indent) for inst in self._inst]
        return "\n".join(parts)

    def stdout(self, *, indent: bool = True):
        """直接列印組譯碼（方便 quick demo）。"""
        print(self.encode(indent=indent))