#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试ComfyUI中VIDEO类型的结构
分析VIDEO类型输入的实际属性和方法
"""

import sys
import os

# 添加父目录到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def analyze_video_type_structure():
    """分析VIDEO类型的结构"""
    
    print("=== 分析ComfyUI中VIDEO类型的结构 ===")
    
    # 模拟不同类型的视频输入
    test_cases = [
        # 模拟文件对象
        type('MockFile', (), {
            'read': lambda: b'file_content',
            'name': 'test.mp4',
            'filename': '/path/to/test.mp4'
        })(),
        
        # 模拟有filename属性的对象
        type('MockVideo', (), {
            'filename': '/path/to/video.mp4',
            'size': 1024,
            'type': 'video/mp4'
        })(),
        
        # 模拟字节数据
        b'video_data_bytes',
        
        # 模拟文件路径字符串
        '/path/to/video.mp4',
        
        # 模拟复杂对象
        type('MockComplexVideo', (), {
            'data': b'complex_video_data',
            'metadata': {'format': 'mp4', 'duration': 10},
            'path': '/path/to/complex.mp4'
        })(),
        
        # 模拟空对象
        type('MockEmpty', (), {})(),
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- 测试案例 {i}: {type(test_input).__name__} ---")
        print(f"类型: {type(test_input)}")
        print(f"属性: {dir(test_input)}")
        
        if hasattr(test_input, '__dict__'):
            print(f"__dict__: {test_input.__dict__}")
        
        # 测试各种属性
        test_attributes = ['read', 'filename', 'name', 'path', 'data', 'size', 'type']
        for attr in test_attributes:
            if hasattr(test_input, attr):
                value = getattr(test_input, attr)
                print(f"  {attr}: {type(value)} = {value}")
        
        # 测试特殊方法
        special_methods = ['__bytes__', '__str__', '__repr__']
        for method in special_methods:
            if hasattr(test_input, method):
                try:
                    result = getattr(test_input, method)()
                    print(f"  {method}(): {type(result)} = {result}")
                except Exception as e:
                    print(f"  {method}(): 调用失败 - {e}")
        
        # 测试可调用性
        if callable(test_input):
            print(f"  可调用: 是")
            try:
                result = test_input()
                print(f"  调用结果: {type(result)} = {result}")
            except Exception as e:
                print(f"  调用失败: {e}")
        else:
            print(f"  可调用: 否")
        
        # 测试长度
        try:
            length = len(test_input)
            print(f"  长度: {length}")
        except Exception as e:
            print(f"  长度: 无法获取 - {e}")
        
        # 测试迭代
        try:
            iterable = iter(test_input)
            print(f"  可迭代: 是")
            # 尝试获取前几个元素
            items = []
            for j, item in enumerate(iterable):
                if j < 3:  # 只取前3个
                    items.append(item)
                else:
                    break
            print(f"  迭代前3项: {items}")
        except Exception as e:
            print(f"  可迭代: 否 - {e}")

def test_video_processing_logic():
    """测试视频处理逻辑"""
    
    print("\n=== 测试视频处理逻辑 ===")
    
    # 模拟一个复杂的视频对象
    class MockComfyUIVideo:
        def __init__(self):
            self.filename = "/tmp/test_video.mp4"
            self.data = b"fake_video_data" * 1000
            self.metadata = {"format": "mp4", "duration": 30}
            self.size = len(self.data)
        
        def read(self):
            return self.data
        
        def __str__(self):
            return f"MockComfyUIVideo(filename={self.filename}, size={self.size})"
    
    mock_video = MockComfyUIVideo()
    
    print(f"模拟视频对象: {mock_video}")
    print(f"类型: {type(mock_video)}")
    print(f"属性: {dir(mock_video)}")
    print(f"__dict__: {mock_video.__dict__}")
    
    # 测试各种读取方法
    print("\n测试读取方法:")
    
    # 方法1: 通过read()方法
    if hasattr(mock_video, 'read'):
        try:
            data = mock_video.read()
            print(f"  通过read()读取: {len(data)} 字节")
        except Exception as e:
            print(f"  通过read()读取失败: {e}")
    
    # 方法2: 通过filename属性
    if hasattr(mock_video, 'filename'):
        try:
            file_path = mock_video.filename
            print(f"  检测到文件路径: {file_path}")
            # 这里我们不会真正读取文件，只是模拟
            print(f"  模拟从文件路径读取: 成功")
        except Exception as e:
            print(f"  从文件路径读取失败: {e}")
    
    # 方法3: 通过data属性
    if hasattr(mock_video, 'data'):
        try:
            data = mock_video.data
            print(f"  通过data属性读取: {len(data)} 字节")
        except Exception as e:
            print(f"  通过data属性读取失败: {e}")
    
    # 方法4: 通过bytes()转换
    try:
        data = bytes(mock_video)
        print(f"  通过bytes()转换: {len(data)} 字节")
    except Exception as e:
        print(f"  通过bytes()转换失败: {e}")

if __name__ == "__main__":
    analyze_video_type_structure()
    test_video_processing_logic()
    print("\n🎉 调试分析完成！")
    print("\n💡 建议:")
    print("1. 在ComfyUI中查看VIDEO类型输出的实际结构")
    print("2. 根据实际结构调整视频处理逻辑")
    print("3. 测试不同类型的视频输入")

