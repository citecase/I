import feedparser
import os

# Configuration
FEED_URL = "https://caseciter.com/rss/"
TARGET_FILE = "daily.md"

def run():
    # Parse the RSS feed
    feed = feedparser.parse(FEED_URL)
    
    # Check if the file exists; if so, read it to prevent duplicates
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    new_links_batch = ""

    # Process entries from oldest to newest to maintain correct "newest at top" order
    for entry in reversed(feed.entries):
        # We use the unique URL to check if we've already logged this post
        if entry.link not in existing_content:
            print(f"New link found: {entry.title}")
            # Format as a clean Markdown bullet point
            line = f"* [{entry.title}]({entry.link})\n"
            new_links_batch = line + new_links_batch

    if new_links_batch:
        # Prepend the new batch of links to the existing file content
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_links_batch + existing_content)
        print(f"Successfully updated {TARGET_FILE}")
    else:
        print("No new updates found since the last check.")

if __name__ == "__main__":
    run()
