import feedparser
import os
import requests
import google.generativeai as genai

# Load keys from the Cloud Vault
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

RSS_FEEDS = [
    "https://www.reddit.com/r/buildapcsales/new/.rss",
    "https://www.reddit.com/r/gamedeals/new/.rss",
    "https://www.reddit.com/r/switchdeals/new/.rss"
]

def check_glitch(title):
    try:
        prompt = f"Is '{title}' a 'GLITCH' (price error, 90% off) or 'SALE'? Reply GLITCH or SALE."
        response = model.generate_content(prompt)
        return response.text.strip().upper()
    except:
        return "ERROR"

def send_alert(title, link):
    data = {"content": f"🚨 **GLITCH:** {title}\n{link}"}
    requests.post(DISCORD_WEBHOOK, json=data)

if __name__ == "__main__":
    print("--- SCANNING ---")
    for feed in RSS_FEEDS:
        d = feedparser.parse(feed, agent="Mozilla/5.0")
        for entry in d.entries[:5]:
            if any(w in entry.title.lower() for w in ['price error', 'glitch', 'misprice', 'free']):
                if "GLITCH" in check_glitch(entry.title):
                    send_alert(entry.title, entry.link)
                  
