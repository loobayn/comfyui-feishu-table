#!/usr/bin/env python3
"""
测试其他应用权限
"""

import requests
import json

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

def test_app_access(access_token, target_app_id):
    """测试是否能访问指定应用"""
    print(f"🔍 测试访问应用 {target_app_id}...")
    
    # 测试获取表格列表
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{target_app_id}/tables"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            tables = data.get("data", {}).get("items", [])
            print(f"  ✅ 成功访问应用!")
            print(f"  找到 {len(tables)} 个表格")
            
            for i, table in enumerate(tables):
                table_id = table.get('table_id')
                table_name = table.get('name', 'Unknown')
                print(f"    {i+1}. {table_name} ({table_id})")
            
            return True
        else:
            print(f"  ❌ 访问失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"    错误代码: {error_data.get('code')}")
                print(f"    错误信息: {error_data.get('msg')}")
            except:
                print(f"    错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ 请求异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("测试其他应用权限")
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
    
    # 2. 测试访问目标应用
    print(f"\n🔍 测试访问目标应用...")
    target_app_id = "CSPQbCY1OazvLnsxgWicjW0hnYd"
    
    can_access = test_app_access(access_token, target_app_id)
    
    if can_access:
        print(f"\n✅ 您的应用可以访问目标应用!")
        print(f"💡 您可以直接使用该应用的表格")
    else:
        print(f"\n❌ 您的应用无法访问目标应用")
        print(f"💡 需要:")
        print(f"   1. 为目标应用添加权限")
        print(f"   2. 或者创建新的多维表格")
        print(f"   3. 或者使用有权限的应用")
    
    return 0

if __name__ == "__main__":
    main()

