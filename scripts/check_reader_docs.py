#!/usr/bin/env python3
"""Static checks for the active GitHub Markdown reader routes (standard library).

Run ``python scripts/check_reader_docs.py`` from any directory. ``--self-test``
also exercises deliberately broken targets/anchors in a temporary directory.
This is not a Markdown renderer, TeX validator, browser/accessibility test, or
external-URL checker. Historical pages are checked as link destinations only;
their own outgoing links are outside the active route checked here.
"""
from __future__ import annotations

import argparse
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "20954b2ae96e8a5ea95749475fd6b0724b2d5e6b"
# Verified from docs/DIALOGUE_REPORT.md at BASELINE: SHA-256 of the ordered
# (question heading, generated anchor) pairs as UTF-8 compact JSON. Keeping this
# small immutable fingerprint makes shallow clones and source snapshots work
# without Git history, network retrieval, or a separate checkpoint archive.
BASELINE_QUESTION_SHA256 = "06a4a7ca0e14a3f0eb994683497e05de54d1617983b2da297c5c180bd056486f"
QUESTION_IDS = tuple((
    "M1 M2 M3 M4 M5 M6 M7 M8 M9 A1 A2 B1 B2 B3 B4 B5 C1 C2 C3 C4 "
    "D1 D2 D3 D4 E1 E2 E3 E4 E5 E6 F1 F2 F3 F4 F5 G1 G2 G3 H1 H2 H3"
).split())
ACTIVE = (
    "LICENSE_STATUS.md", "THIRD_PARTY_NOTICES.md", "CONTRIBUTING.md", "docs/PUBLIC_RELEASE.md",
    "README.md", "docs/PROJECT_GUIDE.md", "docs/TUTORIAL_BRIDGE.md",
    "docs/NOTATION.md", "docs/DIALOGUE_REPORT.md", "docs/DIALOGUE_QUESTION_MAP.md",
    "docs/THEORY.md", "docs/NUMERICAL_METHODS.md", "docs/CLAIM_EVIDENCE_MAP.md",
    "docs/RELATED_WORK.md", "docs/REPRODUCTION.md", "docs/CODE_MAP.md",
    "docs/FIGURE_BASELINE.md", "docs/REPRODUCIBILITY_LIMITS.md",
    "docs/SCIENTIFIC_STORY.md", "docs/00_START_HERE.md",
    "docs/RESULTS_AT_A_GLANCE.md", "docs/FAQ.md", "docs/SCOPE_AND_LIMITATIONS.md",
    "docs/EVIDENCE_REASSESSMENT.md", "docs/FIGURE1_UNCERTAINTY.md",
    "docs/FIGURE1_CAPTION.md", "docs/DATA_POLICY.md", "figures/README.md", "scripts/figures/README.md",
)
QUESTION = re.compile(r"^(M[1-9]|[A-H][1-9][0-9]*)\.\s")


def prose_lines(text: str) -> tuple[list[str], list[str]]:
    """Mask fenced code without moving line numbers; check fence/math balance."""
    lines, errors = [], []
    fence = None
    display = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            lines.append("")
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]), number)
            lines.append("")
            continue
        lines.append(line)
        # Inline code can contain literal dollars and link-shaped examples.
        plain = re.sub(r"(`+).*?\1", "", line)
        tokens = list(re.finditer(r"(?<!\\)(?:\$\$|\$)", plain))
        singles = 0
        for token in tokens:
            if token[0] == "$$":
                display = None if display else number
            elif display is None:
                singles += 1
        if singles % 2:
            errors.append(f"line {number}: unmatched inline math dollar (literal currency needs \\$)")
    if fence:
        errors.append(f"line {fence[2]}: unclosed code fence")
    if display:
        errors.append(f"line {display}: unclosed display math delimiter")
    return lines, errors


def slug(heading: str) -> str:
    """GitHub-style slugs for the plain/inline-markup headings used here."""
    heading = re.sub(r"!?\[([^]]*)\]\([^)]*\)", r"\1", heading)
    heading = unescape(re.sub(r"<[^>]*>", "", heading)).lower()
    return "".join(
        ch for ch in heading
        if ch in "-_ " or unicodedata.category(ch)[0] in "LNM"
    ).replace(" ", "-")


