#!/usr/bin/env python3
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "translations" / "zh_blocks_template"
OVERRIDE_DIR = ROOT / "translations" / "zh_blocks_overrides"
OUT_DIR = ROOT / "translations" / "zh_blocks"
INLINE_PLACEHOLDER_RE = re.compile(r"⟦(\d+)⟧")
INLINE_TAGS = {"a", "code", "cite", "em", "span"}


def inline_fragments(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find()
    if root is None:
        return []
    fragments = []
    for tag in root.find_all(INLINE_TAGS):
        if any(isinstance(parent, Tag) and parent.name in INLINE_TAGS for parent in tag.parents if parent is not root):
            continue
        fragments.append(str(tag))
    return fragments


def resolve_placeholders(source_item: dict, zh: str) -> str:
    if "⟦" not in zh:
        return zh
    fragments = inline_fragments(source_item.get("html", ""))

    def replace(match: re.Match[str]) -> str:
        index = int(match.group(1))
        if index >= len(fragments):
            raise ValueError(f"{source_item['id']} uses missing inline placeholder ⟦{index}⟧")
        return fragments[index]

    return INLINE_PLACEHOLDER_RE.sub(replace, zh)


def load_overrides(stem: str) -> dict[str, str]:
    paths = []
    single_file = OVERRIDE_DIR / f"{stem}.json"
    if single_file.exists():
        paths.append(single_file)
    fragment_dir = OVERRIDE_DIR / stem
    if fragment_dir.exists():
        paths.extend(sorted(fragment_dir.glob("*.json")))

    overrides = {}
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data:
            if item.get("zh"):
                overrides[item["id"]] = item["zh"]
    return overrides


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    translated = 0
    for template_path in sorted(TEMPLATE_DIR.glob("*.json")):
        items = json.loads(template_path.read_text(encoding="utf-8"))
        overrides = load_overrides(template_path.stem)
        for item in items:
            if item["id"] in overrides:
                item["zh"] = resolve_placeholders(item, overrides[item["id"]])
        (OUT_DIR / template_path.name).write_text(
            json.dumps(items, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        total += len(items)
        translated += sum(1 for item in items if item.get("zh"))
    print(f"Wrote {translated}/{total} translated blocks to {OUT_DIR}")


if __name__ == "__main__":
    main()
