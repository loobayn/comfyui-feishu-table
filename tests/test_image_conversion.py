#!/usr/bin/env python3
"""
测试图片格式转换功能
"""

import numpy as np
from PIL import Image
import io

def test_tensor_like_conversion():
    """测试类似Tensor的图片格式转换"""
    print("🔍 测试类似Tensor的图片格式转换...")
    
    # 模拟torch.Tensor格式（numpy数组）
    height, width = 64, 64
    channels = 3
    
    # 创建不同数据类型的测试图片
    test_cases = [
        {
            "name": "float32 (0-1范围)",
            "data": np.random.random((height, width, channels)).astype(np.float32),
            "description": "float32类型，值范围0-1"
        },
        {
            "name": "float32 (0-255范围)",
            "data": np.random.random((height, width, channels)).astype(np.float32) * 255,
            "description": "float32类型，值范围0-255"
        },
        {
            "name": "uint8",
            "data": np.random.randint(0, 256, (height, width, channels), dtype=np.uint8),
            "description": "uint8类型，值范围0-255"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📸 测试: {test_case['name']}")
        print(f"  描述: {test_case['description']}")
        print(f"  数据类型: {test_case['data'].dtype}")
        print(f"  数据形状: {test_case['data'].shape}")
        print(f"  值范围: {test_case['data'].min():.2f} - {test_case['data'].max():.2f}")
        
        try:
            # 模拟修复后的转换逻辑
            image_array = test_case['data']
            
            # 确保图片是3通道RGB格式
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                # 如果是float类型，转换为0-255范围
                if image_array.dtype == np.float32 or image_array.dtype == np.float64:
                    if image_array.max() <= 1.0:
                        image_array = (image_array * 255).astype(np.uint8)
                    else:
                        image_array = image_array.astype(np.uint8)
                else:
                    image_array = image_array.astype(np.uint8)
                
                pil_image = Image.fromarray(image_array)
                
                # 转换为PNG格式的bytes
                img_buffer = io.BytesIO()
                pil_image.save(img_buffer, format='PNG')
                image_bytes = img_buffer.getvalue()
                
                print(f"  ✅ 转换成功!")
                print(f"    图片尺寸: {pil_image.size}")
                print(f"    图片模式: {pil_image.mode}")
                print(f"    转换后大小: {len(image_bytes)} bytes")
                
            else:
                print(f"  ❌ 转换失败: 不支持的图片形状")
                
        except Exception as e:
            print(f"  ❌ 转换异常: {str(e)}")

def test_pil_image_conversion():
    """测试PIL.Image格式转换"""
    print(f"\n🔍 测试PIL.Image格式转换...")
    
    try:
        # 创建PIL图片
        height, width = 32, 32
        pil_image = Image.new('RGB', (width, height), color='red')
        
        print(f"  ✅ PIL图片创建成功!")
        print(f"    图片尺寸: {pil_image.size}")
        print(f"    图片模式: {pil_image.mode}")
        
        # 转换为bytes
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        
        print(f"    转换后大小: {len(image_bytes)} bytes")
        
    except Exception as e:
        print(f"  ❌ PIL图片转换异常: {str(e)}")

def test_error_cases():
    """测试错误情况"""
    print(f"\n🔍 测试错误情况...")
    
    # 测试不支持的形状
    try:
        # 2D数组（缺少通道维度）
        test_2d = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        print(f"  测试2D数组: {test_2d.shape}")
        
        if len(test_2d.shape) == 3 and test_2d.shape[2] == 3:
            print(f"  ✅ 2D数组转换成功")
        else:
            print(f"  ❌ 2D数组不支持，需要3通道RGB格式")
            
    except Exception as e:
        print(f"  2D数组测试异常: {str(e)}")
    
    # 测试4D数组
    try:
        # 4D数组（批次维度）
        test_4d = np.random.randint(0, 256, (1, 64, 64, 3), dtype=np.uint8)
        print(f"  测试4D数组: {test_4d.shape}")
        
        if len(test_4d.shape) == 3 and test_4d.shape[2] == 3:
            print(f"  ✅ 4D数组转换成功")
        else:
            print(f"  ❌ 4D数组不支持，需要3通道RGB格式")
            
    except Exception as e:
        print(f"  4D数组测试异常: {str(e)}")

def main():
    """主函数"""
    print("测试图片格式转换功能")
    print("=" * 60)
    
    # 1. 测试类似Tensor的格式转换
    test_tensor_like_conversion()
    
    # 2. 测试PIL.Image格式转换
    test_pil_image_conversion()
    
    # 3. 测试错误情况
    test_error_cases()
    
    # 4. 总结
    print(f"\n" + "=" * 60)
    print("🎯 转换功能测试完成!")
    print("\n💡 支持的格式:")
    print("✅ torch.Tensor (3通道RGB)")
    print("✅ numpy.ndarray (3通道RGB)")
    print("✅ PIL.Image")
    print("\n❌ 不支持的格式:")
    print("❌ 2D数组（缺少通道维度）")
    print("❌ 4D数组（批次维度）")
    print("❌ 非RGB格式")
    
    return 0

if __name__ == "__main__":
    main()
