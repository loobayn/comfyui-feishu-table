#!/usr/bin/env python3
"""
简单的上传测试
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

def test_simple_upload(access_token):
    """测试简单上传"""
    print(f"🔍 测试简单上传...")
    
    # 创建测试图片
    height, width = 20, 20
    test_image = np.zeros((height, width, 3), dtype=np.uint8)
    test_image[:, :] = [255, 0, 0]  # 红色
    
    # 转换为bytes
    pil_image = Image.fromarray(test_image)
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    
    print(f"✅ 测试图片创建成功，大小: {len(image_bytes)} bytes")
    
    # 测试上传
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    files = {
        'file': ('test_simple.png', image_bytes, 'image/png')
    }
    
    try:
        print(f"  尝试上传到: {url}")
        response = requests.post(url, headers=headers, files=files, timeout=60)
        
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True, result
        else:
            print(f"  ❌ 失败! 响应: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"  异常: {str(e)}")
        return False, None

def main():
    """主函数"""
    print("简单的上传测试")
    print("=" * 60)
    
    # 配置信息
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
    
    # 2. 测试上传
    success, result = test_simple_upload(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 上传测试成功！")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print("❌ 上传测试失败")
        print("\n🔍 可能的原因:")
        print("1. 权限配置不完整")
        print("2. API参数格式错误")
        print("3. 需要企业级权限")
    
    return 0

if __name__ == "__main__":
    main()


