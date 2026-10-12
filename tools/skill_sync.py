#!/usr/bin/env python3
"""Manual saved-source import. Standard library only; no chat access or polling."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile, ZIP_DEFLATED

NAMES = {"script-visual-assets", "script-video-shot-director", "manga-reasoning-storyboard"}
ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tree_id(files):
    return digest(json.dumps(files, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def safe_path(value):
    p = PurePosixPath(value)
    require(value and not p.is_absolute() and ".." not in p.parts and "\\" not in value
            and str(p) == value and value != ".", f"Unsafe relative path: {value}")
    return value


def inventory(folder):
    require(folder.is_dir() and not folder.is_symlink(), f"Missing/unsafe directory: {folder}")
    files = {}
    for p in sorted(folder.rglob("*")):
        require(not p.is_symlink(), f"Symlink not allowed: {p}")
        if p.is_dir():
            continue
        require(p.is_file(), f"Non-regular file: {p}")
        relative = safe_path(p.relative_to(folder).as_posix())
        files[relative] = digest(p.read_bytes())
    return files


def timestamp(value):
    date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(date.tzinfo is not None, "Source timestamp must include timezone")
    require(date <= datetime.now(timezone.utc), "Source save timestamp is in the future")
    return date


def version(value):
    require(re.fullmatch(r"1\.(0|[1-9][0-9]*)", value), "Expected maintenance version 1.N")
    return tuple(map(int, value.split(".")))


def check_links(folder):
    # Check ordinary inline local Markdown links. Dynamic script dependencies still
    # need the maintenance author's complete inventory and dependency review.
    for p in folder.rglob("*.md"):
        content = p.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", content):
            url = urlsplit(target.strip("<>"))
            if url.scheme or url.netloc or not url.path:
                continue
            q = (p.parent / unquote(url.path)).resolve()
            require(q.is_relative_to(folder.resolve()) and q.exists(),
                    f"Missing/out-of-bundle Markdown reference: {p.name} -> {target}")


def verify_entry(root, entry):
    snapshot = root / safe_path(entry["snapshot"])
    require(snapshot.resolve().is_relative_to(root.resolve()), "Snapshot escapes repository")
    payload = snapshot / "payload"
    actual = inventory(payload)
    require(actual == entry["files"], f"Changed, missing or extra files: {snapshot}")
    require(tree_id(actual) == entry["content_sha256"], f"Content digest mismatch: {snapshot}")
    source = read_json(snapshot / "source.json")
    require(source == {k: v for k, v in entry.items() if k != "history"},
            f"Source metadata mismatch: {snapshot}")
    check_links(payload)


def verify(root):
    registry = read_json(root / "registry/latest.json")
    require(registry.get("schema") == 1 and set(registry["skills"]) == NAMES, "Invalid registry")
    count = 0
    for name, current in registry["skills"].items():
        previous = None
        for historical in current["history"]:
            require(historical["name"] == name, "Skill history name mismatch")
            require(historical["parent_content_sha256"] == previous, "Broken history chain")
            verify_entry(root, historical)
            previous = historical["content_sha256"]
            count += 1
        if current.get("snapshot"):
            require(current["history"] and all(current[k] == v for k, v in current["history"][-1].items()),
                    "Latest entry does not match history tip")
            verify_entry(root, current)
        else:
            require(not current["history"], "Missing current pointer")
    return registry, count


def import_bundle(root, bundle):
    registry, _ = verify(root)
    require(not bundle.is_symlink(), "Bundle root cannot be a symlink")
    metadata = read_json(bundle / "release.json")
    require(metadata.get("schema") == 1 and metadata.get("source_saved") is True,
            "Only confirmed saved maintenance exports can be imported")
    require(metadata.get("source") == "chatgpt-maintenance", "Maintenance must remain the authority")
    require(bool(metadata.get("save_evidence", "").strip()), "Missing maintenance save evidence/confirmation")
    require(isinstance(metadata.get("skills"), list) and metadata["skills"], "Empty export")
    planned, seen = [], set()
    now = datetime.now(timezone.utc).isoformat()
    for item in metadata["skills"]:
        name = item["name"]
        require(name in NAMES and name not in seen, "Unknown or duplicate Skill")
        seen.add(name)
        old = registry["skills"][name]
        require(bool(item["revision"].strip()), "Missing source revision")
        v = version(item["weekly_version"])
        saved = timestamp(item["source_updated_at"])
        folder = bundle / name
        actual = inventory(folder)
        require("SKILL.md" in actual, f"{name}: missing SKILL.md")
        require(actual == item["files"], f"{name}: full file inventory / SHA-256 mismatch")
        check_links(folder)
        content = tree_id(actual)
        if old.get("snapshot") and all(item[k] == old[k] for k in
                ("weekly_version", "revision", "source_updated_at", "parent_content_sha256", "files")):
            continue  # Exact replay is a no-op, including after later updates to other Skills.
        require(item["parent_content_sha256"] == old.get("content_sha256"),
                f"{name}: stale parent; obtain an export based on the current saved-source revision")
        if old.get("snapshot"):
            require(v >= version(old["weekly_version"]), f"{name}: version rollback rejected")
            require(saved > timestamp(old["source_updated_at"]), f"{name}: stale save timestamp")
            require(item["revision"] not in {e["revision"] for e in old["history"]},
                    f"{name}: reused revision identifier")
            require(content not in {e["content_sha256"] for e in old["history"][:-1]},
                    f"{name}: obsolete content restoration rejected")
        prior_files = set(old.get("files", {}))
        removed = sorted(prior_files - set(actual))
        withdrawn = set(old.get("withdrawn_paths", []))
        restored = withdrawn & set(actual)
        require(restored == set(item.get("restored_paths", [])),
                f"{name}: restoring withdrawn files requires exact maintenance restored_paths declaration")
        snapshot = f"registry/snapshots/{name}/{digest((item['revision'] + ':' + content).encode())}"
        entry = {**item, "content_sha256": content, "snapshot": snapshot,
                 "source": metadata["source"], "save_evidence": metadata["save_evidence"],
                 "imported_at": now, "sync_status": "manual_import_local",
                 "verification_status": "file_hashes_and_inline_links_verified",
                 "source_authenticity": "maintenance_confirmation_not_independently_verified",
                 "source_saved_confirmed": True, "dynamic_dependencies": "unverified",
                 "production_read_status": "unverified", "removed_paths": removed,
                 "withdrawn_paths": sorted((withdrawn | set(removed)) - restored)}
        registry["skills"][name] = {**entry, "history": old["history"] + [entry]}
        planned.append((folder, snapshot, entry))
    # Reject unlisted top-level files/Skills, so nothing in a declared export is silently omitted.
    require({p.name for p in bundle.iterdir()} == seen | {"release.json"}, "Unlisted bundle entries")
    if not planned:
        return {"imported": [], "result": "identical_export_no_change"}
    registry_path = root / "registry"
    with tempfile.TemporaryDirectory(prefix=".import-", dir=registry_path) as temporary:
        stage = Path(temporary)
        for index, (folder, relative, entry) in enumerate(planned):
            staged = stage / str(index)
            staged.mkdir()
            shutil.copytree(folder, staged / "payload")
            write_json(staged / "source.json", entry)
            require(inventory(staged / "payload") == entry["files"], "Source changed during import")
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                verify_entry(root, entry)  # Safe retry after an interrupted pointer update.
            else:
                staged.rename(target)
        registry["channels"]["maintenance_to_codex"] = "manual_import"
        registry["channels"]["codex_to_github"] = "pending_push"
        write_json(stage / "latest.json", registry)
        os.replace(stage / "latest.json", registry_path / "latest.json")
    return {"imported": [e[2]["name"] for e in planned], "production_read": "unverified"}


def export_bundle(root, output):
    registry, _ = verify(root)
    active = [s for s in registry["skills"].values() if s.get("snapshot")]
    require(active, "No real Skill imported; cannot export a production bundle")
    require(not output.exists(), "Refusing to overwrite an existing export")
    with ZipFile(output, "x", ZIP_DEFLATED) as archive:
        archive.writestr("latest.json", json.dumps(registry, ensure_ascii=False, indent=2))
        for s in active:
            for filename in s["files"]:
                archive.write(root / s["snapshot"] / "payload" / filename, f"{s['name']}/{filename}")
        archive.write(root / "docs/production-access.md", "production-access.md")
    return {"export": str(output), "sha256": digest(output.read_bytes()), "production_read": "unverified"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("verify")
    importer = sub.add_parser("import")
    importer.add_argument("bundle", type=Path)
    exporter = sub.add_parser("export")
    exporter.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "import":
            result = import_bundle(args.repo, args.bundle)
        elif args.command == "export":
            result = export_bundle(args.repo, args.output)
        elif args.command == "verify":
            _, count = verify(args.repo)
            result = {"verified_snapshots": count, "skill_behavior": "unverified", "production_read": "unverified"}
        else:
            # Lightweight preflight: read only the manifest, never full Skill files.
            result = read_json(args.repo / "registry/latest.json")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
