# Vercel Deployment Guide

## Environment Variables Setup

In your Vercel dashboard, make sure to set these environment variables:

1. `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
2. `TELEGRAM_CHAT_ID` - Your Telegram chat ID
3. `GITHUB_ACCESS_TOKEN` - Your GitHub personal access token
4. `GIST_ID` - Your GitHub Gist ID (optional, for tracking releases)

## Files Structure

The deployment expects this structure:

```
/
├── main.py                 # Main logic
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
└── api/
    ├── index.py           # Main page handler (auto-triggers check)
    └── check.py           # Direct API endpoint for checks
```

## How it works

1. **Main page (`/`)**: Shows status page and automatically runs the check
2. **API endpoint (`/api/check`)**: Direct endpoint for manual triggers
3. **Automatic execution**: Every time someone visits the main page, it checks for new GitHub releases

## Testing Locally

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your `.env` file with the required variables
3. Run: `python main.py` (for direct testing)
4. Or test the handlers: `python test_vercel_compatibility.py`

## Deployment

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set the environment variables in Vercel dashboard
4. Deploy!

The service will automatically check for new GitHub releases whenever someone visits your Vercel URL.
