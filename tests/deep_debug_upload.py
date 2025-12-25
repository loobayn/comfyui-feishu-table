#!/usr/bin/env python3
"""
深度调试图片上传功能
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

def test_different_upload_strategies(access_token):
    """测试不同的上传策略"""
    print(f"🔍 测试不同的上传策略...")
    
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
    
    # 策略1：尝试不同的Content-Type
    print(f"\n📤 策略1: 尝试不同的Content-Type")
    
    content_types = [
        "image/png",
        "image/jpeg", 
        "application/octet-stream",
        "multipart/form-data"
    ]
    
    for content_type in content_types:
        print(f"  尝试Content-Type: {content_type}")
        
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": content_type
            }
            
            files = {
                'file': ('test_content_type.png', image_bytes, content_type)
            }
            
            response = requests.post(
                "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
                headers=headers,
                files=files,
                timeout=60
            )
            
            print(f"    状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ 成功! Content-Type: {content_type}")
                return True, result, f"Content-Type: {content_type}"
            else:
                print(f"    ❌ 失败: {response.text[:100]}...")
                
        except Exception as e:
            print(f"    异常: {str(e)}")
    
    # 策略2：尝试不同的文件大小
    print(f"\n📤 策略2: 尝试不同的文件大小")
    
    # 创建更小的图片
    small_height, small_width = 10, 10
    small_image = np.zeros((small_height, small_width, 3), dtype=np.uint8)
    small_image[:, :] = [128, 128, 128]  # 灰色
    
    pil_small = Image.fromarray(small_image)
    small_buffer = io.BytesIO()
    pil_small.save(small_buffer, format='PNG')
    small_bytes = small_buffer.getvalue()
    
    print(f"  尝试小图片，大小: {len(small_bytes)} bytes")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        files = {
            'file': ('test_small.png', small_bytes, 'image/png')
        }
        
        response = requests.post(
            "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            headers=headers,
            files=files,
            timeout=60
        )
        
        print(f"    状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"    ✅ 成功! 小图片上传")
            return True, result, "小图片上传"
        else:
            print(f"    ❌ 失败: {response.text[:100]}...")
            
    except Exception as e:
        print(f"    异常: {str(e)}")
    
    # 策略3：尝试不同的API端点组合
    print(f"\n📤 策略3: 尝试不同的API端点组合")
    
    api_combinations = [
        {
            "name": "upload_all + 空参数",
            "url": "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            "files": {'file': ('test_api.png', image_bytes, 'image/png')},
            "data": {}
        },
        {
            "name": "upload_all + 基础参数",
            "url": "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            "files": {'file': ('test_api.png', image_bytes, 'image/png')},
            "data": {'type': 'image'}
        },
        {
            "name": "upload_all + 完整参数",
            "url": "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            "files": {'file': ('test_api.png', image_bytes, 'image/png')},
            "data": {'type': 'image', 'parent_node': 'root', 'name': 'test_api.png'}
        }
    ]
    
    for combo in api_combinations:
        print(f"  尝试: {combo['name']}")
        
        try:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            response = requests.post(
                combo["url"],
                headers=headers,
                files=combo["files"],
                data=combo["data"],
                timeout=60
            )
            
            print(f"    状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ 成功! {combo['name']}")
                return True, result, combo['name']
            else:
                print(f"    ❌ 失败: {response.text[:100]}...")
                
        except Exception as e:
            print(f"    异常: {str(e)}")
    
    # 策略4：尝试不同的认证方式
    print(f"\n📤 策略4: 尝试不同的认证方式")
    
    auth_methods = [
        {
            "name": "Bearer Token",
            "headers": {"Authorization": f"Bearer {access_token}"}
        },
        {
            "name": "Authorization Header",
            "headers": {"Authorization": f"Bearer {access_token}", "X-Auth-Token": access_token}
        },
        {
            "name": "Query Parameter",
            "headers": {"Authorization": f"Bearer {access_token}"},
            "params": {"access_token": access_token}
        }
    ]
    
    for auth_method in auth_methods:
        print(f"  尝试认证方式: {auth_method['name']}")
        
        try:
            files = {
                'file': ('test_auth.png', image_bytes, 'image/png')
            }
            
            params = auth_method.get("params", {})
            
            response = requests.post(
                "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
                headers=auth_method["headers"],
                files=files,
                params=params,
                timeout=60
            )
            
            print(f"    状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ 成功! 认证方式: {auth_method['name']}")
                return True, result, f"认证方式: {auth_method['name']}"
            else:
                print(f"    ❌ 失败: {response.text[:100]}...")
                
        except Exception as e:
            print(f"    异常: {str(e)}")
    
    # 策略5：尝试不同的文件格式
    print(f"\n📤 策略5: 尝试不同的文件格式")
    
    # 创建JPEG图片
    jpeg_image = np.zeros((20, 20, 3), dtype=np.uint8)
    jpeg_image[:, :] = [255, 255, 0]  # 黄色
    
    pil_jpeg = Image.fromarray(jpeg_image)
    jpeg_buffer = io.BytesIO()
    pil_jpeg.save(jpeg_buffer, format='JPEG', quality=95)
    jpeg_bytes = jpeg_buffer.getvalue()
    
    print(f"  尝试JPEG格式，大小: {len(jpeg_bytes)} bytes")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        files = {
            'file': ('test_jpeg.jpg', jpeg_bytes, 'image/jpeg')
        }
        
        response = requests.post(
            "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            headers=headers,
            files=files,
            timeout=60
        )
        
        print(f"    状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"    ✅ 成功! JPEG格式")
            return True, result, "JPEG格式"
        else:
            print(f"    ❌ 失败: {response.text[:100]}...")
            
    except Exception as e:
        print(f"    异常: {str(e)}")
    
    return False, None, None

def main():
    """主函数"""
    print("深度调试图片上传功能")
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
        print("❌ 无法获取访问令牌，调试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 深度调试上传功能
    success, result, method = test_different_upload_strategies(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 找到可用的上传方法！")
        print(f"成功方法: {method}")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        print(f"\n💡 关键发现:")
        print("1. 通过深度调试找到了正确的上传方法")
        print("2. 现在可以修复上传节点了")
        print("3. 或者使用新的参数组合")
        
    else:
        print("❌ 所有策略都失败了")
        print("\n🔍 深度分析:")
        print("1. 问题可能在于权限配置")
        print("2. 或者API端点本身有问题")
        print("3. 或者需要特定的企业级配置")
        
        print(f"\n📚 下一步建议:")
        print("1. 检查飞书企业版权限要求")
        print("2. 或者联系飞书技术支持")
        print("3. 或者先使用读取和写入功能")
        
        print(f"\n💡 当前可用功能:")
        print("✅ 读取多维表格数据")
        print("✅ 筛选列和行")
        print("✅ 写入文本数据")
        print("❌ 图片上传功能")
    
    return 0

if __name__ == "__main__":
    main()

