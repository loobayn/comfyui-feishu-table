#!/usr/bin/env python3
"""
测试所有飞书节点是否能正确使用配置节点
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config_node():
    """测试配置节点"""
    print("=== 测试配置节点 ===")
    try:
        from feishu_config_node import FeishuConfigNode
        
        config_node = FeishuConfigNode()
        config = config_node.create_config(
            'test_id', 
            'test_secret', 
            'https://test.feishu.cn/base/APP123?table=TABLE456'
        )[0]
        
        print(f"✅ 配置节点测试通过")
        print(f"   配置信息: {config}")
        return config
        
    except Exception as e:
        print(f"❌ 配置节点测试失败: {e}")
        return None

def test_table_node(config):
    """测试表格读取节点"""
    print("\n=== 测试表格读取节点 ===")
    try:
        from feishu_table_node import FeishuTableNode
        
        table_node = FeishuTableNode()
        
        # 测试输入类型
        input_types = table_node.INPUT_TYPES()
        if 'feishu_config' in input_types['required']:
            print(f"✅ 表格节点输入类型正确，包含feishu_config")
        else:
            print(f"❌ 表格节点输入类型错误，缺少feishu_config")
            return False
        
        # 测试函数签名
        import inspect
        sig = inspect.signature(table_node.get_table_data)
        if 'feishu_config' in sig.parameters:
            print(f"✅ 表格节点函数签名正确，接受feishu_config参数")
        else:
            print(f"❌ 表格节点函数签名错误，不接受feishu_config参数")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 表格节点测试失败: {e}")
        return False

def test_write_node(config):
    """测试表格写入节点"""
    print("\n=== 测试表格写入节点 ===")
    try:
        from feishu_write_node import FeishuWriteNode
        
        write_node = FeishuWriteNode()
        
        # 测试输入类型
        input_types = write_node.INPUT_TYPES()
        if 'feishu_config' in input_types['required']:
            print(f"✅ 写入节点输入类型正确，包含feishu_config")
        else:
            print(f"❌ 写入节点输入类型错误，缺少feishu_config")
            return False
        
        # 测试函数签名
        import inspect
        sig = inspect.signature(write_node.write_to_table)
        if 'feishu_config' in sig.parameters:
            print(f"✅ 写入节点函数签名正确，接受feishu_config参数")
        else:
            print(f"❌ 写入节点函数签名错误，不接受feishu_config参数")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 写入节点测试失败: {e}")
        return False

def test_upload_node(config):
    """测试图片上传节点"""
    print("\n=== 测试图片上传节点 ===")
    try:
        from feishu_upload_node import FeishuUploadNode
        
        upload_node = FeishuUploadNode()
        
        # 测试输入类型
        input_types = upload_node.INPUT_TYPES()
        if 'feishu_config' in input_types['required']:
            print(f"✅ 上传节点输入类型正确，包含feishu_config")
        else:
            print(f"❌ 上传节点输入类型错误，缺少feishu_config")
            return False
        
        # 测试函数签名
        import inspect
        sig = inspect.signature(upload_node.upload_to_table)
        if 'feishu_config' in sig.parameters:
            print(f"✅ 上传节点函数签名正确，接受feishu_config参数")
        else:
            print(f"❌ 上传节点函数签名错误，不接受feishu_config参数")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 上传节点测试失败: {e}")
        return False

def test_fetch_image_node(config):
    """测试图片获取节点"""
    print("\n=== 测试图片获取节点 ===")
    try:
        from feishu_fetch_image_node import FeishuFetchImageNode
        
        fetch_node = FeishuFetchImageNode()
        
        # 测试输入类型
        input_types = fetch_node.INPUT_TYPES()
        if 'feishu_config' in input_types['required']:
            print(f"✅ 获取图片节点输入类型正确，包含feishu_config")
        else:
            print(f"❌ 获取图片节点输入类型错误，缺少feishu_config")
            return False
        
        # 测试函数签名
        import inspect
        sig = inspect.signature(fetch_node.fetch_images)
        if 'feishu_config' in sig.parameters:
            print(f"✅ 获取图片节点函数签名正确，接受feishu_config参数")
        else:
            print(f"❌ 获取图片节点函数签名错误，不接受feishu_config参数")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 获取图片节点测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("飞书多维表格插件 - 配置节点集成测试")
    print("=" * 60)
    
    # 测试配置节点
    config = test_config_node()
    if not config:
        print("❌ 配置节点测试失败，无法继续")
        return
    
    # 测试所有其他节点
    results = []
    results.append(test_table_node(config))
    results.append(test_write_node(config))
    results.append(test_upload_node(config))
    results.append(test_fetch_image_node(config))
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("测试总结:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有测试通过！({passed}/{total})")
        print("🎉 配置节点集成成功，所有飞书节点都可以使用配置节点了！")
    else:
        print(f"❌ 部分测试失败 ({passed}/{total})")
        print("请检查失败的节点配置")
    
    print("\n使用方法:")
    print("1. 在ComfyUI中添加'飞书配置节点'")
    print("2. 填写App ID、App Secret和表格链接")
    print("3. 将配置节点的输出连接到其他飞书节点")
    print("4. 其他节点会自动使用配置中的认证信息")

if __name__ == "__main__":
    main()

