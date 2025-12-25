#!/usr/bin/env python3
"""
基于飞书官方文档的图片上传测试
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

def test_official_upload_methods(access_token):
    """基于官方文档测试上传方法"""
    print(f"🔍 基于飞书官方文档测试上传方法...")
    
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
    
    # 方法1：使用官方推荐的upload_all API
    print(f"\n📤 方法1: 使用 upload_all API")
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 根据官方文档，尝试正确的参数格式
    files = {
        'file': ('test_official.png', image_bytes, 'image/png')
    }
    
    # 官方文档推荐的参数组合
    official_params = [
        # 基础参数
        {},
        
        # 指定文件类型
        {'type': 'image'},
        
        # 指定父节点
        {'parent_node': 'root'},
        
        # 完整参数
        {'type': 'image', 'parent_node': 'root'},
        
        # 使用空字符串
        {'type': '', 'parent_node': ''}
    ]
    
    for i, params in enumerate(official_params, 1):
        print(f"  尝试参数组合 {i}: {params}")
        
        try:
            response = requests.post(url, headers=headers, files=files, data=params, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result, f"upload_all + {params}"
            else:
                print(f"  ❌ 失败! 状态码: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  错误: {error_data.get('msg', '未知错误')}")
                except:
                    print(f"  错误: {response.text}")
                    
        except Exception as e:
            print(f"  异常: {str(e)}")
    
    # 方法2：尝试其他可能的API端点
    print(f"\n📤 方法2: 尝试其他API端点")
    
    alternative_endpoints = [
        "https://open.feishu.cn/open-apis/drive/v1/files/upload",
        "https://open.feishu.cn/open-apis/drive/v1/media/upload",
        "https://open.feishu.cn/open-apis/drive/v1/files",
        "https://open.feishu.cn/open-apis/im/v1/files"
    ]
    
    for endpoint in alternative_endpoints:
        print(f"  尝试端点: {endpoint}")
        
        try:
            response = requests.post(endpoint, headers=headers, files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 成功! 端点: {endpoint}")
                print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result, f"endpoint: {endpoint}"
            elif response.status_code == 404:
                print(f"  ❌ 端点不存在")
            else:
                print(f"  ❌ 状态码: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  错误: {error_data.get('msg', '未知错误')}")
                except:
                    print(f"  错误: {response.text}")
                    
        except Exception as e:
            print(f"  异常: {str(e)}")
    
    # 方法3：尝试不同的文件字段名
    print(f"\n📤 方法3: 尝试不同的文件字段名")
    
    field_names = ['file', 'image', 'attachment', 'upload', 'data']
    
    for field_name in field_names:
        print(f"  尝试字段名: {field_name}")
        
        try:
            files = {
                field_name: ('test_field.png', image_bytes, 'image/png')
            }
            
            response = requests.post(url, headers=headers, files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 成功! 字段名: {field_name}")
                print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True, result, f"field_name: {field_name}"
            else:
                print(f"  ❌ 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"  异常: {str(e)}")
    
    return False, None, None

def main():
    """主函数"""
    print("基于飞书官方文档的图片上传测试")
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
    
    # 2. 基于官方文档测试上传
    success, result, method = test_official_upload_methods(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 找到可用的上传方法！")
        print(f"成功方法: {method}")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        print(f"\n💡 关键发现:")
        print("1. 基于官方文档找到了正确的上传方法")
        print("2. 现在可以修复上传节点了")
        print("3. 或者使用新的API端点")
        
    else:
        print("❌ 所有官方方法都失败了")
        print("\n🔍 可能的原因:")
        print("1. 需要特定的权限配置")
        print("2. 或者需要先创建文件夹结构")
        print("3. 或者需要使用不同的认证方式")
        
        print(f"\n📚 建议查看:")
        print("1. 飞书Drive API权限配置")
        print("2. 文件夹创建API")
        print("3. 其他文件上传方式")
    
    return 0

if __name__ == "__main__":
    main()

