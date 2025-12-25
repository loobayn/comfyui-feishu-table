#!/usr/bin/env python3
"""
检查表格字段
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

def check_table_fields(access_token, app_id, table_id):
    """检查表格字段"""
    print(f"🔍 检查表格 {table_id} 的字段...")
    
    # 获取表格字段
    fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(fields_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            fields = data.get("data", {}).get("items", [])
            print(f"✅ 找到 {len(fields)} 个字段")
            
            for i, field in enumerate(fields):
                field_id = field.get('field_id')
                field_name = field.get('field_name', 'Unknown')
                field_type = field.get('type', 'Unknown')
                print(f"  {i+1}. {field_name} ({field_type}) - ID: {field_id}")
                
                # 检查是否为附件字段
                if field_type == 'image' or field_type == 'attachment':
                    print(f"      🖼️  这是附件字段!")
                
            return fields
        else:
            print(f"❌ 获取字段失败: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return []

def check_table_records(access_token, app_id, table_id):
    """检查表格记录"""
    print(f"\n🔍 检查表格 {table_id} 的记录...")
    
    records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(records_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("data", {}).get("items", [])
            print(f"✅ 找到 {len(records)} 条记录")
            
            if records:
                first_record = records[0]
                fields = first_record.get('fields', {})
                print(f"📋 第一条记录的字段:")
                
                for field_name, field_data in fields.items():
                    field_type = type(field_data).__name__
                    if isinstance(field_data, dict):
                        field_type = f"dict({field_data.get('type', 'unknown')})"
                    print(f"    {field_name}: {field_type} - {field_data}")
            
            return records
        else:
            print(f"❌ 获取记录失败: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return []

def main():
    """主函数"""
    print("检查表格字段")
    print("=" * 60)
    
    # 配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "xvplUXRwDzCmeYoPMlv7if23MB2lQIzu"
    target_app_id = "CSPQbCY1OazvLnsxgWicjW0hnYd"
    target_table_id = "tblPlnQ7x0dYGWC8"
    
    print(f"📋 配置信息:")
    print(f"   App ID: {app_id}")
    print(f"   App Secret: {app_secret[:10]}...")
    print(f"   目标应用: {target_app_id}")
    print(f"   目标表格: {target_table_id}")
    
    # 1. 获取访问令牌
    print(f"\n🔑 获取访问令牌...")
    access_token = get_access_token(app_id, app_secret)
    if not access_token:
        print("❌ 无法获取访问令牌，测试终止")
        return
    
    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
    
    # 2. 检查表格字段
    fields = check_table_fields(access_token, target_app_id, target_table_id)
    
    # 3. 检查表格记录
    records = check_table_records(access_token, target_app_id, target_table_id)
    
    # 4. 总结
    if fields:
        print(f"\n📝 字段总结:")
        attachment_fields = [f for f in fields if f.get('type') in ['image', 'attachment']]
        if attachment_fields:
            print(f"✅ 找到附件字段: {[f.get('field_name') for f in attachment_fields]}")
            print(f"💡 请在节点中使用这些字段名作为目标列")
        else:
            print(f"❌ 未找到附件字段")
            print(f"💡 需要创建附件类型的字段")
    
    return 0

if __name__ == "__main__":
    main()

