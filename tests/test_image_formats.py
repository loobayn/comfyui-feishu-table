#!/usr/bin/env python3
"""
测试各种图片格式的转换功能
"""

import numpy as np
from PIL import Image
import io

def test_various_image_formats():
    """测试各种图片格式的转换"""
    print("🔍 测试各种图片格式的转换功能...")
    
    # 测试用例
    test_cases = [
        {
            "name": "4D批次 [1, H, W, C]",
            "data": np.random.randint(0, 256, (1, 64, 64, 3), dtype=np.uint8),
            "description": "4D数组，批次维度，HWC格式"
        },
        {
            "name": "4D批次 [1, C, H, W]",
            "data": np.random.randint(0, 256, (1, 3, 64, 64), dtype=np.uint8),
            "description": "4D数组，批次维度，CHW格式"
        },
        {
            "name": "3D CHW [C, H, W]",
            "data": np.random.randint(0, 256, (3, 64, 64), dtype=np.uint8),
            "description": "3D数组，CHW格式"
        },
        {
            "name": "3D HWC RGB [H, W, 3]",
            "data": np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8),
            "description": "3D数组，HWC格式，RGB"
        },
        {
            "name": "3D HWC RGBA [H, W, 4]",
            "data": np.random.randint(0, 256, (64, 64, 4), dtype=np.uint8),
            "description": "3D数组，HWC格式，RGBA"
        },
        {
            "name": "3D HWC 灰度 [H, W, 1]",
            "data": np.random.randint(0, 256, (64, 64, 1), dtype=np.uint8),
            "description": "3D数组，HWC格式，单通道"
        },
        {
            "name": "2D 灰度 [H, W]",
            "data": np.random.randint(0, 256, (64, 64), dtype=np.uint8),
            "description": "2D数组，单通道灰度图"
        },
        {
            "name": "float32 0-1范围",
            "data": np.random.random((64, 64, 3)).astype(np.float32),
            "description": "float32类型，值范围0-1"
        },
        {
            "name": "float32 0-255范围",
            "data": (np.random.random((64, 64, 3)) * 255).astype(np.float32),
            "description": "float32类型，值范围0-255"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📸 测试: {test_case['name']}")
        print(f"  描述: {test_case['description']}")
        print(f"  数据类型: {test_case['data'].dtype}")
        print(f"  数据形状: {test_case['data'].shape}")
        
        try:
            # 模拟修复后的转换逻辑
            image_data = test_case['data']
            image_array = image_data.copy() if isinstance(image_data, np.ndarray) else image_data
            pil_image = None
            
            if hasattr(image_data, 'cpu'):  # 处理torch.Tensor
                # 转换为numpy数组
                if hasattr(image_data, 'numpy'):
                    image_array = image_data.cpu().numpy()
                else:
                    image_array = image_data.cpu().detach().numpy()
                
                # 处理不同维度的图片
                if len(image_array.shape) == 4:  # [batch, H, W, C] 或 [batch, C, H, W]
                    if image_array.shape[1] == 3:  # [batch, C, H, W]
                        image_array = image_array[0].transpose(1, 2, 0)  # 取第一个批次，调整通道顺序
                    else:  # [batch, H, W, C]
                        image_array = image_array[0]  # 取第一个批次
                elif len(image_array.shape) == 3:
                    if image_array.shape[0] == 3:  # [C, H, W]
                        image_array = image_array.transpose(1, 2, 0)  # 调整通道顺序
                    elif image_array.shape[2] == 3:  # [H, W, C] - RGB
                        image_array = image_array
                    elif image_array.shape[2] == 4:  # [H, W, C] - RGBA
                        # 转换为RGB（去掉透明通道）
                        image_array = image_array[:, :, :3]
                    elif image_array.shape[2] == 1:  # [H, W, 1] - 灰度图
                        # 转换为RGB（重复3次）
                        image_array = np.repeat(image_array, 3, axis=2)
                    else:
                        print(f"  ❌ 转换失败: 不支持的通道数 {image_array.shape[2]}")
                        continue
                elif len(image_array.shape) == 2:  # [H, W] - 单通道
                    # 转换为RGB（重复3次）
                    image_array = np.expand_dims(image_array, axis=2)
                    image_array = np.repeat(image_array, 3, axis=2)
                else:
                    print(f"  ❌ 转换失败: 不支持的图片形状 {image_array.shape}")
                    continue
                
                # 数据类型转换和范围调整
                if image_array.dtype == np.float32 or image_array.dtype == np.float64:
                    if image_array.max() <= 1.0:
                        image_array = (image_array * 255).astype(np.uint8)
                    else:
                        image_array = image_array.astype(np.uint8)
                else:
                    image_array = image_array.astype(np.uint8)
                
                pil_image = Image.fromarray(image_array)
                
            elif isinstance(image_data, np.ndarray):
                # 处理numpy数组格式的图片
                image_array = image_data.copy()  # 避免修改原数组
                
                # 处理不同维度的图片
                if len(image_array.shape) == 4:  # [batch, H, W, C] 或 [batch, C, H, W]
                    if image_array.shape[1] == 3:  # [batch, C, H, W]
                        image_array = image_array[0].transpose(1, 2, 0)  # 取第一个批次，调整通道顺序
                    else:  # [batch, H, W, C]
                        image_array = image_array[0]  # 取第一个批次
                elif len(image_array.shape) == 3:
                    if image_array.shape[0] == 3:  # [C, H, W]
                        image_array = image_array.transpose(1, 2, 0)  # 调整通道顺序
                    elif image_array.shape[2] == 3:  # [H, W, C] - RGB
                        image_array = image_array
                    elif image_array.shape[2] == 4:  # [H, W, C] - RGBA
                        # 转换为RGB（去掉透明通道）
                        image_array = image_array[:, :, :3]
                    elif image_array.shape[2] == 1:  # [H, W, 1] - 灰度图
                        # 转换为RGB（重复3次）
                        image_array = np.repeat(image_array, 3, axis=2)
                    else:
                        print(f"  ❌ 转换失败: 不支持的通道数 {image_array.shape[2]}")
                        continue
                elif len(image_array.shape) == 2:  # [H, W] - 单通道
                    # 转换为RGB（重复3次）
                    image_array = np.expand_dims(image_array, axis=2)
                    image_array = np.repeat(image_array, 3, axis=2)
                else:
                    print(f"  ❌ 转换失败: 不支持的图片形状 {image_array.shape}")
                    continue
                
                # 数据类型转换和范围调整
                if image_array.dtype == np.float32 or image_array.dtype == np.float64:
                    if image_array.max() <= 1.0:
                        image_array = (image_array * 255).astype(np.uint8)
                    else:
                        image_array = image_array.astype(np.uint8)
                else:
                    image_array = image_array.astype(np.uint8)
                
                pil_image = Image.fromarray(image_array)
                
            elif hasattr(image_data, 'save'):  # 处理PIL.Image
                pil_image = image_data
                # 确保PIL图片是RGB模式
                if pil_image.mode != 'RGB':
                    if pil_image.mode == 'RGBA':
                        # 创建白色背景
                        background = Image.new('RGB', pil_image.size, (255, 255, 255))
                        background.paste(pil_image, mask=pil_image.split()[-1])  # 使用alpha通道作为mask
                        pil_image = background
                    elif pil_image.mode == 'L':  # 灰度图
                        pil_image = pil_image.convert('RGB')
                    else:
                        pil_image = pil_image.convert('RGB')
            else:
                print(f"  ❌ 不支持的图片格式: {type(image_data)}")
                continue
            
            # 转换为PNG格式的bytes
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format='PNG')
            image_bytes = img_buffer.getvalue()
            
            print(f"  ✅ 转换成功!")
            print(f"    最终形状: {image_array.shape}")
            print(f"    最终类型: {image_array.dtype}")
            print(f"    图片尺寸: {pil_image.size}")
            print(f"    图片模式: {pil_image.mode}")
            print(f"    转换后大小: {len(image_bytes)} bytes")
            
        except Exception as e:
            print(f"  ❌ 转换异常: {str(e)}")

