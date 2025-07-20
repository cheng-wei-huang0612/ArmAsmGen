#!/usr/bin/env python3

from armasmgen import *

def demo_file_export():
    """演示檔案匯出功能"""

    x0 = x_reg(0)
    x1 = x_reg(1)
    x2 = x_reg(2)
    x22 = x_reg(22)
    
    with ASMCode() as asm:
        # 定義一些常數
        asm.equ("MAGIC_NUMBER", "42")
        asm.equ("BUFFER_SIZE", "0x1000")
        
        # 主函數
        with Block(label="main") as m:
            # 一個簡單的加法運算例子
            m.ADD(x0, x1, x22)      # x0 = x1 + x2
            m.ADD_imm("x3", "x4", 10)        # x3 = x4 + 10
            m.SUB("x5", "x6", "x7")          # x5 = x6 - x7
            m.MUL("x8", "x9", "x10")         # x8 = x9 * x10
        
        # 工具函數
        with Block(label="utility") as util:
            util.ADD_imm("x0", "x0", 1)      # increment
            
    # 輸出到控制台
    print("輸出到控制台：")
    asm.stdout()
    
    # 匯出到檔案
    filepath = "examples/exported_assembly.s"
    asm.export_to_file(filepath)
    print(f"\n已將組譯碼匯出到：{filepath}")

if __name__ == "__main__":
    demo_file_export()
