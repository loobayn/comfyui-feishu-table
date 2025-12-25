# ComfyUI 飞书多维表格插件

这是一个用于ComfyUI的飞书多维表格集成插件，支持读取、写入、上传图片和获取图片等功能。

## 功能特性

- **飞书多维表格节点**: 读取表格数据，支持筛选和多种输出格式
- **飞书多维表格写入节点**: 将文本写入指定单元格，支持筛选条件
- **飞书多维表格附件上传节点**: 上传图片到表格，支持筛选和添加新行
- **飞书图片获取节点**: 从表格中获取图片，支持筛选和索引选择
- **飞书配置节点**: 集中管理飞书API配置

## 文件结构

```
comfyui_feishu_table/
├── __init__.py                 # 插件入口文件
├── feishu_table_node.py        # 表格读取节点
├── feishu_write_node.py        # 表格写入节点
├── feishu_upload_node.py       # 图片上传节点
├── feishu_fetch_image_node.py  # 图片获取节点
├── feishu_config_node.py       # 配置管理节点
├── config.json                 # 配置文件
├── requirements.txt            # 依赖包列表
├── install.bat                 # Windows安装脚本
├── install.sh                  # Linux/Mac安装脚本
├── docs/                       # 文档文件夹
│   ├── README.md              # 详细说明文档
│   ├── QUICK_START.md         # 快速开始指南
│   ├── README_CONFIG.md        # 配置节点说明
│   ├── FILTER_SYNTAX.md       # 筛选语法说明
│   └── SUMMARY.md             # 功能总结
├── examples/                   # 示例文件夹
│   └── example_workflow.json  # 工作流示例
├── tests/                      # 测试文件夹
│   └── *.py                   # 各种测试脚本
└── js/                        # 前端JavaScript文件
```

## 快速开始

1. 将插件文件夹复制到 `ComfyUI/custom_nodes/` 目录
2. 重启ComfyUI
3. 在节点列表中找到"飞书工具"分类
4. 使用"飞书配置节点"配置API信息
5. 连接其他飞书节点使用

## 详细文档

- [快速开始指南](docs/QUICK_START.md)
- [配置节点说明](docs/README_CONFIG.md)
- [筛选语法说明](docs/FILTER_SYNTAX.md)
- [输出格式说明](docs/OUTPUT_FORMAT.md)
- [视频上传说明](docs/VIDEO_UPLOAD_NODE.md)
- [功能总结](docs/SUMMARY.md)

## 依赖要求

- Python 3.7+
- requests
- Pillow (PIL)
- torch (可选，用于图片处理)

## 许可证

MIT License

