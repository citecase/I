import feedparser
import os

FEED_URL = "https://caseciter.com/rss/"
TARGET_FILE = "daily.md"

def run():
    # Use 'content:encoded' for full blog/note text
    feed = feedparser.parse(FEED_URL)
    
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    new_entries_text = ""

    # Reverse to keep chronological order (newest at top)
    for entry in reversed(feed.entries):
        if entry.link not in existing_content:
            print(f"Adding full notes for: {entry.title}")
            
            # GHOST TIP: Full content is usually in 'content_encoded' or 'summary'
            # We try 'content_encoded' first, then fall back to 'description'
            full_notes = entry.get('content_encoded', entry.get('description', 'No content found.'))

            entry_md = f"## {entry.title}\n"
            entry_md += f"*Source: {entry.link}*\n\n"
            entry_md += f"{full_notes}\n"
            entry_md += "\n---\n\n"
            
            new_entries_text = entry_md + new_entries_text

    if new_entries_text:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_entries_text + existing_content)
        print("Done!")
    else:
        print("Everything is already up to date.")

if __name__ == "__main__":
    run()
