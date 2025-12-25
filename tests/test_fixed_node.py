#!/usr/bin/env python3
"""
测试修复后的节点功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_upload_node import FeishuUploadNode
import numpy as np
from PIL import Image
import io

def test_node():
    """测试节点功能"""
    print("🔍 测试修复后的FeishuUploadNode...")
    
    # 创建节点实例
    node = FeishuUploadNode()
    
    # 配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/CSPQbCY1OazvLnsxgWicjW0hnYd?table=tblPlnQ7x0dYGWC8&view=vew5tYVpod"
    target_column = "附件"  # 根据您的表格列名调整
    filter_condition = ""  # 空字符串表示添加行模式
    add_rows = True
    rows_to_add = 1
    image_name = "test_node"
    
    print(f"📋 测试配置:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   表格链接: {table_url}")
    print(f"   目标列: {target_column}")
    print(f"   添加行: {add_rows}")
    print(f"   行数: {rows_to_add}")
    
    # 创建测试图片
    print(f"\n🖼️  创建测试图片...")
    height, width = 64, 64
    test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # 转换为PIL Image
    pil_image = Image.fromarray(test_image)
    print(f"✅ 测试图片创建成功: {width}x{height} RGB")
    
    # 测试节点
    print(f"\n🚀 开始测试节点...")
    try:
        result_image, result_message = node.upload_to_table(
            app_id, app_secret, table_url, pil_image, 
            target_column, filter_condition, add_rows, rows_to_add, image_name
        )
        
        print(f"\n📊 测试结果:")
        print(f"   返回图片: {type(result_image)}")
        print(f"   返回消息: {result_message}")
        
        if "成功" in result_message or "完成" in result_message:
            print(f"✅ 测试成功!")
        else:
            print(f"❌ 测试失败: {result_message}")
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_node()

