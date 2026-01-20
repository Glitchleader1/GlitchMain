import requests
import os
import time
from datetime import datetime, timezone

# --- TEST CONFIGURATION ---
# 1. The Targets: We are looking at specific deal subreddits only.
# 2. The Query: We are searching for "sale" (which is everywhere) just to prove it works.
TARGET_URL = "https://www.reddit.com/r/buildapcsales+gamedeals+consoledeals+4kbluray+frugalmalefashion/search.json?q=sale&restrict_sr=on&sort=new&limit=5"

HEADERS = {"User-Agent": "GlitchHunter/1.0"}
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(title, link, subreddit):
    if not WEBHOOK_URL:
        return
    
    data = {
        "content": f"🚨 **VERIFICATION ALERT** 🚨\n\n**Subreddit:** r/{subreddit}\n**Item:** {title}\n[Click to View]({link})"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_for_glitches():
    print(f"Checking specific subreddits for 'sale'...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS)
        response.raise_for_status()
        posts = response.json()['data']['children']
        
        for post in posts:
            post_data = post['data']
            created_utc = post_data['created_utc']
            title = post_data['title']
            subreddit = post_data['subreddit']
            permalink = f"https://www.reddit.com{post_data['permalink']}"
            
            # --- NO TIME FILTER FOR THIS TEST ---
            # We want to see the last 5 posts no matter what, 
            # just to prove we are reading the right list.
            print(f"--> Found post in r/{subreddit}: {title}")
            send_discord_alert(title, permalink, subreddit)

        print(f"Test complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_for_glitches()
