#!/usr/bin/env python3
"""
调试图片上传错误
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

def debug_upload_error(access_token):
    """调试上传错误"""
    print(f"🔍 调试图片上传错误...")
    
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
    
    # 测试云盘API
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    files = {
        'file': ('test_debug.png', image_bytes, 'image/png')
    }
    
    # 尝试不同的参数组合
    data_combinations = [
        {'type': 'image'},
        {'type': 'image', 'parent_node': 'root'},
        {'type': 'image', 'name': 'test_debug.png'},
        {'type': 'image', 'parent_node': 'root', 'name': 'test_debug.png'},
        {}
    ]
    
    for i, data in enumerate(data_combinations, 1):
        print(f"\n📤 尝试组合 {i}: {data}")
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            
            print(f"  状态码: {response.status_code}")
            print(f"  响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result
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
    
    return False, None

def main():
    """主函数"""
    print("调试图片上传错误")
    print("=" * 60)
    
    # 配置信息
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    
    print(f"📋 配置信息:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    
    # 1. 获取访问令牌
    print(f"\n🔑 获取访问令牌...")
    access_token = get_access_token(app_id, app_secret)
    if not access_token:
        print("❌ 无法获取访问令牌，调试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 调试上传错误
    success, result = debug_upload_error(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 找到可用的上传参数！")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print("❌ 所有参数组合都失败了")
        print("\n🔍 可能的原因:")
        print("1. 权限配置问题")
        print("2. API参数格式错误")
        print("3. 需要先创建文件夹")
        print("4. 文件大小或格式限制")
    
    return 0

if __name__ == "__main__":
    main()

