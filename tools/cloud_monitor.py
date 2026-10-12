#!/usr/bin/env python3
"""Cloud repository audit. Explicitly does not claim access to ChatGPT chats."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

import skill_sync


def tree_fingerprint(root):
    """Git tree IDs let an immutable checkout reuse a previous complete audit."""
    try:
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True)
        if dirty.strip():
            return None
        return {part: subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{part}"], cwd=root, text=True).strip()
            for part in ("registry", "tools")}
    except subprocess.CalledProcessError:
        return None


def audit(root, previous=None):
    fingerprint = tree_fingerprint(root)
    report = {
        "schema": 1,
        "checked_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
        "overall_status": "blocked_source_connection",
        "maintenance_chat_access": "not_connected",
        "maintenance_save_success": "unverified",
        "automatic_maintenance_repair": "not_available",
        "production_session_reads": "unverified",
        "repository_integrity": "unverified",
        "verified_snapshots": 0,
        "audit_tree": fingerprint,
        "skills": {},
        "limitations": [
            "没有读取 ChatGPT 维护会话或已安装技能库的连接，无法判断它是否刚更新。",
            "仓库校验成功不等于 ChatGPT 保存成功，也不等于制作会话已读取。",
            "无法自动修复维护端保存失败；不会回滚规则或伪造成功状态。",
        ],
    }
    try:
        registry = skill_sync.read_json(root / "registry/latest.json")
        skill_sync.require(registry.get("schema") == 1 and set(registry["skills"]) == skill_sync.NAMES,
                           "Invalid registry")
        report["skills"] = {name: {
            "weekly_version": entry.get("weekly_version"), "revision": entry.get("revision"),
            "content_sha256": entry.get("content_sha256"),
            "source_updated_at": entry.get("source_updated_at"),
            "saved_snapshots": len(entry.get("history", [])),
            "import_status": entry.get("sync_status", "unverified"),
        } for name, entry in registry["skills"].items()}
        if (fingerprint and isinstance(previous, dict) and previous.get("schema") == 1
                and previous.get("audit_tree") == fingerprint
                and previous.get("repository_integrity") == "verified"
                and isinstance(previous.get("verified_snapshots"), int)
                and previous["verified_snapshots"] > 0):
            count = previous["verified_snapshots"]
            report["check_mode"] = "unchanged_git_trees_reused_verified_result"
        else:
            _, count = skill_sync.verify(root)
            report["check_mode"] = "full_repository_file_verification"
        report["verified_snapshots"] = count
        report["repository_integrity"] = "verified" if count else "awaiting_real_skill_files"
    except (OSError, ValueError, KeyError, TypeError) as error:
        report["overall_status"] = "repository_integrity_failed"
        report["repository_integrity"] = "failed"
        report["error"] = str(error)
    return report


def markdown(report):
    lines = ["# Skill 云端核验报告", "", f"检查时间：{report['checked_at']}", "",
             f"总体状态：`{report['overall_status']}`", "",
             f"仓库文件：`{report['repository_integrity']}`；已校验历史快照：{report['verified_snapshots']}。",
             "", "| Skill | 周版本 | 修订 | 留存快照 |", "| --- | --- | --- | --- |"]
    for name, entry in report["skills"].items():
        lines.append(f"| {name} | {entry['weekly_version'] or '未收到'} | "
                     f"{entry['revision'] or '未收到'} | {entry['saved_snapshots']} |")
    lines += ["", "## 尚未接通的能力", ""]
    lines.extend(f"- {item}" for item in report["limitations"])
    if report.get("error"):
        lines += ["", "检查错误：", "```", report["error"], "```"]
    if report.get("run_url"):
        lines += ["", f"GitHub Actions 运行记录：{report['run_url']}"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    previous = None
    if args.previous and args.previous.is_file():
        try:
            previous = skill_sync.read_json(args.previous)
        except (OSError, ValueError):
            pass  # Invalid cache never bypasses an actual audit.
    report = audit(args.repo, previous)
    report["execution"] = "github_actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local"
    if report["execution"] == "github_actions":
        report["source_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=args.repo, text=True).strip()
        report["trigger_commit"] = os.environ.get("GITHUB_SHA")
        report["run_url"] = (f"https://github.com/{os.environ['GITHUB_REPOSITORY']}"
                             f"/actions/runs/{os.environ['GITHUB_RUN_ID']}")
        report["event"] = os.environ.get("GITHUB_EVENT_NAME")
    args.output.mkdir(parents=True, exist_ok=True)
    skill_sync.write_json(args.output / "latest.json", report)
    (args.output / "latest.md").write_text(markdown(report), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    # Exit status concerns report generation. The report's explicit status is
    # authoritative; a green workflow is never described as ChatGPT save success.


if __name__ == "__main__":
    main()
