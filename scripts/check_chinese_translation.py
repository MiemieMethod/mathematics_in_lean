#!/usr/bin/env python3
import re
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "html"
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
TEXT_SELECTORS = [
    "div[itemprop='articleBody'] h1",
    "div[itemprop='articleBody'] h2",
    "div[itemprop='articleBody'] h3",
    "div[itemprop='articleBody'] p",
    "div[itemprop='articleBody'] li",
    "div[itemprop='articleBody'] dt",
    "div[itemprop='articleBody'] dd",
]
ALLOWED_ENGLISH = {
    "Lean",
    "Mathlib",
    "VS Code",
    "GitHub",
    "Zulip",
    "Loogle",
    "API",
    "Ctrl",
    "Cmd",
    "Mac",
    "Windows",
}


def has_chinese(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def english_words(text: str) -> list[str]:
    stripped = re.sub(r"`[^`]*`", " ", text)
    return [w for w in re.findall(r"[A-Za-z][A-Za-z-]*", stripped) if w not in ALLOWED_ENGLISH]


def main() -> None:
    failures = []
    for path in sorted(HTML.glob("C*.html")):
        if path.name not in CONTENT_PAGES:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
        for selector in TEXT_SELECTORS:
            for tag in soup.select(selector):
                if tag.name == "p" and tag.find_parent("li") is not None:
                    continue
                for hidden in tag.select("a.headerlink"):
                    hidden.extract()
                text = " ".join(tag.get_text(" ").split())
                if not text or text == "¶":
                    continue
                if not has_chinese(text) and len(english_words(text)) >= 3:
                    failures.append((path.name, text[:180]))
    for filename, text in failures[:200]:
        safe_text = text.encode("ascii", "backslashreplace").decode("ascii")
        print(f"{filename}: {safe_text}")
    if failures:
        raise SystemExit(f"{len(failures)} likely untranslated blocks")
    print("All checked article blocks contain Chinese text.")


if __name__ == "__main__":
    main()
