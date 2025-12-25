#!/usr/bin/env python3
"""
测试用户提供的方法：先上传文件获取file_token，再创建记录
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

def upload_file_to_feishu(access_token, image_bytes, image_name):
    """上传文件到飞书云盘，获取file_token"""
    print(f"📤 上传文件到飞书云盘...")
    
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    files = {
        'file': (f"{image_name}.png", image_bytes, 'image/png')
    }
    
    data = {
        'file_name': f"{image_name}.png",
        'parent_type': 'bitable_image',
        'parent_node': 'CSPQbCY1OazvLnsxgWicjW0hnYd',
        'size': len(image_bytes)
    }
    
    print(f"  文件名: {image_name}.png")
    print(f"  文件大小: {len(image_bytes)} bytes")
    print(f"  上传参数: {data}")
    
    try:
        response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
        
        print(f"  响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 文件上传成功!")
            print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 提取file_token
            file_token = result.get("data", {}).get("file_token")
            if file_token:
                print(f"  文件token: {file_token}")
                return file_token
            else:
                print(f"  ❌ 未找到file_token")
                return None
        else:
            print(f"  ❌ 文件上传失败!")
            try:
                error_data = response.json()
                print(f"  错误代码: {error_data.get('code')}")
                print(f"  错误信息: {error_data.get('msg')}")
            except:
                print(f"  错误响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"  ❌ 上传异常: {str(e)}")
        return None

def create_record_with_image(access_token, app_id, table_id, file_token, target_column):
    """使用file_token创建包含图片的记录"""
    print(f"📝 创建包含图片的记录...")
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 使用您提供的方法：直接使用file_token，不需要type字段
    payload = {
        "fields": {
            target_column: [
                {
                    "file_token": file_token
                }
            ]
        }
    }
    
    print(f"  请求URL: {url}")
    print(f"  请求载荷: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"  响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 记录创建成功!")
            print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查飞书是否返回了错误（即使HTTP状态码是200）
            if result.get('code') == 0:
                print(f"  🎉 飞书确认成功!")
                record_id = result.get("data", {}).get("record", {}).get("record_id")
                if record_id:
                    print(f"  记录ID: {record_id}")
                return True
            else:
                print(f"  ❌ 飞书返回错误!")
                error_code = result.get('code')
                error_msg = result.get('msg')
                print(f"  错误代码: {error_code}")
                print(f"  错误信息: {error_msg}")
                return False
        else:
            print(f"  ❌ 记录创建失败!")
            try:
                error_data = response.json()
                error_code = error_data.get('code')
                error_msg = error_data.get('msg')
                print(f"  错误代码: {error_code}")
                print(f"  错误信息: {error_msg}")
            except:
                print(f"  错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ 创建记录异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("测试用户提供的方法：先上传文件获取file_token，再创建记录")
    print("=" * 80)
    
    # 配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    target_app_id = "CSPQbCY1OazvLnsxgWicjW0hnYd"
    target_table_id = "tblPlnQ7x0dYGWC8"
    target_column = "生成图片"
    
    print(f"📋 配置信息:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   目标应用: {target_app_id}")
    print(f"   目标表格: {target_table_id}")
    print(f"   目标列: {target_column}")
    
    # 1. 获取访问令牌
    print(f"\n🔑 获取访问令牌...")
    access_token = get_access_token(app_id, app_secret)
    if not access_token:
        print("❌ 无法获取访问令牌，测试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 创建测试图片
    print(f"\n🖼️  创建测试图片...")
    height, width = 64, 64
    test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    pil_image = Image.fromarray(test_image)
    
    # 转换为bytes
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    
    print(f"✅ 测试图片创建成功: {width}x{height} RGB，大小: {len(image_bytes)} bytes")
    
    # 3. 上传文件获取file_token
    print(f"\n🚀 步骤1: 上传文件获取file_token...")
    file_token = upload_file_to_feishu(access_token, image_bytes, "test_user_method")
    
    if not file_token:
        print("❌ 文件上传失败，测试终止")
        return
    
    # 4. 使用file_token创建记录
    print(f"\n🚀 步骤2: 使用file_token创建记录...")
    success = create_record_with_image(access_token, target_app_id, target_table_id, file_token, target_column)
    
    if success:
        print(f"\n🎉 测试成功!")
        print(f"💡 您的方法完全正确!")
        print(f"📝 总结:")
        print(f"   1. 使用 /drive/v1/files/upload_all 上传文件获取 file_token")
        print(f"   2. 使用 /bitable/v1/apps/{target_app_id}/tables/{target_table_id}/records 创建记录")
        print(f"   3. 在 fields.{target_column} 中使用 [{{'file_token': '{file_token}'}}] 格式")
    else:
        print(f"\n❌ 测试失败")
        print(f"💡 请检查错误信息")
    
    return 0

if __name__ == "__main__":
    main()

