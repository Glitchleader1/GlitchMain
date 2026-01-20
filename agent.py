import requests
import os
import time
from datetime import datetime, timezone

# --- CONFIGURATION ---
# The URL to search Reddit for "glitch" or "price error" sorted by newest
# This acts like an RSS feed but in JSON format which is easier for robots to read.
TARGET_URL = "https://www.reddit.com/search.json?q=glitch+OR+%22price+error%22+OR+misprice&sort=new&limit=10"

# Keywords to validate (double check to ensure high quality)
KEYWORDS = ["glitch", "error", "mistake", "price", "wrong"]

# Discord Webhook (loaded from the environment for security)
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Browser User-Agent (Required so Reddit doesn't block the script)
HEADERS = {"User-Agent": "GlitchHunter/1.0"}

def send_discord_alert(title, link, price_hint=""):
    if not WEBHOOK_URL:
        print("Error: No Discord Webhook URL found.")
        return

    data = {
        "content": f"🚨 **GLITCH ALERT** 🚨\n\n**{title}**\n{price_hint}\n[Click to View Deal]({link})"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"Sent alert for: {title}")
    else:
        print(f"Failed to send alert: {response.status_code}")

def check_for_glitches():
    print(f"Checking {TARGET_URL}...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        posts = data['data']['children']
        
        # Get the current time to ensure we don't alert on old stuff
        # (In a simple script, we just check the top 10 results. 
        # For a pro version, we would save the last seen ID to a file.)
        
        found_count = 0
        
        for post in posts:
            post_data = post['data']
            title = post_data['title']
            url = post_data['url']
            permalink = f"https://www.reddit.com{post_data['permalink']}"
            created_utc = post_data['created_utc']
            
            # Check if the post is recent (last 20 minutes)
            # This prevents reposting old deals every time the script runs
            post_time = datetime.fromtimestamp(created_utc, timezone.utc)
            now = datetime.now(timezone.utc)
            time_diff = (now - post_time).total_seconds() / 60
            
            if time_diff <= 20: # Only alert if posted in the last 20 mins
                 print(f"Found fresh post: {title}")
                 send_discord_alert(title, permalink)
                 found_count += 1
            else:
                # If we hit old posts, we can stop checking
                pass 

        print(f"Scan complete. Found {found_count} new alerts.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_for_glitches()
