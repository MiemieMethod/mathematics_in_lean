#!/usr/bin/env python3
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import NavigableString


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "html"
TRANSLATION_DIR = ROOT / "translations" / "zh_blocks"
TEMPLATE_DIR = ROOT / "translations" / "zh_blocks_template"
VERSION = "v4.30.0"

FALLBACK_TITLE_MAP = {
    "Introduction": "引言",
    "Getting Started": "入门",
    "Overview": "概览",
    "Basics": "基础",
    "Calculating": "计算",
    "Proving Identities in Algebraic Structures": "证明代数结构中的恒等式",
    "Using Theorems and Lemmas": "使用定理和引理",
    "More examples using apply and rw": "使用 apply 和 rw 的更多例子",
    "Proving Facts about Algebraic Structures": "证明关于代数结构的事实",
    "Logic": "逻辑",
    "Implication and the Universal Quantifier": "蕴含与全称量词",
    "The Existential Quantifier": "存在量词",
    "Negation": "否定",
    "Conjunction and Iff": "合取与当且仅当",
    "Disjunction": "析取",
    "Sequences and Convergence": "序列与收敛",
    "Sets and Functions": "集合与函数",
    "Sets": "集合",
    "Functions": "函数",
    "The Schröder-Bernstein Theorem": "施罗德-伯恩斯坦定理",
    "Elementary Number Theory": "初等数论",
    "Irrational Roots": "无理根",
    "Induction and Recursion": "归纳与递归",
    "Infinitely Many Primes": "无穷多个素数",
    "More Induction": "更多归纳法",
    "Discrete Mathematics": "离散数学",
    "Finsets and Fintypes": "有限集与有限类型",
    "Counting Arguments": "计数论证",
    "Inductively Defined Types": "归纳定义的类型",
    "Structures": "结构",
    "Defining structures": "定义结构",
    "Algebraic Structures": "代数结构",
    "Building the Gaussian Integers": "构造高斯整数",
    "Hierarchies": "层级结构",
    "Morphisms": "态射",
    "Sub-objects": "子对象",
    "Groups and Rings": "群与环",
    "Monoids and Groups": "幺半群与群",
    "Rings": "环",
    "Linear algebra": "线性代数",
    "Vector spaces and linear maps": "向量空间与线性映射",
    "Subspaces and quotients": "子空间与商",
    "Endomorphisms": "自同态",
    "Matrices, bases and dimension": "矩阵、基与维数",
    "Topology": "拓扑",
    "Filters": "滤子",
    "Metric spaces": "度量空间",
    "Topological spaces": "拓扑空间",
    "Differential Calculus": "微分学",
    "Elementary Differential Calculus": "初等微分学",
    "Differential Calculus in Normed Spaces": "赋范空间中的微分学",
    "Integration and Measure Theory": "积分与测度论",
    "Elementary Integration": "初等积分",
    "Measure Theory": "测度论",
    "Integration": "积分",
}

UI_REPLACEMENTS = {
    "Mathematics in Lean": "Lean 形式化数学",
    "Search docs": "搜索文档",
    "View page source": "查看页面源码",
    "Index": "索引",
    "Search": "搜索",
    "Next": "下一页",
    "Previous": "上一页",
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

PROTECTED_PARENTS = {"script", "style", "pre", "code", "math"}


def plain_text(html: str) -> str:
    return " ".join(BeautifulSoup(html, "html.parser").get_text(" ").split())


def load_heading_map() -> dict[str, str]:
    mapping = dict(FALLBACK_TITLE_MAP)
    template_items = {}
    if TEMPLATE_DIR.exists():
        for path in sorted(TEMPLATE_DIR.glob("*.json")):
            for item in json.loads(path.read_text(encoding="utf-8")):
                template_items[item["id"]] = item
    if not TRANSLATION_DIR.exists():
        return mapping
    for path in sorted(TRANSLATION_DIR.glob("*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            source_item = item if item.get("tag") else template_items.get(item.get("id", ""), item)
            if source_item.get("tag") not in {"h1", "h2", "h3"}:
                continue
            zh = item.get("zh", "")
            if not zh:
                continue
            mapping[source_item["text"]] = plain_text(zh)
    return mapping


def translate_phrase(text: str, heading_map: dict[str, str]) -> str:
    leading = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()) :]
    core = text.strip()
    if not core:
        return text
    if core in heading_map:
        return f"{leading}{heading_map[core]}{trailing}"
    if core in UI_REPLACEMENTS:
        return f"{leading}{UI_REPLACEMENTS[core]}{trailing}"

    replaced = core
    combined = {**UI_REPLACEMENTS, **heading_map}
    for src, dst in sorted(combined.items(), key=lambda item: len(item[0]), reverse=True):
        replaced = replaced.replace(src, dst)
    replaced = re.sub(
        r"v4\.\d+\.\d+ documentation|0\.1 documentation|v4\.\d+\.\d+ 文档|0\.1 文档",
        f"{VERSION} 中文文档",
        replaced,
    )
    replaced = replaced.replace("documentation", "中文文档")
    return f"{leading}{replaced}{trailing}"


def is_inside_article_body(tag) -> bool:
    return tag.find_parent(attrs={"itemprop": "articleBody"}) is not None


def should_translate_article_node(path: Path, parent) -> bool:
    if path.name != "index.html":
        return False
    if parent.name in {"h1", "h2", "h3"}:
        return True
    return parent.name == "a" and parent.find_parent(class_="toctree-wrapper") is not None


def is_protected_node(node: NavigableString) -> bool:
    parent = node.parent
    return parent is None or parent.find_parent(PROTECTED_PARENTS) is not None or parent.name in PROTECTED_PARENTS


def normalize_html(path: Path, heading_map: dict[str, str]) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    if soup.html is not None:
        soup.html["lang"] = "zh-CN"

    for tag in soup.find_all(True):
        for attr in ("title", "placeholder", "aria-label", "alt"):
            if attr in tag.attrs and isinstance(tag.attrs[attr], str):
                tag.attrs[attr] = translate_phrase(tag.attrs[attr], heading_map)

    for node in soup.find_all(string=True):
        if not isinstance(node, NavigableString) or is_protected_node(node):
            continue
        parent = node.parent
        if parent is None:
            continue
        if is_inside_article_body(parent) and not should_translate_article_node(path, parent):
            continue
        translated = translate_phrase(str(node), heading_map)
        if translated != str(node):
            node.replace_with(NavigableString(translated))

    path.write_text(str(soup), encoding="utf-8")


def normalize_documentation_options() -> None:
    path = HTML / "_static" / "documentation_options.js"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"VERSION: 'v4\.\d+\.\d+'", f"VERSION: '{VERSION}'", text)
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
    heading_map = load_heading_map()
    for path in HTML.glob("*.html"):
        normalize_html(path, heading_map)
    normalize_documentation_options()
    normalize_static_javascript()


if __name__ == "__main__":
    main()
