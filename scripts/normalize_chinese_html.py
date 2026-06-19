#!/usr/bin/env python3
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "html"
VERSION = "v4.30.0"

TITLE_REPLACEMENTS = {
    "0.1 documentation": f"{VERSION} 中文文档",
    "Mathematics in Lean 0.1 documentation": f"Mathematics in Lean {VERSION} 中文文档",
    "0.1 文档": f"{VERSION} 中文文档",
}

TEXT_REPLACEMENTS = {
    "Mathematics in Lean": "Lean 形式化数学",
    "Search docs": "搜索文档",
    "View page source": "查看页面源码",
    "Index": "索引",
    "Next": "下一页",
    "Previous": "上一页",
    "documentation": "文档",
    "Link to this heading": "链接到此标题",
}

STATIC_JS_REPLACEMENTS = {
    ">Builds</a>": ">构建</a>",
    ">Downloads</a>": ">下载</a>",
    "<dt>Search</dt>": "<dt>搜索</dt>",
    'aria-label="Search docs"': 'aria-label="搜索文档"',
    'placeholder="Search docs"': 'placeholder="搜索文档"',
    'clicking on the "Search docs" input': 'clicking on the "搜索文档" input',
    'clicking on "Search docs" input': 'clicking on "搜索文档" input',
    "Hosted by": "托管于",
}


def replace_text(text: str) -> str:
    for src, dst in TEXT_REPLACEMENTS.items():
        text = text.replace(src, dst)
    for src, dst in TITLE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text


def split_protected_blocks(text: str) -> list[str]:
    return re.split(r"(?is)(<script\b.*?</script>|<style\b.*?</style>)", text)


def normalize_html_lang(text: str) -> str:
    html_tag = re.search(r"(?is)<html\b[^>]*>", text)
    if html_tag is None:
        return text

    tag = html_tag.group(0)
    if re.search(r"(?i)\blang\s*=", tag):
        new_tag = re.sub(r"(?i)\blang\s*=\s*(['\"])[^'\"]*\1", 'lang="zh-CN"', tag, count=1)
    else:
        new_tag = tag[:-1] + ' lang="zh-CN">'
    return text[: html_tag.start()] + new_tag + text[html_tag.end() :]


def normalize_html(path: Path) -> None:
    text = normalize_html_lang(path.read_text(encoding="utf-8"))
    parts = split_protected_blocks(text)
    for i in range(0, len(parts), 2):
        parts[i] = replace_text(parts[i])
    path.write_text("".join(parts), encoding="utf-8")


def normalize_documentation_options() -> None:
    path = HTML / "_static" / "documentation_options.js"
    text = path.read_text(encoding="utf-8")
    text = text.replace("VERSION: '0.1'", f"VERSION: '{VERSION}'")
    text = text.replace("LANGUAGE: 'en'", "LANGUAGE: 'zh_CN'")
    path.write_text(text, encoding="utf-8")


def normalize_static_javascript() -> None:
    path = HTML / "_static" / "js" / "versions.js"
    text = path.read_text(encoding="utf-8")
    for src, dst in STATIC_JS_REPLACEMENTS.items():
        text = text.replace(src, dst)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for path in HTML.glob("*.html"):
        normalize_html(path)
    normalize_documentation_options()
    normalize_static_javascript()


if __name__ == "__main__":
    main()
