#!/usr/bin/env python3
"""
测试错误信息显示功能
"""

import requests
import json

def test_error_display():
    """测试错误信息显示"""
    print("🔍 测试错误信息显示功能...")
    
    # 使用错误的参数来触发错误
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    
    headers = {
        "Authorization": "Bearer invalid_token_12345"
    }
    
    files = {
        'file': ('test.png', b'fake_image_data', 'image/png')
    }
    
    # 使用错误的参数
    data = {
        'file_name': 'test.png',
        'parent_type': 'invalid_type',  # 错误的类型
        'parent_node': 'invalid_node',  # 错误的节点
        'size': 100
    }
    
    try:
        print(f"  尝试上传到: {url}")
        print(f"  使用错误参数: {data}")
        
        response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        
        print(f"  响应状态码: {response.status_code}")
        print(f"  响应原因: {response.reason}")
        print(f"  响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 意外成功! 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"  ❌ 预期失败!")
            try:
                error_data = response.json()
                print(f"  错误代码: {error_data.get('code')}")
                print(f"  错误信息: {error_data.get('msg')}")
                print(f"  完整错误响应: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except Exception as json_error:
                print(f"  无法解析JSON错误响应: {json_error}")
                print(f"  原始响应文本: {response.text[:500]}...")
            
            # 生成错误摘要
            error_summary = f"HTTP {response.status_code} {response.reason}"
            if 'error_data' in locals() and error_data:
                error_summary += f" - 错误代码: {error_data.get('code')}, 错误信息: {error_data.get('msg')}"
            
            print(f"  错误摘要: {error_summary}")
            
    except Exception as e:
        print(f"  请求异常: {str(e)}")

def main():
    """主函数"""
    print("测试错误信息显示功能")
    print("=" * 60)
    
    test_error_display()
    
    print(f"\n" + "=" * 60)
    print("🎯 错误信息显示测试完成!")
    print("\n💡 现在节点应该能显示详细的错误信息:")
    print("✅ HTTP状态码")
    print("✅ HTTP原因")
    print("✅ 响应头信息")
    print("✅ 错误代码")
    print("✅ 错误信息")
    print("✅ 完整错误响应")
    
    return 0

if __name__ == "__main__":
    main()

