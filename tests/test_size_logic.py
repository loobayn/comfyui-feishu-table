#!/usr/bin/env python3
"""
测试图片尺寸处理逻辑（不依赖真实API）
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

def test_original_size_handling():
    """测试保持原始尺寸的处理"""
    print("=== 测试保持原始尺寸 ===")
    
    images = create_test_images()
    
    # 真正保持原始尺寸，不进行任何缩放
    batch = []
    for img in images:
        # 直接转换原始图片，不缩放
        arr = np.asarray(img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr)
        batch.append(tensor)
    
    # 返回包含所有图片信息的格式
    result = {
        "images": batch,
        "original_sizes": [(img.width, img.height) for img in images],
        "keep_original_size": True
    }
    
    print(f"返回类型: {type(result)}")
    print(f"图片数量: {len(result['images'])}")
    print("各图片尺寸:")
    for i, (img, size) in enumerate(zip(result['images'], result['original_sizes'])):
        print(f"  图片{i+1}: 原始尺寸 {size[0]}x{size[1]} -> Tensor形状: {img.shape}")
    
    return result

def test_unified_size_handling():
    """测试统一尺寸的处理"""
    print("\n=== 测试统一尺寸 ===")
    
    images = create_test_images()
    
    # 统一到最大尺寸，填充黑色背景
    max_w = max(img.width for img in images)
    max_h = max(img.height for img in images)
    
    print(f"最大尺寸: {max_w}x{max_h}")
    
    batch = []
    for img in images:
        canvas = Image.new('RGB', (max_w, max_h), (0, 0, 0))
        canvas.paste(img, (0, 0))
        arr = np.asarray(canvas).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr)
        batch.append(tensor)
    
    result = torch.stack(batch, dim=0)
    
    print(f"返回类型: {type(result)}")
    print(f"批次形状: {result.shape}")
    print("各图片尺寸:")
    for i, tensor in enumerate(result):
        print(f"  图片{i+1}: {tensor.shape[1]}x{tensor.shape[0]}")
    
    return result

def test_comfyui_compatibility():
    """测试ComfyUI兼容性"""
    print("\n=== 测试ComfyUI兼容性 ===")
    
    # 测试保持原始尺寸的情况
    original_result = test_original_size_handling()
    
    print("\nComfyUI兼容性分析:")
    print("1. 保持原始尺寸模式:")
    print("   - 返回类型: dict (包含图片列表和尺寸信息)")
    print("   - 每张图片保持原始尺寸")
    print("   - 需要ComfyUI特殊处理来支持不同尺寸的图片")
    
    # 测试统一尺寸的情况
    unified_result = test_unified_size_handling()
    
    print("\n2. 统一尺寸模式:")
    print("   - 返回类型: torch.Tensor")
    print("   - 所有图片统一尺寸，兼容ComfyUI")
    print("   - 图片可能被拉伸或填充")

def main():
    print("图片尺寸处理逻辑测试")
    print("=" * 60)
    
    # 测试保持原始尺寸
    original_result = test_original_size_handling()
    
    # 测试统一尺寸
    unified_result = test_unified_size_handling()
    
    # 测试ComfyUI兼容性
    test_comfyui_compatibility()
    
    print("\n" + "=" * 60)
    print("测试总结:")
    print("✅ 保持原始尺寸: 每张图片保持原始尺寸，返回字典格式")
    print("✅ 统一尺寸: 所有图片统一到最大尺寸，返回tensor格式")
    print("⚠️  注意: 保持原始尺寸模式需要ComfyUI特殊支持")

if __name__ == "__main__":
    main()
