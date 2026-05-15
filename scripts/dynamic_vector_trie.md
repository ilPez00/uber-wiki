# DynamicVectorTrie — Flat Contiguous-Array Trie

`dynamic_vector_trie.py` — Semantic compression trie with constant retrieval cost.

## Data Structures

```
TOKEN_DICTIONARY: list[str]  — index = token_id (token 0 reserved for "")
NODE_POOL: list[[token_id, child_start, child_count, terminal]] — flat array
```

Each node: `[token_id: int, child_start: int, child_count: int, terminal: bool]`.
Root is always NODE_POOL[0].

## Key Properties

- **Retrieval cost**: O(query_len × branch_factor) — constant regardless of trie size
- **Serialization**: Binary format with magic header `AURA_TRIE\x00`, versioned
- **In-memory**: Flat arrays, no pointer chasing, CPU-cache friendly

## API

| Method | Description |
|--------|-------------|
| `token_id(token)` | Get or create token ID |
| `token_str(tid)` | Resolve token ID to string |
| `insert(path)` | Insert token path into trie |
| `search(prefix)` | Search by prefix, return all terminal paths |
| `prefix_search_flat(tokens, max_tokens)` | Search with bounded token output |
| `serialize(path)` | Write binary trie to file |
| `deserialize(path)` | Load binary trie from file |
| `stats()` | Return node/depth/token statistics |

## Binary Format

- Header: `MAGIC(10) + VERSION(4) + node_count(4) + token_count(4)` = 22 bytes
- Nodes: `token_id(4) + child_start(4) + child_count(4) + terminal(1)` = 13 bytes each
- Dictionary: newline-delimited strings after node pool
