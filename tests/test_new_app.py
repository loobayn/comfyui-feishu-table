#!/usr/bin/env python3
"""
使用新App ID测试完整功能
"""

import numpy as np
from feishu_table_node import FeishuTableNode
from feishu_write_node import FeishuWriteNode
from feishu_upload_node import FeishuUploadNode

def test_read_functionality():
    """测试读取功能"""
    print("🔍 测试读取功能...")
    
    node = FeishuTableNode()
    
    # 新的配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    # 测试参数
    filter_columns = "文本,内容,进度"
    filter_condition = ""
    
    try:
        result, status_msg = node.get_table_data(
            app_id=app_id,
            app_secret=app_secret,
            table_url=table_url,
            filter_columns=filter_columns,
            filter_condition=filter_condition,
            filter_mode="include",
            output_format="text"
        )
        
        if "成功" in status_msg or "获取到" in status_msg:
            print("  ✅ 读取功能正常")
            return True
        else:
            print(f"  ❌ 读取功能异常: {status_msg}")
            return False
            
    except Exception as e:
        print(f"  ❌ 读取功能异常: {str(e)}")
        return False

def test_write_functionality():
    """测试写入功能"""
    print("🔍 测试写入功能...")
    
    node = FeishuWriteNode()
    
    # 新的配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    # 测试参数
    input_text = "新App测试写入功能"
    target_column = "文本"
    filter_condition = ""
    add_rows = True
    rows_to_add = 1
    
    try:
        output_text, status_msg = node.write_to_table(
            app_id=app_id,
            app_secret=app_secret,
            table_url=table_url,
            input_text=input_text,
            target_column=target_column,
            filter_condition=filter_condition,
            add_rows=add_rows,
            rows_to_add=rows_to_add
        )
        
        if "成功添加" in status_msg and "行" in status_msg:
            print("  ✅ 写入功能正常")
            return True
        elif "错误" in status_msg:
            print(f"  ❌ 写入功能异常: {status_msg}")
            return False
        else:
            print(f"  ❓ 写入功能结果不明确: {status_msg}")
            return False
            
    except Exception as e:
        print(f"  ❌ 写入功能异常: {str(e)}")
        return False

def test_upload_functionality():
    """测试图片上传功能"""
    print("🔍 测试图片上传功能...")
    
    node = FeishuUploadNode()
    
    # 创建测试图片
    height, width = 20, 20
    test_image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                test_image[y, x] = [255, 0, 0]  # 红色
            else:
                test_image[y, x] = [0, 0, 255]  # 蓝色
    
    # 新的配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    # 测试参数
    target_column = "附件"
    filter_condition = ""
    add_rows = True
    rows_to_add = 1
    image_name = "new_app_test"
    
    try:
        output_image, status_msg = node.upload_to_table(
            app_id=app_id,
            app_secret=app_secret,
            table_url=table_url,
            image=test_image,
            target_column=target_column,
            filter_condition=filter_condition,
            add_rows=add_rows,
            rows_to_add=rows_to_add,
            image_name=image_name
        )
        
        if "成功添加" in status_msg and "行" in status_msg:
            print("  ✅ 图片上传功能正常")
            return True
        elif "错误" in status_msg:
            print(f"  ❌ 图片上传功能异常: {status_msg}")
            return False
        else:
            print(f"  ❓ 图片上传功能结果不明确: {status_msg}")
            return False
            
    except Exception as e:
        print(f"  ❌ 图片上传功能异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("使用新App ID测试完整功能")
    print("=" * 60)
    
    print("📋 新的配置信息:")
    print("   App ID: cli_a8137df47f38501c")
    print("   App Secret: xvplUXRwDzCmeYoPMlv7if23MB2lQIzu")
    
    print(f"\n💡 预期结果:")
    print("✅ 读取功能应该可以正常工作")
    print("✅ 写入功能应该可以工作")
    print("✅ 图片上传功能可能可以工作（如果新App有正确权限）")
    
    # 1. 测试读取功能
    print(f"\n" + "=" * 60)
    print("1️⃣ 测试读取功能...")
    read_success = test_read_functionality()
    
    # 2. 测试写入功能
    print(f"\n2️⃣ 测试写入功能...")
    write_success = test_write_functionality()
    
    # 3. 测试图片上传功能
    print(f"\n3️⃣ 测试图片上传功能...")
    upload_success = test_upload_functionality()
    
    # 4. 总结
    print(f"\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"   读取功能: {'✅ 正常' if read_success else '❌ 异常'}")
    print(f"   写入功能: {'✅ 正常' if write_success else '❌ 异常'}")
    print(f"   图片上传: {'✅ 正常' if upload_success else '❌ 异常'}")
    
    if read_success and write_success and upload_success:
        print("\n🎉 恭喜！新App ID下所有功能都正常工作！")
        print("\n💡 成功原因:")
        print("1. 新App ID可能有更完整的权限配置")
        print("2. 或者权限已经正确生效")
        
        print(f"\n🚀 您的插件现在可以:")
        print("✅ 读取多维表格数据")
        print("✅ 筛选列和行")
        print("✅ 写入文本数据")
        print("✅ 上传图片附件")
        
    elif read_success and write_success:
        print("\n🎉 读取和写入功能正常！")
        print("❌ 图片上传功能仍有问题")
        
    elif read_success:
        print("\n✅ 读取功能正常")
        print("❌ 写入和图片上传功能需要进一步调试")
        
    else:
        print("\n❌ 基础功能异常，需要检查新App ID的配置")
    
    return 0

if __name__ == "__main__":
    main()

