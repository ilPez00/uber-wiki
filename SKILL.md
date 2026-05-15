---
name: uber-wiki
description: "UberWiki: two-layer compressed wiki for humans and AI with constant token-cost retrieval. Includes DynamicVectorTrie, file scanner, and CLI orchestrator."
context: fork
version: 1.0.0
author: aurora
tags: [wiki, knowledge-management, compression, trie, llm, search, offline, python]
---

# UberWiki — Two-Layer Compressed Wiki

Persistent project knowledge base with constant-cost AI retrieval.
Indexes code, docs, config, logs into a compressed binary trie + llmwiki semantic search.

## When to Use
- Persistent project knowledge base with constant token cost per query
- Index entire project (code + docs + config) into compressed navigable structure
- Two wikis: human (markdown) + AI (compressed trie + search)
- Android bridge export for on-device entity memory

## Prerequisites
- Python 3.10+
- `cargo install llmwiki` (optional — trie works standalone)

## Quickstart

```bash
# In any project:
python scripts/uberwiki_cli.py init --path . --topic "My Project"
python scripts/uberwiki_cli.py sync --full
python scripts/uberwiki_cli.py query "search terms"
```

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/dynamic_vector_trie.py` | Flat contiguous-array trie for semantic compression |
| `scripts/file_scanner.py` | Project file scanner, structural line extractor, hash cache manager |
| `scripts/uberwiki_cli.py` | CLI orchestrator wrapping all components |

Full docs in `scripts/` markdown files.

## Commands (uberwiki_cli)

| Command | Description |
|---------|-------------|
| `init` | Bootstrap `.wiki/` structure |
| `sync` | Incremental scan + trie update |
| `sync --full` | Full rebuild from scratch |
| `ingest <path>` | Add specific file(s) |
| `query <text>` | Search both layers, return ≤400 tokens |
| `profile` | Suggest BPE compound merges |
| `apply-merges` | Apply suggested merges |
| `bridge` | Export to Android JSON |
| `serve` | Start llmwiki MCP server |
| `status` | Show wiki stats |

## Related
- `llm-wiki` skill — human-layer wiki pattern (Karpathy)
- `caveman` skill — ultra-compressed communication, compatible with trie compression
