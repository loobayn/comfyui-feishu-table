#!/usr/bin/env python3
"""
调试筛选逻辑，找出空值识别的问题
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_filter_debug():
    """调试筛选逻辑"""
    print("=== 调试筛选逻辑 ===")
    
    try:
        from feishu_table_node import FeishuTableNode
        
        # 创建节点实例
        node = FeishuTableNode()
        
        # 创建测试数据
        test_records = [
            {
                "fields": {
                    "状态": "完成",
                    "内容": "这是第一条记录",
                    "备注": "有备注"
                }
            },
            {
                "fields": {
                    "状态": "未完成",
                    "内容": "",  # 空字符串
                    "备注": None  # None值
                }
            },
            {
                "fields": {
                    "状态": "进行中",
                    "内容": "这是第三条记录",
                    "备注": []  # 空列表
                }
            },
            {
                "fields": {
                    "状态": "暂停",
                    "内容": "这是第四条记录"
                    # 缺少备注字段
                }
            }
        ]
        
        print(f"测试数据: {len(test_records)} 条记录")
        for i, record in enumerate(test_records):
            print(f"  记录{i+1}: {record['fields']}")
        
        print("\n=== 测试空值识别 ===")
        
        # 测试备注字段的空值识别
        print("\n1. 测试备注字段的空值识别:")
        for i, record in enumerate(test_records):
            fields = record.get('fields', {})
            remark = fields.get('备注', '字段缺失')
            is_empty = node._is_empty_value(remark) if hasattr(node, '_is_empty_value') else None
            print(f"   记录{i+1} 备注: {remark} (类型: {type(remark)}) -> 是否为空: {is_empty}")
        
        # 测试各种筛选条件
        print("\n2. 测试筛选条件:")
        
        # 测试备注+空值
        print("\n   备注+空值:")
        filtered = node.filter_records(test_records, "", "备注+空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"     - {record['fields']}")
        
        # 测试备注+非空值
        print("\n   备注+非空值:")
        filtered = node.filter_records(test_records, "", "备注+非空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"     - {record['fields']}")
        
        # 测试备注-空值
        print("\n   备注-空值:")
        filtered = node.filter_records(test_records, "", "备注-空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"     - {record['fields']}")
        
        # 测试备注-非空值
        print("\n   备注-非空值:")
        filtered = node.filter_records(test_records, "", "备注-非空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"     - {record['fields']}")
        
        # 测试组合条件
        print("\n3. 测试组合条件:")
        print("\n   状态+进行中 且 备注+空值:")
        filtered = node.filter_records(test_records, "", "状态+进行中\n备注+空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"     - {record['fields']}")
        
        print("\n   状态+进行中 且 备注+非空值:")
        filtered = node.filter_records(test_records, "", "状态+进行中\n备注+非空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"     - {record['fields']}")
        
        print("\n=== 问题分析 ===")
        print("根据测试结果，分析筛选逻辑是否正确处理了空值")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_filter_debug()

