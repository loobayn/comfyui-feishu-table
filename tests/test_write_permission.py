#!/usr/bin/env python3
"""
测试写入权限需求
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

def test_write_permission(access_token, app_id):
    """测试写入权限"""
    print(f"🔍 测试写入权限...")
    
    # 先尝试获取表格列表
    print(f"\n1️⃣ 获取表格列表...")
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
                print(f"  ✅ 成功获取表格列表，找到 {len(tables)} 个表格")
                
                if tables:
                    # 使用第一个表格测试写入
                    table_id = tables[0]["table_id"]
                    table_name = tables[0].get("name", "未命名")
                    print(f"  使用表格: {table_name} (ID: {table_id})")
                    
                    # 测试写入权限
                    print(f"\n2️⃣ 测试写入权限...")
                    test_data = {
                        "fields": {
                            "测试字段": "测试值"
                        }
                    }
                    
                    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
                    response = requests.post(url, json=test_data, headers=headers, timeout=30)
                    print(f"  创建记录状态码: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("code") == 0:
                            print(f"  ✅ 写入权限正常！成功创建测试记录")
                            record_id = result.get("data", {}).get("record_id")
                            
                            # 删除测试记录
                            print(f"\n3️⃣ 删除测试记录...")
                            delete_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records/{record_id}"
                            delete_response = requests.delete(delete_url, headers=headers, timeout=30)
                            print(f"  删除记录状态码: {delete_response.status_code}")
                            
                            if delete_response.status_code == 200:
                                print(f"  ✅ 删除权限正常！测试记录已清理")
                            else:
                                print(f"  ❌ 删除权限异常: {delete_response.text}")
                            
                            return True
                        else:
                            print(f"  ❌ 写入失败: {result.get('msg', '未知错误')}")
                            return False
                    elif response.status_code == 403:
                        print(f"  ❌ 权限不足，需要 bitable:app:write 权限")
                        print(f"  错误详情: {response.text}")
                        return False
                    else:
                        print(f"  ❌ 其他错误: {response.text}")
                        return False
                else:
                    print(f"  ❌ 没有找到可用的表格")
                    return False
            else:
                print(f"  ❌ 获取表格列表失败: {data.get('msg', '未知错误')}")
                return False
        else:
            print(f"  ❌ 获取表格列表失败，状态码: {response.status_code}")
            print(f"  错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"  异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("测试写入权限需求")
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
        print("❌ 无法获取访问令牌，测试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 测试写入权限
    success = test_write_permission(access_token, app_id)
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 写入权限测试成功！")
        print("\n💡 当前状态:")
        print("✅ 读取权限正常")
        print("✅ 写入权限正常")
        print("❌ 图片上传权限未知（需要 drive 相关权限）")
        
        print(f"\n🔧 建议:")
        print("1. 读取和写入功能都可以正常使用")
        print("2. 只需要配置 drive 相关权限即可使用图片上传功能")
    else:
        print("❌ 写入权限测试失败")
        print("\n🔍 问题分析:")
        print("1. 可能需要 bitable:app:write 权限")
        print("2. 或者表格不存在/无权限访问")
        print("3. 建议检查表格状态和权限配置")
    
    return 0

if __name__ == "__main__":
    main()
