#!/usr/bin/env python3
"""
验证添加行是否真的成功
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

def check_table_records(access_token, app_id, table_id):
    """检查表格记录"""
    print(f"🔍 检查表格 {table_id} 的记录...")
    
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
            
            for i, record in enumerate(records):
                record_id = record.get('record_id')
                fields = record.get('fields', {})
                print(f"  记录 {i+1}: {record_id}")
                
                # 检查每个字段
                for field_name, field_data in fields.items():
                    if isinstance(field_data, list) and len(field_data) > 0:
                        if isinstance(field_data[0], dict) and field_data[0].get('type') == 'image':
                            print(f"    🖼️  {field_name}: 图片附件 ({len(field_data)} 个)")
                            for j, attachment in enumerate(field_data):
                                print(f"      附件 {j+1}: {attachment.get('type')} - {attachment.get('token', 'N/A')}")
                        else:
                            print(f"    📝  {field_name}: {field_data}")
                    else:
                        print(f"    📝  {field_name}: {field_data}")
            
            return records
        else:
            print(f"❌ 获取记录失败: {response.status_code}")
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

def test_add_row_with_image(access_token, app_id, table_id):
    """测试添加行并包含图片"""
    print(f"🔍 测试添加行并包含图片...")
    
    # 创建测试图片数据（模拟）
    image_data = [{
        "type": "image",
        "token": "test_token_12345"
    }]
    
    # 创建新记录
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "生成图片": image_data
        }
    }
    
    print(f"  请求URL: {url}")
    print(f"  请求载荷: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"  响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 行添加成功!")
            print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查是否真的添加了记录
            print(f"\n🔍 验证记录是否真的添加...")
            records_after = check_table_records(access_token, app_id, table_id)
            
            return True
        else:
            print(f"  ❌ 行添加失败!")
            try:
                error_data = response.json()
                error_code = error_data.get('code')
                error_msg = error_data.get('msg')
                print(f"  错误代码: {error_code}")
                print(f"  错误信息: {error_msg}")
                
                # 显示错误含义
                error_meanings = {
                    "1254045": "字段名不存在 - 指定的字段在表格中不存在",
                    "1254069": "附件字段转换失败 - 附件数据格式不正确",
                    "91402": "资源不存在 - 指定的表格或记录不存在"
                }
                if error_code in error_meanings:
                    print(f"  错误含义: {error_meanings[error_code]}")
                
            except:
                print(f"  错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("验证添加行是否真的成功")
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
    
    # 2. 检查添加前的记录
    print(f"\n🔍 检查添加前的记录...")
    records_before = check_table_records(access_token, target_app_id, target_table_id)
    
    # 3. 测试添加行
    print(f"\n🚀 测试添加行...")
    success = test_add_row_with_image(access_token, target_app_id, target_table_id)
    
    if success:
        print(f"\n✅ 添加行测试完成!")
        print(f"💡 请检查飞书表格是否显示了新行")
    else:
        print(f"\n❌ 添加行测试失败")
    
    return 0

if __name__ == "__main__":
    main()

