import requests
import os
import time
from datetime import datetime, timezone

# --- TEST CONFIGURATION ---
# I added "OR+sale" to the query below. 
# This widens the net significantly so you should catch something.
TARGET_URL = "https://www.reddit.com/search.json?q=glitch+OR+%22price+error%22+OR+sale&sort=new&limit=10"

HEADERS = {"User-Agent": "GlitchHunter/1.0"}
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(title, link):
    if not WEBHOOK_URL:
        print("Error: No Discord Webhook URL found.")
        return
    data = {
        "content": f"🚨 **TEST ALERT (Sale)** 🚨\n\n**{title}**\n[Click to View Deal]({link})"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_for_glitches():
    print(f"Checking {TARGET_URL}...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS)
        response.raise_for_status()
        posts = response.json()['data']['children']
        
        found_count = 0
        for post in posts:
            post_data = post['data']
            created_utc = post_data['created_utc']
            
            # Keep the 20-minute filter to prove the logic works
            post_time = datetime.fromtimestamp(created_utc, timezone.utc)
            now = datetime.now(timezone.utc)
            
            # Debug print to see what it finds in the logs
            print(f"Found post: {post_data['title']} (Age: {(now - post_time).total_seconds() / 60:.1f} mins)")
            
            if (now - post_time).total_seconds() / 60 <= 20:
                 print(f"--> MATCH! Sending alert...")
                 send_discord_alert(post_data['title'], f"https://www.reddit.com{post_data['permalink']}")
                 found_count += 1
        
        print(f"Scan complete. Found {found_count} new alerts.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_for_glitches()
