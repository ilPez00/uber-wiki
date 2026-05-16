import os
import sys
import datetime

WIKI_ROOT = "/home/gio/wiki"

def ingest(content, category="general"):
    """
    Hyperlinked Ingestion Script.
    Appends to raw_log.md and links to related wiki sections.
    """
    timestamp = datetime.datetime.now().isoformat()
    log_path = os.path.join(WIKI_ROOT, "raw_log.md")
    
    # Simple semantic routing
    links = []
    content_lower = content.lower()
    if "git" in content_lower or "repo" in content_lower:
        links.append("[Repos](repos.md)")
    if "key" in content_lower or "token" in content_lower:
        links.append("[Accounts](accounts.md)")
    if "aura" in content_lower or "praxis" in content_lower:
        links.append("[Projects](projects/)")

    link_str = " | ".join(links)
    entry = f"\n---\n### {timestamp} | {category}\n**Related:** {link_str}\n\n{content}\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    
    print(f"Ingested to {log_path}. Links: {link_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ingest.py 'content text' [category]")
        sys.exit(1)
    
    text = sys.argv[1]
    cat = sys.argv[2] if len(sys.argv) > 2 else "general"
    ingest(text, cat)
