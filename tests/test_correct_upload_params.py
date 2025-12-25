#!/usr/bin/env python3
"""
测试正确的上传参数格式
"""

import requests
import json
import numpy as np
from PIL import Image
import io

def get_access_token(app_id, app_secret):
    """获取访问令牌"""
    try:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") == 0:
            return data.get("tenant_access_token")
        else:
            print(f"获取访问令牌失败: {data.get('msg', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"获取访问令牌时发生错误: {str(e)}")
        return None

def test_correct_upload_params(access_token):
    """测试正确的上传参数"""
    print(f"🔍 测试正确的上传参数格式...")
    
    # 创建测试图片
    height, width = 20, 20
    test_image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                test_image[y, x] = [255, 0, 0]  # 红色
            else:
                test_image[y, x] = [0, 0, 255]  # 蓝色
    
    # 转换为bytes
    pil_image = Image.fromarray(test_image)
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    
    print(f"✅ 测试图片创建成功，大小: {len(image_bytes)} bytes")
    
    # 测试云盘API - 使用正确的参数格式
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "multipart/form-data"
    }
    
    # 根据飞书官方文档，尝试正确的参数格式
    files = {
        'file': ('test_correct.png', image_bytes, 'image/png')
    }
    
    # 正确的参数组合（根据官方文档）
    correct_params = [
        # 方法1：只传文件，不传其他参数
        {},
        
        # 方法2：使用正确的字段名
        {'type': 'image', 'parent_node': 'root'},
        
        # 方法3：使用file_token作为parent_node
        {'type': 'image', 'parent_node': 'root'},
        
        # 方法4：不指定type，让API自动识别
        {'parent_node': 'root'},
        
        # 方法5：使用空字符串
        {'type': '', 'parent_node': ''}
    ]
    
    for i, params in enumerate(correct_params, 1):
        print(f"\n📤 尝试正确参数组合 {i}: {params}")
        
        try:
            # 注意：这里使用data而不是json
            response = requests.post(url, headers=headers, files=files, data=params, timeout=60)
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result, params
            else:
                print(f"  ❌ 失败! 响应: {response.text}")
                
                # 尝试解析错误信息
                try:
                    error_data = response.json()
                    print(f"  错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"  原始错误: {response.text}")
                    
        except Exception as e:
            print(f"  异常: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return False, None, None

def main():
    """主函数"""
    print("测试正确的上传参数格式")
    print("=" * 60)
    
    # 新的配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    
    print(f"📋 配置信息:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    
    # 1. 获取访问令牌
    print(f"\n🔑 获取访问令牌...")
    access_token = get_access_token(app_id, app_secret)
    if not access_token:
        print("❌ 无法获取访问令牌，测试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 测试正确的上传参数
    success, result, correct_params = test_correct_upload_params(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 找到正确的上传参数！")
        print(f"成功参数: {correct_params}")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        print(f"\n💡 关键发现:")
        print("1. 新App ID有正确的权限")
        print("2. 问题在于API参数格式")
        print("3. 现在可以修复上传节点了")
        
    else:
        print("❌ 所有参数组合都失败了")
        print("\n🔍 可能的原因:")
        print("1. 需要查看飞书官方文档")
        print("2. 或者需要先创建文件夹")
        print("3. 或者需要其他权限")
    
    return 0

if __name__ == "__main__":
    main()

