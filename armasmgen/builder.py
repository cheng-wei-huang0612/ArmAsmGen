# armasmgen/builder.py
from contextvars import ContextVar
from .core import BaseAsm, Instruction
from .mixins import arithmetic, memory, logic, control, vector_arithmetic

_current: ContextVar["Block"] = ContextVar("_current")

class Block(BaseAsm,
            arithmetic.ArithmeticMixin,
            memory.MemoryMixin,
            logic.LogicMixin,
            control.ControlFlowMixin,
            vector_arithmetic.VectorArithmeticMixin):
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
    
    def emitline(self):
        self.emit(Instruction(
            template="",
            dsts=[], srcs=[], kwargs={},
            depth=self.depth, block=self.label
        ))

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
    def __init__(self, label: str | None = None):
        super().__init__(label=label)

    # ---------- context ----------
    def __enter__(self):
        # 進入區塊前把自己推進 context
        self._token = _current.set(self)

        # 若有 label，先 emit 1 行 label 指令（附層級）
        if self.label:
            self.emit(Instruction(
                template=f".global {self.label}",
                dsts=[], srcs=[], kwargs={},
                depth=self.depth, block=self.label
            ))
            self.emit(Instruction(
                template=f".global _{self.label}",
                dsts=[], srcs=[], kwargs={},
                depth=self.depth, block=self.label
            ))
            self.emit(Instruction(
                template=f"{self.label}:",
                dsts=[], srcs=[], kwargs={},
                depth=self.depth, block=self.label
            ))
            self.emit(Instruction(
                template=f"_{self.label}:",
                dsts=[], srcs=[], kwargs={},
                depth=self.depth, block=self.label
            ))
        return self

    def __exit__(self, exc_type, exc, tb):
        self.emit(Instruction(
            template="ret",
            dsts=[], srcs=[], kwargs={},
            depth=self.depth, block=self.label
        ))
        _current.reset(self._token)
        parent = _current.get(None)
        if parent is not None:
            parent._inst.extend(self._inst)



class BackgroundCode(Block):
    def __init__(self, label: str | None = None):
        super().__init__(label=label)
        self.depth = -1




    # ---------- context ----------
    def __enter__(self):
        # 進入區塊前把自己推進 context
        self._token = _current.set(self)

        

    def __exit__(self, exc_type, exc, tb):

        _current.reset(self._token)
        # 不自動列印；由使用者手動呼叫 stdout()/encode()

    # ---------- export ----------
    def encode(self, *, indent: bool = True) -> str:
        parts = [""]  # Start with an empty line
        parts += [inst.render(indent=indent) for inst in self._inst]
        return "\n".join(parts)

    def stdout(self, *, indent: bool = True):
        """直接列印組譯碼（方便 quick demo）。"""
        print(self.encode(indent=indent))

    def export_to_file(self, filepath: str, *, indent: bool = True):
        """將組譯碼匯出到檔案。"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.encode(indent=indent))


class DataBlock(Block):
    def __init__(self, label: str | None = None, align: int = 4):
        super().__init__(label=label)
        self.align = align

    def add_data(self, size : str, data: int | str):
        if size not in ["byte", "hword", "half", "word", "xword"]:
            raise ValueError("size must be one of 'byte', 'hword', 'half', 'word', 'xword'")
        self.emit(Instruction(
            template=f".{size} {data}",
            dsts=[], srcs=[], kwargs={},
            depth=self.depth, block=self.label
        ))

    def __enter__(self):
        # 進入區塊前把自己推進 context
        self._token = _current.set(self)
        self.emit(Instruction(
            template=f"{self.label}:",  
            dsts=[], srcs=[], kwargs={},
            depth=self.depth, block=self.label
        ))
        self.emit(Instruction(
            template=f".align {self.align}",
            dsts=[], srcs=[], kwargs={},
            depth=self.depth, block=self.label
        ))

        return self
    

    def __exit__(self, exc_type, exc, tb):
        self.emitline()

        # pop context，取得父層
        _current.reset(self._token)
        parent = _current.get(None)

        # 把自己累積的 inst 串接到父層
        if parent is not None:
            parent._inst.extend(self._inst)