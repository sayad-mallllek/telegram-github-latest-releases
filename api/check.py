import sys
import os
import json

# Add the parent directory to the path to import from main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import handler as main_handler
except ImportError as e:
    print(f"❌ Failed to import main handler: {e}")

    def main_handler(request):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Import error: {str(e)}"}),
        }


def api_handler(request):
    """Vercel API handler"""
    return main_handler(request)


def handler(request):
    """Vercel API handler for check route"""
    return api_handler(request)
