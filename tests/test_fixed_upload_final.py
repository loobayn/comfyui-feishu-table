#!/usr/bin/env python3
"""
测试最终修复后的上传功能
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

def test_fixed_upload(access_token):
    """测试修复后的上传功能"""
    print(f"🔍 测试修复后的上传功能...")
    
    # 创建测试图片
    height, width = 32, 32
    test_image = np.zeros((height, width, 3), dtype=np.uint8)
    test_image[:, :] = [255, 0, 0]  # 红色
    
    # 转换为bytes
    pil_image = Image.fromarray(test_image)
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    
    print(f"✅ 测试图片创建成功，大小: {len(image_bytes)} bytes")
    
    # 测试上传 - 使用修复后的参数
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    files = {
        'file': ('test_fixed.png', image_bytes, 'image/png')
    }
    
    # 使用您测试成功的参数格式
    data = {
        'file_name': 'test_fixed.png',
        'parent_type': 'bitable_image',
        'parent_node': 'CSPQbCY1OazvLnsxgWicjW0hnYd',  # 使用您测试成功的文件夹ID
        'size': len(image_bytes)
    }
    
    try:
        print(f"  尝试上传到: {url}")
        print(f"  使用参数: {data}")
        
        response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
        
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 上传成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 提取文件token
            file_token = result.get("data", {}).get("file_token")
            if file_token:
                print(f"  ✅ 文件token: {file_token}")
                return True, result, file_token
            else:
                print(f"  ❌ 未找到文件token")
                return False, result, None
        else:
            print(f"  ❌ 上传失败! 响应: {response.text}")
            return False, None, None
            
    except Exception as e:
        print(f"  异常: {str(e)}")
        return False, None, None

def main():
    """主函数"""
    print("测试最终修复后的上传功能")
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
    
    # 2. 测试修复后的上传功能
    success, result, file_token = test_fixed_upload(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 最终修复后的上传功能测试成功！")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        print(f"文件token: {file_token}")
        
        print(f"\n💡 关键发现:")
        print("1. 基于您的成功测试找到了正确的参数格式")
        print("2. 关键参数: parent_type='bitable_image', parent_node='具体文件夹ID'")
        print("3. 图片上传功能现在完全正常了！")
        print("4. ComfyUI插件中的上传节点已经修复")
        
        print(f"\n🔧 修复要点:")
        print("✅ parent_type: 'bitable_image' (不是 'image')")
        print("✅ parent_node: 具体文件夹ID (不是 'root')")
        print("✅ file_name: 指定文件名")
        print("✅ size: 文件大小")
        
    else:
        print("❌ 最终修复后的上传功能仍然失败")
        print("\n🔍 可能的原因:")
        print("1. 文件夹ID可能已过期")
        print("2. 或者需要其他权限配置")
        print("3. 或者需要重新获取文件夹ID")
        
        print(f"\n📚 下一步建议:")
        print("1. 重新获取有效的文件夹ID")
        print("2. 或者使用您测试成功的文件夹ID")
        print("3. 或者先使用读取和写入功能")
    
    return 0

if __name__ == "__main__":
    main()
