#!/usr/bin/env python3
"""
测试增强功能：空值筛选和格式化输出
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_table_node import FeishuTableNode
import numpy as np
from PIL import Image
import io

def main():
    """主函数"""
    print("测试增强功能：空值筛选和格式化输出")
    print("=" * 60)
    
    # 创建节点实例
    node = FeishuTableNode()
    
    # 测试配置
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/CSPQbCY1OazvLnsxgWicjW0hnYd?table=tblPlnQ7x0dYGWC8&view=vew5tYVpod"
    filter_columns = "文生图\n图生图\n测试"
    filter_condition = "测试+1\n文生图-空值"  # 测试空值筛选功能
    filter_mode = "include"
    output_format = "text"  # 测试新的格式化输出
    max_rows = 1000
    
    print(f"📋 测试配置:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   表格链接: {table_url}")
    print(f"   筛选列: {filter_columns}")
    print(f"   筛选条件: {filter_condition}")
    print(f"   筛选模式: {filter_mode}")
    print(f"   输出格式: {output_format}")
    print(f"   最大行数: {max_rows}")
    
    # 开始测试节点
    print(f"\n🚀 开始测试节点...")
    try:
        result_data, result_message = node.get_table_data(
            app_id, app_secret, table_url, 
            filter_columns, filter_condition, filter_mode, 
            output_format, max_rows
        )
        
        print(f"\n📊 测试结果:")
        print(f"   返回数据: {type(result_data)}")
        print(f"   返回消息: {result_message}")
        
        if result_data:
            print(f"\n📝 格式化后的数据:")
            print("=" * 50)
            print(result_data)
            print("=" * 50)
            
            # 验证格式是否正确
            lines = result_data.strip().split('\n')
            print(f"\n🔍 格式验证:")
            print(f"   总行数: {len(lines)}")
            
            for i, line in enumerate(lines):
                if line.strip():
                    # 检查是否包含行号和&符号
                    if line.startswith(f"{i+1}&") and line.endswith("&"):
                        print(f"   ✅ 第 {i+1} 行格式正确")
                    else:
                        print(f"   ❌ 第 {i+1} 行格式错误: {line}")
            
            print(f"\n✅ 测试成功!")
        else:
            print(f"\n❌ 测试失败")
            print(f"💡 错误信息: {result_message}")
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return 0

if __name__ == "__main__":
    main()

