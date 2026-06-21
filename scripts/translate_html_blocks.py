#!/usr/bin/env python3
import argparse
import copy
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from bs4 import NavigableString


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "html"
TRANSLATIONS = ROOT / "translations" / "zh_blocks.json"
TRANSLATION_DIR = ROOT / "translations" / "zh_blocks"
CONTENT_PAGES = {
    "C01_Introduction.html",
    "C02_Basics.html",
    "C03_Logic.html",
    "C04_Sets_and_Functions.html",
    "C05_Elementary_Number_Theory.html",
    "C06_Discrete_Mathematics.html",
    "C07_Structures.html",
    "C08_Hierarchies.html",
    "C09_Groups_and_Rings.html",
    "C10_Linear_Algebra.html",
    "C11_Topology.html",
    "C12_Differential_Calculus.html",
    "C13_Integration_and_Measure_Theory.html",
}

TRANSLATABLE_SELECTORS = [
    "div[itemprop='articleBody'] h1",
    "div[itemprop='articleBody'] h2",
    "div[itemprop='articleBody'] h3",
    "div[itemprop='articleBody'] p",
    "div[itemprop='articleBody'] li",
    "div[itemprop='articleBody'] dt",
    "div[itemprop='articleBody'] dd",
    "div[itemprop='articleBody'] th",
    "div[itemprop='articleBody'] td",
]

SKIP_CLASSES = {"headerlink"}


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def block_text(tag) -> str:
    cloned = copy.copy(tag)
    for link in cloned.select("a.headerlink"):
        link.extract()
    return normalize_space(cloned.get_text(" "))


def is_translatable(tag) -> bool:
    text = block_text(tag)
    if not text or text in {"¶", ""}:
        return False
    if tag.name in {"script", "style", "pre", "code"}:
        return False
    if tag.name == "p" and tag.find_parent("li") is not None:
        return False
    classes = set(tag.get("class") or [])
    return not classes.intersection(SKIP_CLASSES)


def iter_blocks(path: Path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    seen = set()
    for selector in TRANSLATABLE_SELECTORS:
        for tag in soup.select(selector):
            ident = id(tag)
            if ident in seen or not is_translatable(tag):
                continue
            seen.add(ident)
            yield soup, tag


def stable_id(path: Path, index: int) -> str:
    return f"{path.stem}:{index:04d}"


def extract() -> None:
    items = []
    by_file = {}
    for path in sorted(HTML.glob("*.html")):
        if path.name not in CONTENT_PAGES:
            continue
        index = 0
        for _soup, tag in iter_blocks(path):
            index += 1
            item = {
                "id": stable_id(path, index),
                "file": path.name,
                "tag": tag.name,
                "text": block_text(tag),
                "html": str(tag),
                "zh": "",
            }
            items.append(item)
            by_file.setdefault(path.stem, []).append(item)
    out = TRANSLATIONS.with_name("zh_blocks.template.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    template_dir = out.parent / "zh_blocks_template"
    template_dir.mkdir(parents=True, exist_ok=True)
    for stem, file_items in by_file.items():
        (template_dir / f"{stem}.json").write_text(
            json.dumps(file_items, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(f"Wrote {len(items)} blocks to {out}")


def load_translations() -> dict[str, str]:
    data = []
    if TRANSLATION_DIR.exists():
        for path in sorted(TRANSLATION_DIR.glob("*.json")):
            data.extend(json.loads(path.read_text(encoding="utf-8")))
    elif TRANSLATIONS.exists():
        data = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))
    else:
        raise FileNotFoundError(f"No translations found in {TRANSLATION_DIR} or {TRANSLATIONS}")
    translations = {}
    for item in data:
        zh = item.get("zh", "")
        if zh:
            translations[item["id"]] = zh
    return translations


def set_inner_html(soup: BeautifulSoup, tag, html: str) -> None:
    headerlink = None
    link = tag.select_one("a.headerlink")
    if link is not None:
        headerlink = str(link)
    tag.clear()
    if "<" not in html and ">" not in html:
        tag.append(NavigableString(html))
    else:
        template = BeautifulSoup("<template></template>", "lxml").template
        template.append(BeautifulSoup(html, "html.parser"))
        for node in list(template.contents):
            tag.append(node)
    if headerlink is not None:
        restored = BeautifulSoup(headerlink, "lxml")
        restored_body = restored.body
        restored_nodes = list(restored_body.contents if restored_body else restored.contents)
        for node in restored_nodes:
            tag.append(node)


def apply() -> None:
    translations = load_translations()
    files_with_translations = {item_id.split(":", 1)[0] + ".html" for item_id in translations}
    applied = 0
    for path in sorted(HTML.glob("*.html")):
        if path.name not in CONTENT_PAGES:
            continue
        if path.name not in files_with_translations:
            continue
        text = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(text, "lxml")
        blocks = []
        seen = set()
        for selector in TRANSLATABLE_SELECTORS:
            for tag in soup.select(selector):
                ident = id(tag)
                if ident in seen or not is_translatable(tag):
                    continue
                seen.add(ident)
                blocks.append(tag)
        for index, tag in enumerate(blocks, start=1):
            zh = translations.get(stable_id(path, index))
            if zh:
                set_inner_html(soup, tag, zh)
                applied += 1
        path.write_text(str(soup), encoding="utf-8")
    print(f"Applied {applied} translated blocks")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["extract", "apply"])
    args = parser.parse_args()
    if args.command == "extract":
        extract()
    else:
        apply()


if __name__ == "__main__":
    main()
