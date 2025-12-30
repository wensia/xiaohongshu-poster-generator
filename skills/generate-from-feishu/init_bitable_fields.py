#!/usr/bin/env python3
"""
飞书多维表格字段初始化脚本

从 zodiac-poster/assets/colors.json 读取配置，
自动创建/更新飞书多维表格的下拉菜单字段。

Usage:
    python init_bitable_fields.py [--dry-run] [--create-table]

Options:
    --dry-run       预览模式，不实际创建
    --create-table  创建新表格（如果不存在）
"""

import sys
import json
import argparse
import requests
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
COLORS_JSON = PROJECT_ROOT / "skills" / "zodiac-poster" / "assets" / "colors.json"
sys.path.insert(0, str(PROJECT_ROOT))

# 从 config.py 导入飞书配置
from config import (
    LARK_APP_ID,
    LARK_APP_SECRET,
    get_bitable,
    DEFAULT_BITABLE
)

# 获取默认表格配置
_default_bitable = get_bitable()
LARK_BITABLE_APP_TOKEN = _default_bitable.get("app_token")
LARK_BITABLE_TABLE_ID = _default_bitable.get("table_id")

# 飞书 API 基础 URL
LARK_API_BASE = "https://open.feishu.cn/open-apis"


class LarkBitableClient:
    """飞书多维表格客户端"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None

    def _get_tenant_token(self) -> str:
        """获取 tenant_access_token"""
        if self._token:
            return self._token

        url = f"{LARK_API_BASE}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"获取 token 失败: {data}")

        self._token = data["tenant_access_token"]
        return self._token

    def _headers(self) -> dict:
        """构建请求头"""
        return {
            "Authorization": f"Bearer {self._get_tenant_token()}",
            "Content-Type": "application/json"
        }

    def list_tables(self, app_token: str) -> list:
        """获取多维表格的所有数据表"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables"
        resp = requests.get(url, headers=self._headers())
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"获取表格列表失败: {data}")

        return data.get("data", {}).get("items", [])

    def list_fields(self, app_token: str, table_id: str) -> list:
        """获取数据表的所有字段"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        resp = requests.get(url, headers=self._headers())
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"获取字段列表失败: {data}")

        return data.get("data", {}).get("items", [])

    def create_field(self, app_token: str, table_id: str, field_config: dict) -> dict:
        """创建字段"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        resp = requests.post(url, headers=self._headers(), json=field_config)
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"创建字段失败: {data}")

        return data.get("data", {}).get("field", {})

    def update_field(self, app_token: str, table_id: str, field_id: str, field_config: dict) -> dict:
        """更新字段"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}"
        resp = requests.put(url, headers=self._headers(), json=field_config)
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"更新字段失败: {data}")

        return data.get("data", {}).get("field", {})

    def create_table(self, app_token: str, name: str, fields: list) -> dict:
        """创建数据表"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables"
        resp = requests.post(url, headers=self._headers(), json={
            "table": {
                "name": name,
                "default_view_name": "默认视图",
                "fields": fields
            }
        })
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"创建表格失败: {data}")

        return data.get("data", {})

    def delete_table(self, app_token: str, table_id: str) -> bool:
        """删除数据表"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}"
        resp = requests.delete(url, headers=self._headers())
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"删除表格失败: {data}")

        return True


def load_colors_config() -> dict:
    """加载配色配置"""
    with open(COLORS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_dropdown_options(config: dict) -> dict:
    """
    从 colors.json 生成下拉菜单选项

    Returns:
        {
            "星座": [{"name": "白羊座"}, ...],
            "配色": [{"name": "原版暖杏"}, ...],
            "风格": [{"name": "经典风"}, ...],
            "字体": [{"name": "霞鹜文楷"}, ...]
        }
    """
    options = {}

    # 星座选项
    zodiac_list = list(config.get("zodiac", {}).keys())
    options["星座"] = [{"name": z} for z in zodiac_list]

    # 配色选项
    colors = config.get("colors", {})
    options["配色"] = [{"name": c["name"]} for c in colors.values()]

    # 风格选项
    styles = config.get("styles", {})
    options["风格"] = [{"name": s["name"]} for s in styles.values()]

    # 字体选项
    fonts = config.get("fonts", {})
    options["字体"] = [{"name": f["name"]} for f in fonts.values()]

    # 用途选项
    usages = config.get("usages", {})
    options["用途"] = [{"name": u["name"]} for u in usages.values()]

    return options


def build_field_configs(options: dict) -> list:
    """
    构建字段配置（按合理顺序）

    飞书字段类型:
    - 1: 多行文本
    - 3: 单选
    - 7: 复选框
    - 17: 附件

    字段顺序:
    1. 标题 (首列/索引列)
    2. 星座
    3. 用途
    4. 配色
    5. 风格
    6. 字体
    7. 副标题
    8. 正文内容
    9. 已生成
    10. 生成图片
    11. 生成图片路径
    """
    fields = []

    # 1. 标题 - 首列（索引字段）
    fields.append({
        "field_name": "标题",
        "type": 1,  # 文本
        "property": {"formatter": ""}
    })

    # 2. 星座 - 单选
    if "星座" in options:
        fields.append({
            "field_name": "星座",
            "type": 3,
            "property": {"options": options["星座"]}
        })

    # 3. 用途 - 单选（封面/长文案）
    if "用途" in options:
        fields.append({
            "field_name": "用途",
            "type": 3,
            "property": {"options": options["用途"]}
        })

    # 4. 配色 - 单选
    if "配色" in options:
        fields.append({
            "field_name": "配色",
            "type": 3,
            "property": {"options": options["配色"]}
        })

    # 5. 风格 - 单选
    if "风格" in options:
        fields.append({
            "field_name": "风格",
            "type": 3,
            "property": {"options": options["风格"]}
        })

    # 6. 字体 - 单选
    if "字体" in options:
        fields.append({
            "field_name": "字体",
            "type": 3,
            "property": {"options": options["字体"]}
        })

    # 7. 副标题 - 文本
    fields.append({
        "field_name": "副标题",
        "type": 1,
        "property": {"formatter": ""}
    })

    # 8. 正文内容 - 多行文本
    fields.append({
        "field_name": "正文内容",
        "type": 1,
        "property": {"formatter": ""}
    })

    # 9. 已生成 - 复选框
    fields.append({
        "field_name": "已生成",
        "type": 7,
    })

    # 10. 生成图片 - 附件
    fields.append({
        "field_name": "生成图片",
        "type": 17,
    })

    # 11. 生成图片路径 - 文本（记录本地路径）
    fields.append({
        "field_name": "生成图片路径",
        "type": 1,
        "property": {"formatter": ""}
    })

    # 12. 已发布 - 复选框（小红书发布状态）
    fields.append({
        "field_name": "已发布",
        "type": 7,
    })

    # 13. 小红书发送文案 - 文本（用户预设的发布文案，优先使用）
    fields.append({
        "field_name": "小红书发送文案",
        "type": 1,
        "property": {"formatter": ""}
    })

    return fields


def print_preview(options: dict, fields: list):
    """打印预览信息"""
    print("\n" + "=" * 60)
    print("飞书多维表格字段初始化预览")
    print("=" * 60)

    print("\n📋 下拉菜单选项:")
    for name, opts in options.items():
        opt_names = [o["name"] for o in opts]
        print(f"\n  【{name}】({len(opts)}个选项)")
        for i, n in enumerate(opt_names, 1):
            print(f"    {i}. {n}")

    print("\n📝 将创建/更新的字段:")
    type_map = {1: "文本", 3: "单选", 7: "复选框", 17: "附件"}
    for field in fields:
        ftype = type_map.get(field["type"], str(field["type"]))
        print(f"  - {field['field_name']} ({ftype})")

    print("\n" + "=" * 60)


def init_fields(client: LarkBitableClient, app_token: str, table_id: str,
                field_configs: list, options: dict, dry_run: bool = False):
    """初始化字段"""

    if dry_run:
        print("\n🔍 预览模式，不会实际修改飞书表格")
        return

    # 获取现有字段
    existing_fields = client.list_fields(app_token, table_id)
    existing_map = {f["field_name"]: f for f in existing_fields}

    print(f"\n📊 现有字段: {len(existing_fields)} 个")

    created = 0
    updated = 0
    skipped = 0

    for config in field_configs:
        field_name = config["field_name"]

        if field_name in existing_map:
            existing = existing_map[field_name]
            # 如果是单选字段，更新选项
            if config["type"] == 3 and field_name in options:
                try:
                    client.update_field(app_token, table_id, existing["field_id"], {
                        "field_name": field_name,
                        "type": 3,
                        "property": {
                            "options": options[field_name]
                        }
                    })
                    print(f"  ✅ 更新字段: {field_name}")
                    updated += 1
                except Exception as e:
                    print(f"  ⚠️  更新失败 {field_name}: {e}")
                    skipped += 1
            else:
                print(f"  ⏭️  跳过已存在: {field_name}")
                skipped += 1
        else:
            # 创建新字段
            try:
                client.create_field(app_token, table_id, config)
                print(f"  ✅ 创建字段: {field_name}")
                created += 1
            except Exception as e:
                print(f"  ❌ 创建失败 {field_name}: {e}")

    print(f"\n📈 完成: 创建 {created} / 更新 {updated} / 跳过 {skipped}")


def main():
    parser = argparse.ArgumentParser(description="初始化飞书多维表格字段")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改")
    parser.add_argument("--create-table", action="store_true", help="创建新表格")
    parser.add_argument("--recreate", action="store_true", help="删除旧表格并重新创建")
    parser.add_argument("--table-name", default="星座海报生成", help="新表格名称")
    parser.add_argument("--table-id", help="指定表格ID（覆盖环境变量）")
    args = parser.parse_args()

    # 检查配置
    if not LARK_APP_ID or not LARK_APP_SECRET:
        print("❌ 错误: 请在 config.py 中配置 LARK_APP_ID 和 LARK_APP_SECRET")
        sys.exit(1)

    if not LARK_BITABLE_APP_TOKEN:
        print("❌ 错误: 请在 config.py 的 LARK_BITABLES 中配置 app_token")
        sys.exit(1)

    # 加载配置
    print("📖 加载配置文件...")
    config = load_colors_config()
    options = generate_dropdown_options(config)
    fields = build_field_configs(options)

    # 打印预览
    print_preview(options, fields)

    if args.dry_run:
        print("\n✨ 预览完成（--dry-run 模式）")
        return

    # 初始化客户端
    client = LarkBitableClient(LARK_APP_ID, LARK_APP_SECRET)

    table_id = args.table_id or LARK_BITABLE_TABLE_ID

    # 重建模式：先删除旧表格
    if args.recreate and table_id:
        print(f"\n🗑️  删除旧表格 (ID: {table_id})...")
        try:
            client.delete_table(LARK_BITABLE_APP_TOKEN, table_id)
            print("✅ 旧表格已删除")
            table_id = None  # 清空，后面会创建新表格
        except Exception as e:
            print(f"⚠️  删除失败: {e}")

    if args.create_table or args.recreate:
        # 创建新表格
        print(f"\n🆕 创建新表格: {args.table_name}")
        result = client.create_table(LARK_BITABLE_APP_TOKEN, args.table_name, fields)
        table_id = result.get("table_id")
        print(f"✅ 表格已创建，ID: {table_id}")
        print(f"\n💡 请将 table_id 添加到 config.py 的 LARK_BITABLES 中:")
        print(f'    "table_id": "{table_id}",')
    else:
        if not table_id:
            # 列出现有表格供选择
            print("\n📋 获取现有表格列表...")
            tables = client.list_tables(LARK_BITABLE_APP_TOKEN)

            if not tables:
                print("❌ 没有找到任何表格，请使用 --create-table 创建新表格")
                sys.exit(1)

            print("\n现有表格:")
            for i, t in enumerate(tables, 1):
                print(f"  {i}. {t['name']} (ID: {t['table_id']})")

            # 使用第一个表格
            table_id = tables[0]["table_id"]
            print(f"\n⚠️  未指定 table_id，将使用第一个表格: {tables[0]['name']}")

        # 初始化字段
        print(f"\n🔧 初始化表格字段 (table_id: {table_id})...")
        init_fields(client, LARK_BITABLE_APP_TOKEN, table_id, fields, options, args.dry_run)

    print("\n✨ 完成!")


if __name__ == "__main__":
    main()
