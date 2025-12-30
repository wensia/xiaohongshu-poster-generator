#!/usr/bin/env python3
"""
MCP 状态检查器 - 统一检查各 MCP 服务的安装和运行状态

在执行需要 MCP 的操作前调用此脚本，确保服务正常运行。
如果检查失败会立即中断并给出明确提示。

Usage:
    python mcp_checker.py --check lark          # 检查飞书 MCP
    python mcp_checker.py --check xiaohongshu   # 检查小红书 MCP
    python mcp_checker.py --check all           # 检查所有 MCP
    python mcp_checker.py --check xiaohongshu --auto-start  # 自动启动服务
    python mcp_checker.py --check xiaohongshu --auto-login  # 自动启动登录工具

Exit codes:
    0 - 所有检查通过
    1 - 检查失败，需要用户操作
    2 - 参数错误
"""

import sys
import json
import socket
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 从 config.py 导入配置
from config import (
    LARK_APP_ID,
    LARK_APP_SECRET,
    LARK_BITABLES,
    DEFAULT_BITABLE,
    get_bitable
)

# 小红书 MCP 配置
XHS_MCP_DIR = PROJECT_ROOT / "xiaohongshu-mcp"
XHS_MCP_BIN = XHS_MCP_DIR / "xiaohongshu-mcp-darwin-arm64"
XHS_LOGIN_BIN = XHS_MCP_DIR / "xiaohongshu-login-darwin-arm64"
XHS_COOKIES = XHS_MCP_DIR / "cookies.json"
XHS_MCP_PORT = 18060

# 获取默认表格配置
_default_bitable = get_bitable()
LARK_APP_TOKEN = _default_bitable.get("app_token", "")
LARK_TABLE_ID = _default_bitable.get("table_id", "")


class MCPCheckResult:
    """MCP 检查结果"""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.actions: List[str] = []  # 需要用户执行的操作
        self.details: Dict = {}

    def add_error(self, msg: str, action: str = None):
        self.errors.append(msg)
        if action:
            self.actions.append(action)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def is_ready(self) -> bool:
        return self.passed and len(self.errors) == 0


def check_port(port: int, host: str = "localhost") -> bool:
    """检查端口是否开放"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        return sock.connect_ex((host, port)) == 0
    except:
        return False
    finally:
        sock.close()


def check_lark_mcp() -> MCPCheckResult:
    """检查飞书 MCP 状态"""
    result = MCPCheckResult("飞书 MCP (lark-mcp)")

    # 1. 检查配置
    if not LARK_APP_ID or LARK_APP_ID == "cli_xxxxxxxxxx":
        result.add_error(
            "LARK_APP_ID 未配置",
            "在 config.py 中设置 LARK_APP_ID"
        )

    if not LARK_APP_SECRET or "xxx" in LARK_APP_SECRET:
        result.add_error(
            "LARK_APP_SECRET 未配置",
            "在 config.py 中设置 LARK_APP_SECRET"
        )

    if not LARK_APP_TOKEN:
        result.add_error(
            "LARK_BITABLE_APP_TOKEN 未配置",
            "在 config.py 的 LARK_BITABLES 中设置 app_token"
        )

    if not LARK_TABLE_ID:
        result.add_error(
            "LARK_BITABLE_TABLE_ID 未配置",
            "在 config.py 的 LARK_BITABLES 中设置 table_id"
        )

    # 2. 检查 MCP 配置文件
    mcp_config_path = PROJECT_ROOT / ".mcp.json"
    has_lark_mcp = False

    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, "r") as f:
                config = json.load(f)
                servers = config.get("mcpServers", {})
                if "lark-mcp" in servers or "lark" in servers:
                    has_lark_mcp = True
                    result.details["config_location"] = "project (.mcp.json)"
        except:
            pass

    # 检查用户级配置
    if not has_lark_mcp:
        user_paths = [
            Path.home() / ".claude" / "mcp.json",
            Path.home() / ".config" / "claude" / "mcp.json",
        ]
        for p in user_paths:
            if p.exists():
                try:
                    with open(p, "r") as f:
                        config = json.load(f)
                        if "lark-mcp" in config.get("mcpServers", {}):
                            has_lark_mcp = True
                            result.details["config_location"] = f"user ({p})"
                            break
                except:
                    pass

    if not has_lark_mcp:
        result.add_error(
            "lark-mcp 未配置",
            f"""运行以下命令安装:
