# FileScanner — Project Scanner & Structural Extractor

`file_scanner.py` — Scan project directories, extract structural lines, manage MD5 hash cache.

## Features

- **Recursive file discovery**: Walks project tree, respects `.uberwikiignore`
- **Binary detection**: Uses extension + magic bytes to skip non-text files
- **Structural extraction**: Per-language regex patterns extract classes, functions, imports, headings
- **Hash cache**: MD5-based incremental sync — only re-index changed files
- **Exclusion**: Respects `.gitignore` patterns + built-in excludes (node_modules, .git, __pycache__, etc.)

## Supported Languages

| Extension | Extracted Patterns |
|-----------|-------------------|
| `.ts`, `.tsx` | classes, interfaces, types, enums, functions, constants |
| `.js`, `.jsx` | classes, functions, exports, constants |
| `.py` | classes, functions, async functions |
| `.go` | functions, structs, interfaces |
| `.rs` | structs, enums, functions, traits, impls, macros |
| `.rb` | classes, modules, functions |
| `.swift` | classes, structs, enums, protocols, extensions, functions, vars |
| `.c`, `.h` | functions, structs, defines |
| `.md` | headings (h1-h6), first sentences of paragraphs |
| `.json` | top-level keys (first 30) |
| `.yaml`, `.yml`, `.toml`, `.ini`, `.env` | key-value pairs |

## API

| Function | Description |
|----------|-------------|
| `scan_project(root, exclude_dirs, use_gitignore)` | Walk project, return all text files |
| `extract_structural_lines(file_path, ext)` | Parse file for structural tokens |
| `load_hash_cache(path)` | Load MD5 hash cache from JSON |
| `save_hash_cache(path, cache)` | Persist MD5 hash cache to JSON |
| `compute_diff(files, cache)` | Compare current files vs cache, return added/modified/removed |
| `is_binary(path)` | Check if file is binary (extension + magic bytes) |
