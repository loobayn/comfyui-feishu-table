#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的图片处理功能
验证torch.Tensor类型的处理是否正确
"""

import sys
import os
import tempfile

# 添加父目录到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_video_upload_node import FeishuVideoUploadNode

def test_torch_tensor_processing():
    """测试torch.Tensor类型的图片处理"""
    
    print("=== 测试torch.Tensor图片处理 ===")
    
    try:
        # 尝试导入torch
        import torch
        import numpy as np
        print("✅ 成功导入torch和numpy")
    except ImportError as e:
        print(f"❌ 无法导入torch: {e}")
        print("请确保已安装torch库")
        return
    
    node = FeishuVideoUploadNode()
    
    # 创建测试用的torch.Tensor
    print("\n--- 创建测试torch.Tensor ---")
    
    # 测试案例1: 3D RGB tensor (height, width, channels)
    print("测试案例1: 3D RGB tensor")
    rgb_tensor = torch.randn(512, 512, 3)  # 模拟RGB图像
    rgb_tensor = torch.clamp(rgb_tensor, 0, 1)  # 限制在0-1范围
    print(f"RGB tensor形状: {rgb_tensor.shape}")
    print(f"RGB tensor数据类型: {rgb_tensor.dtype}")
    print(f"RGB tensor值范围: {rgb_tensor.min().item():.3f} - {rgb_tensor.max().item():.3f}")
    
    # 测试案例2: 4D batch tensor (batch, height, width, channels)
    print("\n测试案例2: 4D batch tensor")
    batch_tensor = torch.randn(2, 256, 256, 3)  # 模拟batch图像
    batch_tensor = torch.clamp(batch_tensor, 0, 1)
    print(f"Batch tensor形状: {batch_tensor.shape}")
    print(f"Batch tensor数据类型: {batch_tensor.dtype}")
    
    # 测试案例3: 2D grayscale tensor (height, width)
    print("\n测试案例3: 2D grayscale tensor")
    gray_tensor = torch.randn(128, 128)  # 模拟灰度图像
    gray_tensor = torch.clamp(gray_tensor, 0, 1)
    print(f"Grayscale tensor形状: {gray_tensor.shape}")
    print(f"Grayscale tensor数据类型: {gray_tensor.dtype}")
    
    # 测试案例4: RGBA tensor (height, width, 4)
    print("\n测试案例4: RGBA tensor")
    rgba_tensor = torch.randn(64, 64, 4)  # 模拟RGBA图像
    rgba_tensor = torch.clamp(rgba_tensor, 0, 1)
    print(f"RGBA tensor形状: {rgba_tensor.shape}")
    print(f"RGBA tensor数据类型: {rgba_tensor.dtype}")
    
    # 测试图片处理逻辑
    print("\n--- 测试图片处理逻辑 ---")
    
    test_cases = [
        ("RGB tensor", rgb_tensor),
        ("Batch tensor", batch_tensor),
        ("Grayscale tensor", gray_tensor),
        ("RGBA tensor", rgba_tensor),
    ]
    
    for case_name, test_tensor in test_cases:
        print(f"\n处理: {case_name}")
        try:
            # 检查是否有numpy方法
            if hasattr(test_tensor, 'numpy') and callable(test_tensor.numpy):
                print(f"  ✅ 检测到numpy方法")
                
                # 转换为numpy数组
                if hasattr(test_tensor, 'is_cuda') and test_tensor.is_cuda:
                    test_tensor = test_tensor.cpu()
                    print(f"  ✅ 已移动到CPU")
                
                numpy_array = test_tensor.numpy()
                print(f"  ✅ 转换为numpy数组，形状: {numpy_array.shape}")
                
                # 处理不同的tensor形状
                if len(numpy_array.shape) == 4:  # (batch, height, width, channels)
                    numpy_array = numpy_array[0]  # 取第一个batch
                    print(f"  ✅ 取第一个batch，新形状: {numpy_array.shape}")
                elif len(numpy_array.shape) == 3:  # (height, width, channels)
                    pass  # 直接使用
                elif len(numpy_array.shape) == 2:  # (height, width) - 灰度图
                    numpy_array = np.stack([numpy_array] * 3, axis=-1)  # 转换为RGB
                    print(f"  ✅ 转换为RGB，新形状: {numpy_array.shape}")
                
                # 确保是3通道RGB
                if numpy_array.shape[-1] == 4:  # RGBA
                    numpy_array = numpy_array[:, :, :3]  # 转换为RGB
                    print(f"  ✅ 转换为RGB，新形状: {numpy_array.shape}")
                elif numpy_array.shape[-1] == 1:  # 单通道
                    numpy_array = np.stack([numpy_array[:, :, 0]] * 3, axis=-1)  # 转换为3通道
                    print(f"  ✅ 转换为3通道，新形状: {numpy_array.shape}")
                
                # 确保值在0-255范围内
                if numpy_array.dtype == np.float32 or numpy_array.dtype == np.float64:
                    if numpy_array.max() <= 1.0:
                        numpy_array = (numpy_array * 255).astype(np.uint8)
                        print(f"  ✅ 值范围从0-1转换为0-255")
                    else:
                        numpy_array = numpy_array.astype(np.uint8)
                        print(f"  ✅ 值范围已转换为0-255")
                elif numpy_array.dtype != np.uint8:
                    numpy_array = numpy_array.astype(np.uint8)
                    print(f"  ✅ 数据类型转换为uint8")
                
                print(f"  ✅ 最终数组形状: {numpy_array.shape}")
                print(f"  ✅ 最终数据类型: {numpy_array.dtype}")
                print(f"  ✅ 值范围: {numpy_array.min()} - {numpy_array.max()}")
                
                # 模拟转换为PIL Image和字节数据
                try:
                    from PIL import Image
                    pil_image = Image.fromarray(numpy_array)
                    print(f"  ✅ 成功创建PIL Image，模式: {pil_image.mode}")
                    
                    # 模拟保存为JPEG
                    import io
                    buffer = io.BytesIO()
                    pil_image.save(buffer, format='JPEG', quality=95)
                    image_bytes = buffer.getvalue()
                    buffer.close()
                    print(f"  ✅ 成功转换为JPEG字节数据，大小: {len(image_bytes)} 字节")
                    
                except Exception as e:
                    print(f"  ❌ PIL转换失败: {e}")
                
            else:
                print(f"  ❌ 没有numpy方法")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n=== 测试完成 ===")

def test_process_image_data_method():
    """测试process_image_data方法"""
    
    print("\n=== 测试process_image_data方法 ===")
    
    try:
        import torch
        import numpy as np
        print("✅ 成功导入torch和numpy")
    except ImportError as e:
        print(f"❌ 无法导入torch: {e}")
        return
    
    node = FeishuVideoUploadNode()
    
    # 创建测试tensor
    test_tensor = torch.randn(256, 256, 3)
    test_tensor = torch.clamp(test_tensor, 0, 1)
    print(f"创建测试tensor: {test_tensor.shape}, {test_tensor.dtype}")
    
    try:
        # 调用process_image_data方法
        print("调用process_image_data方法...")
        result = node.process_image_data(test_tensor)
        
        if result[0] is not None:
            image_data, file_name = result
            print(f"✅ 处理成功！")
            print(f"  文件名: {file_name}")
            print(f"  数据大小: {len(image_data)} 字节")
        else:
            print(f"❌ 处理失败: {result[1]}")
            
    except Exception as e:
        print(f"❌ 调用方法时发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_torch_tensor_processing()
    test_process_image_data_method()
    print("\n🎉 所有测试完成！")
    print("\n📝 下一步：")
    print("1. 在ComfyUI中测试修复后的图片上传功能")
    print("2. 验证torch.Tensor类型的图片处理")
    print("3. 检查图片上传到飞书多维表格")