def headings(lines: list[str]) -> list[tuple[str, str]]:
    found, used = [], set()
    for index, line in enumerate(lines):
        atx = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        title = atx[1] if atx else None
        if title is None and index + 1 < len(lines) and line.strip():
            if re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
                title = line.strip()
        if title is None:
            continue
        base, suffix = slug(title), 0
        anchor = base
        while anchor in used:
            suffix += 1
            anchor = f"{base}-{suffix}"
        used.add(anchor)
        found.append((title, anchor))
    return found


class HTMLLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.links: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("id", "name" if tag == "a" else "id"):
            if values.get(key):
                self.anchors.add(values[key])
        key = "href" if tag == "a" else "src" if tag in {"img", "source"} else None
        if key and values.get(key):
            self.links.append((self.getpos()[0], values[key]))


def destination(value: str) -> str:
    value = value.strip()
    if value.startswith("<") and ">" in value:
        return value[1:value.index(">")]
    return re.split(r"\s+[\"']", value, maxsplit=1)[0]


def markdown_links(lines: list[str]) -> tuple[list[tuple[int, str]], list[str]]:
    """Parse inline and reference links, allowing balanced URL parentheses."""
    links, errors, definitions = [], [], {}
    normalize = lambda label: " ".join(label.split()).casefold()
    for line in lines:
        match = re.match(r"^ {0,3}\[([^]]+)\]:\s*(.+)$", line)
        if match:
            definitions[normalize(match[1])] = destination(match[2])
    for number, line in enumerate(lines, 1):
        if re.match(r"^ {0,3}\[[^]]+\]:", line):
            continue
        plain = re.sub(r"(`+).*?\1", "", line)
        consumed = set()
        for match in re.finditer(r"!?\[[^]\n]*\]\(", plain):
            depth, end = 1, match.end()
            while end < len(plain) and depth:
                if plain[end] == "\\":
                    end += 2
                    continue
                depth += (plain[end] == "(") - (plain[end] == ")")
                end += 1
            if depth:
                errors.append(f"line {number}: unclosed inline link destination")
            else:
                links.append((number, destination(plain[match.end():end - 1])))
            consumed.update(range(match.start(), end))
        for match in re.finditer(r"!?\[([^]\n]+)\](?:\[([^]\n]*)\])?", plain):
            if match.start() in consumed:
                continue
            label = normalize(match[2] or match[1])
            if label in definitions:
                links.append((number, definitions[label]))
            elif match[2] is not None:
                errors.append(f"line {number}: undefined link reference [{match[2] or match[1]}]")
    return links, errors


def document(text: str) -> tuple[set[str], list[tuple[int, str]], list[str]]:
    lines, errors = prose_lines(text)
    markup = HTMLLinks()
    markup.feed("\n".join(lines))
    links, link_errors = markdown_links(lines)
    return ({anchor for _, anchor in headings(lines)} | markup.anchors,
            links + markup.links, errors + link_errors)


def check_files(root: Path, paths: tuple[str, ...]) -> tuple[list[str], int]:
    errors, count, cache = [], 0, {}
    for relative in paths:
        source = root / relative
        if not source.is_file():
            errors.append(f"{relative}: missing active route page")
            continue
        cache[source.resolve()] = document(source.read_text(encoding="utf-8"))
    for relative in paths:
        source = root / relative
        if not source.is_file():
            continue
        _, links, local_errors = cache[source.resolve()]
        errors.extend(f"{relative}: {error}" for error in local_errors)
        for line, raw in links:
            parsed = urlsplit(unescape(raw))
            if parsed.scheme or parsed.netloc:
                continue
            count += 1
            target = unquote(parsed.path)
            candidate = ((root / target.lstrip("/")) if target.startswith("/") else
                         (source.parent / target if target else source)).resolve()
            label = f"{relative}:{line} -> {raw}"
            if not candidate.is_relative_to(root.resolve()):
                errors.append(f"{label}: target escapes repository")
            elif not candidate.exists():
                errors.append(f"{label}: missing target")
            elif parsed.fragment and candidate.suffix.lower() == ".md":
                if candidate not in cache:
                    cache[candidate] = document(candidate.read_text(encoding="utf-8"))
                if unquote(parsed.fragment) not in cache[candidate][0]:
                    errors.append(f"{label}: missing Markdown anchor")
    return errors, count


