#!/usr/bin/env python3
"""
ComfyUI飞书多维表格插件测试脚本
用于验证插件的基本功能是否正常
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试基本导入"""
    try:
        import requests
        print("✓ requests 模块导入成功")
    except ImportError as e:
        print(f"✗ requests 模块导入失败: {e}")
        return False
    
    try:
        import urllib3
        print("✓ urllib3 模块导入成功")
    except ImportError as e:
        print(f"✗ urllib3 模块导入失败: {e}")
        return False
    
    return True

def test_node_class():
    """测试节点类"""
    try:
        from feishu_table_node import FeishuTableNode
        print("✓ FeishuTableNode 类导入成功")
        
        # 创建实例
        node = FeishuTableNode()
        print("✓ FeishuTableNode 实例创建成功")
        
        # 检查输入类型
        input_types = node.INPUT_TYPES()
        if "required" in input_types and "app_id" in input_types["required"]:
            print("✓ INPUT_TYPES 配置正确")
        else:
            print("✗ INPUT_TYPES 配置不正确")
            return False
        
        # 检查返回类型
        if hasattr(node, 'RETURN_TYPES') and node.RETURN_TYPES == ("STRING", "STRING"):
            print("✓ RETURN_TYPES 配置正确")
        else:
            print("✗ RETURN_TYPES 配置不正确")
            return False
        
        # 检查函数名
        if hasattr(node, 'FUNCTION') and node.FUNCTION == "get_table_data":
            print("✓ FUNCTION 配置正确")
        else:
            print("✗ FUNCTION 配置不正确")
            return False
        
        # 检查分类
        if hasattr(node, 'CATEGORY') and node.CATEGORY == "飞书工具":
            print("✓ CATEGORY 配置正确")
        else:
            print("✗ CATEGORY 配置不正确")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 节点类测试失败: {e}")
        return False

def test_url_parsing():
    """测试URL解析功能"""
    try:
        from feishu_table_node import FeishuTableNode
        node = FeishuTableNode()
        
        # 测试URL解析
        test_url = "https://example.feishu.cn/base/xxx/xxx?table=tbl123&sheet=sheet456"
        table_id, sheet_id = node.extract_table_info(test_url)
        
        if table_id == "tbl123" and sheet_id == "sheet456":
            print("✓ URL解析功能正常")
            return True
        else:
            print(f"✗ URL解析功能异常: table_id={table_id}, sheet_id={sheet_id}")
            return False
            
    except Exception as e:
        print(f"✗ URL解析测试失败: {e}")
        return False

def test_filtering():
    """测试筛选功能"""
    try:
        from feishu_table_node import FeishuTableNode
        node = FeishuTableNode()
        
        # 模拟记录数据
        test_records = [
            {"fields": {"重点内容": "任务1", "完成进度": "未完成", "负责人": "张三"}},
            {"fields": {"重点内容": "任务2", "完成进度": "完成", "负责人": "李四"}},
            {"fields": {"重点内容": "任务3", "完成进度": "未完成", "负责人": "王五"}}
        ]
        
        # 测试筛选
        filtered = node.filter_records(
            test_records, 
            "重点内容\n完成进度", 
            "完成进度=未完成", 
            "include"
        )
        
        if len(filtered) == 2:
            print("✓ 筛选功能正常")
            return True
        else:
            print(f"✗ 筛选功能异常: 期望2条记录，实际{len(filtered)}条")
            return False
            
    except Exception as e:
        print(f"✗ 筛选功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("ComfyUI飞书多维表格插件测试")
    print("=" * 40)
    
    tests = [
        ("基本导入测试", test_imports),
        ("节点类测试", test_node_class),
        ("URL解析测试", test_url_parsing),
        ("筛选功能测试", test_filtering)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name} 失败")
    
    print("\n" + "=" * 40)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！插件应该可以正常工作。")
        return 0
    else:
        print("❌ 部分测试失败，请检查插件配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
