#!/usr/bin/env python3
"""Create a DynaCortex Hub Quarto topic scaffold."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


VALID_KINDS = {
    "implementation",
    "note",
    "experiment",
    "troubleshooting",
    "reference",
    "literature",
    "report",
    "inbox",
}


SECTION_DEFAULT_KIND = {
    "01-system-foundations": "reference",
    "02-implementation": "implementation",
    "03-experiments": "experiment",
    "04-reference": "reference",
    "05-literature": "literature",
    "06-reports": "report",
    "07-inbox": "inbox",
    "08-notes": "note",
    "09-troubleshooting": "troubleshooting",
}


def slugify(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def frontmatter(title: str, kind: str, author: str | None) -> str:
    lines = [
        "---",
        f'title: "{title}"',
        'description: "TBD"',
        f"categories: [{kind}]",
        "status: draft",
    ]
    if author:
        lines.extend(
            [
                "date: last-modified",
                "date-format: DD/MM/YYYY HH:mm:ssZ[Z]",
                f'author: "{author}"',
            ]
        )
    lines.append("---")
    return "\n".join(lines)


def body_for_kind(title: str, kind: str) -> str:
    sections = {
        "note": [
            "Mục tiêu",
            "Ý tưởng chính",
            "Công thức / khái niệm",
            "Liên quan đến DynaCortex",
            "Ghi chú thêm",
        ],
        "experiment": [
            "1. Mục tiêu",
            "2. Giả thuyết",
            "3. Setup",
            "4. Quy trình",
            "5. Kết quả",
            "6. Phân tích",
            "7. Kết luận",
        ],
        "troubleshooting": [
            "Triệu chứng",
            "Nguyên nhân có thể",
            "Cách kiểm tra nhanh",
            "Cách xử lý",
            "Lệnh liên quan",
        ],
        "implementation": [
            "Mục tiêu",
            "Phần cứng / phần mềm cần chuẩn bị",
            "Tóm tắt cấu hình",
            "Quy trình thực hiện",
            "Kiểm tra sau khi hoàn tất",
            "Lỗi thường gặp",
            "Tài liệu và nguồn tham khảo",
        ],
        "reference": ["Mục đích", "Bảng tra cứu", "Lệnh liên quan", "Ghi chú"],
        "literature": ["Thông tin bài báo", "Ý tưởng chính", "Liên quan đến DynaCortex", "Ghi chú"],
        "report": ["Tóm tắt", "Bối cảnh", "Phương pháp", "Kết quả", "Kết luận"],
        "inbox": ["Ý tưởng", "Ngữ cảnh", "Việc cần xử lý tiếp"],
    }[kind]
    headings = "\n\n".join(f"## {section}" for section in sections)
    return f"# {title}\n\n{headings}\n"


def create_topic(root: Path, section: str, topic: str, title: str | None, kind: str | None, author: str | None) -> Path:
    slug = slugify(topic)
    if not slug:
        raise ValueError("Topic slug is empty after normalization.")

    section_dir = root / section
    if not section_dir.exists():
        raise FileNotFoundError(f"Section folder does not exist: {section}")

    resolved_kind = kind or SECTION_DEFAULT_KIND.get(section, "note")
    if resolved_kind not in VALID_KINDS:
        raise ValueError(f"Invalid kind '{resolved_kind}'. Expected one of: {', '.join(sorted(VALID_KINDS))}")

    page_title = title or title_from_slug(slug)
    topic_dir = section_dir / slug
    index_file = topic_dir / "index.qmd"
    if index_file.exists():
        raise FileExistsError(f"Page already exists: {index_file}")

    for subdir in ("assets/images", "assets/diagrams", "assets/tables", "assets/exports"):
        (topic_dir / subdir).mkdir(parents=True, exist_ok=True)

    content = f"{frontmatter(page_title, resolved_kind, author)}\n\n{body_for_kind(page_title, resolved_kind)}"
    index_file.write_text(content, encoding="utf-8")
    return index_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("section", help="Section folder, e.g. 02-implementation")
    parser.add_argument("topic", help="Topic slug or title; normalized to kebab-case")
    parser.add_argument("--root", default=".", help="Quarto project root, default: current directory")
    parser.add_argument("--title", help="Human-readable page title")
    parser.add_argument("--kind", choices=sorted(VALID_KINDS), help="Page type/template")
    parser.add_argument("--author", help="Optional author name to include with last-modified date")
    args = parser.parse_args()

    try:
        index_file = create_topic(
            root=Path(args.root).resolve(),
            section=args.section,
            topic=args.topic,
            title=args.title,
            kind=args.kind,
            author=args.author,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(index_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
