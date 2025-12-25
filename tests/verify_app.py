#!/usr/bin/env python3
"""
验证飞书应用是否存在和状态
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

def verify_app_status(access_token, app_id):
    """验证应用状态"""
    print(f"🔍 验证应用状态...")
    
    # 测试1: 基础认证
    print(f"\n1️⃣ 测试基础认证...")
    if access_token:
        print(f"   ✅ 基础认证成功，令牌: {access_token[:20]}...")
    else:
        print(f"   ❌ 基础认证失败")
        return False
    
    # 测试2: 尝试访问应用信息
    print(f"\n2️⃣ 测试应用信息访问...")
    try:
        url = f"https://open.feishu.cn/open-apis/application/v6/apps/{app_id}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            app_data = response.json()
            print(f"  ✅ 应用信息获取成功")
            print(f"  应用名称: {app_data.get('data', {}).get('name', '未知')}")
            print(f"  应用描述: {app_data.get('data', {}).get('description', '无描述')}")
        elif response.status_code == 403:
            print(f"  ❌ 权限不足，需要更多权限")
        elif response.status_code == 404:
            print(f"  ❌ 应用不存在或无法访问")
        else:
            print(f"  ❓ 未知状态: {response.text}")
            
    except Exception as e:
        print(f"  异常: {str(e)}")
    
    # 测试3: 尝试访问多维表格
    print(f"\n3️⃣ 测试多维表格访问...")
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                tables = data.get("data", {}).get("items", [])
                print(f"  ✅ 多维表格访问成功，找到 {len(tables)} 个表格")
                for i, table in enumerate(tables[:3]):  # 只显示前3个
                    print(f"    表格 {i+1}: {table.get('name', '未命名')} (ID: {table.get('table_id', '未知')})")
            else:
                print(f"  ❌ 多维表格API错误: {data.get('msg', '未知错误')}")
        elif response.status_code == 403:
            print(f"  ❌ 权限不足，需要 bitable 相关权限")
        elif response.status_code == 400:
            error_data = response.json()
            if error_data.get("code") == 91402:
                print(f"  ❌ 应用不存在或无权限访问多维表格")
                print(f"  错误详情: {error_data.get('msg', '未知错误')}")
            else:
                print(f"  ❌ 其他错误: {error_data.get('msg', '未知错误')}")
        else:
            print(f"  ❓ 未知状态: {response.text}")
            
    except Exception as e:
        print(f"  异常: {str(e)}")
    
    # 测试4: 尝试访问云盘
    print(f"\n4️⃣ 测试云盘访问...")
    try:
        url = "https://open.feishu.cn/open-apis/drive/v1/files/root"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                print(f"  ✅ 云盘访问成功")
                root_info = data.get("data", {})
                print(f"  根目录ID: {root_info.get('token', '未知')}")
            else:
                print(f"  ❌ 云盘API错误: {data.get('msg', '未知错误')}")
        elif response.status_code == 403:
            print(f"  ❌ 权限不足，需要 drive 相关权限")
        else:
            print(f"  ❓ 未知状态: {response.text}")
            
    except Exception as e:
        print(f"  异常: {str(e)}")
    
    return True

def main():
    """主函数"""
    print("验证飞书应用状态")
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
        print("❌ 无法获取访问令牌，验证终止")
        return
    
    # 2. 验证应用状态
    verify_app_status(access_token, app_id)
    
    # 3. 总结和建议
    print(f"\n" + "=" * 60)
    print("📋 验证完成！")
    print("\n💡 问题分析和建议:")
    print("1. 如果基础认证成功但其他API失败，说明权限配置不足")
    print("2. 如果所有API都失败，可能应用ID或App Secret有误")
    print("3. 建议在飞书开放平台检查:")
    print("   - 应用是否已发布")
    print("   - 权限是否已申请并审核通过")
    print("   - 应用是否在正确的租户下")
    print("4. 权限申请建议:")
    print("   - 搜索 'bitable' 申请多维表格权限")
    print("   - 搜索 'drive' 申请云盘权限")
    
    return 0

if __name__ == "__main__":
    main()
