#!/usr/bin/env python3
"""
检查飞书应用当前权限状态
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

def check_app_permissions(access_token, app_id):
    """检查应用权限"""
    try:
        # 尝试获取应用信息
        url = f"https://open.feishu.cn/open-apis/application/v6/apps/{app_id}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"应用信息API状态码: {response.status_code}")
        
        if response.status_code == 200:
            app_data = response.json()
            print(f"应用信息: {json.dumps(app_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"获取应用信息失败: {response.text}")
        
        # 尝试获取应用权限列表
        url = f"https://open.feishu.cn/open-apis/application/v6/apps/{app_id}/permissions"
        response = requests.get(url, headers=headers, timeout=30)
        print(f"\n权限列表API状态码: {response.status_code}")
        
        if response.status_code == 200:
            perm_data = response.json()
            print(f"权限列表: {json.dumps(perm_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"获取权限列表失败: {response.text}")
            
    except Exception as e:
        print(f"检查权限时发生错误: {str(e)}")

def test_bitable_api(access_token, app_id):
    """测试多维表格API权限"""
    print(f"\n🔍 测试多维表格API权限...")
    
    # 测试读取权限
    print(f"\n📖 测试读取权限...")
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"  获取表格列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 读取权限正常，响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"  ❌ 读取权限失败: {response.text}")
            
    except Exception as e:
        print(f"  测试读取权限时发生错误: {str(e)}")
    
    # 测试写入权限（创建测试记录）
    print(f"\n✍️ 测试写入权限...")
    try:
        # 先获取一个表格ID
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0 and data.get("data", {}).get("items"):
                table_id = data["data"]["items"][0]["table_id"]
                print(f"  找到表格ID: {table_id}")
                
                # 尝试创建测试记录
                url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
                test_data = {
                    "fields": {
                        "测试字段": "测试值"
                    }
                }
                
                response = requests.post(url, json=test_data, headers=headers, timeout=30)
                print(f"  创建记录状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ 写入权限正常，响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    
                    # 删除测试记录
                    if result.get("code") == 0:
                        record_id = result.get("data", {}).get("record_id")
                        if record_id:
                            delete_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records/{record_id}"
                            delete_response = requests.delete(delete_url, headers=headers, timeout=30)
                            print(f"  删除测试记录状态码: {delete_response.status_code}")
                else:
                    print(f"  ❌ 写入权限失败: {response.text}")
            else:
                print(f"  无法获取表格列表: {data}")
        else:
            print(f"  无法获取表格列表，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"  测试写入权限时发生错误: {str(e)}")

def main():
    """主函数"""
    print("检查飞书应用权限状态")
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
        print("❌ 无法获取访问令牌，检查终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 检查应用权限
    print(f"\n🔍 检查应用权限...")
    check_app_permissions(access_token, app_id)
    
    # 3. 测试多维表格API权限
    test_bitable_api(access_token, app_id)
    
    # 4. 总结
    print(f"\n" + "=" * 60)
    print("📋 权限检查完成！")
    print("\n💡 建议:")
    print("1. 如果读取权限正常，说明基本权限已配置")
    print("2. 如果写入权限失败，需要添加相应的写入权限")
    print("3. 权限名称可能是: bitable:app:write, bitable:table:write 等")
    print("4. 建议在飞书开放平台搜索 'bitable' 相关权限")
    
    return 0

if __name__ == "__main__":
    main()
