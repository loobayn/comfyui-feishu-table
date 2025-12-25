#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面测试format_output函数的各种情况
包括不同类型的数据和空值处理
"""

import sys
import os

# 添加父目录到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_table_node import FeishuTableNode

def test_comprehensive_format():
    """全面测试format_output函数"""
    
    # 创建节点实例
    node = FeishuTableNode()
    
    # 模拟各种情况的表格记录数据
    test_records = [
        {
            "fields": {
                "文生图": "一只大型的可爱动物，一位年轻性感的欧美白人女生。动物比人稍微大一点，动物与人有互动的效果。动物与人物要有情绪的感觉，比如微笑，恐惧，皱眉头。画面要有真实感，背景可以是室外的草地或者是室内。",
                "标签": "",
                "进度": "进行中",
                "状态": None,
                "附件": [],
                "备注": "这是一个测试记录"
            }
        },
        {
            "fields": {
                "文生图": "123",
                "标签": "重要",
                "进度": "",
                "状态": "完成",
                "附件": ["file1.jpg", "file2.png"],
                "备注": None
            }
        },
        {
            "fields": {
                "文生图": None,
                "标签": "紧急",
                "进度": "待处理",
                "状态": "",
                "附件": [],
                "备注": "第三个记录"
            }
        }
    ]
    
    # 测试列名
    test_columns = "文生图\n标签\n进度\n状态\n附件\n备注"
    
    print("=== 全面测试format_output函数 ===")
    print(f"测试记录数量: {len(test_records)}")
    print(f"测试列名: {test_columns}")
    print()
    
    # 调用format_output函数
    result = node.format_output(test_records, test_columns)
    
    print("=== 优化后的输出结果 ===")
    print(result)
    print()
    
    # 验证结果
    print("=== 验证结果 ===")
    lines = result.strip().split('\n')
    
    # 检查每行是否都有正确的行号前缀
    for i, line in enumerate(lines, 1):
        expected_prefixes = [
            f"{i}&文生图:",
            f"{i}&标签:",
            f"{i}&进度:",
            f"{i}&状态:",
            f"{i}&附件:",
            f"{i}&备注:"
        ]
        
        all_prefixes_found = True
        for prefix in expected_prefixes:
            if prefix in line:
                print(f"✅ 行{i}: 找到 {prefix}")
            else:
                print(f"❌ 行{i}: 未找到 {prefix}")
                all_prefixes_found = False
        
        if all_prefixes_found:
            print(f"🎉 行{i}: 所有列都有正确的行号前缀")
        else:
            print(f"⚠️  行{i}: 部分列缺少行号前缀")
        print()
    
    # 检查空值处理
    print("=== 空值处理验证 ===")
    if "(空)" in result:
        print("✅ 空值正确显示为 (空)")
    else:
        print("❌ 空值处理可能有问题")
    
    # 检查行号后缀
    print("=== 行号后缀验证 ===")
    for i in range(1, len(test_records) + 1):
        if f"{i}#" in result:
            print(f"✅ 找到行{i}的后缀: {i}#")
        else:
            print(f"❌ 未找到行{i}的后缀: {i}#")
    
    print()
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_comprehensive_format()

