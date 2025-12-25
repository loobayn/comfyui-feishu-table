"""
飞书文本编辑节点
用于编辑和修改文本内容
"""

import re

class FeishuTextEditorNode:
    """
    飞书文本编辑节点
    
    功能：
    1. 提供一个多行文本框用于编辑文本
    2. 支持文本内容的修改和格式化
    3. 根据第一个条件删除文本中对应的内容和前面的内容
    4. 根据第二个条件删除文本中对应的内容和后面的内容
    5. 可选择是否保留条件框中的关键词内容
    6. 输出编辑后的文本内容
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点的输入参数
        """
        return {
            "required": {
                "输入文本": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "在此编辑文本内容...",
                    "label": "文本内容"
                }),
                "删除前面条件": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "删除条件（删除该关键词及其前面的所有内容）",
                    "label": "删除前面内容条件"
                }),
                "删除后面条件": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "删除条件（删除该关键词及其后面的所有内容）",
                    "label": "删除后面内容条件"
                }),
                "保留关键词": ("BOOLEAN", {
                    "default": False,
                    "label_on": "保留关键词",
                    "label_off": "删除关键词"
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("输出文本",)
    
    FUNCTION = "edit_text"
    CATEGORY = "飞书工具"
    
    def edit_text(self, 输入文本: str, 删除前面条件: str, 删除后面条件: str, 保留关键词: bool) -> tuple:
        """
        编辑文本内容，根据条件删除指定内容
        
        Args:
            输入文本: 输入的文本内容
            删除前面条件: 删除该关键词及其前面的所有内容
            删除后面条件: 删除该关键词及其后面的所有内容
            保留关键词: 是否保留条件框中的关键词内容
            
        Returns:
            tuple: 包含编辑后的文本
        """
        result_text = 输入文本
        
        try:
            # 处理第一个条件：删除匹配内容及其前面的所有内容
            if 删除前面条件.strip():
                index = result_text.find(删除前面条件)
                if index != -1:
                    if 保留关键词:
                        # 保留关键词，只删除前面的内容
                        result_text = result_text[index:]
                        print(f"已删除'{删除前面条件}'前面的内容，保留关键词")
                    else:
                        # 删除关键词及其前面的内容
                        result_text = result_text[index + len(删除前面条件):]
                        print(f"已删除'{删除前面条件}'及其前面的内容")
            
            # 处理第二个条件：删除匹配内容及其后面的所有内容
            if 删除后面条件.strip():
                index = result_text.find(删除后面条件)
                if index != -1:
                    if 保留关键词:
                        # 保留关键词，只删除后面的内容
                        result_text = result_text[:index + len(删除后面条件)]
                        print(f"已删除'{删除后面条件}'后面的内容，保留关键词")
                    else:
                        # 删除关键词及其后面的内容
                        result_text = result_text[:index]
                        print(f"已删除'{删除后面条件}'及其后面的内容")
                
            return (result_text,)
                
        except Exception as e:
            print(f"文本处理过程中发生错误: {str(e)}")
            return (输入文本,)
