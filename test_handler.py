#!/usr/bin/env python3
"""
Test script to verify the Vercel handler works correctly
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import handler
import json


class MockRequest:
    """Mock request object for testing"""

    def __init__(self, method="GET", path="/"):
        self.method = method
        self.path = path
        self.args = {}


def test_handler():
    """Test the serverless handler"""
    print("🧪 Testing Vercel handler...")

    # Create mock request
    request = MockRequest()

    try:
        # Call the handler
        result = handler(request)

        # Print results
        print(f"Status Code: {result['statusCode']}")
        print(f"Headers: {json.dumps(result['headers'], indent=2)}")

        # Parse and pretty print body
        body = json.loads(result["body"])
        print(f"Response Body: {json.dumps(body, indent=2)}")

        if result["statusCode"] == 200:
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")


if __name__ == "__main__":
    test_handler()
