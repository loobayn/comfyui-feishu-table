#!/usr/bin/env python3
"""
测试可访问的表格
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

def find_accessible_tables(access_token, app_id):
    """查找可访问的表格"""
    print(f"🔍 查找应用 {app_id} 中的表格...")
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            tables = data.get("data", {}).get("items", [])
            print(f"✅ 找到 {len(tables)} 个表格")
            
            for i, table in enumerate(tables):
                table_id = table.get('table_id')
                table_name = table.get('name', 'Unknown')
                print(f"  {i+1}. {table_name} ({table_id})")
                
                # 测试访问该表格
                test_table_access(access_token, app_id, table_id)
                
            return tables
        else:
            print(f"❌ 获取表格列表失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  错误代码: {error_data.get('code')}")
                print(f"  错误信息: {error_data.get('msg')}")
            except:
                print(f"  错误响应: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return []

def test_table_access(access_token, app_id, table_id):
    """测试表格访问权限"""
    print(f"    🔍 测试访问表格 {table_id}...")
    
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
            print(f"      ✅ 成功访问! 记录数量: {len(records)}")
            
            # 显示字段信息
            if records:
                first_record = records[0]
                fields = first_record.get('fields', {})
                print(f"      📋 字段列表: {list(fields.keys())}")
                
                # 查找附件字段
                attachment_fields = []
                for field_name, field_data in fields.items():
                    if isinstance(field_data, dict) and field_data.get('type') == 'image':
                        attachment_fields.append(field_name)
                
                if attachment_fields:
                    print(f"      🖼️  附件字段: {attachment_fields}")
                else:
                    print(f"      📝 无附件字段")
            
            return True
        else:
            print(f"      ❌ 访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"      ❌ 请求异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("查找可访问的表格")
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
    
    # 2. 查找可访问的表格
    print(f"\n🔍 查找可访问的表格...")
    tables = find_accessible_tables(access_token, app_id)
    
    if tables:
        print(f"\n✅ 找到 {len(tables)} 个可访问的表格")
        print(f"💡 您可以使用这些表格来测试节点功能")
        
        # 显示使用建议
        print(f"\n📝 使用建议:")
        print(f"   1. 选择一个有附件字段的表格")
        print(f"   2. 复制表格链接")
        print(f"   3. 在节点中使用该链接")
        print(f"   4. 设置目标列为附件字段名")
        
    else:
        print(f"\n❌ 未找到可访问的表格")
        print(f"💡 请检查:")
        print(f"   1. 应用权限配置")
        print(f"   2. 是否有创建的多维表格")
        print(f"   3. 或者为现有表格添加权限")
    
    return 0

if __name__ == "__main__":
    main()

