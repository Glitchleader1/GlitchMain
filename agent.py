import os
import requests

# 1. Get the Secret
webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

print("--- DIAGNOSTIC START ---")

# 2. Check if the Secret exists
if not webhook_url:
    print("❌ CRITICAL ERROR: The 'DISCORD_WEBHOOK_URL' secret is MISSING or EMPTY.")
    print("Fix: Go to Settings > Secrets and Variables > Actions and check the name.")
    exit(1)
else:
    print("✅ Secret found (Hidden for security).")

# 3. Try to send a raw message
print(f"Attempting to send message to Discord...")
data = {"content": "🚨 **CONNECTION TEST** 🚨\nIf you see this, the bot is working!"}

try:
    response = requests.post(webhook_url, json=data)
    
    # 4. Check the result code
    if response.status_code == 204:
        print("✅ SUCCESS: Discord accepted the message (204). Check your channel!")
    elif response.status_code == 401:
        print("❌ FAILED: 401 Unauthorized. Your Webhook URL is invalid.")
    elif response.status_code == 404:
        print("❌ FAILED: 404 Not Found. The Webhook URL does not exist.")
    else:
        print(f"❌ FAILED: Error Code {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ CRITICAL EXCEPTION: {e}")

print("--- DIAGNOSTIC END ---")
