#!/usr/bin/env python3
"""
测试简化后的飞书文本提取节点
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_extract():
    """测试简化的文本提取节点"""
    print("=== 测试简化后的飞书文本提取节点 ===")
    
    try:
        from feishu_text_extract_node import FeishuTextExtractNode
        
        # 创建节点实例
        node = FeishuTextExtractNode()
        
        # 测试数据
        test_input = """1&文生图: 一只大型的可爱动物，一位年轻性感的欧美白人女生。动物比人稍微大一点，动物与人有互动的效果。动物与人物要有情绪的感觉，比如微笑，恐惧，皱眉头。画面要有真实感，背景可以是室外的草地或者是室内。1#
2&文生图: 可爱的动物2#
3&进度: 进行中3#
4&状态: 完成4#"""
        
        print(f"测试输入:\n{test_input}")
        
        print("\n=== 测试范围提取 ===")
        
        # 测试1：提取第1行内容（不包含标记）
        print("\n1. 提取第1行内容（不包含标记）:")
        result = node.extract_text(
            test_input, "1&文生图: ", "1#", False
        )
        print(f"起始标记: 1&文生图: ")
        print(f"结束标记: 1#")
        print(f"结果: {result}")
        
        # 测试2：提取第2行内容（不包含标记）
        print("\n2. 提取第2行内容（不包含标记）:")
        result = node.extract_text(
            test_input, "2&文生图: ", "2#", False
        )
        print(f"起始标记: 2&文生图: ")
        print(f"结束标记: 2#")
        print(f"结果: {result}")
        
        # 测试3：提取第2行内容（包含标记）
        print("\n3. 提取第2行内容（包含标记）:")
        result = node.extract_text(
            test_input, "2&文生图: ", "2#", True
        )
        print(f"起始标记: 2&文生图: ")
        print(f"结束标记: 2#")
        print(f"结果: {result}")
        
        # 测试4：提取进度信息
        print("\n4. 提取进度信息:")
        result = node.extract_text(
            test_input, "3&进度: ", "3#", False
        )
        print(f"起始标记: 3&进度: ")
        print(f"结束标记: 3#")
        print(f"结果: {result}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_extract()
