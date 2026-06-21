#!/usr/bin/env python3
"""Check DynaCortex Hub Quarto source conventions without external deps."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ALLOWED_STATUS = {"draft", "standard", "review", "deprecated"}
SOURCE_EXCLUDES = {".git", ".quarto", "_site", "docs", "__pycache__"}
LOCAL_EXTENSIONS = {
    ".bib",
    ".csv",
    ".gif",
    ".html",
    ".jpeg",
    ".jpg",
    ".md",
    ".pdf",
    ".png",
    ".qmd",
    ".svg",
    ".webp",
    ".yml",
    ".yaml",
}


@dataclass
class Message:
    level: str
    path: Path
    text: str


def iter_qmd_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.qmd"):
        if any(part in SOURCE_EXCLUDES for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 0

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}, 0

    data: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.startswith(" ") or raw.startswith("-"):
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, end + 1


def strip_anchor(path_text: str) -> str:
    return path_text.split("#", 1)[0].split("?", 1)[0]


def is_external_link(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
        or lowered.startswith("#")
        or lowered.startswith("@")
    )


def normalize_link_target(target: str) -> str:
    cleaned = target.strip().strip("<>").strip()
    cleaned = cleaned.split("{", 1)[0].strip()
    cleaned = strip_anchor(cleaned)
    return unquote(cleaned)


def local_link_exists(root: Path, source: Path, target: str) -> bool:
    normalized = normalize_link_target(target)
    if not normalized or is_external_link(normalized):
        return True
    if normalized.startswith("/"):
        candidate = root / normalized.lstrip("/")
    else:
        candidate = source.parent / normalized
    return candidate.exists()


def should_check_target(target: str) -> bool:
    normalized = normalize_link_target(target)
    if not normalized or is_external_link(normalized):
        return False
    return Path(normalized).suffix.lower() in LOCAL_EXTENSIONS


def check_frontmatter(path: Path, text: str, root: Path) -> list[Message]:
    messages: list[Message] = []
    data, body_start = parse_frontmatter(text)
    rel = path.relative_to(root)

    if not data:
        return [Message("ERROR", rel, "Missing YAML front matter.")]

    for required in ("title", "status"):
        if not data.get(required):
            messages.append(Message("ERROR", rel, f"Missing required front matter: {required}."))

    if not data.get("description"):
        messages.append(Message("WARN", rel, "Missing recommended front matter: description."))

    status = data.get("status")
    if status and status not in ALLOWED_STATUS:
        messages.append(
            Message(
                "WARN",
                rel,
                f"Unknown status '{status}'. Expected one of: {', '.join(sorted(ALLOWED_STATUS))}.",
            )
        )

    categories = data.get("categories")
    if categories is not None and not (categories.startswith("[") and categories.endswith("]")):
        messages.append(Message("WARN", rel, "Prefer inline categories list: categories: [tag-one, tag-two]."))

    title = data.get("title")
    body = "\n".join(text.splitlines()[body_start:])
    h1 = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    if h1 and title and h1.group(1).strip() != title:
        messages.append(Message("WARN", rel, "H1 does not match front matter title."))

    return messages


def check_links(path: Path, text: str, root: Path) -> list[Message]:
    messages: list[Message] = []
    rel = path.relative_to(root)
    image_targets = re.findall(r"!\[[^\]]*]\(([^)]+)\)", text)
    link_targets = re.findall(r"(?<!!)\[[^\]]+]\(([^)]+)\)", text)

    for target in image_targets:
        if should_check_target(target) and not local_link_exists(root, path, target):
            messages.append(Message("ERROR", rel, f"Missing image asset: {normalize_link_target(target)}"))

    for target in link_targets:
        if should_check_target(target) and not local_link_exists(root, path, target):
            messages.append(Message("WARN", rel, f"Local link target not found: {normalize_link_target(target)}"))

    return messages


def check_quarto_sidebar(root: Path) -> list[Message]:
    config = root / "_quarto.yml"
    if not config.exists():
        return [Message("ERROR", Path("_quarto.yml"), "Missing _quarto.yml.")]

    messages: list[Message] = []
    text = config.read_text(encoding="utf-8")
    candidates = re.findall(r"(?:file:\s*|-\s+)([A-Za-z0-9_./-]+\.qmd)", text)
    for raw in sorted(set(candidates)):
        if not (root / raw).exists():
            messages.append(Message("ERROR", Path("_quarto.yml"), f"Navigation target not found: {raw}"))
    return messages


def run(root: Path) -> list[Message]:
    messages: list[Message] = []
    for path in iter_qmd_files(root):
        text = path.read_text(encoding="utf-8")
        messages.extend(check_frontmatter(path, text, root))
        messages.extend(check_links(path, text, root))
    messages.extend(check_quarto_sidebar(root))
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Quarto project root, default: current directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    messages = run(root)
    errors = [message for message in messages if message.level == "ERROR"]
    warnings = [message for message in messages if message.level == "WARN"]

    for message in messages:
        print(f"{message.level}: {message.path}: {message.text}")

    print(f"Checked {len(iter_qmd_files(root))} QMD file(s): {len(errors)} error(s), {len(warnings)} warning(s).")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
