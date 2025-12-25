#!/usr/bin/env python3
"""
测试筛选模式（不添加新行）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_upload_node import FeishuUploadNode
import numpy as np
from PIL import Image
import io

def main():
    """主函数"""
    print("测试筛选模式（不添加新行）")
    print("=" * 60)
    
    # 创建节点实例
    node = FeishuUploadNode()
    
    # 测试配置
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/CSPQbCY1OazvLnsxgWicjW0hnYd?table=tblPlnQ7x0dYGWC8&view=vew5tYVpod"
    target_column = "生成图片"
    filter_condition = "测试+1"  # 使用实际存在的列和值
    add_rows = False  # 不添加新行，使用筛选模式
    rows_to_add = 1
    image_name = "test_filter_mode"
    
    print(f"📋 测试配置:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   表格链接: {table_url}")
    print(f"   目标列: {target_column}")
    print(f"   筛选条件: {filter_condition}")
    print(f"   添加行: {add_rows}")
    print(f"   行数: {rows_to_add}")
    
    # 创建测试图片
    print(f"\n🖼️  创建测试图片...")
    height, width = 32, 32
    test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    pil_image = Image.fromarray(test_image)
    
    # 转换为bytes
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    
    print(f"✅ 测试图片创建成功: {width}x{height} RGB")
    
    # 开始测试节点
    print(f"\n🚀 开始测试节点...")
    try:
        result_image, result_message = node.upload_to_table(
            app_id, app_secret, table_url, pil_image, 
            target_column, filter_condition, add_rows, rows_to_add, image_name
        )
        
        print(f"\n📊 测试结果:")
        print(f"   返回图片: {type(result_image)}")
        print(f"   返回消息: {result_message}")
        
        if "✅" in result_message:
            print(f"✅ 测试成功!")
        else:
            print(f"❌ 测试失败")
            print(f"💡 错误信息: {result_message}")
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return 0

if __name__ == "__main__":
    main()
