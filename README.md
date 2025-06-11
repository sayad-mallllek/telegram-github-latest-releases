# Telegram GitHub Latest Releases

A Python script that monitors GitHub repositories for new releases and sends notifications to a Telegram bot.

## Features

- Monitor multiple GitHub repositories for new releases
- Send formatted notifications to Telegram with release notes
- Track release state using GitHub Gists to avoid duplicate notifications
- Support for serverless deployment (Vercel, AWS Lambda, etc.)
- Markdown formatting for better readability in Telegram

## Setup

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
4. Get your chat ID where you want to receive notifications

### 2. Environment Variables

Set the following environment variables:

```bash
GITHUB_ACCESS_TOKEN=your_github_token_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
GIST_ID=your_gist_id_here  # Optional: for tracking releases
```

### 3. Configuration

Edit the `REPOS` list in `main.py` to include the repositories you want to monitor:

```python
REPOS = [
    "nestjs/nest",
    "microsoft/typescript",
    "your-org/your-repo",
    # Add more repositories as needed
]
```

### 4. Installation

```bash
pip install -r requirements.txt
```

### 5. Usage

**Local Development:**

```bash
python main.py
```

**Vercel Deployment:**

1. Install Vercel CLI: `npm install -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel`
4. Set environment variables in Vercel dashboard
5. Visit your deployed site - it will automatically check for releases!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## How it works

1. Fetches the latest release for each configured repository
2. Compares with previously stored release IDs (from GitHub Gist)
3. If a new release is found, formats the release notes and sends to Telegram
4. Updates the stored release IDs to prevent duplicate notifications

## Message Format

The Telegram messages include:

- Repository name and release version
- Formatted release notes (converted from GitHub markdown)
- Direct link to the release page
