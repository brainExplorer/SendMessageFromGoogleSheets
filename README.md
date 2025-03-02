# Google Sheets, Python, Selenium, web scrapping
We build an automated web scraping and messaging tool. This tool will:
1️⃣ Scrape user data from a specific website.
2️⃣ Check for duplicate entries in a Google Sheet.
3️⃣ Send automated messages to selected users.
4️⃣ Run automatically every 15 minutes, 24/7.


? What You’ll Do (Your Tasks):
✅ Web Scraping & Data Collection
- Open a specific website.
- Search for users in North Carolina, USA.
- Apply filters to exclude vendors and show only online users.
- Extract and store the following details:
- Username
- User Type (Vendor or Consumer)
- Location
- Status (Online now, last seen X minutes ago)
- Save the collected data into a Google Sheet.

✅ Duplicate Check in Google Sheets
- Scan the spreadsheet to detect duplicate usernames.
- Use a simple formula to mark duplicates in a new column.

✅ Automate Messaging to Users
- Loop through the collected users in the spreadsheet.
- Skip users marked as "Duplicate" or "Vendors".
- Send a pre-written message to the rest.
- If messaging is blocked, update the Google Sheet as "Blocked".
- If the message is sent successfully, update it as "Messaged".

✅ Run Automatically Every 15 Minutes
- The tool should run 24/7 without manual input.
- Set up a scheduler (cron job, task runner, or cloud function) to run the program every 15 minutes.
