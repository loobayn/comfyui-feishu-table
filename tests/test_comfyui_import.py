#!/usr/bin/env python3
"""
测试ComfyUI插件导入
"""

import sys
import os

# 模拟ComfyUI的导入环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_plugin_import():
    """测试插件导入"""
    try:
        # 尝试导入插件
        from comfyui_feishu_table import __init__ as plugin_init
        
        print("✓ 插件包导入成功")
        
        # 检查节点映射
        if hasattr(plugin_init, 'NODE_CLASS_MAPPINGS'):
            print(f"✓ 节点映射: {plugin_init.NODE_CLASS_MAPPINGS}")
        else:
            print("✗ 缺少NODE_CLASS_MAPPINGS")
            
        if hasattr(plugin_init, 'NODE_DISPLAY_NAME_MAPPINGS'):
            print(f"✓ 节点显示名称: {plugin_init.NODE_DISPLAY_NAME_MAPPINGS}")
        else:
            print("✗ 缺少NODE_DISPLAY_NAME_MAPPINGS")
            
        return True
        
    except ImportError as e:
        print(f"✗ 插件导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 其他错误: {e}")
        return False

def test_node_class():
    """测试节点类"""
    try:
        from comfyui_feishu_table.feishu_table_node import FeishuTableNode
        
        print("✓ 节点类导入成功")
        
        # 创建实例
        node = FeishuTableNode()
        print("✓ 节点实例创建成功")
        
        # 检查必要属性
        if hasattr(node, 'INPUT_TYPES'):
            print("✓ INPUT_TYPES 存在")
        else:
            print("✗ 缺少 INPUT_TYPES")
            
        if hasattr(node, 'RETURN_TYPES'):
            print("✓ RETURN_TYPES 存在")
        else:
            print("✗ 缺少 RETURN_TYPES")
            
        if hasattr(node, 'FUNCTION'):
            print("✓ FUNCTION 存在")
        else:
            print("✗ 缺少 FUNCTION")
            
        if hasattr(node, 'CATEGORY'):
            print("✓ CATEGORY 存在")
        else:
            print("✗ 缺少 CATEGORY")
            
        return True
        
    except Exception as e:
        print(f"✗ 节点类测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("ComfyUI飞书表格插件导入测试")
    print("=" * 40)
    
    # 测试插件导入
    print("\n1. 测试插件导入:")
    plugin_ok = test_plugin_import()
    
    # 测试节点类
    print("\n2. 测试节点类:")
    node_ok = test_node_class()
    
    print("\n" + "=" * 40)
    if plugin_ok and node_ok:
        print("🎉 所有测试通过！插件应该可以被ComfyUI正确加载。")
        print("\n如果仍然搜索不到节点，请检查：")
        print("1. ComfyUI是否完全重启")
        print("2. 控制台是否有错误信息")
        print("3. 插件文件夹权限是否正确")
    else:
        print("❌ 部分测试失败，请检查插件配置。")
    
    return 0 if plugin_ok and node_ok else 1

if __name__ == "__main__":
    sys.exit(main())
