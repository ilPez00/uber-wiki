# PROJECT: LLMWIKI
> Scalable knowledge indexing engine.

---

## OVERVIEW
A Rust-based implementation of Andrej Karpathy's LLM-Wiki pattern. Solves the $index.md$ token bottleneck.

## ARCHITECTURE
- **Engine:** Rust, Tantivy (BM25), fastembed (Semantic).
- **Format:** Frontmatter-enriched Markdown.
- **Retrieval:** Hybrid Search (Keyword + Semantic).

## SOURCE
- Located at: `~/llmwiki/`.
- Repository: [llmwiki](https://github.com/krakiun/llmwiki.git).

---
[Home](../index.md)
