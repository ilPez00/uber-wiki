---
title: How To Use This Wiki
description: Wiki usage guide. Ingest with ingest.py, llmwiki for search/MCP, uberwiki_cli for sync and Aura bridge export.
tags: [guide, workflow, wiki]
updated: 2026-05-17
---
# HOW TO USE THIS WIKI
> Automated and Manual knowledge management.

---

## 1. INGESTING NEW DATA
Use the `ingest.py` script to add notes, chat logs, or project updates.
```bash
python3 ~/wiki/ingest.py "Added new feature to Praxis backend." "praxis"
```
The script will:
- Append to `raw_log.md`.
- Suggest links to relevant wiki pages (Repos, Accounts, etc.).

## 2. LLMWIKI INTEGRATION
Once the Gemma 4 model finishes downloading to `/media/gio/Volume/models/`:
1. Use `llmwiki index` to build the search index.
2. Use `llmwiki search "query"` for lightning-fast hybrid retrieval.

## 3. UPDATING ACCOUNTS
If you add new API keys to `~/ai/.env`, the wiki will detect them during the next scan or you can manually update `accounts.md`.

---
[Home](index.md)
