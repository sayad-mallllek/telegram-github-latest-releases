import sys
import os

# Add the parent directory to the path to import from main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import handler


def api_handler(request):
    """Vercel API handler"""
    return handler(request)


# Export the handler for Vercel
handler = api_handler