claude mcp add lark-mcp -s user -- npx -y @larksuiteoapi/lark-mcp mcp \\
  -a {LARK_APP_ID or '<APP_ID>'} \\
  -s {LARK_APP_SECRET or '<APP_SECRET>'} \\
  -t bitable.v1.app_table.list,bitable.v1.app_table_record.list,bitable.v1.app_table_record.create,bitable.v1.app_table_record.update,bitable.v1.app_table_field.list"""
        )

    result.passed = len(result.errors) == 0
    result.details["has_config"] = has_lark_mcp
    result.details["env_configured"] = bool(LARK_APP_ID and LARK_APP_SECRET)

    return result


def check_xiaohongshu_mcp(auto_start: bool = False, auto_login: bool = False) -> MCPCheckResult:
    """检查小红书 MCP 状态"""
    result = MCPCheckResult("小红书 MCP (xiaohongshu)")

    # 1. 检查二进制文件
    if not XHS_MCP_BIN.exists():
        result.add_error(
            f"xiaohongshu-mcp 二进制文件不存在: {XHS_MCP_BIN}",
            "请从 https://github.com/xpzouying/xiaohongshu-mcp 下载对应版本"
        )
        return result

    result.details["bin_exists"] = True

    # 2. 检查 MCP 服务是否运行
    service_running = check_port(XHS_MCP_PORT)
    result.details["service_running"] = service_running

    if not service_running:
        if auto_start:
            # 尝试自动启动
            try:
                subprocess.Popen(
                    [str(XHS_MCP_BIN), "-headless=true"],
                    cwd=str(XHS_MCP_DIR),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("  正在启动 xiaohongshu-mcp 服务...")
                import time
                time.sleep(2)
                service_running = check_port(XHS_MCP_PORT)
                result.details["service_running"] = service_running
                if service_running:
                    print("  ✅ 服务启动成功")
            except Exception as e:
                result.add_error(f"自动启动失败: {e}")

        if not service_running:
            result.add_error(
                "xiaohongshu-mcp 服务未运行",
                f"cd {XHS_MCP_DIR} && ./xiaohongshu-mcp-darwin-arm64 -headless=true &"
            )
            return result

    # 3. 检查登录状态
    cookies_valid = False
    if XHS_COOKIES.exists():
        try:
            with open(XHS_COOKIES, "r") as f:
                cookies = json.load(f)
                if cookies and len(cookies) > 0:
                    cookies_valid = True
                    result.details["cookies_count"] = len(cookies)
        except:
            pass

    result.details["cookies_valid"] = cookies_valid

    if not cookies_valid:
        if auto_login and XHS_LOGIN_BIN.exists():
            # 启动登录工具
            print("  正在启动登录工具，请用小红书 App 扫码...")
            try:
                subprocess.run(
                    [str(XHS_LOGIN_BIN)],
                    cwd=str(XHS_MCP_DIR),
                    timeout=120
                )
                # 重新检查
                if XHS_COOKIES.exists():
                    with open(XHS_COOKIES, "r") as f:
                        cookies = json.load(f)
                        if cookies and len(cookies) > 0:
                            cookies_valid = True
                            result.details["cookies_valid"] = True
                            print("  ✅ 登录成功")
            except subprocess.TimeoutExpired:
                result.add_error("登录超时")
            except Exception as e:
                result.add_error(f"登录失败: {e}")

        if not cookies_valid:
            result.add_error(
                "小红书未登录",
                f"cd {XHS_MCP_DIR} && ./xiaohongshu-login-darwin-arm64"
            )

    # 4. 检查 .mcp.json 配置
    mcp_config = PROJECT_ROOT / ".mcp.json"
    has_xhs_config = False

    if mcp_config.exists():
        try:
            with open(mcp_config, "r") as f:
                config = json.load(f)
                if "xiaohongshu" in config.get("mcpServers", {}):
                    has_xhs_config = True
        except:
            pass

    if not has_xhs_config:
        result.add_warning("xiaohongshu MCP 未在 .mcp.json 中配置（可能使用的是其他配置方式）")

    result.details["has_config"] = has_xhs_config
    result.passed = len(result.errors) == 0

    return result


def print_result(result: MCPCheckResult, verbose: bool = True):
    """打印检查结果"""
    status = "✅" if result.passed else "❌"
    print(f"\n{status} {result.name}")

    if verbose and result.details:
        for key, value in result.details.items():
            print(f"   {key}: {value}")

    for warning in result.warnings:
        print(f"   ⚠️  {warning}")

    for error in result.errors:
        print(f"   ❌ {error}")

    if result.actions:
        print(f"\n   📋 需要执行的操作:")
        for i, action in enumerate(result.actions, 1):
            print(f"   {i}. {action}")


def print_summary(results: List[MCPCheckResult]):
    """打印检查总结"""
    print("\n" + "=" * 60)

    all_passed = all(r.passed for r in results)

    if all_passed:
        print("✅ 所有 MCP 检查通过，可以继续执行")
    else:
        print("❌ MCP 检查未通过，请按照上述提示操作后重试")
        print("\n💡 快速修复:")

        all_actions = []
        for r in results:
            all_actions.extend(r.actions)

        for i, action in enumerate(all_actions, 1):
            print(f"\n   步骤 {i}:")
            print(f"   {action}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="MCP 状态检查器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --check lark              检查飞书 MCP
  %(prog)s --check xiaohongshu       检查小红书 MCP
  %(prog)s --check all               检查所有 MCP
  %(prog)s --check xiaohongshu --auto-start   自动启动服务
  %(prog)s --check xiaohongshu --auto-login   自动启动登录
"""
    )
    parser.add_argument(
        "--check", "-c",
        choices=["lark", "xiaohongshu", "xhs", "all"],
        required=True,
        help="要检查的 MCP 服务"
    )
    parser.add_argument(
        "--auto-start",
        action="store_true",
        help="自动启动未运行的服务"
    )
    parser.add_argument(
        "--auto-login",
        action="store_true",
        help="自动启动登录工具（小红书）"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 格式输出"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，仅返回状态码"
    )

    args = parser.parse_args()

    results = []

    # 执行检查
    if args.check in ["lark", "all"]:
        results.append(check_lark_mcp())

    if args.check in ["xiaohongshu", "xhs", "all"]:
        results.append(check_xiaohongshu_mcp(
            auto_start=args.auto_start,
            auto_login=args.auto_login
        ))

    # 输出结果
    if args.json:
        output = {
            "ready": all(r.passed for r in results),
            "checks": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "errors": r.errors,
                    "warnings": r.warnings,
                    "actions": r.actions,
                    "details": r.details
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif not args.quiet:
        print("\n" + "=" * 60)
        print("MCP 状态检查")
        print("=" * 60)

        for result in results:
            print_result(result)

        print_summary(results)

    # 返回状态码
    if all(r.passed for r in results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
