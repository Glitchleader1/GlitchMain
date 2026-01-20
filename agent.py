name: Glitch Hunter

on:
  schedule:
    - cron: '*/5 * * * *'  # The "Every 5 Minutes" setting
  workflow_dispatch:      # The Manual Button

jobs:
  scrape_and_alert:
    runs-on: ubuntu-latest

    steps:
      - name: Check out the code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run the scraper script
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python agent.py
