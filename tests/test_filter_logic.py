#!/usr/bin/env python3
"""
测试筛选逻辑，特别是空值和非空值的处理
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_filter_logic():
    """测试筛选逻辑"""
    print("=== 测试筛选逻辑 ===")
    
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
        
        print("\n=== 测试各种筛选条件 ===")
        
        # 测试1: 列名+空值
        print("\n1. 测试: 内容+空值")
        filtered = node.filter_records(test_records, "", "内容+空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"   - {record['fields']}")
        
        # 测试2: 列名+非空值
        print("\n2. 测试: 内容+非空值")
        filtered = node.filter_records(test_records, "", "内容+非空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"   - {record['fields']}")
        
        # 测试3: 列名-空值
        print("\n3. 测试: 内容-空值")
        filtered = node.filter_records(test_records, "", "内容-空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"   - {record['fields']}")
        
        # 测试4: 列名-非空值
        print("\n4. 测试: 内容-非空值")
        filtered = node.filter_records(test_records, "", "内容-非空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"   - {record['fields']}")
        
        # 测试5: 组合条件
        print("\n5. 测试组合条件: 状态+进行中\\n内容+空值")
        filtered = node.filter_records(test_records, "", "状态+进行中\n内容+空值", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"   - {record['fields']}")
        
        # 测试6: 排除条件
        print("\n6. 测试排除条件: 状态-完成")
        filtered = node.filter_records(test_records, "", "状态-完成", "include")
        print(f"   结果: {len(filtered)} 条记录")
        for record in filtered:
            print(f"   - {record['fields']}")
        
        print("\n=== 测试总结 ===")
        print("✅ 所有筛选条件测试完成")
        print("📋 支持的筛选语法:")
        print("   - 列名+关键词: 仅包含该列包含关键词的行")
        print("   - 列名-关键词: 排除列包含关键词的行")
        print("   - 列名+空值: 仅包含该列为空的行")
        print("   - 列名-空值: 排除该列为空的行")
        print("   - 列名+非空值: 仅包含该列非空的行")
        print("   - 列名-非空值: 排除该列非空的行")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_filter_logic()

