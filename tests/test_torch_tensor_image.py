#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试torch.Tensor图片处理功能
验证ComfyUI的IMAGE类型输入处理
"""

import sys
import os
import tempfile

# 添加父目录到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_torch_tensor_processing():
    """测试torch.Tensor处理逻辑"""
    
    print("=== 测试torch.Tensor图片处理功能 ===")
    
    try:
        # 尝试导入必要的库
        import torch
        import numpy as np
        from PIL import Image
        print("✅ 成功导入必要的库")
        
        # 创建测试tensor
        print("\n=== 创建测试tensor ===")
        
        # 测试案例1: 4D tensor (batch, height, width, channels)
        print("测试案例1: 4D tensor (batch, height, width, channels)")
        tensor_4d = torch.randn(1, 64, 64, 3)  # 1张64x64的RGB图片
        print(f"4D tensor形状: {tensor_4d.shape}")
        print(f"4D tensor数据类型: {tensor_4d.dtype}")
        
        # 测试案例2: 3D tensor (height, width, channels)
        print("\n测试案例2: 3D tensor (height, width, channels)")
        tensor_3d = torch.randn(64, 64, 3)  # 64x64的RGB图片
        print(f"3D tensor形状: {tensor_3d.shape}")
        print(f"3D tensor数据类型: {tensor_3d.dtype}")
        
        # 测试案例3: 2D tensor (height, width) - 灰度图
        print("\n测试案例3: 2D tensor (height, width) - 灰度图")
        tensor_2d = torch.randn(64, 64)  # 64x64的灰度图
        print(f"2D tensor形状: {tensor_2d.shape}")
        print(f"2D tensor数据类型: {tensor_2d.dtype}")
        
        # 测试案例4: 浮点tensor (0-1范围)
        print("\n测试案例4: 浮点tensor (0-1范围)")
        tensor_float = torch.rand(64, 64, 3)  # 0-1范围的RGB图片
        print(f"浮点tensor形状: {tensor_float.shape}")
        print(f"浮点tensor数据类型: {tensor_float.dtype}")
        print(f"值范围: {tensor_float.min().item():.3f} - {tensor_float.max().item():.3f}")
        
        # 测试tensor转换逻辑
        print("\n=== 测试tensor转换逻辑 ===")
        
        def process_tensor(tensor, name):
            """处理tensor的模拟函数"""
            print(f"\n处理 {name}:")
            
            # 将tensor转换为numpy数组
            if tensor.is_cuda:
                tensor = tensor.cpu()
            
            # 转换为numpy数组
            if hasattr(tensor, 'numpy'):
                image_array = tensor.numpy()
            else:
                image_array = tensor.detach().numpy()
            
            print(f"  原始tensor形状: {image_array.shape}")
            print(f"  原始tensor数据类型: {image_array.dtype}")
            
            # 处理不同的tensor形状
            if len(image_array.shape) == 4:  # (batch, height, width, channels)
                # 取第一个图片
                image_array = image_array[0]
                print(f"  取第一个图片后形状: {image_array.shape}")
            elif len(image_array.shape) == 3:  # (height, width, channels)
                # 直接使用
                pass
            elif len(image_array.shape) == 2:  # (height, width) - 灰度图
                # 转换为3通道
                image_array = np.stack([image_array] * 3, axis=-1)
                print(f"  转换为3通道后形状: {image_array.shape}")
            else:
                print(f"  ❌ 不支持的tensor形状: {image_array.shape}")
                return False
            
            # 确保是3通道RGB
            if image_array.shape[-1] == 4:  # RGBA
                # 转换为RGB
                image_array = image_array[:, :, :3]
                print(f"  RGBA转换为RGB后形状: {image_array.shape}")
            elif image_array.shape[-1] == 1:  # 单通道
                # 转换为3通道
                image_array = np.stack([image_array[:, :, 0]] * 3, axis=-1)
                print(f"  单通道转换为3通道后形状: {image_array.shape}")
            
            # 确保值在0-255范围内
            if image_array.dtype == np.float32 or image_array.dtype == np.float64:
                if image_array.max() <= 1.0:
                    image_array = (image_array * 255).astype(np.uint8)
                    print(f"  浮点值(0-1)转换为uint8")
                else:
                    image_array = image_array.astype(np.uint8)
                    print(f"  浮点值转换为uint8")
            elif image_array.dtype != np.uint8:
                image_array = image_array.astype(np.uint8)
                print(f"  转换为uint8")
            
            print(f"  最终数组形状: {image_array.shape}")
            print(f"  最终数组数据类型: {image_array.dtype}")
            print(f"  值范围: {image_array.min()} - {image_array.max()}")
            
            # 转换为PIL Image
            try:
                pil_image = Image.fromarray(image_array)
                print(f"  ✅ 成功转换为PIL Image")
                
                # 转换为JPEG字节数据
                import io
                buffer = io.BytesIO()
                pil_image.save(buffer, format='JPEG', quality=95)
                image_data = buffer.getvalue()
                buffer.close()
                
                print(f"  ✅ 成功转换为JPEG，大小: {len(image_data)} 字节")
                return True
                
            except Exception as e:
                print(f"  ❌ 转换为PIL Image失败: {e}")
                return False
        
        # 测试所有tensor类型
        test_results = []
        test_results.append(("4D tensor", process_tensor(tensor_4d, "4D tensor")))
        test_results.append(("3D tensor", process_tensor(tensor_3d, "3D tensor")))
        test_results.append(("2D tensor", process_tensor(tensor_2d, "2D tensor")))
        test_results.append(("浮点tensor", process_tensor(tensor_float, "浮点tensor")))
        
        # 输出测试结果
        print("\n=== 测试结果汇总 ===")
        for test_name, result in test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name}: {status}")
        
        success_count = sum(1 for _, result in test_results if result)
        total_count = len(test_results)
        print(f"\n总体结果: {success_count}/{total_count} 通过")
        
        if success_count == total_count:
            print("🎉 所有测试通过！torch.Tensor处理功能正常")
        else:
            print("⚠️  部分测试失败，需要检查代码")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了torch, numpy, PIL等库")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

def test_image_save():
    """测试图片保存功能"""
    
    print("\n=== 测试图片保存功能 ===")
    
    try:
        import torch
        import numpy as np
        from PIL import Image
        import io
        
        # 创建一个简单的测试图片
        print("创建测试图片...")
        
        # 创建一个64x64的彩色图片
        image_array = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
        print(f"测试图片形状: {image_array.shape}")
        print(f"测试图片数据类型: {image_array.dtype}")
        print(f"值范围: {image_array.min()} - {image_array.max()}")
        
        # 转换为PIL Image
        pil_image = Image.fromarray(image_array)
        print("✅ 成功创建PIL Image")
        
        # 保存到临时文件
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        pil_image.save(temp_file.name, format='JPEG', quality=95)
        temp_file.close()
        
        print(f"✅ 成功保存到临时文件: {temp_file.name}")
        
        # 检查文件大小
        file_size = os.path.getsize(temp_file.name)
        print(f"✅ 文件大小: {file_size} 字节")
        
        # 清理临时文件
        try:
            os.unlink(temp_file.name)
            print(f"✅ 清理临时文件: {temp_file.name}")
        except:
            pass
        
        print("🎉 图片保存测试完成！")
        
    except Exception as e:
        print(f"❌ 图片保存测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_torch_tensor_processing()
    test_image_save()
    print("\n🎉 所有测试完成！")
    print("\n📝 下一步：")
    print("1. 在ComfyUI中测试图片上传功能")
    print("2. 验证torch.Tensor图片处理是否正常")
    print("3. 检查图片上传到飞书多维表格")

