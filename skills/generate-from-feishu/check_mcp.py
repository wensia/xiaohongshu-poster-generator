#!/usr/bin/env python3
"""
飞书 MCP 检测脚本

检查 lark-mcp 是否已安装和配置，并提供安装命令。

Usage:
    python check_mcp.py [--install-cmd] [--check-only]
"""

import sys
import json
import subprocess
import argparse
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 从 config.py 导入配置
from config import LARK_APP_ID, LARK_APP_SECRET

# MCP 需要的权限
REQUIRED_TOOLS = [
    "bitable.v1.app_table.list",
    "bitable.v1.app_table_record.list",
    "bitable.v1.app_table_record.create",
    "bitable.v1.app_table_record.update",
    "bitable.v1.app_table_field.list",
    "bitable.v1.app_table_field.create",
]


def check_mcp_installed() -> dict:
    """
    检查 lark-mcp 是否安装

    Returns:
        {
            "installed": bool,
            "location": "global" | "project" | None,
            "config_path": str | None,
            "has_lark": bool
        }
    """
    result = {
        "installed": False,
        "location": None,
        "config_path": None,
        "has_lark": False
    }

    # 检查项目级 .mcp.json
    project_mcp = PROJECT_ROOT / ".mcp.json"
    if project_mcp.exists():
        try:
            with open(project_mcp, "r") as f:
                config = json.load(f)
                servers = config.get("mcpServers", {})
                if "lark-mcp" in servers or "lark" in servers:
                    result["installed"] = True
                    result["location"] = "project"
                    result["config_path"] = str(project_mcp)
                    result["has_lark"] = True
                    return result
        except:
            pass

    # 检查用户级 MCP 配置
    user_mcp_paths = [
        Path.home() / ".claude" / "mcp.json",
        Path.home() / ".config" / "claude" / "mcp.json",
    ]

    for mcp_path in user_mcp_paths:
        if mcp_path.exists():
            try:
                with open(mcp_path, "r") as f:
                    config = json.load(f)
                    servers = config.get("mcpServers", {})
                    if "lark-mcp" in servers or "lark" in servers:
                        result["installed"] = True
                        result["location"] = "global"
                        result["config_path"] = str(mcp_path)
                        result["has_lark"] = True
                        return result
            except:
                pass

    # 尝试运行 claude mcp list 命令检查
    try:
        proc = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "lark" in proc.stdout.lower():
            result["installed"] = True
            result["location"] = "global"
            result["has_lark"] = True
    except:
        pass

    return result


def check_env_config() -> dict:
    """
    检查环境变量配置

    Returns:
        {
            "has_app_id": bool,
            "has_app_secret": bool,
            "app_id": str (masked),
            "complete": bool
        }
    """
    result = {
        "has_app_id": bool(LARK_APP_ID and LARK_APP_ID != "cli_xxxxxxxxxx"),
        "has_app_secret": bool(LARK_APP_SECRET and "xxx" not in LARK_APP_SECRET),
        "app_id": LARK_APP_ID[:10] + "..." if LARK_APP_ID else "",
        "complete": False
    }
    result["complete"] = result["has_app_id"] and result["has_app_secret"]
    return result


def generate_install_command(app_id: str = None, app_secret: str = None) -> str:
    """生成 MCP 安装命令"""
    aid = app_id or LARK_APP_ID or "<APP_ID>"
    asec = app_secret or LARK_APP_SECRET or "<APP_SECRET>"

    tools = ",".join(REQUIRED_TOOLS)

    cmd = f'''claude mcp add lark-mcp -s user -- npx -y @anthropic-ai/lark-mcp mcp \\
  -a {aid} \\
  -s {asec} \\
  -t {tools}'''

    return cmd


def generate_project_mcp_config() -> dict:
    """生成项目级 .mcp.json 配置"""
    return {
        "mcpServers": {
            "lark-mcp": {
                "command": "npx",
                "args": [
                    "-y",
                    "@anthropic-ai/lark-mcp",
                    "mcp",
                    "-a", LARK_APP_ID or "<APP_ID>",
                    "-s", LARK_APP_SECRET or "<APP_SECRET>",
                    "-t", ",".join(REQUIRED_TOOLS)
                ]
            }
        }
    }


def print_status(mcp_status: dict, env_status: dict):
    """打印检测状态"""
    print("\n" + "=" * 60)
    print("飞书 MCP 配置检测")
    print("=" * 60)

    # 环境变量状态
    print("\n📋 环境变量配置:")
    if env_status["complete"]:
        print(f"  ✅ LARK_APP_ID: {env_status['app_id']}")
        print(f"  ✅ LARK_APP_SECRET: 已配置")
    else:
        if not env_status["has_app_id"]:
            print("  ❌ LARK_APP_ID: 未配置")
        else:
            print(f"  ✅ LARK_APP_ID: {env_status['app_id']}")
        if not env_status["has_app_secret"]:
            print("  ❌ LARK_APP_SECRET: 未配置")
        else:
            print("  ✅ LARK_APP_SECRET: 已配置")

    # MCP 状态
    print("\n🔌 MCP 服务状态:")
    if mcp_status["installed"] and mcp_status["has_lark"]:
        print(f"  ✅ lark-mcp 已安装")
        print(f"  📍 位置: {mcp_status['location']}")
        if mcp_status["config_path"]:
            print(f"  📁 配置: {mcp_status['config_path']}")
    else:
        print("  ❌ lark-mcp 未安装")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="检测飞书 MCP 安装状态")
    parser.add_argument("--install-cmd", action="store_true", help="输出安装命令")
    parser.add_argument("--check-only", action="store_true", help="仅检测，不输出详情")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--project-config", action="store_true", help="生成项目级配置")
    args = parser.parse_args()

    mcp_status = check_mcp_installed()
    env_status = check_env_config()

    if args.json:
        print(json.dumps({
            "mcp": mcp_status,
            "env": env_status,
            "ready": mcp_status["has_lark"] and env_status["complete"]
        }, indent=2))
        return

    if args.check_only:
        if mcp_status["has_lark"] and env_status["complete"]:
            print("ready")
            sys.exit(0)
        else:
            print("not_ready")
            sys.exit(1)

    if args.project_config:
        config = generate_project_mcp_config()
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return

    # 打印状态
    print_status(mcp_status, env_status)

    # 如果需要安装
    if not mcp_status["has_lark"]:
        print("\n📦 安装命令:")
        print("-" * 60)

        if not env_status["complete"]:
            print("\n⚠️  请先在 config.py 中配置 LARK_APP_ID 和 LARK_APP_SECRET")
            print("\n示例命令（请替换占位符）:\n")

        print(generate_install_command())

        print("\n" + "-" * 60)
        print("\n💡 或者添加到项目 .mcp.json:")
        print(json.dumps(generate_project_mcp_config(), indent=2, ensure_ascii=False))

    if args.install_cmd:
        print("\n" + generate_install_command())

    # 返回状态码
    if mcp_status["has_lark"] and env_status["complete"]:
        print("\n✨ 配置完成，可以使用飞书 MCP！")
        sys.exit(0)
    else:
        print("\n⚠️  请完成上述配置后再使用")
        sys.exit(1)


if __name__ == "__main__":
    main()
