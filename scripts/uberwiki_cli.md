# UberWiki CLI — Orchestrator

`uberwiki_cli.py` — Command-line interface that ties DynamicVectorTrie + FileScanner together.

## Commands

### `init`
Bootstrap `.wiki/` structure in target project.
```
python uberwiki_cli.py init --path . --topic "My Project"
```
Creates: `.wiki/human/`, `.wiki/ai/`, `.wiki/human/index.md`, `.wiki/human/log.md`

### `sync`
Incremental project scan + trie update. Only reprocesses changed files (MD5 diff).
```
python uberwiki_cli.py sync --path .
python uberwiki_cli.py sync --full --path .   # Full rebuild
```

### `ingest`
Add specific files to the wiki manually.
```
python uberwiki_cli.py ingest src/main.ts --path .
```

### `query`
Search both human (markdown) and AI (trie) layers. Returns ≤400 tokens.
```
python uberwiki_cli.py query "memory compression" --path .
```
Search strategy:
1. Exact phrase match
2. Individual word match
3. Case-insensitive fallback
4. Dictionary token substring match

### `profile`
Suggest BPE compound merges for trie compression optimization.
```
python uberwiki_cli.py profile --path .
```

### `apply-merges`
Apply suggested BPE merges after reviewing profile output.
```
python uberwiki_cli.py apply-merges --path .
```

### `bridge`
Export trie to Android-compatible JSON format for on-device use.
```
python uberwiki_cli.py bridge --path .
adb push .wiki/ai/bridge.json /sdcard/Download/
```

### `serve`
Start llmwiki MCP server for AI tool access.
```
python uberwiki_cli.py serve --path .
```

### `status`
Show wiki statistics (files indexed, trie size, token count).
```
python uberwiki_cli.py status --path .
```
Example output:
```
Wiki root: /project/.wiki
Human wiki: 12 files, 45 KB
AI wiki: 2.8M nodes, 14717 tokens, 37 MB
```

## Architecture

```
uberwiki_cli.py (orchestrator)
  ├── dynamic_vector_trie.py (trie data structure)
  ├── file_scanner.py (project scanning + extraction)
  ├── vector_decompress.py (trie → human-readable)
  └── bpe_radix_profiler.py (optional, compression analysis)
```
