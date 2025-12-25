#!/usr/bin/env python3
"""
测试使用现有字段
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_upload_node import FeishuUploadNode
import numpy as np
from PIL import Image

def test_existing_field():
    """测试使用现有字段"""
    print("🔍 测试使用现有字段...")
    
    # 创建节点实例
    node = FeishuUploadNode()
    
    # 配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/CSPQbCY1OazvLnsxgWicjW0hnYd?table=tblPlnQ7x0dYGWC8&view=vew5tYVpod"
    target_column = "生成图片"  # 使用现有的字段
    filter_condition = ""  # 空字符串表示添加行模式
    add_rows = True
    rows_to_add = 1
    image_name = "test_existing_field"
    
    print(f"📋 测试配置:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   表格链接: {table_url}")
    print(f"   目标列: {target_column}")
    print(f"   添加行: {add_rows}")
    print(f"   行数: {rows_to_add}")
    
    # 创建测试图片
    print(f"\n🖼️  创建测试图片...")
    height, width = 32, 32
    test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
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
    test_existing_field()

