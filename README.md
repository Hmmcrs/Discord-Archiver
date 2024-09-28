# Discord Message Scraper

This tool allows you to scrape messages from Discord channels where you have permission. **Do not use this tool with your main account**; it may lead to account suspension.

---

## Quick Setup Instructions

### 1. **Install Python**

- Download Python from [python.org](https://www.python.org/downloads/).
- During installation, **check the box** that says **Add Python to PATH**.

### 2. **Install Required Packages**

1. Open Command Prompt (Windows) or Terminal (macOS/Linux).
2. Run the following commands:
   ```bash
   pip install requests
   pip install python-dateutil
3. Ensure Files Are in the Right Location
Both the main.py script and config.json file should be on your Desktop for the tool to work correctly.
4. Modify config.json
Open the config.json file that is already in the repository.
Replace the placeholders with your user token (from a secondary account) and channel ID:
json
Copy code
{
  "token": "YOUR_DISCORD_TOKEN_HERE",
  "channel_id": "YOUR_CHANNEL_ID_HERE"
}
5. Run the Script
In Command Prompt or Terminal, navigate to your Desktop:

bash
Copy code
cd %USERPROFILE%\Desktop  # For Windows
or

bash
Copy code
cd ~/Desktop  # For macOS
Run the script:

bash
Copy code
python main.py
