#!/usr/bin/env python3
"""
测试：飞书多维表格获取图片节点
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from feishu_fetch_image_node import FeishuFetchImageNode


def main():
    print("测试：飞书多维表格获取图片节点")
    print("=" * 60)

    # 配置信息
    app_id = "cli_a8137df47f38501c"
    app_secret = "u-dnhEPT1zZ4YUASTjuFmKSC41h_8B51aXgW20h4kEyEFO"
    table_url = "https://fqrqkwpqx5.feishu.cn/base/CSPQbCY1OazvLnsxgWicjW0hnYd?table=tblPlnQ7x0dYGWC8&view=vew5tYVpod"
    target_column = "生成图片"
    
    # 尝试两种场景：优先用非空值，否则不加筛选
    filter_condition = "生成图片+非空值"
    image_index = 1  # 选择第1张图片

    print("开始拉取(生成图片+非空值)...")
    images, msg, extracted = node.fetch_images(app_id, app_secret, table_url,
                                               target_column, filter_condition,
                                               image_index, "文生图")
    print("返回：", msg)
    print("返回类型:", type(images))
    
    print("批次形状:", images.shape if hasattr(images, 'shape') else type(images))
    
    print("\n提取的内容：")
    print(extracted if extracted else "(无)")

    if hasattr(images, 'shape') and images.shape[0] == 0:
        print("尝试无筛选再次拉取...")
        images2, msg2, extracted2 = node.fetch_images(app_id, app_secret, table_url,
                                                       target_column, "",
                                                       image_index, "文生图")
        print("返回：", msg2)
        print("返回类型:", type(images2))
        
        print("批次形状:", images2.shape if hasattr(images2, 'shape') else type(images2))
        
        print("提取的内容：")
        print(extracted2 if extracted2 else "(无)")


if __name__ == "__main__":
    node = FeishuFetchImageNode()
    main()
