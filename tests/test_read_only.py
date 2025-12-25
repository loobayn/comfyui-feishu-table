#!/usr/bin/env python3
"""
测试当前权限下的读取功能
"""

import numpy as np
from feishu_table_node import FeishuTableNode

def test_read_functionality():
    """测试读取功能"""
    print("🔍 测试当前权限下的读取功能...")
    
    node = FeishuTableNode()
    
    # 配置信息
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    print(f"📋 配置信息:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   表格链接: {table_url}")
    
    # 测试参数 - 只读取，不筛选
    filter_columns = "文本,内容,进度"  # 指定要获取的列
    filter_condition = ""  # 不筛选行
    
    print(f"\n🚀 开始测试读取功能...")
    print(f"   要获取的列: {filter_columns}")
    print(f"   行筛选条件: {filter_condition if filter_condition else '无筛选'}")
    
    try:
        # 执行节点
        result, status_msg = node.get_table_data(
            app_id=app_id,
            app_secret=app_secret,
            table_url=table_url,
            filter_columns=filter_columns,
            filter_condition=filter_condition,
            filter_mode="include",
            output_format="text"
        )
        
        print(f"\n📊 测试结果:")
        print(f"   输出类型: {type(result)}")
        print(f"   状态信息: {status_msg}")
        
        if result:
            print(f"   获取到的内容:")
            print(f"   {result}")
            
            # 分析结果
            if "错误" in status_msg:
                print("❌ 读取功能测试失败")
                return False
            elif "成功" in status_msg or "获取到" in status_msg:
                print("✅ 读取功能测试成功！")
                return True
            else:
                print("❓ 读取功能测试结果不明确")
                return False
        else:
            print("❌ 没有获取到任何内容")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_with_different_columns():
    """测试不同的列组合"""
    print(f"\n🔍 测试不同的列组合...")
    
    node = FeishuTableNode()
    
    # 配置信息
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    # 测试不同的列组合
    column_combinations = [
        "文本",           # 单列
        "内容",           # 单列
        "进度",           # 单列
        "文本,内容",      # 两列
        "内容,进度",      # 两列
        "文本,内容,进度"  # 三列
    ]
    
    for columns in column_combinations:
        print(f"\n📋 测试列组合: {columns}")
        
        try:
            result, status_msg = node.get_table_data(
                app_id=app_id,
                app_secret=app_secret,
                table_url=table_url,
                filter_columns=columns,
                filter_condition="",
                filter_mode="include",
                output_format="text"
            )
            
            if result:
                print(f"  ✅ 成功获取内容，长度: {len(str(result))}")
                print(f"  状态: {status_msg}")
            else:
                print(f"  ❌ 未获取到内容")
                print(f"  状态: {status_msg}")
                
        except Exception as e:
            print(f"  ❌ 异常: {str(e)}")

def main():
    """主函数"""
    print("测试当前权限下的读取功能")
    print("=" * 60)
    
    print("📋 当前已配置的权限:")
    print("✅ bitable:app")
    print("✅ bitable:app:readonly")
    print("❌ bitable:app:write (未配置)")
    print("❌ drive:drive (未配置)")
    print("❌ drive:file (未配置)")
    print("❌ drive:file:upload (未配置)")
    
    print(f"\n💡 预期结果:")
    print("✅ 读取功能应该可以正常工作")
    print("❌ 写入功能无法工作")
    print("❌ 图片上传功能无法工作")
    
    # 1. 测试基本读取功能
    print(f"\n" + "=" * 60)
    success = test_read_functionality()
    
    # 2. 测试不同列组合
    if success:
        test_with_different_columns()
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 读取功能测试成功！")
        print("\n💡 当前状态:")
        print("✅ 可以读取多维表格数据")
        print("✅ 可以筛选列和行")
        print("❌ 无法写入数据（需要 bitable:app:write）")
        print("❌ 无法上传图片（需要 drive 相关权限）")
        
        print(f"\n🔧 下一步建议:")
        print("1. 如果需要写入功能，申请 bitable:app:write 权限")
        print("2. 如果需要图片上传，申请 drive:drive, drive:file, drive:file:upload 权限")
        print("3. 或者先使用读取功能，等权限配置完成后再测试完整功能")
    else:
        print("❌ 读取功能测试失败")
        print("\n🔍 可能的原因:")
        print("1. 权限配置不完整")
        print("2. 表格链接有误")
        print("3. 网络连接问题")
    
    return 0

if __name__ == "__main__":
    main()
