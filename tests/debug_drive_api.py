#!/usr/bin/env python3
"""
调试飞书云盘API的详细错误信息
"""

import requests
import json
import numpy as np
from PIL import Image
import io

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

def test_drive_api_methods(access_token, image_bytes, image_name):
    """测试不同的云盘API方法"""
    
    print(f"\n🔍 测试不同的云盘API方法...")
    
    # 方法1: 使用 /drive/v1/files/upload_all (官方推荐)
    print(f"\n📤 方法1: /drive/v1/files/upload_all")
    try:
        url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # 准备文件数据
        files = {
            'file': (f"{image_name}.png", image_bytes, 'image/png')
        }
        
        # 尝试不同的参数组合
        data_combinations = [
            # 组合1: 基础参数
            {'type': 'image'},
            
            # 组合2: 带parent_node
            {'type': 'image', 'parent_node': 'root'},
            
            # 组合3: 带name
            {'type': 'image', 'name': f"{image_name}.png"},
            
            # 组合4: 完整参数
            {'type': 'image', 'parent_node': 'root', 'name': f"{image_name}.png"},
            
            # 组合5: 空参数
            {}
        ]
        
        for i, data in enumerate(data_combinations, 1):
            print(f"  尝试组合 {i}: {data}")
            
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            
            print(f"    状态码: {response.status_code}")
            print(f"    响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"    成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result
            else:
                print(f"    失败! 响应: {response.text}")
                
                # 尝试解析错误信息
                try:
                    error_data = response.json()
                    print(f"    错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"    原始错误: {response.text}")
                    
    except Exception as e:
        print(f"    异常: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 方法2: 尝试其他可能的端点
    print(f"\n📤 方法2: 尝试其他端点")
    
    alternative_endpoints = [
        "https://open.feishu.cn/open-apis/drive/v1/files",
        "https://open.feishu.cn/open-apis/drive/v1/media/upload_all",
        "https://open.feishu.cn/open-apis/drive/v1/files/upload"
    ]
    
    for endpoint in alternative_endpoints:
        print(f"  尝试端点: {endpoint}")
        try:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            files = {
                'file': (f"{image_name}.png", image_bytes, 'image/png')
            }
            
            data = {'type': 'image'}
            
            response = requests.post(endpoint, headers=headers, files=files, data=data, timeout=30)
            print(f"    状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"    成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result
            else:
                print(f"    失败: {response.text[:200]}...")
                
        except Exception as e:
            print(f"    异常: {str(e)}")
    
    return False, None

def main():
    """主函数"""
    print("飞书云盘API调试测试")
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
        print("❌ 无法获取访问令牌，测试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 创建测试图片
    print(f"\n🖼️ 创建测试图片...")
    test_image = create_test_image()
    print(f"✅ 测试图片创建成功，尺寸: {test_image.shape}")
    
    # 转换为bytes
    pil_image = Image.fromarray(test_image)
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    print(f"✅ 图片转换为bytes成功，大小: {len(image_bytes)} bytes")
    
    # 3. 测试云盘API
    success, result = test_drive_api_methods(access_token, image_bytes, "debug_test")
    
    # 4. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 找到可用的API方法！")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print("❌ 所有API方法都失败了")
        print("\n🔍 可能的原因:")
        print("1. 缺少 drive:file:write 权限")
        print("2. API参数格式不正确")
        print("3. 需要先创建文件夹或指定正确的parent_node")
        print("4. 文件大小或格式限制")
    
    return 0

if __name__ == "__main__":
    main()
