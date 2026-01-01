#!/usr/bin/env python3
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import config


DEFAULT_MCP_URL = "http://localhost:18060/mcp"


class McpClient:
    def __init__(self, url: str, timeout: int = 60) -> None:
        self.url = url
        self.timeout = timeout
        self.session_id: str | None = None
        self._next_id = 1

    def initialize(self) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": self._allocate_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "xhs-notes-analyze", "version": "0.1.0"},
            },
        }
        result = self._request(payload)
        self._notify("notifications/initialized")
        return result

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None, timeout: int | None = None) -> Any:
        payload = {
            "jsonrpc": "2.0",
            "id": self._allocate_id(),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        }
        response = self._request(payload, timeout=timeout)
        if "error" in response:
            raise RuntimeError(f"tool call error: {response['error']}")
        result = response.get("result", {})
        if result.get("isError"):
            raise RuntimeError(f"tool call failed: {result}")
        content = result.get("content", [])
        text_items = [item.get("text") for item in content if item.get("type") == "text" and item.get("text")]
        if len(text_items) == 1:
            return _try_json(text_items[0])
        return result

    def _notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        self._request(payload)

    def _allocate_id(self) -> int:
        current = self._next_id
        self._next_id += 1
        return current

    def _request(self, payload: dict[str, Any], timeout: int | None = None) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id
        request = Request(self.url, data=data, headers=headers, method="POST")
        try:
            with urlopen(request, timeout=timeout or self.timeout) as response:
                body = response.read().decode("utf-8")
                session_id = response.headers.get("mcp-session-id")
                if session_id:
                    self.session_id = session_id
                return json.loads(body) if body else {}
        except HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8")
            except Exception:
                detail = ""
            raise RuntimeError(f"mcp request failed: {exc} {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"mcp request failed: {exc}") from exc


def _try_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _parse_count(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return 0
    text = text.replace(",", "")
    lower = text.lower()
    if lower.endswith("万"):
        return int(float(lower[:-1]) * 10000)
    if lower.endswith("w"):
        return int(float(lower[:-1]) * 10000)
    if lower.endswith("k"):
        return int(float(lower[:-1]) * 1000)
    try:
        return int(float(lower))
    except ValueError:
        return 0


def _extract_interactions(items: list[dict[str, Any]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        key = item.get("type")
        if not key:
            continue
        result[key] = _parse_count(item.get("count"))
    return result


def _build_note_rows(feeds: list[dict[str, Any]], followers: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for feed in feeds:
        note = feed.get("noteCard", {})
        interact = note.get("interactInfo", {})
        likes = _parse_count(interact.get("likedCount"))
        collects = _parse_count(interact.get("collectedCount"))
        comments = _parse_count(interact.get("commentCount"))
        shares = _parse_count(interact.get("sharedCount"))
        engagement = likes + collects + comments + shares
        row = {
            "note_id": feed.get("id", ""),
            "title": note.get("displayTitle", ""),
            "note_type": note.get("type", ""),
            "likes": likes,
            "collects": collects,
            "comments": comments,
            "shares": shares,
            "engagement": engagement,
            "engagement_rate": round(engagement / followers, 6) if followers else 0,
            "xsec_token": feed.get("xsecToken", ""),
        }
        rows.append(row)
    return rows


def _summarize(notes: list[dict[str, Any]]) -> dict[str, Any]:
    total_notes = len(notes)
    totals = {
        "likes": sum(item["likes"] for item in notes),
        "collects": sum(item["collects"] for item in notes),
        "comments": sum(item["comments"] for item in notes),
        "shares": sum(item["shares"] for item in notes),
        "engagement": sum(item["engagement"] for item in notes),
    }
    averages = {
        key: round(value / total_notes, 2) if total_notes else 0
        for key, value in totals.items()
    }
    type_counts: dict[str, int] = {}
    for item in notes:
        note_type = item.get("note_type") or "unknown"
        type_counts[note_type] = type_counts.get(note_type, 0) + 1

    def top_by(metric: str, limit: int = 5) -> list[dict[str, Any]]:
        return [
            {
                "note_id": item["note_id"],
                "title": item["title"],
                metric: item[metric],
            }
            for item in sorted(notes, key=lambda n: n[metric], reverse=True)[:limit]
        ]

    return {
        "total_notes": total_notes,
        "totals": totals,
        "averages": averages,
        "note_types": type_counts,
        "top_by_likes": top_by("likes"),
        "top_by_engagement": top_by("engagement"),
        "top_by_collects": top_by("collects"),
        "top_by_comments": top_by("comments"),
        "top_by_shares": top_by("shares"),
    }


def _write_outputs(output_dir: Path, profile: dict[str, Any], notes: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "xhs_notes_profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "xhs_notes_notes.json").write_text(
        json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "xhs_notes_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    csv_path = output_dir / "xhs_notes.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "note_id",
                "title",
                "note_type",
                "likes",
                "collects",
                "comments",
                "shares",
                "engagement",
                "engagement_rate",
                "xsec_token",
            ],
        )
        writer.writeheader()
        writer.writerows(notes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and analyze Xiaohongshu notes via MCP.")
    parser.add_argument("--user-id", default=config.XIAOHONGSHU_USER_ID)
    parser.add_argument("--nickname", default=config.XIAOHONGSHU_NICKNAME)
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL)
    parser.add_argument("--output-dir", default=str(config.OUTPUT_DIR))
    parser.add_argument("--no-write", action="store_true", help="Only print summary, skip file output.")
    args = parser.parse_args()

    client = McpClient(args.mcp_url, timeout=90)
    client.initialize()

    search = client.call_tool("search_feeds", {"keyword": args.nickname})
    feeds = search.get("feeds", [])
    if not feeds:
        raise RuntimeError("search_feeds returned no results; check nickname or login status.")

    xsec_token = None
    for feed in feeds:
        user = feed.get("noteCard", {}).get("user", {})
        if user.get("userId") == args.user_id:
            xsec_token = feed.get("xsecToken")
            break
    if not xsec_token:
        xsec_token = feeds[0].get("xsecToken")
    if not xsec_token:
        raise RuntimeError("unable to locate xsec_token from search results.")

    profile = client.call_tool(
        "user_profile",
        {"user_id": args.user_id, "xsec_token": xsec_token},
        timeout=180,
    )

    interactions = _extract_interactions(profile.get("interactions", []))
    followers = interactions.get("fans", 0)
    notes = _build_note_rows(profile.get("feeds", []), followers)
    summary = _summarize(notes)
    summary.update(
        {
            "user_id": args.user_id,
            "nickname": profile.get("userBasicInfo", {}).get("nickname", args.nickname),
            "desc": profile.get("userBasicInfo", {}).get("desc", ""),
            "followers": followers,
            "follows": interactions.get("follows", 0),
            "likes_and_collects_total": interactions.get("interaction", 0),
        }
    )

    if not args.no_write:
        _write_outputs(Path(args.output_dir), profile, notes, summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
