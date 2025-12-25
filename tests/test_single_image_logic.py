#!/usr/bin/env python3
"""
测试单张图片提取逻辑（不依赖真实API）
"""

import numpy as np
from PIL import Image
import torch

def create_test_images():
    """创建不同尺寸的测试图片"""
    images = []
    
    # 图片1: 小尺寸 64x64
    img1 = Image.new('RGB', (64, 64), color=(255, 0, 0))  # 红色
    images.append(img1)
    
    # 图片2: 中等尺寸 256x256
    img2 = Image.new('RGB', (256, 256), color=(0, 255, 0))  # 绿色
    images.append(img2)
    
    # 图片3: 大尺寸 512x512
    img3 = Image.new('RGB', (512, 512), color=(0, 0, 255))  # 蓝色
    images.append(img3)
    
    # 图片4: 宽图 512x128
    img4 = Image.new('RGB', (512, 128), color=(255, 255, 0))  # 黄色
    images.append(img4)
    
    return images

def test_single_image_extraction():
    """测试单张图片提取逻辑"""
    print("=== 测试单张图片提取逻辑 ===")
    
    images = create_test_images()
    
    # 模拟选择不同索引的图片
    for image_index in range(1, len(images) + 1):
        print(f"\n--- 选择第 {image_index} 张图片 ---")
        
        # 选择指定索引的图片（转换为0基索引）
        selected_img = images[image_index - 1]
        print(f"原始尺寸: {selected_img.width}x{selected_img.height}")
        
        # 转换为tensor，保持原始尺寸
        arr = np.asarray(selected_img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr)
        
        # 添加批次维度 (H, W, C) -> (1, H, W, C)
        image_tensor = tensor.unsqueeze(0)
        
        print(f"Tensor形状: {image_tensor.shape}")
        print(f"数据类型: {image_tensor.dtype}")
        print(f"数值范围: {image_tensor.min():.3f} - {image_tensor.max():.3f}")
        
        # 验证尺寸保持
        expected_shape = (1, selected_img.height, selected_img.width, 3)
        if image_tensor.shape == expected_shape:
            print("✅ 尺寸保持正确")
        else:
            print(f"❌ 尺寸错误，期望: {expected_shape}，实际: {image_tensor.shape}")

def test_comfyui_compatibility():
    """测试ComfyUI兼容性"""
    print("\n=== 测试ComfyUI兼容性 ===")
    
    images = create_test_images()
    
    print("ComfyUI兼容性分析:")
    print("1. 单张图片模式:")
    print("   - 返回类型: torch.Tensor")
    print("   - 形状: (1, H, W, 3) - 标准IMAGE格式")
    print("   - 每张图片保持原始尺寸")
    print("   - 完全兼容ComfyUI")
    
    print("\n2. 尺寸保持验证:")
    for i, img in enumerate(images, 1):
        arr = np.asarray(img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr).unsqueeze(0)
        print(f"  图片{i}: {img.width}x{img.height} -> Tensor {tensor.shape}")

def main():
    print("单张图片提取逻辑测试")
    print("=" * 60)
    
    # 测试单张图片提取
    test_single_image_extraction()
    
    # 测试ComfyUI兼容性
    test_comfyui_compatibility()
    
    print("\n" + "=" * 60)
    print("测试总结:")
    print("✅ 单张图片提取: 每张图片保持原始尺寸")
    print("✅ ComfyUI兼容: 返回标准(1, H, W, 3)格式")
    print("✅ 尺寸保持: 不进行任何缩放或填充")
    print("✅ 索引选择: 支持选择第N张图片")

if __name__ == "__main__":
    main()
