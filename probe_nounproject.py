import os
import requests
from requests_oauthlib import OAuth1
import json

api_key = os.environ.get("NOUNPROJECT_API_KEY")
api_secret = os.environ.get("NOUNPROJECT_API_SECRET")

if not api_key or not api_secret:
    print("Error: API keys not found")
    exit(1)

auth = OAuth1(api_key, api_secret)
base_url = "https://api.thenounproject.com/v2"

def test_endpoint(endpoint, params=None):
    url = f"{base_url}/{endpoint}"
    print(f"Testing {url} with params {params}")
    try:
        response = requests.get(url, auth=auth, params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "icons" in data:
                print(f"Found {len(data['icons'])} icons")
                if len(data['icons']) > 0:
                    print(f"First icon: {data['icons'][0].get('term')}, ID: {data['icons'][0].get('id')}")
            elif "icon" in data:
                 print(f"Found icon: {data['icon'].get('term')}")
            else:
                print("Keys:", data.keys())
        else:
            print(response.text[:200])
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

# Test 1: Search icons by term (standard assumption)
test_endpoint("icon", params={"query": "cat", "limit": 1})

# Test 2: Search icons endpoint (plural)
test_endpoint("icons", params={"query": "cat", "limit": 1})

# Test 3: Search icons by term in path
test_endpoint("icon/cat") # Probably by ID, but checking

# Test 4: Search icons by term in path (plural)
test_endpoint("icons/cat")
