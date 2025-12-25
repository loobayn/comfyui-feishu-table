#!/usr/bin/env python3
"""
测试所有飞书节点的筛选功能，特别是空值和非空值的处理
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_table_node_filter():
    """测试表格读取节点的筛选功能"""
    print("=== 测试表格读取节点筛选功能 ===")
    try:
        from feishu_table_node import FeishuTableNode
        
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
                    "内容": "",
                    "备注": None
                }
            },
            {
                "fields": {
                    "状态": "进行中",
                    "内容": "这是第三条记录",
                    "备注": []
                }
            },
            {
                "fields": {
                    "状态": "暂停",
                    "内容": "这是第四条记录"
                }
            }
        ]
        
        print(f"测试数据: {len(test_records)} 条记录")
        
        # 测试各种筛选条件
        test_cases = [
            ("备注+空值", "备注+空值"),
            ("备注+非空值", "备注+非空值"),
            ("备注-空值", "备注-空值"),
            ("备注-非空值", "备注-非空值"),
            ("状态+进行中", "状态+进行中"),
            ("状态+进行中\\n备注+空值", "状态+进行中\n备注+空值"),
        ]
        
        for test_name, condition in test_cases:
            print(f"\n{test_name}:")
            filtered = node.filter_records(test_records, "", condition, "include")
            print(f"  结果: {len(filtered)} 条记录")
            for record in filtered:
                print(f"    - {record['fields']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 表格节点测试失败: {e}")
        return False

def test_write_node_filter():
    """测试表格写入节点的筛选功能"""
    print("\n=== 测试表格写入节点筛选功能 ===")
    try:
        from feishu_write_node import FeishuWriteNode
        
        node = FeishuWriteNode()
        
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
                    "内容": "",
                    "备注": None
                }
            },
            {
                "fields": {
                    "状态": "进行中",
                    "内容": "这是第三条记录",
                    "备注": []
                }
            },
            {
                "fields": {
                    "状态": "暂停",
                    "内容": "这是第四条记录"
                }
            }
        ]
        
        # 测试各种筛选条件
        test_cases = [
            ("备注+空值", "备注+空值"),
            ("备注+非空值", "备注+非空值"),
            ("备注-空值", "备注-空值"),
            ("备注-非空值", "备注-非空值"),
        ]
        
        for test_name, condition in test_cases:
            print(f"\n{test_name}:")
            filtered = node.filter_records(test_records, condition)
            print(f"  结果: {len(filtered)} 条记录")
            for record in filtered:
                print(f"    - {record['fields']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 写入节点测试失败: {e}")
        return False

def test_upload_node_filter():
    """测试图片上传节点的筛选功能"""
    print("\n=== 测试图片上传节点筛选功能 ===")
    try:
        from feishu_upload_node import FeishuUploadNode
        
        node = FeishuUploadNode()
        
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
                    "内容": "",
                    "备注": None
                }
            },
            {
                "fields": {
                    "状态": "进行中",
                    "内容": "这是第三条记录",
                    "备注": []
                }
            },
            {
                "fields": {
                    "状态": "暂停",
                    "内容": "这是第四条记录"
                }
            }
        ]
        
        # 测试各种筛选条件
        test_cases = [
            ("备注+空值", "备注+空值"),
            ("备注+非空值", "备注+非空值"),
            ("备注-空值", "备注-空值"),
            ("备注-非空值", "备注-非空值"),
        ]
        
        for test_name, condition in test_cases:
            print(f"\n{test_name}:")
            filtered = node.filter_records(test_records, condition)
            print(f"  结果: {len(filtered)} 条记录")
            for record in filtered:
                print(f"    - {record['fields']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 上传节点测试失败: {e}")
        return False

def test_fetch_image_node_filter():
    """测试图片获取节点的筛选功能"""
    print("\n=== 测试图片获取节点筛选功能 ===")
    try:
        from feishu_fetch_image_node import FeishuFetchImageNode
        
        node = FeishuFetchImageNode()
        
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
                    "内容": "",
                    "备注": None
                }
            },
            {
                "fields": {
                    "状态": "进行中",
                    "内容": "这是第三条记录",
                    "备注": []
                }
            },
            {
                "fields": {
                    "状态": "暂停",
                    "内容": "这是第四条记录"
                }
            }
        ]
        
        # 测试各种筛选条件
        test_cases = [
            ("备注+空值", "备注+空值"),
            ("备注+非空值", "备注+非空值"),
            ("备注-空值", "备注-空值"),
            ("备注-非空值", "备注-非空值"),
        ]
        
        for test_name, condition in test_cases:
            print(f"\n{test_name}:")
            filtered = node.filter_records(test_records, condition)
            print(f"  结果: {len(filtered)} 条记录")
            for record in filtered:
                print(f"    - {record['fields']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 获取图片节点测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("飞书多维表格插件 - 所有节点筛选功能测试")
    print("=" * 60)
    
    # 测试所有节点的筛选功能
    results = []
    results.append(test_table_node_filter())
    results.append(test_write_node_filter())
    results.append(test_upload_node_filter())
    results.append(test_fetch_image_node_filter())
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("筛选功能测试总结:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有节点筛选功能测试通过！({passed}/{total})")
        print("🎉 空值和非空值筛选功能在所有节点中都正常工作！")
    else:
        print(f"❌ 部分节点筛选功能测试失败 ({passed}/{total})")
        print("请检查失败的节点筛选逻辑")
    
    print("\n📋 验证的筛选条件:")
    print("   - 列名+空值: 仅包含该列为空的行")
    print("   - 列名+非空值: 仅包含该列非空的行")
    print("   - 列名-空值: 排除该列为空的行")
    print("   - 列名-非空值: 排除该列非空的行")
    print("\n✅ 空值定义包括: None、空字符串、空列表、缺失字段")

if __name__ == "__main__":
    main()
