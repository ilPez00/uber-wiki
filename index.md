# UberWiki — Two-Layer Compressed Wiki

**Persistent project knowledge base with constant-cost AI retrieval.**

First run indexes EVERY text file in a project (code, docs, config, logs) into a Dynamic Vector Trie + llmwiki search index. Subsequent runs are incremental (MD5 hash diff). Constant token cost per retrieval (≤400 tokens) regardless of wiki size.

## Contents

- `SKILL.md` — Skill manifest for loading as an AI agent skill
- `llm-wiki.md` — Full guide: LLM Wiki pattern for Big Long Hard Tasks
- `scripts/` — Python implementation + documentation

## Scripts

| Script | Doc | Description |
|--------|-----|-------------|
| `dynamic_vector_trie.py` | [doc](scripts/dynamic_vector_trie.md) | Flat contiguous-array trie for semantic compression |
| `file_scanner.py` | [doc](scripts/file_scanner.md) | Project scanner, structural line extractor, hash cache |
| `uberwiki_cli.py` | [doc](scripts/uberwiki_cli.md) | Orchestrator CLI (init, sync, query, bridge, serve) |

## Quickstart

```bash
# Load as skill (in Claude Code / opencode):
#   /skill uber-wiki

# Or run directly:
python scripts/uberwiki_cli.py init --path . --topic "My Project"
python scripts/uberwiki_cli.py sync --full --path .
python scripts/uberwiki_cli.py query "search terms" --path .
python scripts/uberwiki_cli.py status --path .
```

## Architecture

```
uberwiki_cli.py (orchestrator)
  ├── dynamic_vector_trie.py (binary trie — AI layer)
  ├── file_scanner.py (scan + extract — input pipeline)
  └── llmwiki (optional — semantic search)
```

## References

- [llm-wiki.md](llm-wiki.md) — Full LLM Wiki pattern documentation
- `/home/gio/.agents/skills/uberwiki/` — Original skill location (includes vector_decompress.py + bpe_radix_profiler.py)
