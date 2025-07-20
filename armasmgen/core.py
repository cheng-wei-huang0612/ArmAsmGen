# armasmgen/core.py
from dataclasses import dataclass
from typing import List, Dict, Any, Union


@dataclass
class Instruction:
    template: str
    dsts: List[str]
    srcs: List[str]
    kwargs: Dict[str, Any]
    depth: int = 0              # 新增 → 代表縮排層級
    block: str | None = None    # 新增 → 產生指令的 block label

    def render(self, indent: bool = False) -> str:
        def _fmt(k, v): 
            if isinstance(v, int):
                # Check if the template already has # for this parameter
                placeholder = "{" + k + "}"
                if f"#{placeholder}" in self.template:
                    # Template already has #, don't add another one
                    return str(v)
                else:
                    # Template doesn't have #, add it
                    return f"#{v}"
            return v
        
        body = self.template.format(**{k: _fmt(k, v) for k, v in self.kwargs.items()})

        return ("    " * self.depth + body) if indent else body
class BaseAsm:
    def __init__(self):
        self._inst: List[Instruction] = []

    def emit(self, inst: Instruction):
        inst.depth = getattr(self, 'depth', 0)
        self._inst.append(inst)

    def lines(self):
        for i in self._inst:
            yield i.render()

    def to_string(self):
        return "\n".join(self.lines())