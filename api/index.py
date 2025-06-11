import sys
import os

# Add the parent directory to the path to import from main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import handler
import json


def index_handler(request):
    """Main index handler that shows a simple web interface and triggers the check"""

    # Always trigger the GitHub releases check when the page is visited
    try:
        print("🔍 Triggering GitHub releases check from main page visit...")
        check_result = handler(request)
        check_successful = check_result.get("statusCode") == 200

        # Parse the result to get meaningful info
        if check_successful:
            try:
                body_data = json.loads(check_result.get("body", "{}"))
                new_releases = body_data.get("new_releases_count", 0)
                total_repos = body_data.get("total_repositories", 0)
                status_message = f"✅ Check completed! Found {new_releases} new releases out of {total_repos} repositories."
                status_class = "success"
            except:
                status_message = "✅ Check completed successfully!"
                status_class = "success"
        else:
            status_message = "❌ Check failed. Please try again later."
            status_class = "error"

    except Exception as e:
        print(f"❌ Error during automatic check: {str(e)}")
        status_message = f"❌ Error during check: {str(e)}"
        status_class = "error"
        check_successful = False

    # Return a simple HTML page with the check results
    html_content = (
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GitHub Releases Monitor</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px; 
                margin: 50px auto; 
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { 
                color: #333; 
                text-align: center;
                margin-bottom: 30px;
            }
            .button {
                background-color: #0066cc;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                display: block;
                margin: 20px auto;
                text-decoration: none;
                text-align: center;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #0052a3;
            }
            .info {
                background-color: #e7f3ff;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                border-left: 4px solid #0066cc;
            }
            .status {
                text-align: center;
                margin: 20px 0;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            .success { background-color: #d4edda; color: #155724; }
            .error { background-color: #f8d7da; color: #721c24; }
            .loading { background-color: #fff3cd; color: #856404; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 GitHub Releases Monitor</h1>
            
            <div class="status """
        + status_class
        + """">
                """
        + status_message
        + """
            </div>
            
            <div class="info">
                <p><strong>This service monitors GitHub repositories for new releases and sends notifications to Telegram.</strong></p>
                <p>The check runs automatically whenever you visit this page!</p>
            </div>
            
            <button class="button" onclick="window.location.reload()">Check Again</button>
            
            <div class="info">
                <h3>How it works:</h3>
                <ul>
                    <li>Monitors configured GitHub repositories</li>
                    <li>Sends formatted notifications to Telegram when new releases are found</li>
                    <li>Tracks release state to avoid duplicate notifications</li>
                    <li>Automatically triggered every time this page is visited</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*",
        },
        "body": html_content,
    }


# Export the handler for Vercel
handler = index_handler
