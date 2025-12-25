"""
飞书多维表格图片获取节点
从指定列（附件/图片字段）中按筛选条件获取图片，并输出为IMAGE批量。
支持与其它节点一致的筛选语法：列名+关键词 / 列名-关键词 / 列名+非空值 / 列名-空值 / 列名-非空值
"""

from typing import Any, Dict, List, Optional, Tuple
import io
import json
import re

import numpy as np
import requests
from PIL import Image
from urllib.parse import urlparse, parse_qs
import torch

# 尝试导入ComfyUI的folder_paths模块
try:
    import folder_paths
except ImportError:
    folder_paths = None


class FeishuFetchImageNode:
    """飞书多维表格图片获取节点"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "飞书配置": ("FEISHU_CONFIG",),
                "目标列名": ("STRING", {"default": "生成图片", "multiline": False}),
                "筛选条件": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "筛选条件（每行一条）：\n列名+关键词 / 列名-关键词 / 列名+非空值 / 列名-空值 / 列名-非空值"
                }),
                "图片索引": ("INT", {
                    "default": 1, 
                    "min": 1, 
                    "max": 64, 
                    "step": 1,
                    "label": "选择第几张图片"
                }),
                "提取列名": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "placeholder": "要提取的其他列名（每行一个），如：\n文生图\n状态\n备注\n\n留空则不提取其他内容"
                }),
            },
            "optional": {
                "列分隔符": ("STRING", {
                    "multiline": True,
                    "default": " | ",
                    "placeholder": "自定义列分隔符，默认为 ' | '。例如：\n- 使用逗号：, \n- 使用分号：; \n- 使用制表符：\\t\n- 使用换行：\\n\n- 使用自定义符号：→\n- 使用多个字符：---\n- 留空则使用默认分隔符"
                }),
                "显示预览": ("BOOLEAN", {
                    "default": True,
                    "label_on": "显示预览",
                    "label_off": "隐藏预览"
                })
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("图片", "状态信息", "提取的内容", "使用说明")
    FUNCTION = "fetch_images"
    CATEGORY = "飞书工具"
    OUTPUT_NODE = True

    def IS_CHANGED(self, **kwargs):
        # 让节点在每次执行时都刷新，确保预览能正确显示
        import time
        return str(time.time())

    # =============== 基础 API ===============
    def get_access_token(self, app_id: str, app_secret: str) -> Optional[str]:
        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            payload = {"app_id": app_id, "app_secret": app_secret}
            print(f"🔑 获取访问令牌: app_id={app_id}, app_secret={app_secret[:10]}...")
            resp = requests.post(url, json=payload, timeout=30)
            print(f"🔑 响应状态: {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            print(f"🔑 响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            if data.get("code") == 0:
                token = data.get("tenant_access_token")
                print(f"🔑 获取到访问令牌: {token[:20]}...")
                return token
            else:
                print(f"🔑 获取访问令牌失败: {data.get('msg', '未知错误')}")
            return None
        except Exception as e:
            print(f"🔑 获取访问令牌异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def extract_table_info(self, table_url: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            parsed = urlparse(table_url)
            path_parts = parsed.path.split('/')
            app_id = None
            if 'base' in path_parts:
                idx = path_parts.index('base')
                if len(path_parts) > idx + 1:
                    app_id = path_parts[idx + 1]
            table_id = parse_qs(parsed.query).get('table', [None])[0]
            return app_id, table_id
        except Exception:
            return None, None

    def get_table_records(self, access_token: str, app_id: str, table_id: str, page_size: int = 100) -> List[Dict]:
        """获取表格记录"""
        records: List[Dict] = []
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
            params: Dict[str, Any] = {"page_size": page_size}
            headers = {"Authorization": f"Bearer {access_token}"}
            while True:
                r = requests.get(url, headers=headers, params=params, timeout=30)
                if r.status_code != 200:
                    break
                j = r.json()
                if j.get('code') != 0:
                    break
                batch = j.get('data', {}).get('items', [])
                records.extend(batch)
                page_token = j.get('data', {}).get('page_token')
                if not page_token:
                    break
                params["page_token"] = page_token
        except Exception:
            pass
        return records

    # =============== 筛选 ===============
    def _is_empty_value(self, v: Any) -> bool:
        if v is None:
            return True
        if isinstance(v, str) and not v.strip():
            return True
        if isinstance(v, list) and len(v) == 0:
            return True
        if isinstance(v, dict):
            text_content = v.get('text', '') or v.get('name', '') or str(v)
            return not text_content or not text_content.strip()
        return False

    def _value_contains(self, v: Any, needle: str) -> bool:
        if v is None:
            return False
        needle_l = str(needle).lower()
        if isinstance(v, list):
            return any(needle_l in str(x).lower() for x in v)
        if isinstance(v, dict):
            text_content = v.get('text', '') or v.get('name', '') or str(v)
            return needle_l in text_content.lower()
        return needle_l in str(v).lower()

    def _check_condition(self, v: Any, cond: str) -> bool:
        if cond == "空值":
            return self._is_empty_value(v)
        if cond == "非空值":
            return not self._is_empty_value(v)
        return self._value_contains(v, cond)

    def filter_records(self, records: List[Dict], filter_condition: str) -> List[Dict]:
        if not filter_condition.strip():
            return records
        include_conds: List[Tuple[str, str]] = []
        exclude_conds: List[Tuple[str, str]] = []
        for raw in filter_condition.strip().split('\n'):
            line = raw.strip()
            if not line:
                continue
            m = re.match(r"^\s*([^+\-=\s]+)\s*([+-])\s*(.+?)\s*$", line)
            if m:
                col = m.group(1).strip()
                op = m.group(2)
                val = m.group(3).strip()
                (include_conds if op == '+' else exclude_conds).append((col, val))
                continue
            if '=' in line:
                col, val = line.split('=', 1)
                include_conds.append((col.strip(), val.strip()))

        out: List[Dict] = []
        for rec in records:
            fields = rec.get('fields', {})
            ok_inc = True
            if include_conds:
                for col, val in include_conds:
                    if not self._check_condition(fields.get(col, None), val):
                        ok_inc = False
                        break
            if not ok_inc:
                continue
            hit_exc = False
            for col, val in exclude_conds:
                if self._check_condition(fields.get(col, None), val):
                    hit_exc = True
                    break
            if not hit_exc:
                out.append(rec)
        return out

    # =============== 下载图片 ===============
    def _download_image_by_file_token(self, access_token: str, file_token: str) -> Optional[Image.Image]:
        """按文件token下载图片。尝试多种下载方式。"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 方案一：GET /open-apis/drive/v1/files/download?file_token=xxx
        try:
            url1 = "https://open.feishu.cn/open-apis/drive/v1/files/download"
            print(f"  🔍 尝试方案1: {url1}")
            resp = requests.get(url1, headers=headers, params={"file_token": file_token}, timeout=60, allow_redirects=True)
            print(f"  📡 方案1状态: {resp.status_code}")
            if resp.status_code == 200 and resp.content:
                img = Image.open(io.BytesIO(resp.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                print(f"  ✅ 方案1成功，尺寸: {img.size}, 模式: {img.mode}")
                return img
        except Exception as e:
            print(f"  ❌ 方案1异常: {str(e)}")
        
        # 方案二：GET /open-apis/drive/v1/files/{file_token}/download
        try:
            url2 = f"https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/download"
            print(f"  🔍 尝试方案2: {url2}")
            resp2 = requests.get(url2, headers=headers, timeout=60, allow_redirects=True)
            print(f"  📡 方案2状态: {resp2.status_code}")
            if resp2.status_code == 200 and resp2.content:
                img = Image.open(io.BytesIO(resp2.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                print(f"  ✅ 方案2成功，尺寸: {img.size}, 模式: {img.mode}")
                return img
        except Exception as e:
            print(f"  ❌ 方案2异常: {str(e)}")
        
        # 方案三：GET /open-apis/drive/v1/medias/{file_token}/download
        try:
            url3 = f"https://open.feishu.cn/open-apis/drive/v1/medias/{file_token}/download"
            print(f"  🔍 尝试方案3: {url3}")
            resp3 = requests.get(url3, headers=headers, timeout=60, allow_redirects=True)
            print(f"  📡 方案3状态: {resp3.status_code}")
            if resp3.status_code == 200 and resp3.content:
                img = Image.open(io.BytesIO(resp3.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                print(f"  ✅ 方案3成功，尺寸: {img.size}, 模式: {img.mode}")
                return img
        except Exception as e:
            print(f"  ❌ 方案3异常: {str(e)}")
        
        # 方案四：GET /open-apis/drive/v1/medias/{file_token}/download?extra=...
        try:
            url4 = f"https://open.feishu.cn/open-apis/drive/v1/medias/{file_token}/download"
            params = {
                "extra": json.dumps({"bitablePerm": {"tableId": "tblPlnQ7x0dYGWC8", "rev": 5}})
            }
            print(f"  🔍 尝试方案4: {url4} 带参数")
            resp4 = requests.get(url4, headers=headers, params=params, timeout=60, allow_redirects=True)
            print(f"  📡 方案4状态: {resp4.status_code}")
            if resp4.status_code == 200 and resp4.content:
                img = Image.open(io.BytesIO(resp4.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                print(f"  ✅ 方案4成功，尺寸: {img.size}, 模式: {img.mode}")
                return img
        except Exception as e:
            print(f"  ❌ 方案4异常: {str(e)}")
        
        return None

    def _get_tmp_download_urls(self, access_token: str, file_tokens: List[str], table_id: str) -> Dict[str, str]:
        """获取临时下载链接"""
        if not file_tokens:
            return {}
        
        try:
            url = "https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url"
            
            # 构建请求参数
            params = {
                "file_tokens": ",".join(file_tokens),
                "extra": json.dumps({"bitablePerm": {"tableId": table_id, "rev": 5}})
            }
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            print(f"📥 获取 {len(file_tokens)} 个文件的临时下载链接...")
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            print(f"📡 临时下载链接请求状态: {response.status_code}")
            print(f"📡 请求URL: {url}")
            print(f"📡 请求参数: {params}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📡 响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                if data.get("code") == 0:
                    tmp_urls = {}
                    items = data.get("data", {}).get("tmp_download_urls", [])
                    for item in items:
                        file_token = item.get("file_token")
                        tmp_url = item.get("tmp_download_url")
                        if file_token and tmp_url:
                            tmp_urls[file_token] = tmp_url
                            print(f"✅ 获取到 {file_token} 的临时下载链接")
                    return tmp_urls
                else:
                    print(f"❌ 获取临时下载链接失败: {data.get('msg', '未知错误')}")
                    print(f"❌ 错误代码: {data.get('code')}")
            else:
                print(f"❌ 临时下载链接请求失败: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"❌ 错误响应: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
                except:
                    print(f"❌ 原始响应: {response.text[:500]}")
                
        except Exception as e:
            print(f"❌ 获取临时下载链接异常: {str(e)}")
            import traceback
            traceback.print_exc()
            
        return {}

    def _download_image_by_tmp_url(self, tmp_url: str) -> Optional[Image.Image]:
        """使用临时下载链接下载图片"""
        try:
            response = requests.get(tmp_url, timeout=60, allow_redirects=True)
            
            if response.status_code == 200 and response.content:
                img = Image.open(io.BytesIO(response.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                print(f"✅ 图片下载成功，尺寸: {img.size}, 模式: {img.mode}")
                return img
            else:
                print(f"❌ 临时链接下载失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 临时链接下载异常: {str(e)}")
            
        return None

    def _gather_image_tokens(self, records: List[Dict], target_column: str) -> List[Dict]:
        """收集所有图片token和对应的记录信息"""
        result = []
        for rec in records:
            fields = rec.get('fields', {})
            val = fields.get(target_column)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict) and item.get('file_token'):
                        result.append({
                            'file_token': item['file_token'],
                            'record': rec,
                            'fields': fields
                        })
        return result

    def _to_single_image(self, image: Image.Image) -> torch.Tensor:
        """将单张图片转换为tensor，保持原始尺寸"""
        if image is None:
            return torch.zeros((1, 64, 64, 3), dtype=torch.float32)
        
        # 直接转换原始图片，不进行任何缩放
        arr = np.asarray(image).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr)
        
        # 添加批次维度 (H, W, C) -> (1, H, W, C)
        return tensor.unsqueeze(0)

    def _extract_single_record_content(self, image_record: Dict, extract_columns: str, column_separator: str = " | ") -> str:
        """提取单条记录的其他列内容，使用与获取文本节点相同的格式"""
        if not extract_columns.strip():
            return ""
        
        # 兼容多种分隔符：英文逗号, 中文逗号，顿号、英文/中文分号，以及换行/回车
        parts = re.split(r"[\,\uFF0C\u3001;\uFF1B\n\r]+", extract_columns.strip())
        column_names = [col.strip() for col in parts if col.strip()]
        if not column_names:
            return ""
        
        fields = image_record['fields']
        record_index = 1  # 图片节点只处理单条记录，所以索引固定为1
        
        # 使用与获取文本节点相同的格式，字段内容用***标记
        line_parts = []
        for col_name in column_names:
            if col_name in fields:
                value = fields[col_name]
                if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                    line_parts.append(f"获取结果{record_index}&{col_name}***(空)***")
                elif isinstance(value, list):
                    # 处理列表类型字段（如富文本、附件等）
                    if value and isinstance(value[0], dict):
                        # 富文本或附件字段
                        if 'text' in value[0]:
                            text_content = ', '.join([item.get('text', '') for item in value if item.get('text')])
                            line_parts.append(f"获取结果{record_index}&{col_name}***({text_content})***")
                        elif 'name' in value[0]:
                            # 附件字段
                            names = [item.get('name', '') for item in value if item.get('name')]
                            line_parts.append(f"获取结果{record_index}&{col_name}***({', '.join(names)})***")
                        else:
                            line_parts.append(f"获取结果{record_index}&{col_name}***({str(value)})***")
                    else:
                        # 普通列表
                        content = ', '.join(map(str, value))
                        line_parts.append(f"获取结果{record_index}&{col_name}***({content})***")
                else:
                    # 普通字段
                    line_parts.append(f"获取结果{record_index}&{col_name}***({value})***")
            else:
                line_parts.append(f"获取结果{record_index}&{col_name}***(空)***")
        
        # 使用分隔符连接各列数据，并添加结尾标识
        line_content = column_separator.join(line_parts)
        return f"{line_content}&获取结果{record_index}#"

    # =============== 主入口 ===============
    def fetch_images(self, 飞书配置: dict, 目标列名: str, 筛选条件: str,
                     图片索引: int, 提取列名: str = "", 列分隔符: str = " | ", 显示预览: bool = True) -> Tuple[torch.Tensor, str, str]:
        # 从配置中获取认证信息
        app_id = 飞书配置.get("app_id", "")
        app_secret = 飞书配置.get("app_secret", "")
        table_url = 飞书配置.get("table_url", "")
        url_app_id = 飞书配置.get("url_app_id", "")
        table_id = 飞书配置.get("table_id", "")
        
        # 验证配置
        if not app_id or not app_secret or not table_url:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：配置信息不完整，请检查飞书配置节点", "", usage_image)}
        
        if not url_app_id or not table_id:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：表格链接格式无效，请检查飞书配置节点", "", usage_image)}
        
        # 1. token
        token = self.get_access_token(app_id, app_secret)
        if not token:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：无法获取访问令牌", "", usage_image)}
        # 2. 拉取记录并筛选
        records = self.get_table_records(token, url_app_id, table_id)
        if records is None or len(records) == 0:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：未获取到任何记录", "", usage_image)}
        filtered = self.filter_records(records, 筛选条件)
        if len(filtered) == 0:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：筛选条件未匹配到记录", "", usage_image)}
        # 3. 收集所有图片token和记录信息
        print(f"🔍 筛选后的记录数量: {len(filtered)}")
        all_image_records = self._gather_image_tokens(filtered, 目标列名)
        print(f"🔍 找到的图片记录总数: {len(all_image_records)}")
        if len(all_image_records) == 0:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：目标列未找到任何图片附件", "", usage_image)}
        
        # 4. 选择指定索引的图片
        if 图片索引 > len(all_image_records):
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), f"错误：图片索引 {图片索引} 超出范围，总共只有 {len(all_image_records)} 张图片", "", usage_image)}
        
        selected_record = all_image_records[图片索引 - 1]  # 转换为0基索引
        print(f"🔍 选择第 {图片索引} 张图片，记录ID: {selected_record['record'].get('record_id', '未知')}")
        
        # 处理自定义分隔符，如果为空则使用默认分隔符
        if 列分隔符 is None or 列分隔符 == "":
            列分隔符 = " | "
        
        # 处理特殊字符转义
        列分隔符 = 列分隔符.replace('\\n', '\n').replace('\\t', '\t')
        
        # 提取其他列内容
        extracted_content = self._extract_single_record_content(selected_record, 提取列名, 列分隔符)
        
        # 5. 获取临时下载链接
        file_token = selected_record['file_token']
        tmp_urls = self._get_tmp_download_urls(token, [file_token], table_id)
        if not tmp_urls:
            print("⚠️ 无法获取临时下载链接，尝试直接下载")
        
        # 6. 下载选中的图片
        img = None
        # 优先使用临时下载链接
        if file_token in tmp_urls:
            img = self._download_image_by_tmp_url(tmp_urls[file_token])
        
        # 如果临时链接失败，尝试直接下载
        if img == None:
            img = self._download_image_by_file_token(token, file_token)
        
        if img is None:
            usage_image = self._load_usage_image()
            return {"ui": {"images": []}, "result": (self._placeholder_image(), "错误：图片下载失败", extracted_content, usage_image)}
        
        # 7. 转换为tensor，保持原始尺寸
        image_tensor = self._to_single_image(img)
        
        # 8. 加载使用说明图片
        usage_image = self._load_usage_image()
        
        # 9. 根据开关决定是否准备预览图片数据
        if 显示预览:
            preview_image = self._prepare_preview_image(img, 图片索引)
            return {
                "ui": {"images": [preview_image]}, 
                "result": (image_tensor, f"成功获取第 {图片索引} 张图片，尺寸: {img.width}x{img.height}", extracted_content, usage_image)
            }
        else:
            return {
                "ui": {"images": []}, 
                "result": (image_tensor, f"成功获取第 {图片索引} 张图片，尺寸: {img.width}x{img.height}（预览已关闭）", extracted_content, usage_image)
            }

    def _empty_image(self) -> torch.Tensor:
        return torch.zeros((0, 64, 64, 3), dtype=torch.float32)

    def _load_usage_image(self) -> torch.Tensor:
        """加载使用说明图片（从节点目录中加载）"""
        import os
        
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

    def _create_placeholder_usage_image(self) -> torch.Tensor:
        """创建一个带文字的占位使用说明图片"""
        from PIL import Image, ImageDraw, ImageFont
        
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
            return self._placeholder_image(400, 300)
        """返回一个占位黑图，避免下游 SaveImage 在空批情况下报 index 错误。"""
        return torch.zeros((1, height, width, 3), dtype=torch.float32)

    def _prepare_preview_image(self, img: Image.Image, image_index: int = 1) -> dict:
        """准备用于节点预览的图片数据 - 保持原图尺寸"""
        import os
        import uuid
        import tempfile
        
        try:
            # 获取临时目录
            if folder_paths is not None:
                temp_dir = folder_paths.get_temp_directory()
            else:
                temp_dir = tempfile.gettempdir()
            
            # 生成唯一的文件名
            filename = f"feishu_image_{image_index}_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(temp_dir, filename)
            
            # 直接保存原图，不进行任何缩放压缩
            img.save(filepath, format='PNG')
            
            print(f"✅ 预览图片已保存: {filepath}, 尺寸: {img.width}x{img.height}")
            
            # 返回预览数据
            return {
                "filename": filename,
                "subfolder": "",
                "type": "temp"
            }
            
        except Exception as e:
            print(f"❌ 准备预览图片失败: {str(e)}")
            # 如果失败，返回空的预览数据
            return {
                "filename": "",
                "subfolder": "",
                "type": "temp"
            }


