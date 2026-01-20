import requests
import os
import time
from datetime import datetime, timezone

# --- CONFIGURATION ---
TARGET_URL = "https://www.reddit.com/search.json?q=glitch+OR+%22price+error%22+OR+misprice&sort=new&limit=10"
HEADERS = {"User-Agent": "GlitchHunter/1.0"}
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(title, link):
    if not WEBHOOK_URL:
        return 
    
    data = {
        "content": f"🚨 **GLITCH ALERT** 🚨\n\n**{title}**\n[Click to View Deal]({link})"
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
            title = post_data['title']
            permalink = f"https://www.reddit.com{post_data['permalink']}"
            
            # THE TIME FILTER: Only alert if less than 20 mins old
            post_time = datetime.fromtimestamp(created_utc, timezone.utc)
            now = datetime.now(timezone.utc)
            minutes_ago = (now - post_time).total_seconds() / 60
            
            if minutes_ago <= 20:
                 print(f"--> FRESH DEAL FOUND ({minutes_ago:.1f} mins ago): {title}")
                 send_discord_alert(title, permalink)
                 found_count += 1
            else:
                print(f"Skipping old post: {title} ({minutes_ago:.1f} mins old)")

        print(f"Scan complete. Found {found_count} new alerts.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_for_glitches()
