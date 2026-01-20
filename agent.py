import feedparser
import requests
import os
import time
from datetime import datetime, timezone, timedelta

# --- CONFIGURATION ---
# Source: Slickdeals Popular Deals (Sorted by Newest)
RSS_URL = "https://slickdeals.net/newsearch.php?mode=popdeals&searcharea=deals&sort=newest&rss=1"

# Keywords to trigger an alert
KEYWORDS = ["glitch", "price error", "mistake", "misprice", "steal", "crazy", "free"]

# SET THIS TO TRUE TO TEST THE CONNECTION (Sends top 3 deals instantly)
# SET TO FALSE TO WAIT FOR REAL GLITCHES
TEST_MODE = True 

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(title, link, is_test=False):
    if not WEBHOOK_URL:
        return
    
    alert_type = "🚨 **TEST ALERT** 🚨" if is_test else "🔥 **GLITCH DETECTED** 🔥"
    
    data = {
        "content": f"{alert_type}\n\n**{title}**\n[Click to View Deal]({link})"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_slickdeals():
    print(f"Reading RSS Feed: {RSS_URL}...")
    feed = feedparser.parse(RSS_URL)
    
    print(f"Found {len(feed.entries)} entries.")
    
    found_count = 0
    
    for i, entry in enumerate(feed.entries):
        title = entry.title
        link = entry.link
        
        # In RSS, 'published_parsed' is a time struct. We convert to simple time.
        # Note: Slickdeals RSS sometimes delays timestamps, so we check the last 30 mins.
        
        # --- TEST MODE LOGIC ---
        if TEST_MODE and i < 3:
            print(f"Sending Test Alert: {title}")
            send_discord_alert(title, link, is_test=True)
            found_count += 1
            continue

        # --- REAL HUNTING LOGIC ---
        # 1. Check Keywords
        if any(keyword in title.lower() for keyword in KEYWORDS):
            print(f"--> MATCH FOUND: {title}")
            send_discord_alert(title, link, is_test=False)
            found_count += 1
        else:
            # Optional: Print what it saw just to be sure
            # print(f"Checked: {title} (No Match)")
            pass

    print(f"Scan complete. Alerts sent: {found_count}")

if __name__ == "__main__":
    check_slickdeals()
