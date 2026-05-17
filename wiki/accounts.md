---
title: Accounts & Keys
description: Account metadata and secret locations. GitHub ilPez00, Stripe, SerpAPI, AIMLAPI, Mistral/Gemini/Groq keys in ~/ai/.env.
tags: [accounts, keys, auth]
updated: 2026-05-17
---
# ACCOUNTS & KEYS
> Central repository of account metadata and secret locations.

## GITHUB
- **User:** ilPez00
- **Email:** pezzingiovanniantonio@gmail.com
- **Auth:** SSH keys in `~/.ssh/known_hosts`, `gh` credential helper.
- **Tokens:** `AI_GITHUB_TOKEN` stored in `~/.env`.

## SERVICES (From .env)
- **Stripe:** `PRAXIS_STRIPE_SECRET_KEY` (Accountability betting).
- **SerpAPI:** `SEARCH_SERPAPI_KEY` (Web search).
- **AIMLAPI:** `AIMLAPI_KEY` (LLM proxy).
- **Mistral/Gemini/Groq:** Keys distributed in `~/ai/.env`.

---
[Home](index.md)
