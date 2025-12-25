#!/usr/bin/env python3
"""
测试文件夹创建和文件上传
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

def test_folder_creation_and_upload(access_token):
    """测试文件夹创建和文件上传"""
    print(f"🔍 测试文件夹创建和文件上传...")
    
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
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 步骤1：尝试获取根文件夹信息
    print(f"\n📁 步骤1: 获取根文件夹信息")
    try:
        root_url = "https://open.feishu.cn/open-apis/drive/v1/files/root"
        response = requests.get(root_url, headers=headers, timeout=30)
        
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            root_data = response.json()
            print(f"  ✅ 成功获取根文件夹信息")
            print(f"  响应: {json.dumps(root_data, indent=2, ensure_ascii=False)}")
            
            # 提取根文件夹的token
            root_token = root_data.get("data", {}).get("token")
            if root_token:
                print(f"  根文件夹token: {root_token}")
            else:
                print(f"  ❌ 未找到根文件夹token")
                root_token = "root"
        else:
            print(f"  ❌ 获取根文件夹失败: {response.text}")
            root_token = "root"
            
    except Exception as e:
        print(f"  异常: {str(e)}")
        root_token = "root"
    
    # 步骤2：尝试创建文件夹
    print(f"\n📁 步骤2: 尝试创建文件夹")
    try:
        create_folder_url = "https://open.feishu.cn/open-apis/drive/v1/files"
        
        folder_data = {
            "name": "ComfyUI测试文件夹",
            "type": "folder",
            "parent_token": root_token
        }
        
        response = requests.post(create_folder_url, headers=headers, json=folder_data, timeout=30)
        
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            folder_result = response.json()
            print(f"  ✅ 成功创建文件夹")
            print(f"  响应: {json.dumps(folder_result, indent=2, ensure_ascii=False)}")
            
            # 提取新文件夹的token
            new_folder_token = folder_result.get("data", {}).get("token")
            if new_folder_token:
                print(f"  新文件夹token: {new_folder_token}")
                target_parent = new_folder_token
            else:
                print(f"  ❌ 未找到新文件夹token")
                target_parent = root_token
        else:
            print(f"  ❌ 创建文件夹失败: {response.text}")
            target_parent = root_token
            
    except Exception as e:
        print(f"  异常: {str(e)}")
        target_parent = root_token
    
    # 步骤3：尝试上传文件到指定文件夹
    print(f"\n📤 步骤3: 尝试上传文件到文件夹")
    
    # 使用不同的上传方法
    upload_methods = [
        # 方法1：使用upload_all到指定文件夹
        {
            "name": "upload_all到指定文件夹",
            "url": "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            "method": "post",
            "files": {'file': ('test_folder.png', image_bytes, 'image/png')},
            "data": {'parent_node': target_parent}
        },
        
        # 方法2：使用files API创建文件
        {
            "name": "files API创建文件",
            "url": "https://open.feishu.cn/open-apis/drive/v1/files",
            "method": "post",
            "json": {
                "name": "test_folder.png",
                "type": "image",
                "parent_token": target_parent
            }
        },
        
        # 方法3：使用multipart上传
        {
            "name": "multipart上传",
            "url": "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
            "method": "post",
            "files": {'file': ('test_multipart.png', image_bytes, 'image/png')},
            "data": {'parent_node': target_parent, 'type': 'image'}
        }
    ]
    
    for method in upload_methods:
        print(f"  尝试方法: {method['name']}")
        
        try:
            if method["method"] == "post":
                if "files" in method:
                    # 文件上传
                    response = requests.post(
                        method["url"], 
                        headers={"Authorization": f"Bearer {access_token}"},
                        files=method["files"],
                        data=method.get("data", {}),
                        timeout=60
                    )
                else:
                    # JSON上传
                    response = requests.post(
                        method["url"], 
                        headers=headers,
                        json=method["json"],
                        timeout=60
                    )
                
                print(f"    状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"    ✅ 成功! 方法: {method['name']}")
                    print(f"    响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    return True, result, method['name']
                else:
                    print(f"    ❌ 失败: {response.text}")
                    
        except Exception as e:
            print(f"    异常: {str(e)}")
    
    return False, None, None

def main():
    """主函数"""
    print("测试文件夹创建和文件上传")
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
    
    # 2. 测试文件夹创建和文件上传
    success, result, method = test_folder_creation_and_upload(access_token)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 找到可用的上传方法！")
        print(f"成功方法: {method}")
        print(f"成功响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        print(f"\n💡 关键发现:")
        print("1. 需要先创建文件夹结构")
        print("2. 或者使用特定的API端点")
        print("3. 现在可以修复上传节点了")
        
    else:
        print("❌ 所有方法都失败了")
        print("\n🔍 可能的原因:")
        print("1. 权限配置不完整")
        print("2. 或者需要使用不同的认证方式")
        print("3. 或者需要企业级权限")
        
        print(f"\n📚 下一步建议:")
        print("1. 检查新App的完整权限配置")
        print("2. 查看飞书企业版权限要求")
        print("3. 或者先使用读取和写入功能")
    
    return 0

if __name__ == "__main__":
    main()

