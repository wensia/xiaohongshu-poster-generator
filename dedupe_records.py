#!/usr/bin/env python3
"""
去重飞书多维表格记录
- 拉取所有记录
- 按标题去重
- 删除重复且没有生成套图的记录
"""
import requests
import json
from collections import defaultdict

# 飞书配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

def get_token():
    """获取访问令牌"""
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()["tenant_access_token"]

def fetch_all_records(token):
    """获取所有记录"""
    all_records = []
    page_token = None

    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token

        resp = requests.get(
            f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records",
            headers={"Authorization": f"Bearer {token}"},
            params=params
        )
        data = resp.json()

        if data.get("code") != 0:
            print(f"Error: {data}")
            break

        records = data.get("data", {}).get("items", [])
        all_records.extend(records)

        page_token = data.get("data", {}).get("page_token")
        if not page_token:
            break

    return all_records

def delete_record(token, record_id):
    """删除记录"""
    resp = requests.delete(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return resp.json()

def analyze_duplicates(records):
    """分析重复记录"""
    # 按标题分组
    title_groups = defaultdict(list)

    for record in records:
        fields = record.get("fields", {})
        title = fields.get("标题", "")

        # 提取标题文本（可能是富文本格式）
        if isinstance(title, list):
            title = "".join([t.get("text", "") for t in title])
        elif isinstance(title, dict):
            title = title.get("text", str(title))

        if title:
            title_groups[title].append({
                "record_id": record.get("record_id"),
                "title": title,
                "已生成": fields.get("已生成", False),
                "附件": fields.get("生成图片") or fields.get("附件"),
                "星座": fields.get("星座"),
                "模板": fields.get("模板"),
            })

    return title_groups

def main():
    print("=" * 60)
    print("飞书多维表格记录去重工具")
    print("=" * 60)

    # 1. 获取 token
    print("\n1. 获取访问令牌...")
    token = get_token()
    print("   ✓ 获取成功")

    # 2. 拉取所有记录
    print("\n2. 拉取所有记录...")
    records = fetch_all_records(token)
    print(f"   ✓ 共获取 {len(records)} 条记录")

    # 3. 分析重复
    print("\n3. 分析重复记录...")
    title_groups = analyze_duplicates(records)

    # 找出重复的标题
    duplicates = {title: group for title, group in title_groups.items() if len(group) > 1}

    print(f"   - 唯一标题数: {len(title_groups)}")
    print(f"   - 重复标题数: {len(duplicates)}")

    # 4. 分析需要删除的记录
    to_delete = []

    print("\n4. 重复记录详情:")
    print("-" * 60)

    for title, group in duplicates.items():
        print(f"\n标题: {title}")
        print(f"  重复数量: {len(group)}")

        # 检查每条记录的状态
        has_generated = []
        not_generated = []

        for r in group:
            has_attachment = bool(r["附件"])
            is_generated = r["已生成"] or has_attachment

            info = f"    - {r['record_id'][:8]}... | 已生成: {r['已生成']} | 有附件: {has_attachment}"
            print(info)

            if is_generated:
                has_generated.append(r)
            else:
                not_generated.append(r)

        # 如果有已生成的，删除未生成的
        if has_generated and not_generated:
            for r in not_generated:
                to_delete.append(r)
                print(f"      → 标记删除: {r['record_id'][:8]}... (有其他已生成的记录)")
        # 如果都没生成，保留第一条
        elif not has_generated and len(not_generated) > 1:
            for r in not_generated[1:]:
                to_delete.append(r)
                print(f"      → 标记删除: {r['record_id'][:8]}... (保留第一条)")

    print("\n" + "=" * 60)
    print(f"待删除记录数: {len(to_delete)}")
    print("=" * 60)

    if not to_delete:
        print("\n没有需要删除的记录")
        return

    # 5. 确认删除
    print("\n待删除记录列表:")
    for r in to_delete:
        print(f"  - {r['title']} ({r['record_id'][:8]}...)")

    confirm = input("\n是否确认删除这些记录? (yes/no): ")

    if confirm.lower() == "yes":
        print("\n5. 执行删除...")
        success = 0
        failed = 0

        for r in to_delete:
            result = delete_record(token, r["record_id"])
            if result.get("code") == 0:
                print(f"   ✓ 已删除: {r['title']}")
                success += 1
            else:
                print(f"   ✗ 删除失败: {r['title']} - {result}")
                failed += 1

        print(f"\n删除完成: 成功 {success}, 失败 {failed}")
    else:
        print("\n已取消删除操作")

if __name__ == "__main__":
    main()
