#!/usr/bin/env python3
"""
飞书配置节点 - 用于存储和分发认证信息
"""

import json
from typing import Dict, Any

class FeishuConfigNode:
    """飞书配置节点，用于存储认证信息和表格配置"""
    
    def __init__(self):
        self.app_id = ""
        self.app_secret = ""
        self.table_url = ""
        self.url_app_id = ""
        self.table_id = ""
        self._parsed = False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "应用ID": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "飞书应用的App ID"
                }),
                "应用密钥": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "飞书应用的App Secret"
                }),
                "表格链接": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "飞书多维表格链接"
                })
            }
        }
    
    RETURN_TYPES = ("FEISHU_CONFIG", "IMAGE")
    RETURN_NAMES = ("飞书配置", "使用说明")
    FUNCTION = "create_config"
    CATEGORY = "飞书工具"
    
    def create_config(self, 应用ID: str, 应用密钥: str, 表格链接: str) -> tuple:
        """创建飞书配置"""
        self.app_id = 应用ID.strip()
        self.app_secret = 应用密钥.strip()
        self.table_url = 表格链接.strip()
        
        # 解析表格信息
        self._parse_table_info()
        
        # 创建配置对象
        config = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "table_url": self.table_url,
            "url_app_id": self.url_app_id,
            "table_id": self.table_id,
            "parsed": self._parsed
        }
        
        # 加载使用说明图片
        usage_image = self._load_usage_image()
        
        return (config, usage_image)
    
    def _parse_table_info(self):
        """解析表格链接信息"""
        try:
            if not self.table_url:
                self._parsed = False
                return
            
            # 解析飞书多维表格链接
            # 格式: https://xxx.feishu.cn/base/APP_ID?table=TABLE_ID&view=VIEW_ID
            if "base/" in self.table_url:
                # 新版本链接格式
                parts = self.table_url.split("base/")
                if len(parts) >= 2:
                    app_part = parts[1].split("?")[0]
                    self.url_app_id = app_part
                    
                    # 提取table_id
                    if "table=" in self.table_url:
                        table_part = self.table_url.split("table=")[1]
                        self.table_id = table_part.split("&")[0]
                        self._parsed = True
            elif "wiki/" in self.table_url:
                # 旧版本链接格式
                parts = self.table_url.split("wiki/")
                if len(parts) >= 2:
                    app_part = parts[1].split("?")[0]
                    self.url_app_id = app_part
                    
                    # 提取table_id
                    if "table=" in self.table_url:
                        table_part = self.table_url.split("table=")[1]
                        self.table_id = table_part.split("&")[0]
                        self._parsed = True
        except Exception as e:
            print(f"解析表格链接失败: {e}")
            self._parsed = False
    
    def get_config_info(self) -> Dict[str, Any]:
        """获取配置信息"""
        return {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "table_url": self.table_url,
            "url_app_id": self.url_app_id,
            "table_id": self.table_id,
            "parsed": self._parsed
        }
    
    def validate_config(self) -> tuple[bool, str]:
        """验证配置是否有效"""
        if not self.app_id:
            return False, "App ID 不能为空"
        if not self.app_secret:
            return False, "App Secret 不能为空"
        if not self.table_url:
            return False, "表格链接不能为空"
        if not self._parsed:
            return False, "表格链接格式无效，无法解析"
        
        return True, "配置有效"

    def _load_usage_image(self):
        """加载使用说明图片（从节点目录中加载）"""
        import os
        from PIL import Image
        import torch
        import numpy as np
        
        # 从节点目录中加载图片
        current_dir = os.path.dirname(__file__)
        usage_image_path = os.path.join(current_dir, "usage_guide.jpg")
        
        try:
            # 检查文件是否存在
            if os.path.exists(usage_image_path):
                # 加载图片
                img = Image.open(usage_image_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                print(f"✅ 成功加载使用说明图片: {usage_image_path}, 尺寸: {img.width}x{img.height}")
                
                # 转换为tensor
                return self._to_single_image(img)
            else:
                print(f"⚠️ 使用说明图片不存在: {usage_image_path}")
                # 如果文件不存在，返回一个带文字的占位图片
                return self._create_placeholder_usage_image()
                
        except Exception as e:
            print(f"❌ 加载使用说明图片失败: {str(e)}")
            # 出错时返回占位图片
            return self._create_placeholder_usage_image()

    def _create_placeholder_usage_image(self):
        """创建一个带文字的占位使用说明图片"""
        from PIL import Image, ImageDraw, ImageFont
        import torch
        import numpy as np
        
        try:
            # 创建一个白色背景的图片
            width, height = 400, 300
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # 尝试使用系统字体，如果失败则使用默认字体
            try:
                # Windows系统字体
                font = ImageFont.truetype("msyh.ttc", 20)  # 微软雅黑
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
            
            # 绘制文字
            text_lines = [
                "使用说明图片",
                "",
                "图片文件路径:",
                "节点目录/usage_guide.jpg",
                "",
                "图片文件缺失，请联系开发者"
            ]
            
            y_offset = 50
            for line in text_lines:
                # 计算文字位置（居中）
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                
                draw.text((x, y_offset), line, fill='black', font=font)
                y_offset += 30
            
            print("✅ 创建了占位使用说明图片")
            return self._to_single_image(img)
            
        except Exception as e:
            print(f"❌ 创建占位图片失败: {str(e)}")
            # 最后的备用方案：返回纯色图片
            return torch.zeros((1, 300, 400, 3), dtype=torch.float32)

    def _to_single_image(self, image):
        """将单张图片转换为tensor"""
        if image is None:
            return torch.zeros((1, 64, 64, 3), dtype=torch.float32)
        
        # 直接转换原始图片，不进行任何缩放
        arr = np.asarray(image).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr)
        
        # 添加批次维度 (H, W, C) -> (1, H, W, C)
        return tensor.unsqueeze(0)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "FeishuConfigNode": FeishuConfigNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FeishuConfigNode": "飞书配置节点"
}

