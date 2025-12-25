#!/usr/bin/env python3
"""
测试修复后的飞书表格插件
"""

from feishu_table_node import FeishuTableNode

def test_url_parsing():
    """测试URL解析功能"""
    print("🔍 测试URL解析功能...")
    
    node = FeishuTableNode()
    
    # 测试您的实际链接
    test_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    app_id, table_id = node.extract_table_info(test_url)
    
    print(f"解析结果:")
    print(f"  应用ID: {app_id}")
    print(f"  表格ID: {table_id}")
    
    expected_app_id = "FPNXbI1LKar6Y3sfue3cDZeon1g"
    expected_table_id = "tblTooQfnEL6ZaVE"
    
    if app_id == expected_app_id and table_id == expected_table_id:
        print("✅ URL解析测试通过！")
        return True
    else:
        print("❌ URL解析测试失败！")
        print(f"  期望应用ID: {expected_app_id}")
        print(f"  期望表格ID: {expected_table_id}")
        return False

def test_node_execution():
    """测试节点执行功能"""
    print("\n🚀 测试节点执行功能...")
    
    node = FeishuTableNode()
    
    # 使用您的实际配置
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    print("正在执行节点...")
    print("这可能需要几秒钟时间...")
    
    try:
        # 执行节点
        output_data, status_msg = node.get_table_data(
            app_id=app_id,
            app_secret=app_secret,
            table_url=table_url,
            filter_columns="",
            filter_condition="",
            filter_mode="include",
            output_format="json",
            max_rows=10
        )
        
        print(f"\n执行结果:")
        print(f"  状态信息: {status_msg}")
        print(f"  输出数据长度: {len(output_data)} 字符")
        
        if "错误" not in status_msg:
            print("✅ 节点执行测试通过！")
            print(f"  获取到的数据预览: {output_data[:200]}...")
            return True
        else:
            print("❌ 节点执行测试失败！")
            print(f"  错误信息: {status_msg}")
            return False
            
    except Exception as e:
        print(f"❌ 节点执行时发生异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("修复后的飞书表格插件测试")
    print("=" * 50)
    
    # 测试URL解析
    url_ok = test_url_parsing()
    
    if url_ok:
        # 测试节点执行
        execution_ok = test_node_execution()
        
        print("\n" + "=" * 50)
        if execution_ok:
            print("🎉 所有测试通过！插件已修复，应该可以正常工作了。")
            print("\n💡 现在请在ComfyUI中重新运行飞书表格节点。")
        else:
            print("❌ 节点执行测试失败，可能还有其他问题。")
    else:
        print("\n❌ URL解析测试失败，插件仍有问题。")
    
    return 0

if __name__ == "__main__":
    main()
