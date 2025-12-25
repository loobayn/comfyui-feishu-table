#!/usr/bin/env python3
"""
测试飞书API连接
"""

import requests
import json

def test_feishu_auth():
    """测试飞书认证"""
    app_id = "cli_a813c1b0ce3e900b"
    app_secret = "vedWW9z16cqWFzlPggibfgHhj5ftXMCs"
    
    print("🔐 测试飞书API认证...")
    
    try:
        # 获取访问令牌
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"响应状态: {data}")
        
        if data.get("code") == 0:
            access_token = data.get("tenant_access_token")
            print(f"✅ 认证成功！访问令牌: {access_token[:20]}...")
            return access_token
        else:
            print(f"❌ 认证失败: {data.get('msg', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"❌ 认证请求失败: {str(e)}")
        return None

def test_table_access(access_token, app_id, table_id):
    """测试表格访问权限"""
    if not access_token:
        print("❌ 没有访问令牌，跳过表格访问测试")
        return False
    
    print(f"\n📊 测试表格访问权限...")
    print(f"应用ID: {app_id}")
    print(f"表格ID: {table_id}")
    
    try:
        # 尝试获取表格元数据
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            if data.get("code") == 0:
                print("✅ 表格访问成功！")
                return True
            else:
                print(f"❌ 表格访问失败: {data.get('msg', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 表格访问请求失败: {str(e)}")
        return False

def test_table_records(access_token, app_id, table_id):
    """测试获取表格记录"""
    if not access_token:
        print("❌ 没有访问令牌，跳过记录获取测试")
        return False
    
    print(f"\n📋 测试获取表格记录...")
    
    try:
        # 尝试获取表格记录
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
        params = {
            "page_size": 10
        }
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            if data.get("code") == 0:
                records = data.get("data", {}).get("items", [])
                print(f"✅ 成功获取 {len(records)} 条记录！")
                return True
            else:
                print(f"❌ 获取记录失败: {data.get('msg', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 记录获取请求失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("飞书API连接测试 - 新表格ID")
    print("=" * 50)
    
    # 新的表格信息
    app_id = "FPNXbI1LKar6Y3sfue3cDZeon1g"
    table_id = "tblTooQfnEL6ZaVE"
    
    print(f"应用ID: {app_id}")
    print(f"表格ID: {table_id}")
    print("=" * 50)
    
    # 测试认证
    access_token = test_feishu_auth()
    
    if not access_token:
        print("\n❌ 认证失败，无法继续测试")
        return
    
    # 测试表格访问
    table_access = test_table_access(access_token, app_id, table_id)
    
    if table_access:
        # 测试获取记录
        test_table_records(access_token, app_id, table_id)
    
    print("\n" + "=" * 50)
    print("测试完成！")
    
    if table_access:
        print("\n💡 建议：")
        print("1. 在ComfyUI中使用新的表格链接")
        print("2. 确认链接格式正确")
        print("3. 重新运行飞书表格节点")
    else:
        print("\n❌ 问题：")
        print("1. 应用权限可能不足")
        print("2. 表格ID可能不正确")
        print("3. 应用可能未正确发布到企业")

if __name__ == "__main__":
    main()
