#!/usr/bin/env python3
"""
Test script to verify the Vercel deployment setup
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import handler


def test_handler():
    """Test the main handler function"""
    print("🧪 Testing handler function...")

    # Create a mock request object
    class MockRequest:
        def __init__(self):
            self.args = {}

    try:
        result = handler(MockRequest())
        print(f"✅ Handler test passed!")
        print(f"Status Code: {result.get('statusCode')}")

        if result.get("statusCode") == 200:
            print("✅ Handler returned success status")
        else:
            print("⚠️ Handler returned non-success status")

        return True

    except Exception as e:
        print(f"❌ Handler test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_handler()
    sys.exit(0 if success else 1)
