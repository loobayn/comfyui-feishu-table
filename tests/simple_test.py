#!/usr/bin/env python3
"""
简单测试插件结构
"""

# 直接导入节点类
from feishu_table_node import FeishuTableNode

print("✓ 节点类导入成功")

# 创建实例
node = FeishuTableNode()
print("✓ 节点实例创建成功")

# 检查属性
print(f"✓ INPUT_TYPES: {hasattr(node, 'INPUT_TYPES')}")
print(f"✓ RETURN_TYPES: {hasattr(node, 'RETURN_TYPES')}")
print(f"✓ FUNCTION: {hasattr(node, 'FUNCTION')}")
print(f"✓ CATEGORY: {hasattr(node, 'CATEGORY')}")

print(f"✓ 节点分类: {node.CATEGORY}")
print(f"✓ 节点函数: {node.FUNCTION}")
print(f"✓ 返回类型: {node.RETURN_TYPES}")

print("\n🎉 插件结构验证完成！")
print("现在请重启ComfyUI，插件应该可以正常显示。")
