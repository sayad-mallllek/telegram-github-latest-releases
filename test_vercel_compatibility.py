#!/usr/bin/env python3
"""
Test script to verify the Vercel serverless functions work correctly
"""

import sys
import os
import json

# Test the main handler
print("🧪 Testing main.py handler...")
try:
    from main import handler as main_handler

    class MockRequest:
        pass

    result = main_handler(MockRequest())
    print(f"✅ Main handler test - Status: {result.get('statusCode')}")

    if result.get("statusCode") == 200:
        body = json.loads(result.get("body", "{}"))
        print(f"   - Message: {body.get('message', 'No message')}")
        print(f"   - Status: {body.get('status', 'Unknown')}")
    else:
        print(f"   - Error: {result.get('body', 'No error info')}")

except Exception as e:
    print(f"❌ Main handler test failed: {e}")
    sys.exit(1)

# Test the API handlers
print("\n🧪 Testing API handlers...")

try:
    sys.path.append("api")
    from api.index import handler as index_handler
    from api.check import handler as check_handler

    # Test index handler
    result = index_handler(MockRequest())
    print(f"✅ Index handler test - Status: {result.get('statusCode')}")

    # Test check handler
    result = check_handler(MockRequest())
    print(f"✅ Check handler test - Status: {result.get('statusCode')}")

except Exception as e:
    print(f"❌ API handler test failed: {e}")
    sys.exit(1)

print("\n✅ All tests passed! Ready for deployment.")
