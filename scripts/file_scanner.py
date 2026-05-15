#!/usr/bin/env python3
"""
file_scanner.py — Scan project directories, extract structural lines, manage hash cache.

Scans project files, respects .uberwikiignore patterns, detects text vs binary,
extracts structural tokens per file type, manages MD5 hashes for incremental sync.

No external dependencies.
"""

from __future__ import annotations
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Optional

# Directories to always skip
DEFAULT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules",
    ".venv", "venv", ".tox", ".eggs", "eggs",
    "build", "dist", "target", ".gradle", "out",
    ".index", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".opencode", ".claude", ".cursor", ".agents",
    "aura_venv", ".terraform", ".serverless",
}

# Binary extensions to skip
BINARY_EXTENSIONS = {
    ".apk", ".aab", ".jar", ".aar", ".dex", ".class",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".svg",
    ".mp3", ".mp4", ".avi", ".mov", ".wav", ".flac", ".ogg", ".m4a",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".so", ".dylib", ".dll", ".o", ".a", ".lib",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pyc", ".pyo", ".pyd",
    ".whl", ".egg", ".deb", ".rpm",
    ".keystore", ".jks", ".p12", ".pfx",
    ".min.js", ".min.css",
}

# Text extensions to include
TEXT_EXTENSIONS = {
    # Documentation
    ".md", ".mdx", ".txt", ".rst", ".adoc", ".asciidoc", ".org",
    # Python
    ".py", ".pyi", ".pyx",
    # Kotlin/Java
    ".kt", ".kts", ".java",
    # Rust
    ".rs",
    # Web
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte",
    ".html", ".htm", ".xhtml", ".xml",
    ".css", ".scss", ".sass", ".less", ".stylus",
    # Go
    ".go",
    # Ruby
    ".rb", ".erb",
    # C/C++
    ".c", ".h", ".cpp", ".hpp", ".cc", ".hh", ".cxx", ".hxx",
    # Swift
    ".swift",
    # Config
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".env", ".properties", ".gradle", ".gradle.kts",
    # Shell
    ".sh", ".bash", ".zsh", ".fish",
    # SQL
    ".sql", ".graphql", ".prisma",
    # Docker
    "Dockerfile", "docker-compose.yml",
    # Other
    ".csv", ".tsv",
    ".log", ".lock", ".patch",
    ".proto", ".thrift",
    "Makefile", "CMakeLists.txt",
    ".terraform", ".hcl",
}

# Files to ALWAYS include regardless of extension
NAMED_FILES = {
    "Dockerfile", "Makefile", "CMakeLists.txt",
    ".gitignore", ".dockerignore",
    "docker-compose.yml", "docker-compose.yaml",
}

# ── Language-specific structural extractors ───────────────────────────