def check_questions(root: Path) -> list[str]:
    """Keep baseline question IDs and old heading URLs available after editing."""
    report = "docs/DIALOGUE_REPORT.md"
    current = (root / report).read_text(encoding="utf-8")
    questions = [(title, anchor) for title, anchor in
                 headings(prose_lines(current)[0]) if QUESTION.match(title)]
    ids = tuple(QUESTION.match(title)[1] for title, _ in questions)
    encoded = json.dumps(questions, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    errors = []
    if ids != QUESTION_IDS:
        errors.append(f"{report}: nine main/32 appendix question ID inventory or order changed")
    if hashlib.sha256(encoded).hexdigest() != BASELINE_QUESTION_SHA256:
        errors.append(f"{report}: question headings or original destinations differ from verified baseline {BASELINE}")
    question_map = (root / "docs/DIALOGUE_QUESTION_MAP.md").read_text(encoding="utf-8")
    for (title, baseline_anchor), identifier in zip(questions, ids):
        targets = re.findall(
            rf"\[{identifier}\b[^]]*\]\(DIALOGUE_REPORT\.md#([^)]+)\)", question_map)
        allowed = {baseline_anchor, identifier.lower()}
        if len(targets) != 1 or targets[0] not in allowed:
            errors.append(f"docs/DIALOGUE_QUESTION_MAP.md: {identifier} needs one link to its own answer")
        if identifier.lower() in targets:
            # The new short alias must precede that question, not another answer.
            pattern = rf'<a\s+id=[\"\']{identifier.lower()}[\"\']\s*></a>\s*#{{2,3}}\s+{identifier}\.\s'
            if not re.search(pattern, current):
                errors.append(f"{report}: short anchor #{identifier.lower()} is not at its question")
    return errors


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="reader-docs-") as directory:
        root = Path(directory)
        (root / "image.png").write_bytes(b"fixture")
        (root / "target.md").write_text(
            '# Repeated\n# Repeated\n# Repeated-1\n<a id="stable"></a>\n', encoding="utf-8")
        (root / "README.md").write_text(
            '[good](target.md#repeated-1-1)\n[explicit](target.md#stable)\n'
            '![image](image.png)\n<img src="image.png">\n[ref][r]\n'
            '[r]: target.md#repeated-1\n$$\nx=1\n$$\n'
            '```md\n[ignored](absent.md)\n```\n', encoding="utf-8")
        assert not check_files(root, ("README.md",))[0]
        with (root / "README.md").open("a", encoding="utf-8") as output:
            output.write('[bad](absent.md)\n[bad anchor](target.md#absent)\n$$\n')
        failures, _ = check_files(root, ("README.md",))
        assert len(failures) == 3, failures
        assert any("missing target" in item for item in failures)
        assert any("missing Markdown anchor" in item for item in failures)
        assert any("unclosed display" in item for item in failures)
    assert prose_lines("```python\nx=1\n")[1] == ["line 1: unclosed code fence"]
    assert prose_lines("$x\n")[1]
    print("self-test passed: valid links and deliberate target/anchor/fence/math failures")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="exercise checker fixtures before checking the repository")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    errors, count = check_files(ROOT, ACTIVE)
    if all((ROOT / name).is_file() for name in ("docs/DIALOGUE_REPORT.md", "docs/DIALOGUE_QUESTION_MAP.md")):
        errors.extend(check_questions(ROOT))
    if errors:
        print("reader documentation check failed:\n" + "\n".join(f"  - {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"reader documentation checks passed: {len(ACTIVE)} active pages, {count} local links/images, 41 baseline question destinations")
    print("Static checks only; external citations, rendered mathematics, mobile layout and accessibility need separate inspection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
