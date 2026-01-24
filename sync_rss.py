import feedparser
import os

FEED_URL = "https://caseciter.com/rss/"
TARGET_FILE = "daily.md"

def run():
    feed = feedparser.parse(FEED_URL)
    
    # Read existing content to avoid duplicates
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    new_entries_text = ""

    # Reverse entries to process oldest to newest (so newest ends up on top)
    for entry in reversed(feed.entries):
        # Check if this specific link is already in our file
        if entry.link not in existing_content:
            print(f"Adding new post: {entry.title}")
            
            # Formatting the entry for the Markdown file
            entry_md = f"## {entry.title}\n"
            entry_md += f"*Published on: {entry.published}* \n"
            entry_md += f"**Link:** {entry.link}\n\n"
            entry_md += f"{entry.description}\n"
            entry_md += "\n---\n\n"
            
            new_entries_text = entry_md + new_entries_text

    if new_entries_text:
        # Write new entries at the top of the file
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_entries_text + existing_content)
        print("daily.md updated.")
    else:
        print("No new posts to add.")

if __name__ == "__main__":
    run()