EXTRACTORS: dict[str, list[tuple[re.Pattern, callable]]] = {
    ".py": [
        (re.compile(r"^class\s+(\w+)"), lambda m: f"class {m.group(1)}"),
        (re.compile(r"^(?:async\s+)?def\s+(\w+)"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^@(?:staticmethod|classmethod|property)"), lambda m: m.group(0)),
    ],
    ".kt": [
        (re.compile(r"^(?:class|object|interface|enum class|data class|sealed class|abstract class)\s+(\w+)"),
         lambda m: f"class {m.group(1)}"),
        (re.compile(r"^fun\s+(\w+)"), lambda m: f"fun {m.group(1)}"),
        (re.compile(r"^val\s+(\w+)"), lambda m: f"val {m.group(1)}"),
        (re.compile(r"^var\s+(\w+)"), lambda m: f"var {m.group(1)}"),
    ],
    ".java": [
        (re.compile(r"^(?:public|private|protected)?\s*(?:class|interface|enum|@interface|record)\s+(\w+)"),
         lambda m: f"class {m.group(1)}"),
        (re.compile(r"^\s*(?:public|private|protected|static|final|abstract|synchronized|native)\s+.*?(\w+)\s*\("),
         lambda m: f"method {m.group(1)}"),
    ],
    ".rs": [
        (re.compile(r"^fn\s+(\w+)"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^struct\s+(\w+)"), lambda m: f"struct {m.group(1)}"),
        (re.compile(r"^enum\s+(\w+)"), lambda m: f"enum {m.group(1)}"),
        (re.compile(r"^trait\s+(\w+)"), lambda m: f"trait {m.group(1)}"),
        (re.compile(r"^impl(?:\s*<[^>]*>)?\s+(\w+)"), lambda m: f"impl {m.group(1)}"),
        (re.compile(r"^mod\s+(\w+)"), lambda m: f"mod {m.group(1)}"),
        (re.compile(r"^type\s+(\w+)"), lambda m: f"type {m.group(1)}"),
        (re.compile(r"^const\s+(\w+)"), lambda m: f"const {m.group(1)}"),
    ],
    ".ts": [
        (re.compile(r"^(?:export\s+)?(?:class|interface|type|enum)\s+(\w+)"),
         lambda m: f"class {m.group(1)}"),
        (re.compile(r"^(?:export\s+)?function\s+(\w+)"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*[=:]"),
         lambda m: f"const {m.group(1)}"),
    ],
    ".js": [
        (re.compile(r"^(?:class|function)\s+(\w+)"), lambda m: f"class {m.group(1)}"),
        (re.compile(r"^(?:const|let|var)\s+(\w+)\s*="), lambda m: f"const {m.group(1)}"),
        (re.compile(r"^(?:export\s+)?(?:default\s+)?(?:function|class)\s+(\w+)"),
         lambda m: f"fn {m.group(1)}"),
    ],
    ".go": [
        (re.compile(r"^func\s+(\w+)"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^type\s+(\w+)\s+(?:struct|interface)"), lambda m: f"type {m.group(1)}"),
    ],
    ".rb": [
        (re.compile(r"^(?:class|module)\s+(\w+)"), lambda m: f"class {m.group(1)}"),
        (re.compile(r"^def\s+(\w+)"), lambda m: f"fn {m.group(1)}"),
    ],
    ".swift": [
        (re.compile(r"^(?:class|struct|enum|protocol|extension)\s+(\w+)"),
         lambda m: f"class {m.group(1)}"),
        (re.compile(r"^func\s+(\w+)"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^var\s+(\w+)"), lambda m: f"var {m.group(1)}"),
    ],
    ".c": [
        (re.compile(r"^\s*(\w+)\s*\(.*?\)\s*\{"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^struct\s+(\w+)"), lambda m: f"struct {m.group(1)}"),
    ],
    ".h": [
        (re.compile(r"^\s*(\w+)\s*\(.*?\)"), lambda m: f"fn {m.group(1)}"),
        (re.compile(r"^#define\s+(\w+)"), lambda m: f"define {m.group(1)}"),
    ],
}


def extract_structural_lines(file_path: Path, ext: str) -> list[str]:
    """Extract structural tokens from a file for trie insertion."""
    lines = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    # Get extractors for this extension
    extractors = EXTRACTORS.get(ext, [])

    # Markdown: extract headings
    if ext == ".md":
        for line in text.split("\n"):
            m = re.match(r"^(#{1,6})\s+(.+)", line)
            if m:
                level = len(m.group(1))
                heading = m.group(2).strip()
                lines.append(f"h{level}:{heading}")
        # Also extract first sentence of paragraphs
        for para in text.split("\n\n"):
            para = para.strip()
            if para and len(para) > 20 and len(para) < 200:
                first_line = para.split("\n")[0].strip()
                if first_line and not first_line.startswith(("#", "-", "*", ">", "```")):
                    if len(first_line.split()) <= 15:
                        lines.append(first_line)

    # JSON: top-level keys
    elif ext == ".json":
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                for k in list(data.keys())[:30]:
                    lines.append(f"key:{k}")
        except json.JSONDecodeError:
            pass

    # YAML/TOML/INI/ENV: key-value pairs
    elif ext in (".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env", ".properties"):
        for line in text.split("\n"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key = line.split("=")[0].strip()
                if key.isupper() or "." in key or "_" in key:
                    lines.append(f"config:{key}")
            elif ":" in line and not line.startswith("#"):
                key = line.split(":")[0].strip()
                if key.isidentifier() and not key.startswith("#"):
                    lines.append(f"config:{key}")

    # Gradle: build.gradle / build.gradle.kts
    elif ext in (".gradle", ".gradle.kts"):
        for line in text.split("\n"):
            line = line.strip()
            m = re.match(r"(\w+)\s*\{", line)
            if m and m.group(1) in ("plugins", "android", "dependencies", "defaultConfig",
                                     "buildTypes", "repositories", "signingConfigs"):
                lines.append(f"block:{m.group(1)}")

    # CSV/TSV: headers
    elif ext in (".csv", ".tsv"):
        first_line = text.split("\n")[0].strip()
        if first_line:
            sep = "," if ext == ".csv" else "\t"
            headers = [h.strip() for h in first_line.split(sep)][:20]
            for h in headers:
                if h:
                    lines.append(f"col:{h}")

    # Code files: use extractors
    if extractors:
        seen = set()
        for line in text.split("\n"):
            for pattern, fmt_fn in extractors:
                m = pattern.match(line.strip())
                if m:
                    extracted = fmt_fn(m)
                    if extracted and extracted not in seen:
                        seen.add(extracted)
                        lines.append(extracted)

    # Fallback for unnamed files: try to detect shebang
    if not lines and ext == "":
        first = text.split("\n")[0].strip()
        if first.startswith("#!"):
            lines.append(f"shebang:{first[2:].strip()}")

    return lines[:50]  # cap at 50 structural lines per file


def is_text_file(file_path: Path) -> bool:
    """Check if a file is text by scanning first 512 bytes for null bytes."""
    try:
        with open(file_path, "rb") as f:
            head = f.read(512)
        return b"\x00" not in head
    except Exception:
        return False


def should_include_file(file_path: Path, exclude_dirs: set[str]) -> bool:
    """Check if a file should be included in scanning."""
    # Check parent dirs against exclude list
    for parent in file_path.parents:
        if parent.name in exclude_dirs:
            return False

    # Check named files
    if file_path.name in NAMED_FILES:
        return True

    # Check extension
    ext = file_path.suffix.lower()
    if ext in BINARY_EXTENSIONS:
        return False
    if ext in TEXT_EXTENSIONS:
        return True

    # No extension — check shebang
    if ext == "":
        try:
            with open(file_path, "rb") as f:
                head = f.read(128)
            if head.startswith(b"#!"):
                return True
        except Exception:
            pass

    return False


def scan_project(root_dir: str | Path,
                 exclude_dirs: set[str] | None = None) -> list[dict]:
    """Scan a project directory, returning file info for text files."""
    root = Path(root_dir).resolve()
    exclude = set(DEFAULT_EXCLUDE_DIRS) | (exclude_dirs or set())
    files: list[dict] = []

    try:
        for entry in root.rglob("*"):
            if not entry.is_file():
                continue
            if not should_include_file(entry, exclude):
                continue
            if not is_text_file(entry):
                continue

            rel_path = entry.relative_to(root)
            ext = entry.suffix.lower()
            if not ext and entry.name in NAMED_FILES:
                ext = entry.suffix  # Still '' but name matches

            try:
                content = entry.read_bytes()
                md5 = hashlib.md5(content).hexdigest()
            except Exception:
                continue

            files.append({
                "path": str(rel_path),
                "abs_path": str(entry),
                "ext": ext or Path(entry.name).suffix.lower(),
                "size": entry.stat().st_size,
                "mtime": entry.stat().st_mtime,
                "hash": md5,
            })
    except PermissionError:
        pass

    return sorted(files, key=lambda f: f["path"])


def load_hash_cache(cache_path: str | Path) -> dict[str, str]:
    """Load hash cache from JSON file. Returns {rel_path: md5_hash}."""
    cache_path = Path(cache_path)
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except (json.JSONDecodeError, Exception):
            return {}
    return {}


def save_hash_cache(cache_path: str | Path, hashes: dict[str, str]) -> None:
    """Save hash cache to JSON file."""
    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(hashes, indent=2, sort_keys=True))


def compute_diff(current_files: list[dict],
                 cached_hashes: dict[str, str]) -> dict:
    """Compare current files against hash cache.
    Returns {new: [...], changed: [...], deleted: [...], unchanged: [...]}
    """
    current = {f["path"]: f["hash"] for f in current_files}

    new = [f for f in current_files if f["path"] not in cached_hashes]
    changed = [f for f in current_files
               if f["path"] in cached_hashes and f["hash"] != cached_hashes[f["path"]]]
    deleted = [p for p in cached_hashes if p not in current]
    unchanged = [f for f in current_files if f["path"] in cached_hashes
                 and f["hash"] == cached_hashes[f["path"]]]

    return {
        "new": new,
        "changed": changed,
        "deleted": deleted,
        "unchanged": unchanged,
        "summary": {
            "new": len(new),
            "changed": len(changed),
            "deleted": len(deleted),
            "unchanged": len(unchanged),
            "total": len(current_files),
        },
    }


# ── CLI test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."

    print(f"Scanning: {target}")
    files = scan_project(target)

    print(f"Found {len(files)} text files")
    print(f"Total size: {sum(f['size'] for f in files) / 1024:.0f} KB")

    # Show file type distribution
    from collections import Counter
    ext_counts = Counter(f["ext"] for f in files)
    print("\nBy extension:")
    for ext, count in ext_counts.most_common(15):
        print(f"  {ext or '(none)':12s} {count:4d} files")

    # Show sample structural lines for a few files
    print("\nSample structural extractions:")
    count = 0
    for f in files[:10]:
        lines = extract_structural_lines(Path(f["abs_path"]), f["ext"])
        if lines:
            print(f"  {f['path']}: {lines[:5]}")
            count += 1
            if count >= 5:
                break

    print(f"\nFile scanner test: PASS ({len(files)} files)")
