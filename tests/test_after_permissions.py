#!/usr/bin/env python3
"""
权限配置完成后的测试脚本
"""

import numpy as np
from feishu_upload_node import FeishuUploadNode

def create_test_image():
    """创建一个简单的测试图片"""
    height, width = 20, 20
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                image[y, x] = [255, 0, 0]  # 红色
            else:
                image[y, x] = [0, 0, 255]  # 蓝色
    
    return image

def test_after_permissions():
    """权限配置完成后的测试"""
    print("🔍 权限配置完成后的测试...")
    
    node = FeishuUploadNode()
    
    # 创建测试图片
    test_image = create_test_image()
    print(f"✅ 测试图片创建成功，尺寸: {test_image.shape}")
    
    # 配置信息
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    print(f"📋 配置信息:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   表格链接: {table_url}")
    
    # 测试参数
    target_column = "附件"
    filter_condition = ""
    add_rows = True
    rows_to_add = 1
    image_name = "test_after_permissions"
    
    print(f"\n🚀 开始测试图片上传...")
    print(f"   目标列: {target_column}")
    print(f"   操作模式: 增加行")
    print(f"   增加行数: {rows_to_add}")
    print(f"   图片名称: {image_name}")
    
    try:
        # 执行节点
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
        
        print(f"\n📊 测试结果:")
        print(f"   输出图片类型: {type(output_image)}")
        print(f"   状态信息: {status_msg}")
        
        # 分析结果
        if "成功添加" in status_msg and "行" in status_msg:
            print("🎉 图片上传测试成功！权限配置正确！")
            return True
        elif "错误" in status_msg:
            print("❌ 图片上传测试失败")
            print(f"   错误详情: {status_msg}")
            return False
        else:
            print("❓ 测试结果不明确")
            print(f"   状态信息: {status_msg}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("权限配置完成后的飞书图片上传测试")
    print("=" * 60)
    
    print("⚠️  重要提示:")
    print("请确保您已经在飞书开放平台配置了以下权限:")
    print("1. drive:drive (云盘基础权限)")
    print("2. drive:file (云盘文件权限)")
    print("3. drive:file:upload (云盘文件上传权限)")
    print("4. bitable:app:write (多维表格写入权限)")
    print("\n配置完成后，按任意键继续测试...")
    
    input("按回车键继续...")
    
    # 运行测试
    success = test_after_permissions()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 恭喜！图片上传功能现在完全正常了！")
        print("\n💡 成功原因:")
        print("1. 使用了正确的云盘API端点")
        print("2. 配置了必要的云盘权限")
        print("3. 代码逻辑正确")
    else:
        print("❌ 仍有问题，请检查:")
        print("1. 权限是否配置正确")
        print("2. 网络连接是否正常")
        print("3. 表格列名是否正确")
    
    return 0

if __name__ == "__main__":
    main()
