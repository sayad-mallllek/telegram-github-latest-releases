import requests
import os
import json
import re
from pathlib import Path
import html2text
from http.server import BaseHTTPRequestHandler

from dotenv import load_dotenv

load_dotenv(override=True)


# List of repositories to monitor (owner/repo format)
REPOS = [
    "nestjs/nest",
    "slackapi/slack-github-action",
    "microsoft/typescript",
    # Add more repositories as needed
]
GITHUB_ACCESS_TOKEN = os.getenv(
    "GITHUB_ACCESS_TOKEN",
)

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# GitHub Gist configuration
GIST_ID = os.getenv("GIST_ID", "")  # Set this to your Gist ID
GIST_FILENAME = "github_releases_data.json"


def load_last_releases():
    """Load the last known release IDs from GitHub Gist"""
    if not GIST_ID:
        print("⚠️ No GIST_ID provided. Using an empty dictionary for release tracking.")
        return {}

    try:
        # Fetch the gist content
        headers = {
            "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(
            f"https://api.github.com/gists/{GIST_ID}", headers=headers
        )
        response.raise_for_status()

        gist_data = response.json()
        if GIST_FILENAME in gist_data["files"]:
            content = gist_data["files"][GIST_FILENAME]["content"]
            return json.loads(content)
        else:
            print(f"⚠️ File {GIST_FILENAME} not found in Gist. Using empty dictionary.")
            return {}
    except Exception as e:
        print(f"⚠️ Error loading releases from Gist: {str(e)}. Using empty dictionary.")
        return {}


def save_last_release(releases_data):
    """Save the last release IDs to GitHub Gist"""
    if not GIST_ID:
        print("⚠️ No GIST_ID provided. Release data not saved.")
        return

    try:
        # Prepare the gist update payload
        headers = {
            "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        payload = {
            "files": {GIST_FILENAME: {"content": json.dumps(releases_data, indent=2)}}
        }

        # Update the gist
        response = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload
        )
        response.raise_for_status()
        print(f"✅ Successfully updated release data in Gist ({GIST_ID})")
    except Exception as e:
        print(f"❌ Error saving releases to Gist: {str(e)}")


def escape_markdown_v1(text):
    """Escape special characters for Telegram Markdown V1"""
    # Characters that need escaping in Telegram Markdown V1
    escape_chars = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]

    for char in escape_chars:
        text = text.replace(char, f"\\{char}")

    return text


def github_to_telegram_html(text):
    """Convert GitHub markdown to Telegram-compatible HTML"""
    if not text:
        return "No release notes provided."

    # Limit text length for Telegram message limits (4096 characters)
    if len(text) > 2500:  # Leave more room for other message content
        text = text[:2500] + "... (truncated)"

    try:
        # Convert markdown to HTML format that Telegram understands

        # Convert headers to bold text
        text = re.sub(r"^#{1,6}\s+(.+)$", r"<b>\1</b>", text, flags=re.MULTILINE)

        # Handle code blocks - convert to <pre> tags
        text = re.sub(
            r"```([a-zA-Z]*)\n(.*?)```", r"<pre>\2</pre>", text, flags=re.DOTALL
        )

        # Convert inline code `code` to <code>code</code>
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

        # Convert bold **text** to <b>text</b>
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

        # Convert italic _text_ to <i>text</i>
        text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<i>\1</i>", text)

        # Convert strikethrough ~~text~~ to <s>text</s>
        text = re.sub(r"~~([^~]+)~~", r"<s>\1</s>", text)

        # Handle links - convert [text](url) to <a href="url">text</a>
        text = re.sub(
            r"\[([^\]]+)\]\((https?://[^\)]+)\)",
            r'<a href="\2">\1</a>',
            text,
        )

        # Clean up multiple newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove remaining HTML entities that might cause issues
        text = (
            text.replace("&lt;", "&lt;")
            .replace("&gt;", "&gt;")
            .replace("&amp;", "&amp;")
        )

        # Ensure the text doesn't end with incomplete HTML tags
        text = text.strip()

        # Final length check
        if len(text) > 2800:
            text = text[:2800] + "... (truncated)"

        return text

    except Exception as e:
        print(f"⚠️ Error processing HTML: {str(e)}. Using plain text.")
        # If all else fails, return plain text without any formatting
        plain_text = re.sub(r"[*_`\[\]()~>#+=|{}.!-]", "", text)
        return plain_text[:2500] if len(plain_text) > 2500 else plain_text


def send_telegram_message(message, parse_mode="HTML"):
    """Send a message to Telegram using the Bot API"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(
            "⚠️ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not provided. Message not sent."
        )
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # First, try with HTML parsing
    try:
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True

    except requests.exceptions.HTTPError as e:
        if "can't parse entities" in str(e) or "Bad Request" in str(e):
            print(f"⚠️ HTML parsing failed, trying without parse_mode: {str(e)}")

            # Try again without HTML parsing (plain text)
            try:
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": message,
                    "disable_web_page_preview": False,
                }

                response = requests.post(url, json=payload)
                response.raise_for_status()
                print("✅ Message sent as plain text (HTML parsing disabled)")
                return True

            except Exception as e2:
                print(f"❌ Failed to send even as plain text: {str(e2)}")
                if hasattr(e2, "response") and e2.response:
                    print(f"Response: {e2.response.text}")
                return False
        else:
            print(f"❌ Error sending message to Telegram: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response: {e.response.text}")
            return False

    except Exception as e:
        print(f"❌ Unexpected error sending message to Telegram: {str(e)}")
        return False


def main():
    last_releases = load_last_releases()

    for repo in REPOS:
        try:
            # Fetch latest release for this repository
            response = requests.get(
                f"https://api.github.com/repos/{repo}/releases/latest"
            )
            response.raise_for_status()
            latest_release = response.json()

            # Check if this is a new release
            if (
                repo not in last_releases
                or str(latest_release["id"]) != last_releases[repo]
            ):
                # Format release notes for Telegram
                release_notes = github_to_telegram_html(latest_release["body"])

                # Create message for Telegram with HTML formatting
                message = f"🚀 <b>New {repo} Release: {latest_release['name']}</b>\n\n"
                message += f"<b>Release Notes:</b>\n{release_notes}\n\n"
                message += f"<a href=\"{latest_release['html_url']}\">View Release</a>"

                # Send to Telegram
                if send_telegram_message(message):
                    print(
                        f"✅ Notification sent for {repo} release {latest_release['name']}"
                    )
                else:
                    print(
                        f"❌ Failed to send notification for {repo} release {latest_release['name']}"
                    )

                # Update last release ID for this repository
                last_releases[repo] = str(latest_release["id"])

            else:
                print(f"No new releases for {repo}")

        except requests.RequestException as e:
            print(f"❌ Error checking {repo}: {str(e)}")

    # Save all release IDs at once
    save_last_release(last_releases)


def handle_request(request):
    """Handler for serverless function requests"""
    main()
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "GitHub releases check completed successfully"}),
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for Vercel serverless function"""
        result = handle_request(self)
        self.send_response(result["statusCode"])
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(result["body"].encode())
        return


if __name__ == "__main__":
    main()
