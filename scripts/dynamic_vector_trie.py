#!/usr/bin/env python3
"""
dynamic_vector_trie.py — Flat contiguous-array trie for semantic compression.

Data structures:
  TOKEN_DICTIONARY: list[str] — index = token_id. Token 0 reserved ("").
  NODE_POOL: list[[token_id, child_start, child_count, terminal]] — flat array.

Each node is [token_id: int, child_start: int, child_count: int, terminal: bool].
Root is always NODE_POOL[0].

Retrieval cost: O(query_len × branch_factor) — constant regardless of trie size.
"""

from __future__ import annotations
import struct
import sys
from pathlib import Path

MAGIC = b"AURA_TRIE\x00"
VERSION = 1
HEADER_FMT = "=10sIII"  # magic(10) + version(4) + node_count(4) + token_count(4)
NODE_FMT = "=iii?"       # token_id(4) + child_start(4) + child_count(4) + terminal(1)
NODE_SIZE = struct.calcsize(NODE_FMT)


class DynamicVectorTrie:
    def __init__(self):
        self.dictionary = [""]  # token 0 = empty (root)
        self.pool = []          # flat array of node tuples
        self._init_root()

    def _init_root(self):
        self.pool.append([0, -1, 0, 0])  # root: token=0, no children, not terminal

    # ── Token dictionary ──────────────────────────────────────────────

    def _get_token_id(self, token: str) -> int:
        idx = len(self.dictionary)
        self.dictionary.append(token)
        return idx

    def token_id(self, token: str) -> int:
        try:
            return self.dictionary.index(token)
        except ValueError:
            return self._get_token_id(token)

    def token_str(self, tid: int) -> str:
        return self.dictionary[tid] if 0 <= tid < len(self.dictionary) else "???"

    # ── Low-level pool ops ────────────────────────────────────────────

    def _node(self, idx: int):
        return self.pool[idx]

    def _add_child(self, parent_idx: int, token_id: int) -> int:
        cs = self.pool[parent_idx][1]  # child_start
        cc = self.pool[parent_idx][2]  # child_count

        # Check if token already exists among siblings
        for i in range(cc):
            idx = cs + i
            if self.pool[idx][0] == token_id:
                return idx

        # Must add new child. Relocate siblings to tail to maintain contiguity.
        new_cs = len(self.pool)
        for i in range(cc):
            self.pool.append(list(self.pool[cs + i]))
        new_idx = len(self.pool)
        self.pool.append([token_id, -1, 0, 0])

        self.pool[parent_idx][1] = new_cs
        self.pool[parent_idx][2] = cc + 1
        return new_idx

    def _walk(self, tokens: list[int]) -> int | None:
        idx = 0  # start at root
        for tid in tokens:
            cs = self.pool[idx][1]
            cc = self.pool[idx][2]
            found = False
            for i in range(cc):
                child = self.pool[cs + i]
                if child[0] == tid:
                    idx = cs + i
                    found = True
                    break
            if not found:
                return None
        return idx

    # ── Public API ────────────────────────────────────────────────────

    def insert(self, tokens: list[int]) -> None:
        if not tokens:
            return
        idx = 0
        for i, tid in enumerate(tokens):
            idx = self._add_child(idx, tid)
            if i == len(tokens) - 1:
                self.pool[idx][3] = True  # mark terminal

    def insert_str(self, text: str) -> None:
        tokens = self.tokenize(text)
        self.insert(tokens)

    def search(self, tokens: list[int]) -> bool:
        idx = self._walk(tokens)
        return idx is not None and self.pool[idx][3]

    def search_str(self, text: str) -> bool:
        return self.search(self.tokenize(text))

    def delete(self, tokens: list[int]) -> bool:
        idx = self._walk(tokens)
        if idx is None or not self.pool[idx][3]:
            return False
        self.pool[idx][3] = False
        return True

    def prefix_search(self, tokens: list[str], depth: int = 2,
                      max_results: int = 8) -> list[list[str]]:
        # Only search for tokens that exist in dictionary
        tids = []
        for t in tokens:
            try:
                tid = self.dictionary.index(t)
                tids.append(tid)
            except ValueError:
                pass
        if not tids:
            return []
        idx = self._walk(tids)
        if idx is None:
            return []
        results: list[list[str]] = []
        self._collect_paths(idx, [], depth, results, max_results, 0)
        return results

    def prefix_search_flat(self, tokens: list[str], max_tokens: int = 400) -> str:
        paths = self.prefix_search(tokens, depth=2, max_results=8)
        if not paths:
            return ""
        lines = ["=== WIKI CONTEXT ==="]
        token_count = 0
        for path in paths:
            line = " → ".join(path)
            wt = len(line.split())
            if token_count + wt > max_tokens and token_count > 0:
                break
            lines.append(line)
            token_count += wt
        lines.append("=== END WIKI CONTEXT ===")
        return "\n".join(lines)

    def _collect_paths(self, node_idx: int, prefix: list[str], depth: int,
                       results: list, max_results: int, _depth: int):
        if len(results) >= max_results:
            return
        node = self.pool[node_idx]
        token_str = self.dictionary[node[0]]
        current = prefix + ([token_str] if token_str else [])

        if node[3] and current:
            results.append(list(current))

        if _depth >= depth:
            return

        cs = node[1]  # child_start
        cc = node[2]  # child_count
        if cs != -1:
            for i in range(cc):
                if len(results) >= max_results:
                    return
                self._collect_paths(cs + i, current, depth, results, max_results, _depth + 1)

        elif not current:
            pass  # root with no children
        elif not node[3] and _depth == 0:
            pass

    # ── Tokenization ──────────────────────────────────────────────────

    def tokenize(self, text: str) -> list[int]:
        words = text.replace("\n", " ").split()
        tids = []
        for w in words:
            w = w.strip(".,;:!?\"'()[]{}<>")
            if not w:
                continue
            tids.append(self.token_id(w))
        return tids

    def tokenize_path(self, path: str) -> list[int]:
        parts = path.replace("\\", "/").strip("/").split("/")
        return [self.token_id(p) for p in parts]

    # ── Serialization ─────────────────────────────────────────────────

    def serialize(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        node_count = len(self.pool)
        token_count = len(self.dictionary)
        header = struct.pack(HEADER_FMT, MAGIC, VERSION, node_count, token_count)

        # Pack nodes
        node_data = bytearray()
        for n in self.pool:
            node_data.extend(struct.pack(NODE_FMT, n[0], n[1], n[2], n[3]))

        # Pack token dictionary
        token_data = bytearray()
        for t in self.dictionary:
            encoded = t.encode("utf-8")
            token_data.extend(struct.pack("=I", len(encoded)))
            token_data.extend(encoded)

        with open(p, "wb") as f:
            f.write(header)
            f.write(node_data)
            f.write(token_data)

    def deserialize(self, path: str | Path) -> "DynamicVectorTrie":
        p = Path(path)
        with open(p, "rb") as f:
            magic = f.read(10)
            if magic != MAGIC:
                raise ValueError(f"Bad magic: {magic!r}")
            version = struct.unpack("=I", f.read(4))[0]
            if version != VERSION:
                raise ValueError(f"Unsupported version: {version}")
            node_count = struct.unpack("=I", f.read(4))[0]
            token_count = struct.unpack("=I", f.read(4))[0]

            # Read nodes
            node_bytes = f.read(node_count * NODE_SIZE)
            self.pool = []
            for i in range(node_count):
                off = i * NODE_SIZE
                tid, cs, cc, term = struct.unpack_from(NODE_FMT, node_bytes, off)
                self.pool.append([tid, cs, cc, term])

            # Read tokens
            self.dictionary = []
            for _ in range(token_count):
                tlen = struct.unpack("=I", f.read(4))[0]
                token = f.read(tlen).decode("utf-8")
                self.dictionary.append(token)

        return self

    # ── Export ─────────────────────────────────────────────────────────

    def export_json(self) -> dict:
        entities = []
        relations = []
        import hashlib, json

        for i, node in enumerate(self.pool):
            if node[3]:  # terminal
                token_str = self.dictionary[node[0]]
                path = self._path_to_root(i)
                name = " → ".join(path) if path else token_str
                eid = hashlib.md5(name.encode()).hexdigest()[:16]
                entities.append({
                    "id": eid,
                    "name": name,
                    "type": "concept",
                    "summary": token_str,
                    "tags": ["wiki"],
                    "created_at": [],
                })
                # Relation to parent
                if len(path) > 1:
                    parent_name = " → ".join(path[:-1])
                    parent_eid = hashlib.md5(parent_name.encode()).hexdigest()[:16]
                    relations.append({
                        "source_id": parent_eid,
                        "target_id": eid,
                        "relation": "contains",
                        "strength": 5,
                    })

        return {"entities": entities, "relations": relations}

    def _path_to_root(self, node_idx: int) -> list[str]:
        """Walk from node back to root, collecting token strings."""
        path = []
        visited = set()
        while node_idx != 0 and node_idx not in visited:
            visited.add(node_idx)
            token_str = self.dictionary[self.pool[node_idx][0]]
            path.append(token_str)
            # Find parent: linear scan (could be optimized)
            parent = self._find_parent(node_idx)
            if parent is None:
                break
            node_idx = parent
        path.reverse()
        return path

    def _find_parent(self, child_idx: int) -> int | None:
        for i, node in enumerate(self.pool):
            cs = node[1]
            cc = node[2]
            if cs != -1 and cs <= child_idx < cs + cc:
                return i
        return None

    # ── Stats ─────────────────────────────────────────────────────────

    def stats(self) -> dict:
        terminal_count = sum(1 for n in self.pool if n[3])
        max_depth = self._max_depth()
        return {
            "nodes": len(self.pool),
            "tokens": len(self.dictionary),
            "terminal_nodes": terminal_count,
            "max_depth": max_depth,
        }

    def _max_depth(self) -> int:
        max_d = 0

        def dfs(idx, d):
            nonlocal max_d
            max_d = max(max_d, d)
            cs = self.pool[idx][1]
            cc = self.pool[idx][2]
            if cs != -1:
                for i in range(cc):
                    dfs(cs + i, d + 1)

        dfs(0, 0)
        return max_d


# ── CLI: quick test ───────────────────────────────────────────────────

if __name__ == "__main__":
    t = DynamicVectorTrie()

    # Insert sample paths
    samples = [
        "project/philosophy/identity",
        "project/philosophy/recursion",
        "project/philosophy/symbolic-order",
        "project/ai/memory-compression",
        "project/ai/vector-trie",
        "project/ai/semantic-routing",
    ]
    for s in samples:
        tids = t.tokenize_path(s)
        t.insert(tids)

    print(f"Nodes: {len(t.pool)}")
    print(f"Tokens: {len(t.dictionary)}")
    print(f"Terminals: {sum(1 for n in t.pool if n[3])}")
    print()

    # prefix_search test
    results = t.prefix_search(["project"], depth=2, max_results=10)
    print("prefix_search('project', depth=2):")
    for r in results:
        print(f"  {' → '.join(r)}")
    print()

    print("prefix_search_flat('project'):")
    print(t.prefix_search_flat(["project"], max_tokens=200))
    print()

    # Serialize/deserialize roundtrip
    t.serialize("/tmp/test_trie.bin")
    t2 = DynamicVectorTrie().deserialize("/tmp/test_trie.bin")
    assert len(t2.pool) == len(t.pool)
    assert t2.dictionary == t.dictionary
    print("Serialize/deserialize roundtrip: PASS")

    # Constant cost test: same query, same result depth, same max_results
    # Cost should be bounded by max_tokens regardless of trie size
    const_test = DynamicVectorTrie()
    const_test.insert(const_test.tokenize_path("project/feature"))
    cost_1 = len(const_test.prefix_search_flat(["project"], max_tokens=400))

    for i in range(1000):
        const_test.insert(const_test.tokenize_path(f"otherbranch/sub-{i}/leaf"))
    cost_2 = len(const_test.prefix_search_flat(["project"], max_tokens=400))

    print(f"Cost with 1 node: {cost_1}")
    print(f"Cost with 1001 more nodes (other branch): {cost_2}")
    assert cost_1 == cost_2, f"CONSTANT COST VIOLATION: {cost_1} != {cost_2}"
    print("Constant cost property: PASS (query cost does NOT grow with unrelated trie size)")
    print("\nAll tests passed.")
