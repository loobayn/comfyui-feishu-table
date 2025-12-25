#!/usr/bin/env python3
"""
测试飞书应用权限
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

def test_table_access(access_token, app_id, table_id):
    """测试表格访问权限"""
    print(f"🔍 测试访问表格 {table_id}...")
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"  响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("data", {}).get("items", [])
            print(f"  ✅ 成功访问表格!")
            print(f"  记录数量: {len(records)}")
            return True
        else:
            print(f"  ❌ 访问失败!")
            try:
                error_data = response.json()
                print(f"  错误代码: {error_data.get('code')}")
                print(f"  错误信息: {error_data.get('msg')}")
            except:
                print(f"  错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ 请求异常: {str(e)}")
        return False

def test_app_permissions(access_token):
    """测试应用权限"""
    print(f"🔍 测试应用权限...")
    
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"  响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            apps = data.get("data", {}).get("items", [])
            print(f"  ✅ 成功获取应用列表!")
            print(f"  可访问的应用数量: {len(apps)}")
            
            for app in apps[:3]:  # 显示前3个
                print(f"    - {app.get('name', 'Unknown')} ({app.get('app_token')})")
            
            return apps
        else:
            print(f"  ❌ 获取应用列表失败!")
            try:
                error_data = response.json()
                print(f"  错误代码: {error_data.get('code')}")
                print(f"  错误信息: {error_data.get('msg')}")
            except:
                print(f"  错误响应: {response.text}")
            return []
            
    except Exception as e:
        print(f"  ❌ 请求异常: {str(e)}")
        return []

def main():
    """主函数"""
    print("测试飞书应用权限")
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
    
    # 2. 测试应用权限
    print(f"\n🔍 测试应用权限...")
    apps = test_app_permissions(access_token)
    
    # 3. 测试表格访问
    print(f"\n🔍 测试表格访问...")
    
    # 测试您提供的表格
    target_app_id = "CSPQbCY1OazvLnsxgWicjW0hnYd"
    target_table_id = "tblPlnQ7x0dYGWC8"
    
    print(f"  目标表格: {target_app_id}/{target_table_id}")
    
    # 先测试您的App是否能访问目标表格
    can_access = test_table_access(access_token, target_app_id, target_table_id)
    
    if not can_access:
        print(f"\n❌ 您的App无法访问表格 {target_app_id}/{target_table_id}")
        print(f"💡 建议:")
        print(f"   1. 检查表格是否已共享给您的应用")
        print(f"   2. 或者使用有权限访问该表格的App ID")
        print(f"   3. 或者在该表格中为您的应用添加权限")
    
    # 4. 如果有可访问的应用，测试其中一个
    if apps:
        print(f"\n🔍 测试可访问的应用...")
        first_app = apps[0]
        first_app_id = first_app.get('app_token')
        
        if first_app_id:
            print(f"  测试应用: {first_app.get('name', 'Unknown')} ({first_app_id})")
            
            # 获取该应用的表格列表
            tables_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{first_app_id}/tables"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(tables_url, headers=headers, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    tables = data.get("data", {}).get("items", [])
                    print(f"  ✅ 找到 {len(tables)} 个表格")
                    
                    if tables:
                        first_table = tables[0]
                        table_id = first_table.get('table_id')
                        print(f"  测试表格: {first_table.get('name', 'Unknown')} ({table_id})")
                        
                        # 测试访问该表格
                        test_table_access(access_token, first_app_id, table_id)
                        
            except Exception as e:
                print(f"  ❌ 获取表格列表失败: {str(e)}")
    
    return 0

if __name__ == "__main__":
    main()

