#!/usr/bin/env python3

from armasmgen.builder import ASMCode, Block

def demo_export_formats():
    """演示不同的匯出格式選項"""
    
    with ASMCode() as asm:
        # 定義一些常數
        asm.equ("VERSION", "1")
        asm.equ("MAX_SIZE", "0x800")
        
        # 主函數 - 矩陣乘法例子
        with Block(label="matrix_multiply") as mm:
            # 初始化迴圈計數器
            mm.ADD_imm("x19", "xzr", 0)      # i = 0
            mm.ADD_imm("x20", "xzr", 0)      # j = 0
            mm.ADD_imm("x21", "xzr", 0)      # k = 0
            
            # 內層迴圈 - 累加
            with Block(label="inner_loop") as inner:
                inner.MUL("x22", "x1", "x2")      # temp = a[i][k] * b[k][j]
                inner.ADD("x0", "x0", "x22")      # result += temp
                inner.ADD_imm("x21", "x21", 1)    # k++
                
            # 重設計數器
            mm.ADD_imm("x20", "x20", 1)      # j++
            mm.ADD_imm("x19", "x19", 1)      # i++
    
    print("=== 標準格式輸出到控制台 ===")
    asm.stdout()
    
    print("\n=== 無縮排格式輸出 ===")  
    asm.stdout(indent=False)
    
    # 匯出到不同的檔案格式
    print("\n=== 匯出到檔案 ===")
    
    # 標準縮排格式檔案
    asm.export_to_file("examples/matrix_multiply_indented.s")
    print("已匯出標準格式到: examples/matrix_multiply_indented.s")
    
    # 無縮排格式檔案
    asm.export_to_file("examples/matrix_multiply_compact.s", indent=False)
    print("已匯出緊湊格式到: examples/matrix_multiply_compact.s")

if __name__ == "__main__":
    demo_export_formats()
