import requests
import os
import time
from datetime import datetime, timezone

# --- CONFIGURATION ---
# IMPROVED SEARCH: 
# We now only search inside these specific communities:
# r/buildapcsales (Tech/PC parts)
# r/gamedeals (Video Games)
# r/consoledeals (Xbox/PS5/Switch)
# r/4kbluray (Movies/Media)
# r/tools (Home Improvement/Tools)
# r/frugalmalefashion (Clothing/Gear)

# The query looks for "glitch", "price error", or "misprice" inside those groups.
TARGET_URL = "https://www.reddit.com/r/buildapcsales+gamedeals+consoledeals+4kbluray+tools+frugalmalefashion/search.json?q=glitch+OR+%22price+error%22+OR+misprice&restrict_sr=on&sort=new&limit=10"

HEADERS = {"User-Agent": "GlitchHunter/2.0"}
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(title, link, subreddit):
    if not WEBHOOK_URL:
        return 
    
    data = {
        "content": f"🚨 **GLITCH ALERT** in r/{subreddit} 🚨\n\n**{title}**\n[Click to View Deal]({link})"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_for_glitches():
    print(f"Checking targeted subreddits...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS)
        response.raise_for_status()
        
        # Reddit JSON structure varies slightly if no results are found
        data = response.json()
        if 'data' not in data or 'children' not in data['data']:
            print("No posts found or API structure changed.")
            return

        posts = data['data']['children']
        found_count = 0
        
        for post in posts:
            post_data = post['data']
            created_utc = post_data['created_utc']
            title = post_data['title']
            subreddit = post_data['subreddit']
            permalink = f"https://www.reddit.com{post_data['permalink']}"
            
            # --- TIME FILTER ---
            # Only alert if the post is less than 20 minutes old
            post_time = datetime.fromtimestamp(created_utc, timezone.utc)
            now = datetime.now(timezone.utc)
            minutes_ago = (now - post_time).total_seconds() / 60
            
            if minutes_ago <= 20:
                 print(f"--> FRESH DEAL ({minutes_ago:.1f}m ago): {title}")
                 send_discord_alert(title, permalink, subreddit)
                 found_count += 1
            else:
                print(f"Skipping old post in r/{subreddit}: {minutes_ago:.1f} mins old")

        print(f"Scan complete. Found {found_count} new alerts.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_for_glitches()
