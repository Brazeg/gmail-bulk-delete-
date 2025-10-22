# Gmail Bulk Delete Script

A Python script to permanently delete all emails from Gmail inbox and sent folders using the Gmail API. Perfect for transferring business accounts or cleaning up old email accounts.

## ⚠️ Warning

This script **permanently deletes emails** without moving them to trash. Make sure you have backups if needed before running.

### Backup Your Emails First

Before running this script, consider backing up your emails:

- **Google Takeout**: Export all Gmail data as MBOX archive
- **Email Clients**: Mac Mail, Outlook, or Thunderbird can export emails
- **IMAP Backup Tools**: Command-line tools like mbsync, OfflineIMAP, or getmail

## Features

- Deletes all emails from Inbox
- Deletes all emails from Sent folder
- Batch processing (500 emails at a time) for efficiency
- Progress tracking
- Confirmation prompt before deletion

## Prerequisites

- Python 3.6+
- Gmail account
- Google Cloud Console project with Gmail API enabled

## Setup

### 1. Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Set Up Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Gmail API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Gmail API" and enable it

### 3. Create OAuth Credentials

#### Configure OAuth Consent Screen
1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type
3. Fill in required fields:
   - App name: (e.g., "Gmail Cleanup")
   - User support email: Your email
   - Developer contact: Your email
4. Click "Save and Continue"
5. On the "Scopes" page, click "Add or Remove Scopes"
   - Search for "gmail"
   - Select: `https://mail.google.com/` (Full Gmail access)
   - Click "Update" then "Save and Continue"
6. Add test users:
   - Click "Add Users"
   - Enter your Gmail address
   - Save and Continue

#### Create Credentials File
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: Choose "Desktop app"
4. Name: (e.g., "deleteEmails")
5. Click "Create"
6. Click "Download JSON" button (⬇️ icon)
7. Rename the downloaded file to `credentials.json`
8. Move it to the same directory as `deleteEmails.py`

## Usage

```bash
python3 deleteEmails.py
```

### First Run

The first time you run the script:
1. It will open a browser window for authentication
2. Sign in to your Gmail account
3. Grant the necessary permissions
4. Return to the terminal
5. Type `DELETE ALL` to confirm and start deletion

### Subsequent Runs

After the first authentication, the script saves a `token.pickle` file for future use. You won't need to authenticate again unless you revoke access or delete this file.

## How It Works

1. Authenticates with Gmail API using OAuth 2.0
2. Retrieves message IDs from Inbox and Sent folders
3. Batch deletes emails (500 at a time) for efficiency
4. Shows progress after each batch
5. Provides a summary of deleted emails

## File Structure

```
├── deleteEmails.py      # Main script
├── credentials.json     # OAuth credentials (you create this)
└── token.pickle         # Auto-generated after first auth
```

## Troubleshooting

### "Insufficient Permission" Error

Make sure your OAuth consent screen has the `https://mail.google.com/` scope configured, not just `gmail.modify`.

### Browser Authentication Issues

If you're not added as a test user:
1. Go to Google Cloud Console → OAuth consent screen
2. Add your email under "Test users"

### Token Issues

If authentication fails, delete `token.pickle` and run the script again to re-authenticate.

## Security Notes

- The `credentials.json` file contains sensitive information - never commit it to public repositories
- Add `credentials.json` and `token.pickle` to your `.gitignore`
- Only grant access to accounts you trust
- The script runs locally and doesn't send data anywhere except Google's API

## Use Cases

- Business account transfers
- Cleaning up old email accounts
- GDPR compliance (complete data removal)
- Account decommissioning

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Pull requests welcome! For major changes, please open an issue first.

## Disclaimer

This script permanently deletes emails. The author is not responsible for any data loss. Always backup important emails before running.
