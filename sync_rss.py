import feedparser
import os

FEED_URL = "https://caseciter.com/rss/"
TARGET_FILE = "daily.md"

def run():
    # Parsing with namespaces enabled to catch 'content:encoded'
    feed = feedparser.parse(FEED_URL)
    
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    new_entries_text = ""

    # Sort entries by date (oldest to newest) so we prepend correctly
    for entry in reversed(feed.entries):
        if entry.link not in existing_content:
            print(f"Syncing full notes: {entry.title}")
            
            # GHOST SPECIFIC: Get the full blog body
            # We check 'content' list first (common in Atom/Ghost), 
            # then 'content_encoded', then finally 'description'
            full_body = ""
            if 'content' in entry:
                full_body = entry.content[0].value
            elif 'content_encoded' in entry:
                full_body = entry.content_encoded
            else:
                full_body = entry.get('description', 'No content available.')

            # Build the Markdown entry
            entry_md = f"## {entry.title}\n"
            entry_md += f"*Source: {entry.link}*\n\n"
            entry_md += f"{full_body}\n"
            entry_md += "\n---\n\n"
            
            new_entries_text = entry_md + new_entries_text

    if new_entries_text:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            # Newest posts stay at the top
            f.write(new_entries_text + existing_content)
        print(f"Successfully updated {TARGET_FILE}")
    else:
        print("No new notes found on CaseCiter.")

if __name__ == "__main__":
    run()
