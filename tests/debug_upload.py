#!/usr/bin/env python3
"""
飞书图片上传诊断脚本
用于详细分析图片上传失败的具体原因
"""

import numpy as np
import requests
import json
from feishu_upload_node import FeishuUploadNode

def test_feishu_api_directly():
    """直接测试飞书API，绕过节点逻辑"""
    print("🔍 直接测试飞书API...")
    
    # 使用您的配置
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    
    # 1. 测试获取访问令牌
    print("1. 测试获取访问令牌...")
    try:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        response = requests.post(url, json=payload, timeout=30)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get("code") == 0:
                access_token = data.get("tenant_access_token")
                print(f"   ✅ 访问令牌获取成功: {access_token[:20]}...")
                
                # 2. 测试文件上传API
                print("\n2. 测试文件上传API...")
                test_file_upload(access_token)
                
            else:
                print(f"   ❌ 获取访问令牌失败: {data.get('msg')}")
        else:
            print(f"   ❌ HTTP请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 获取访问令牌异常: {str(e)}")

def test_file_upload(access_token):
    """测试文件上传API"""
    try:
        # 创建一个简单的测试图片
        test_image = create_simple_test_image()
        
        # 转换为bytes
        from PIL import Image
        import io
        
        pil_image = Image.fromarray(test_image)
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        
        print(f"   测试图片大小: {len(image_bytes)} bytes")
        
        # 测试不同的上传端点
        upload_endpoints = [
            {
                "name": "IM文件上传",
                "url": "https://open.feishu.cn/open-apis/im/v1/files",
                "data": {'type': 'image', 'image_type': 'message'},
                "files": {'file': ('test.png', image_bytes, 'image/png')}
            },
            {
                "name": "文档文件上传",
                "url": "https://open.feishu.cn/open-apis/drive/v1/files/upload_all",
                "data": {'type': 'image', 'parent_node': 'root'},
                "files": {'file': ('test.png', image_bytes, 'image/png')}
            }
        ]
        
        for endpoint in upload_endpoints:
            print(f"\n   测试 {endpoint['name']}...")
            print(f"   URL: {endpoint['url']}")
            
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            response = requests.post(
                endpoint['url'], 
                headers=headers, 
                files=endpoint['files'],
                data=endpoint['data'],
                timeout=60
            )
            
            print(f"   状态码: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"   ✅ 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    
                    if result.get("code") == 0:
                        print(f"   🎉 {endpoint['name']} 成功！")
                        return True
                    else:
                        print(f"   ❌ API错误: {result.get('msg')}")
                        
                except json.JSONDecodeError:
                    print(f"   ⚠️ 响应不是JSON格式: {response.text[:200]}")
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                print(f"   错误响应: {response.text[:200]}")
                
    except Exception as e:
        print(f"   ❌ 文件上传测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

def create_simple_test_image():
    """创建一个简单的测试图片"""
    # 创建一个10x10的简单图片
    height, width = 10, 10
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 创建简单的图案
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                image[y, x] = [255, 0, 0]  # 红色
            else:
                image[y, x] = [0, 0, 255]  # 蓝色
    
    return image

def test_node_with_debug():
    """使用调试模式测试节点"""
    print("\n🔍 使用调试模式测试节点...")
    
    node = FeishuUploadNode()
    
    # 创建测试图片
    test_image = create_simple_test_image()
    
    # 使用您的配置
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    try:
        # 执行节点
        output_image, status_msg = node.upload_to_table(
            app_id=app_id,
            app_secret=app_secret,
            table_url=table_url,
            image=test_image,
            target_column="附件",
            filter_condition="",
            add_rows=True,
            rows_to_add=1,
            image_name="debug_test"
        )
        
        print(f"\n节点执行结果:")
        print(f"  输出图片类型: {type(output_image)}")
        print(f"  状态信息: {status_msg}")
        
    except Exception as e:
        print(f"❌ 节点执行异常: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """主诊断函数"""
    print("飞书图片上传诊断脚本")
    print("=" * 60)
    
    # 1. 直接测试飞书API
    test_feishu_api_directly()
    
    # 2. 测试节点功能
    test_node_with_debug()
    
    print("\n" + "=" * 60)
    print("诊断完成！请查看上述输出信息分析问题。")

if __name__ == "__main__":
    main()
