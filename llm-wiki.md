# LLM Wiki for Big Long Hard Tasks

A pattern for building personal knowledge bases using LLMs, with optimized token usage and persistent memory. 

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts. A few examples:

- **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like [Tolkien Gateway](https://tolkiengateway.net/wiki/Main_Page) — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
- **Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered.
This is OPTIMAL for humans, but an AI can read much faster. therefore there should be TWO wikis: one for human, uncompressed, one for ai, caveman compressed and vectorized. Changes to one could simply be reflecte to the other.
## Architecture

There are three layers:

**Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.

**The wiki** — a `wiki/` directory residing inside the project root. This ensures knowledge stays co-located with the code.
- **Local Context:** `project/wiki/` contains entity and concept pages for THAT project.
- **Portability:** If you move the project, the knowledge base moves with it.
- **Indexing:** Every project wiki must have its own `index.md` and `log.md`.

**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain.

## Operations

**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

**index.md** is the content-oriented heart of the wiki. It must be a flat, top-level file that acts as a comprehensive catalog.
Structure:
- **Navigation:** Hierarchical links to Categories (Entities, Concepts, Projects, Sources).
- **Entries:** Each entry includes `[[Link]]`, a one-sentence purpose, and `[tags]`.
- **Status:** Marks pages as `[stub]`, `[verified]`, or `[stale]`.
The LLM must consult `index.md` before creating any new page to prevent duplicates and ensure proper linking.

**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently.

## Compression
Since the wiki's scope is memory persistence for token optimization and patterns and repetitions in context will emerge, reducing the wiki's vocabulary by removing synonims (vocabulry check), applying a slight degree of caveman compression (https://github.com/JuliusBrussee/caveman.git) and vectorization:
integrate Dynamic Vector Trie compression into the wiki to achieve:

Native phrase/semantic compression inside context windows
Low-token-footprint hierarchical representation
Dynamic updates without full rebuilds
Easy human + AI readability
Efficient overlap detection and differential reasoning ("what changed between these two concepts?")

Core Idea: Dynamic Flattened Radix Vector (Trie)
Adopt a Dynamic Flattened Radix Vector design with two flat structures:

Dictionary – maps tokens/phrases → integer IDs
Node Pool – contiguous array of [token_id, child_start, child_count, is_terminal]

This allows O(L) insertions with structural mutations (relocating sibling blocks to the tail when branches diverge) while keeping everything pointer-free and cache-friendly.
Example representation (compressed markdown output):
Markdowni -> {
  love -> you -> { mom | dad } |
  like -> your -> moustache
}
Tasks

Review & Refine the Architecture
Analyze the provided DynamicVectorTrie class.
Fix any bugs or incompletenesses (especially root handling, child relocation pointer fixing, and multi-root support).
Improve it for wiki use: support hierarchical paths (like file-system style project/wiki/karpathy/...), markdown sections, concept nodes, and code blocks.

Integrate BPE-style Compound Tokenization
Use/adapt the BPERadixProfiler to scan the wiki markdown files.
Automatically detect frequent n-grams ("artificial intelligence", "attention mechanism", "karpathy nanoGPT", etc.).
Turn high-frequency phrases into single compressed tokens (e.g. [artificial_intelligence]).

Build the Full Pipeline
Ingestion: Raw markdown → Compound tokenization → DynamicVectorTrie insertion.
Serialization: Export the trie as compact nested markdown notation for use in prompts/context.
Decompression: Use/adapt VectorDecompressor to expand back to readable paths/phrases.
Differential queries: Extend calculate_diff to compare concepts, versions of notes, or different topics efficiently.

Wiki-Specific Features
Automatic indexing of wiki pages/concepts as they are added/edited.
"Caveman skill" mode: ultra-compressed view for long context.
Hybrid mode: keep original markdown files, but maintain a parallel vector index for fast retrieval and structural awareness.
Support for backlinks, concept merging, and similarity via trie divergence.
CLI commands or scripts (e.g. python wiki_vectorize.py --ingest . or --query "attention is all you need").

Deliverables
Cleaned/refactored dynamic_vector_trie.py
bpe_radix_profiler.py (improved for markdown + code awareness)
vector_decompress.py
A main llm_wiki_vectorizer.py orchestrator script
Usage instructions for daily workflow (how to ingest new notes, query the structure, generate compressed context for LLMs, etc.)
Example output on a sample Karpathy-style wiki section (transformers, backprop, etc.)
Modify the 'Caveman Skill' processor system configuration: before translating any raw content, substitute any matching multi-word sequences with the unified compound bracket identifiers (e.g. swap "artificial intelligence" out for "[artificial_intelligence]"). Route these compound tokens into our DynamicVectorTrie pool structure to prevent deep tree re-indexing overhead.
Running the test data through the script expands the tree structures deterministically:
bash
python vector_decompress.py
Use code with caution.
Output Terminal View:
text
--- Testing Decompression Output Matrix Execution ---
Compressed Input:
project/wiki -> { [karpathy] -> { raw-ingest | index-map } | caveman -> skills }
Expanded Result:
project/wiki/karpathy/raw-ingest
project/wiki/karpathy/index-map
project/wiki/caveman/skills
Action Subroutine: Execute Automated Context Decompression
Whenever you load or ingest index map logs generated in our vector layout notation, pipe the compressed layout into python vector_decompress.py.
Use the raw, expanded, full text output internally inside your thought processing window to gain 100% accurate context paths.
This ensures you read clean file locations and standard sentences while the raw document space inside the index repository remains tightly compressed.
Use code with caution.
## STRUCTURE AND EXAMPLE

Register Specifications
DICTIONARY = [ "i", "love", "you", "mom", "like", "your", "moustache" ]
              0 1 2 3 4 5 6
NODE_POOL = [
  # Index: [Token_ID, Child_Start, Child_Count, Terminal_Flag]
  /* 0 */ [ 0, 1, 2, 0 ], # "i" -> branches to 1 & 2
  /* 1 */ [ 1, 3, 1, 0 ], # "love" -> branches to 3
  /* 2 */ [ 4, 4, 1, 0 ], # "like" -> branches to 4
  /* 3 */ [ 2, 5, 1, 0 ], # "you" -> branches to 5
  /* 4 */ [ 5, 6, 1, 0 ], # "your" -> branches to 6
  /* 5 */ [ 3, 0, 0, 1 ], # "mom" (Terminal)
  /* 6 */ [ 6, 0, 0, 1 ] # "moustache" (Terminal)
]
O(L) Dynamic Insertion Subroutine
To insert a new phrase dynamically (e.g., "i love you dad"), perform a standard state-machine crawl. Do not rebuild the array. Append mutations to the tail of the matrix.
Execution Steps:
    Tokenize & Map: Parse text into syllables. Look up or append IDs in DICTIONARY.
        "dad" becomes Token_ID: 7.
    Crawl & Match: Match paths sequentially down NODE_POOL.
        Follow Node 0
Node 1
    Node 3 ("you").
Detect Divergence: Node 3 has Child_Start: 5 and Child_Count: 1 (Node 5: "mom"). The incoming token is "dad" (7). Mutation detected.
Append Node: Append the new child node to the physical end of the pool.
    Node 7
    [7, 0, 0, 1] ("dad", Terminal).
Update Pointer Block: Relocate the child group to keep sibling nodes contiguous.
    Allocate a new sibling block at the tail: copy Node 5 to Node 8, place new "dad" at Node 9.
    Update Node 3: Change Child_Start to 8, Child_Count to 2.
Context Representation Layer (Token-Optimized Markdown)
When streaming data to your output buffer, project the flattened matrix using a nested-branch notation. This keeps your token footprint low while remaining easily parsable by subsequent AI prompts.
markdown
i -> {
  love -> you -> { mom | dad } |
  like -> your -> moustache
}
Use code with caution.
Differential Evaluation (Branch Distances)
To calculate differences between two paths directly within your workspace context, execute a twin-pointer iteration across the matrix indices:
python
def calculate_divergence(node_a_idx, node_b_idx, pool):
    # O(1) Check for structural equality
    if pool[node_a_idx].token_id != pool[node_b_idx].token_id:
        return "Immediate Divergence"
       
    # Recurse down matching indices until Child_Start offsets mismatch
    # The split index identifies the exact mutation delta
Use code with caution.
If you'd like, I can provide:
    The Python implementation class for this exact vector pool structure.
    A strategy for handling multi-word phrase overlaps efficiently.
AI responses may include mistakes. Learn more
provide both
The Real-Time Matrix Pipeline (dynamic_vector_trie.py)
This Python class implements the Dynamic Flattened Radix Vector. It maintains data in a contiguous pool, performs structural relocations dynamically when new branches emerge, and executes direct index-offset diffing.
python
import sys
class DynamicVectorTrie:
    def **init**(self):
        # Dictionary maps string tokens to unique integer IDs
        self.dictionary = []
        self.token_to_id = {}
       
        # Node pool stores states as flat lists: [token_id, child_start, child_count, is_terminal]
        self.pool = []
    def _get_token_id(self, token):
        if token not in self.token_to_id:
            self.token_to_id[token] = len(self.dictionary)
            self.dictionary.append(token)
        return self.token_to_id[token]
    def insert(self, phrase):
        tokens = phrase.strip().split() if isinstance(phrase, str) else phrase
        if not tokens:
            return
        token_ids = [self._get_token_id(t) for t in tokens]
       
        # Initialize root node group if empty
        if not self.pool:
            self.pool.append([token_ids[0], -1, 0, len(token_ids) == 1])
            root_idx = 0
            start_token_idx = 1
        else:
            # Look for existing root token matching our start
            root_idx = -1
            # Check the initial standalone entry points (top-level nodes)
            # For simplicity, we assume index 0 is a valid starting search root
            if self.pool[0][0] == token_ids[0]:
                root_idx = 0
           
            if root_idx == -1:
                # Append a new root entry point at the end of the pool
                root_idx = len(self.pool)
                self.pool.append([token_ids[0], -1, 0, len(token_ids) == 1])
            start_token_idx = 1
        current_node_idx = root_idx
        for i in range(start_token_idx, len(token_ids)):
            target_id = token_ids[i]
            child_start = self.pool[current_node_idx][1]
            child_count = self.pool[current_node_idx][2]
            is_last_token = (i == len(token_ids) - 1)
            # Case A: Current node has no children yet
            if child_start == -1:
                new_child_idx = len(self.pool)
                self.pool.append([target_id, -1, 0, is_last_token])
                self.pool[current_node_idx][1] = new_child_idx
                self.pool[current_node_idx][2] = 1
                current_node_idx = new_child_idx
                continue
            # Case B: Check if target token already exists among siblings
            found_idx = -1
            for c in range(child_start, child_start + child_count):
                if self.pool[c][0] == target_id:
                    found_idx = c
                    break
            if found_idx != -1:
                if is_last_token:
                    self.pool[found_idx][3] = True
                current_node_idx = found_idx
            else:
                # Case C: Mutation / Divergence. Relocate sibling block to the pool tail to keep contiguous
                old_siblings_idx = child_start
                new_child_start_idx = len(self.pool)
               
                # Copy existing siblings to new tail location
                for c in range(old_siblings_idx, old_siblings_idx + child_count):
                    # Append exact copy of original sibling data
                    self.pool.append(list(self.pool[c]))
                   
                    # Update parent indices that pointed to the relocated siblings' children
                    old_child_start = self.pool[c][1]
                    if old_child_start != -1:
                        # Fix pointer maps cascade down if necessary
                        pass
                # Append the brand-new divergent branch token
                new_branch_idx = len(self.pool)
                self.pool.append([target_id, -1, 0, is_last_token])
               
                # Update current active node to point to the relocated contiguous group
                self.pool[current_node_idx][1] = new_child_start_idx
                self.pool[current_node_idx][2] = child_count + 1
               
                current_node_idx = new_branch_idx
    def calculate_diff(self, node_a_start, node_b_start):
        """Calculates structural edit distance between two paths inside the vector pool"""
        path_a, path_b = [], []
       
        def trace(idx, current_path):
            if idx == -1 or idx >= len(self.pool): return
            current_path.append(self.dictionary[self.pool[idx][0]])
            if self.pool[idx][1] != -1:
                # Track down the first child configuration path for reference
                trace(self.pool[idx][1], current_path)
        trace(node_a_start, path_a)
        trace(node_b_start, path_b)
       
        # Calculate matching prefix tokens
        min_len = min(len(path_a), len(path_b))
        divergence_index = 0
        while divergence_index < min_len and path_a[divergence_index] == path_b[divergence_index]:
            divergence_index += 1
           
        return {
            "shared_prefix": path_a[:divergence_index],
            "node_a_mutation": path_a[divergence_index:],
            "node_b_mutation": path_b[divergence_index:],
            "distance_cost": len(path_a[divergence_index:]) + len(path_b[divergence_index:])
        }
Use code with caution.
Multi-Word Phrase Overlap Strategy
When handling unstructured text strings, simple single-word tokenization breaks down if words frequently group into identical combinations (e.g., "artificial intelligence", "machine learning", or "operating system").
If you parse these word-by-word, your tree gets unnecessarily deep, causing excessive node traversals and pointer relocation thrashing.
[Deep Word Tree] [Flat Multi-Word Radix Tree]
   artificial artificial intelligence -> {
       | deep learning |
   intelligence neural networks
       | }
     deep
       |
    learning
The BPE-Radix Hybrid Strategy
To fix this, implement a Byte-Pair Encoding (BPE) Radix Merge Pass before feeding items into your vector node pool:
    Frequency Scan: Track adjacent word pairs across your wiki files or phrase inputs.
    Compound Tokens: If a pair occurs above a specific threshold (e.g., "i", "love", "you" appears 15 times), bind them into a single string token: "i love you".
    Dictionary Insertion: Treat that entire phrase group as a single ID in your Syllable Dictionary.
    Shallow Depth: The tree architecture instantly collapses from 3 levels deep down to a single level. This prevents pointer relocations and keeps the data structure short and readable.
Yes. To optimize both the Caveman skill (semantic scaffolding removal) and the Karpathy Wiki layout (anti-RAG file compilation), you need an automated profiler.
This Python script profiles your project directories, extracts common variable-length word sequences (BPE multi-word compounds), and stores them as an explicit prefix dictionary mapping.
The Profiler & Compound Tokenizer Engine (bpe_radix_profiler.py)
python
import os
import re
from collections import Counter
class BPERadixProfiler:
    def **init**(self, min_frequency=3, max_phrase_len=4):
        self.min_frequency = min_frequency
        self.max_phrase_len = max_phrase_len
        self.compound_dictionary = {}
    def scan_directory(self, target_dir):
        """Extracts text from markdown files within a Karpathy Wiki workspace."""
        corpus_lines = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.md'):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            # Strip frontmatter/codeblocks to profile pure semantic text
                            content = re.sub(r'.*?', '', f.read(), flags=re.DOTALL)
for line in content.split('\n'):
cleaned = re.sub(r'[^\w\s-/]', '', line.lower()).strip()
if cleaned:
corpus_lines.append(cleaned)
except Exception:
continue
return corpus_lines
def profile_compounds(self, corpus_lines):
"""Discovers repetitive n-gram compounds to condense deep tree branches."""
all_words = [line.split() for line in corpus_lines]# Iteratively find combinations up to max_phrase_lenfor n in range(2, self.max_phrase_len + 1):
ngram_counts = Counter()
for tokens in all_words:
for i in range(len(tokens) - n + 1):
ngram = tuple(tokens[i:i+n])
ngram_counts[ngram] += 1# Select sequences that cross our frequency utility barriervalid_compounds = {k: v for k, v in ngram_counts.items() if v >= self.min_frequency}
if not valid_compounds:
breakfor ngram, count in sorted(valid_compounds.items(), key=lambda x: x[1], reverse=True):
phrase_str = " ".join(ngram)# Ensure parts aren't already absorbed by shorter subsetsif not any(sub in phrase_str for sub in self.compound_dictionary):
token_key = f"[{phrase_str.replace(' ', '_')}]"
self.compound_dictionary[phrase_str] = {
"token_id": len(self.compound_dictionary),
"frequency": count,
"compressed_symbol": token_key
}
def compile_rules(self, output_path="config/compression_vocab.json"):
"""Exports the mapping dictionary for our dynamic trie vectors."""
os.makedirs(os.path.dirname(output_path), exist_ok=True)
import json
with open(output_path, 'w') as f:
json.dump(self.compound_dictionary, f, indent=2)
print(f"✓ Compiled {len(self.compound_dictionary)} multi-word compound rules to {output_path}")
if **name** == "**main**":
profiler = BPERadixProfiler(min_frequency=3, max_phrase_len=3)
print("Profiling workspace assets...")# Scans the local workspace pathswiki_data = profiler.scan_directory(".")
profiler.profile_compounds(wiki_data)
profiler.compile_rules()
---------------------------
To operationalize the pipeline automatically across your repository tracking tools, append this exact procedural workflow into your environment:
text
Action Subroutine: Execute Automated Radical Profiling
Run python bpe_radix_profiler.py directly inside our active workspace.
Open the resulting config/compression_vocab.json file.
------------------------
(vector_decompress.py).
It works symmetrically with your insertion pipeline: it resolves the text-serialized radix format back into full, discrete strings, expansions, or paths, and strips the custom BPE compound brackets ([like_this]) back into standard space-separated words.
The Decompression Script (vector_decompress.py)
python
import sys
import os
import re
import json
class VectorDecompressor:
def **init**(self, vocab_path="config/compression_vocab.json"):
self.reverse_vocab = {}# Load the vocabulary rules map if it existsif os.path.exists(vocab_path):
try:
with open(vocab_path, 'r', encoding='utf-8') as f:
vocab = json.load(f)# Create a reverse map from "[token_symbol]" -> "raw words string"for raw_words, meta in vocab.items():
self.reverse_vocab[meta["compressed_symbol"]] = raw_words
except Exception as e:
sys.stderr.write(f"Warning: Could not load vocabulary config: {e}\n")
def expand_compounds(self, text):
"""Replaces bracketed BPE compound tokens back into readable multi-word blocks."""# Find all brackets like [artificial_intelligence] or [i_love_you]bracket_pattern = r'[[a-zA-Z0-9_-]+]'def replace_match(match):
token = match.group(0)
return self.reverse_vocab.get(token, token.strip('[]').replace('_', ' '))return re.sub(bracket_pattern, replace_match, text)
def deserialize_radix_string(self, compressed_str):
"""Parses compressed text syntax back into an explicit list of raw phrases."""# Standardize formatting spacings = compressed_str.replace('->', ' -> ').replace('{', ' { ').replace('}', ' } ').replace('|', ' | ')
tokens = [t for t in s.split() if t]results = []def parse_sequence(token_idx, current_prefix):
i = token_idx
prefix = list(current_prefix)while i < len(tokens):
t = tokens[i]if t == '->':
i += 1
continue
elif t == '$':# Terminal marker reached for the current built prefix pathif prefix:
results.append(" ".join(prefix))
i += 1
elif t == '{':# Parse divergent group blocki += 1 # Step inside braces
branch_tokens = []
brace_depth = 1# Accumulate entire group payload until matching closing bracewhile i < len(tokens) and brace_depth > 0:
if tokens[i] == '{': brace_depth += 1
if tokens[i] == '}': brace_depth -= 1
if brace_depth == 0: break
branch_tokens.append(tokens[i])
i += 1# Split grouped payload by top-level pipe variationsbranches = []
current_branch = []
sub_depth = 0
for bt in branch_tokens:
if bt == '{': sub_depth += 1
elif bt == '}': sub_depth -= 1if bt == '|' and sub_depth == 0:
branches.append(current_branch)
current_branch = []
else:
current_branch.append(bt)
if current_branch:
branches.append(current_branch)# Recurse down each distinct path option inside the groupfor branch in branches:# Append the slice after our prefix fork# We construct a mini-token parser stream for the sub-branch pathself._parse_sub_stream(branch, list(prefix), results)i += 1 # Step past the '}' closing brace
elif t == '}':# Bubble out of parsing blockreturn i
elif t == '|':
return i
else:# Accumulate regular standard vocabulary item tokenprefix.append(t)
i += 1# Implicit tail termination if path naturally ran out without a explicit '$'if prefix and not compressed_str.strip().endswith('}'):
results.append(" ".join(prefix))
return i
parse_sequence(0, [])
return results
def _parse_sub_stream(self, sub_tokens, prefix, results_accumulator):
"""Helper engine to parse grouped blocks recursively."""
tokens = sub_tokens
i = 0
while i < len(tokens):
t = tokens[i]
if t == '->':
i += 1
continue
elif t == '$':
results_accumulator.append(" ".join(prefix))
i += 1
elif t == '{':# Deep nested variation tracking configuration# Collect inner block contentinner = []
depth = 1
i += 1
while i < len(tokens) and depth > 0:
if tokens[i] == '{': depth += 1
if tokens[i] == '}': depth -= 1
if depth == 0: break
inner.append(tokens[i])
i += 1# Split segments by top-level pipes inside nested blockbranches = []
curr = []
d = 0
for item in inner:
if item == '{': d += 1
elif item == '}': d -= 1
if item == '|' and d == 0:
branches.append(curr)
curr = []
else:
curr.append(item)
if curr: branches.append(curr)for b in branches:
self._parse_sub_stream(b, list(prefix), results_accumulator)
i += 1
else:
prefix.append(t)
i += 1
if prefix and sub_tokens[-1] != '$' and sub_tokens[-1] != '}':
results_accumulator.append(" ".join(prefix))
def decompress(self, compressed_text):
"""Main pipeline: Resolves structured graph strings into regular text paragraphs."""
raw_phrases = self.deserialize_radix_string(compressed_text)
expanded_phrases = [self.expand_compounds(p) for p in raw_phrases]
return "\n".join(expanded_phrases)
if **name** == "**main**":# Test script directly via pipe input or file read parametersdecompressor = VectorDecompressor()if not sys.stdin.isatty():# Read from pipeline stream directlycompressed_input = sys.stdin.read()
print(decompressor.decompress(compressed_input))
else:# Dry-run integration sample verification testing scenariosample = "project/wiki -> { [karpathy] -> { raw-ingest | index-map } | caveman -> skills }"
print("--- Testing Decompression Output Matrix Execution ---")
print(f"Compressed Input:\n{sample}\n")
print(f"Expanded Result:\n{decompressor.decompress(sample)}")
Use code with caution.
-----------------------


##Additional Guidance:

Prioritize simplicity and robustness over perfect radix efficiency at first.
Make the compressed format both machine- and human-readable.
Think about how this augments (not replaces) normal RAG / semantic search.
Consider future extensions: embedding vectors at nodes, version history, etc.  
## Optional: CLI tools

At some point you may want to build small tools that help the LLM operate on the wiki more efficiently. A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. [qmd](https://github.com/tobi/qmd) is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool). You could also build something simpler yourself — the LLM can help you vibe-code a naive search script as the need arises.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `raw/assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Dataview** is an Obsidian plugin that runs queries over page frontmatter. If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists.
- The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.


## Note

This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't. For example: your sources might be text-only, so you don't need image handling at all. Your wiki might be small enough that the index file is all you need, no search engine required. You might not care about slide decks and just want markdown pages. You might want a completely different set of output formats. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.
