#!/usr/bin/env python3
"""
测试飞书文本提取节点
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_text_extract_node():
    """测试文本提取节点"""
    print("=== 测试飞书文本提取节点 ===")
    
    try:
        from feishu_text_extract_node import FeishuTextExtractNode
        
        # 创建节点实例
        node = FeishuTextExtractNode()
        
        # 测试数据（模拟飞书多维表格节点的输出）
        test_input = """1&文生图: 一只大型的可爱动物，一位年轻性感的欧美白人女生。动物比人稍微大一点，动物与人有互动的效果。动物与人物要有情绪的感觉，比如微笑，恐惧，皱眉头。画面要有真实感，背景可以是室外的草地或者是室内。1#
2&文生图: (空)2#
3&进度: 进行中3#
4&状态: 完成4#"""
        
        print(f"测试输入:\n{test_input}")
        
        print("\n=== 测试行号提取模式 ===")
        
        # 测试提取第1行
        print("\n1. 提取第1行（不包含标记）:")
        result, status, debug = node.extract_text(
            test_input, "行号提取", "1", "", False, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        print(f"调试: {debug}")
        
        # 测试提取第1行（包含标记）
        print("\n2. 提取第1行（包含标记）:")
        result, status, debug = node.extract_text(
            test_input, "行号提取", "1", "", False, True
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        # 测试提取第2行
        print("\n3. 提取第2行:")
        result, status, debug = node.extract_text(
            test_input, "行号提取", "2", "", False, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        print("\n=== 测试列名提取模式 ===")
        
        # 测试提取"文生图"列
        print("\n4. 提取'文生图'列:")
        result, status, debug = node.extract_text(
            test_input, "列名提取", "文生图", "", False, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        # 测试提取所有"文生图"列
        print("\n5. 提取所有'文生图'列:")
        result, status, debug = node.extract_text(
            test_input, "列名提取", "文生图", "", True, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        print("\n=== 测试范围提取模式 ===")
        
        # 测试范围提取（不包含标记）
        print("\n6. 范围提取（不包含标记）:")
        result, status, debug = node.extract_text(
            test_input, "范围提取", "1&文生图: ", "1#", False, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        # 测试范围提取（包含标记）
        print("\n7. 范围提取（包含标记）:")
        result, status, debug = node.extract_text(
            test_input, "范围提取", "1&文生图: ", "1#", False, True
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        print("\n=== 测试边界情况 ===")
        
        # 测试空输入
        print("\n8. 测试空输入:")
        result, status, debug = node.extract_text("", "行号提取", "1", "", False, False)
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        # 测试无效行号
        print("\n9. 测试无效行号:")
        result, status, debug = node.extract_text(
            test_input, "行号提取", "999", "", False, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        # 测试无效列名
        print("\n10. 测试无效列名:")
        result, status, debug = node.extract_text(
            test_input, "列名提取", "不存在的列", "", False, False
        )
        print(f"结果: {result}")
        print(f"状态: {status}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_text_extract_node()
