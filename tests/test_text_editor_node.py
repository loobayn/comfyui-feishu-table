#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书文本编辑节点
"""

from feishu_text_editor_node import FeishuTextEditorNode

def test_text_editor():
    """测试文本编辑功能"""
    print("=== 测试飞书文本编辑节点 ===\n")
    
    # 创建节点实例
    editor = FeishuTextEditorNode()
    
    # 测试用例1：基本功能
    print("测试用例1：基本功能")
    input_text = "（1&文生图: 一只大型的可爱动物。1#）"
    start_keyword = "文生图"
    end_keyword = "可爱"
    
    print(f"输入文本: {input_text}")
    print(f"开始关键词: {start_keyword}")
    print(f"结束关键词: {end_keyword}")
    
    result = editor.edit_text(input_text, start_keyword, end_keyword)
    print(f"输出结果: {result}")
    print(f"期望结果: : 一只大型的")
    print(f"测试{'通过' if result == ': 一只大型的' else '失败'}\n")
    
    # 测试用例2：只设置开始关键词
    print("测试用例2：只设置开始关键词")
    input_text = "（1&文生图: 一只大型的可爱动物。1#）"
    start_keyword = "文生图"
    end_keyword = ""
    
    print(f"输入文本: {input_text}")
    print(f"开始关键词: {start_keyword}")
    print(f"结束关键词: {end_keyword}")
    
    result = editor.edit_text(input_text, start_keyword, end_keyword)
    print(f"输出结果: {result}")
    print(f"期望结果: : 一只大型的可爱动物。1#）")
    print(f"测试{'通过' if result == ': 一只大型的可爱动物。1#）' else '失败'}\n")
    
    # 测试用例3：只设置结束关键词
    print("测试用例3：只设置结束关键词")
    input_text = "（1&文生图: 一只大型的可爱动物。1#）"
    start_keyword = ""
    end_keyword = "可爱"
    
    print(f"输入文本: {input_text}")
    print(f"开始关键词: {start_keyword}")
    print(f"结束关键词: {end_keyword}")
    
    result = editor.edit_text(input_text, start_keyword, end_keyword)
    print(f"输出结果: {result}")
    print(f"期望结果: （1&文生图: 一只大型的")
    print(f"测试{'通过' if result == '（1&文生图: 一只大型的' else '失败'}\n")
    
    # 测试用例4：关键词不存在
    print("测试用例4：关键词不存在")
    input_text = "（1&文生图: 一只大型的可爱动物。1#）"
    start_keyword = "不存在"
    end_keyword = "可爱"
    
    print(f"输入文本: {input_text}")
    print(f"开始关键词: {start_keyword}")
    print(f"结束关键词: {end_keyword}")
    
    result = editor.edit_text(input_text, start_keyword, end_keyword)
    print(f"输出结果: {result}")
    print(f"期望结果: '' (空字符串)")
    print(f"测试{'通过' if result == '' else '失败'}\n")
    
    # 测试用例5：空输入
    print("测试用例5：空输入")
    input_text = ""
    start_keyword = "文生图"
    end_keyword = "可爱"
    
    print(f"输入文本: {input_text}")
    print(f"开始关键词: {start_keyword}")
    print(f"结束关键词: {end_keyword}")
    
    result = editor.edit_text(input_text, start_keyword, end_keyword)
    print(f"输出结果: {result}")
    print(f"期望结果: '' (空字符串)")
    print(f"测试{'通过' if result == '' else '失败'}\n")
    
    # 测试用例6：复杂文本
    print("测试用例6：复杂文本")
    input_text = "第一行：文生图: 内容1\n第二行：文生图: 内容2\n第三行：文生图: 内容3"
    start_keyword = "文生图"
    end_keyword = "内容2"
    
    print(f"输入文本: {input_text}")
    print(f"开始关键词: {start_keyword}")
    print(f"结束关键词: {end_keyword}")
    
    result = editor.edit_text(input_text, start_keyword, end_keyword)
    print(f"输出结果: {result}")
    print(f"期望结果: : 内容1\n第二行：文生图:")
    print(f"测试{'通过' if result == ': 内容1\n第二行：文生图:' else '失败'}\n")

if __name__ == "__main__":
    test_text_editor()