def test_pil_formats():
    """测试PIL图片格式转换"""
    print(f"\n🔍 测试PIL图片格式转换...")
    
    # 测试RGBA图片
    try:
        rgba_image = Image.new('RGBA', (32, 32), (255, 0, 0, 128))  # 半透明红色
        print(f"  测试RGBA图片: {rgba_image.mode}")
        
        # 转换为RGB
        if rgba_image.mode != 'RGB':
            if rgba_image.mode == 'RGBA':
                # 创建白色背景
                background = Image.new('RGB', rgba_image.size, (255, 255, 255))
                background.paste(rgba_image, mask=rgba_image.split()[-1])  # 使用alpha通道作为mask
                rgb_image = background
            elif rgba_image.mode == 'L':  # 灰度图
                rgb_image = rgba_image.convert('RGB')
            else:
                rgb_image = rgba_image.convert('RGB')
        
        print(f"    ✅ RGBA转换成功: {rgba_image.mode} -> {rgb_image.mode}")
        
        # 转换为bytes
        img_buffer = io.BytesIO()
        rgb_image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        print(f"    转换后大小: {len(image_bytes)} bytes")
        
    except Exception as e:
        print(f"  ❌ RGBA转换异常: {str(e)}")
    
    # 测试灰度图片
    try:
        gray_image = Image.new('L', (32, 32), 128)  # 灰度图
        print(f"  测试灰度图片: {gray_image.mode}")
        
        # 转换为RGB
        rgb_image = gray_image.convert('RGB')
        print(f"    ✅ 灰度转换成功: {gray_image.mode} -> {rgb_image.mode}")
        
        # 转换为bytes
        img_buffer = io.BytesIO()
        rgb_image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        print(f"    转换后大小: {len(image_bytes)} bytes")
        
    except Exception as e:
        print(f"  ❌ 灰度转换异常: {str(e)}")

def main():
    """主函数"""
    print("测试各种图片格式的转换功能")
    print("=" * 60)
    
    # 1. 测试numpy数组格式
    test_various_image_formats()
    
    # 2. 测试PIL图片格式
    test_pil_formats()
    
    # 3. 总结
    print(f"\n" + "=" * 60)
    print("🎯 图片格式转换功能测试完成!")
    print("\n💡 支持的格式:")
    print("✅ 4D批次数组 [batch, H, W, C] 或 [batch, C, H, W]")
    print("✅ 3D数组 [C, H, W], [H, W, C], [H, W, 1]")
    print("✅ 2D数组 [H, W] (自动转换为RGB)")
    print("✅ float32/float64 (自动范围调整)")
    print("✅ RGBA (自动转换为RGB)")
    print("✅ 灰度图 (自动转换为RGB)")
    print("✅ PIL.Image (自动模式转换)")
    
    return 0

if __name__ == "__main__":
    main()
