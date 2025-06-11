# Vercel Deployment Guide

## Quick Deployment Steps

1. **Install Vercel CLI** (if not already installed):

   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:

   ```bash
   vercel login
   ```

3. **Deploy the project**:

   ```bash
   vercel
   ```

4. **Set Environment Variables** in Vercel Dashboard or via CLI:
   ```bash
   vercel env add TELEGRAM_BOT_TOKEN
   vercel env add TELEGRAM_CHAT_ID
   vercel env add GITHUB_ACCESS_TOKEN
   vercel env add GIST_ID
   ```

## Environment Variables Required

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID where notifications will be sent
- `GITHUB_ACCESS_TOKEN`: GitHub personal access token for API access
- `GIST_ID`: GitHub Gist ID for storing release state (optional)

## How It Works

Once deployed:

1. **Automatic Trigger**: The function runs automatically when someone visits your Vercel site
2. **Manual Trigger**: You can also trigger it by visiting `/api/check`
3. **Web Interface**: The main page provides a simple interface to manually trigger checks

## API Endpoints

- `/` - Main page with web interface (auto-triggers check)
- `/api/check` - API endpoint to manually trigger release check
- `/api/index` - Same as main page

## Monitoring

- Check Vercel function logs in the Vercel dashboard
- Monitor Telegram for notifications
- Use the web interface to see real-time status

## Troubleshooting

1. **Environment Variables**: Make sure all required env vars are set in Vercel
2. **Function Timeout**: Vercel has execution limits for serverless functions
3. **Rate Limits**: GitHub API has rate limits, consider the frequency of calls
4. **Telegram Bot**: Ensure your bot token is valid and the bot can send messages to the chat
