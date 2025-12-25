#!/usr/bin/env python3
"""
调试URL解析
"""

from urllib.parse import urlparse, parse_qs

def debug_url_parsing():
    """调试URL解析"""
    test_url = "https://fqrqkwpqx5.feishu.cn/base/FPNXbI1LKar6Y3sfue3cDZeon1g?table=tblTooQfnEL6ZaVE&view=vewvGmQonQ"
    
    print(f"测试URL: {test_url}")
    print("=" * 60)
    
    # 解析URL
    parsed_url = urlparse(test_url)
    print(f"解析后的URL对象:")
    print(f"  scheme: {parsed_url.scheme}")
    print(f"  netloc: {parsed_url.netloc}")
    print(f"  path: {parsed_url.path}")
    print(f"  query: {parsed_url.query}")
    print(f"  fragment: {parsed_url.fragment}")
    
    print("\n路径部分分析:")
    path_parts = parsed_url.path.split('/')
    print(f"  路径分割: {path_parts}")
    
    if 'base' in path_parts:
        base_index = path_parts.index('base')
        print(f"  'base' 在索引: {base_index}")
        print(f"  索引 {base_index} 后的元素: {path_parts[base_index:base_index+3]}")
        
        if len(path_parts) > base_index + 2:
            app_id = path_parts[base_index + 2]
            print(f"  应用ID (base_index + 2): {app_id}")
        else:
            print(f"  路径长度不足，无法获取应用ID")
    else:
        print("  路径中未找到 'base'")
    
    print("\n查询参数分析:")
    query_params = parse_qs(parsed_url.query)
    print(f"  查询参数: {query_params}")
    
    table_id = query_params.get('table', [None])[0]
    print(f"  表格ID: {table_id}")
    
    view_id = query_params.get('view', [None])[0]
    print(f"  视图ID: {view_id}")

if __name__ == "__main__":
    debug_url_parsing()
