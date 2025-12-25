#!/usr/bin/env python3
"""
测试修复后的功能
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

def test_add_row_with_image(access_token, app_id, table_id):
    """测试添加行并包含图片"""
    print(f"🔍 测试添加行并包含图片...")
    
    # 创建测试图片
    height, width = 32, 32
    test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # 转换为bytes
    pil_image = Image.fromarray(test_image)
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    
    print(f"✅ 测试图片创建成功，大小: {len(image_bytes)} bytes")
    
    # 先上传图片到云盘
    print(f"📤 上传图片到云盘...")
    upload_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    files = {
        'file': ('test_add_row.png', image_bytes, 'image/png')
    }
    
    data = {
        'file_name': 'test_add_row.png',
        'parent_type': 'bitable_image',
        'parent_node': 'CSPQbCY1OazvLnsxgWicjW0hnYd',
        'size': len(image_bytes)
    }
    
    try:
        response = requests.post(upload_url, headers=headers, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            file_token = result.get("data", {}).get("file_token")
            print(f"✅ 图片上传成功，文件token: {file_token}")
            
            # 现在添加到表格
            print(f"📝 添加行到表格...")
            table_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
            
            # 构建图片附件数据
            image_data = {
                "type": "image",
                "token": file_token
            }
            
            payload = {
                "fields": {
                    "附件": image_data  # 使用"附件"作为列名
                }
            }
            
            print(f"  请求URL: {table_url}")
            print(f"  请求载荷: {json.dumps(payload, indent=2, ensure_ascii=False)}")
            
            response = requests.post(table_url, headers=headers, json=payload, timeout=30)
            
            print(f"  响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 行添加成功!")
                print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"  ❌ 行添加失败!")
                try:
                    error_data = response.json()
                    print(f"  错误代码: {error_data.get('code')}")
                    print(f"  错误信息: {error_data.get('msg')}")
                except:
                    print(f"  错误响应: {response.text}")
                return False
                
        else:
            print(f"❌ 图片上传失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        return False

def test_get_table_records(access_token, app_id, table_id):
    """测试获取表格记录"""
    print(f"🔍 测试获取表格记录...")
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("data", {}).get("items", [])
            print(f"✅ 成功获取 {len(records)} 条记录")
            
            # 显示前几条记录的结构
            if records:
                print(f"📋 第一条记录结构:")
                first_record = records[0]
                print(f"  记录ID: {first_record.get('record_id')}")
                print(f"  字段: {list(first_record.get('fields', {}).keys())}")
                
                # 显示字段详情
                for field_name, field_data in first_record.get('fields', {}).items():
                    print(f"    {field_name}: {type(field_data)} - {field_data}")
            
            return records
        else:
            print(f"❌ 获取记录失败: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 获取记录异常: {str(e)}")
        return []

def main():
    """主函数"""
    print("测试修复后的功能")
    print("=" * 60)
    
    # 配置信息
    app_id = "cli_a8137df47f38501c"  # 使用您之前成功的App ID
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
    
    # 2. 测试获取表格记录
    table_id = "tblPlnQ7x0dYGWC8"  # 从您的链接中提取
    records = test_get_table_records(access_token, app_id, table_id)
    
    # 3. 测试添加行
    if records is not None:
        success = test_add_row_with_image(access_token, app_id, table_id)
        
        if success:
            print(f"\n✅ 添加行测试成功！")
            print(f"请检查您的飞书表格是否显示了新行和图片")
        else:
            print(f"\n❌ 添加行测试失败")
    
    return 0

if __name__ == "__main__":
    main()
