import requests

# Test what routes are available
base_url = "http://localhost:8080"

try:
    response = requests.get(f"{base_url}/docs")
    print(f"Docs available: {response.status_code}")
except:
    pass

try:
    response = requests.get(f"{base_url}/")
    print(f"Root: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Root error: {e}")

try:
    response = requests.get(f"{base_url}/api/v1/status")
    print(f"Status: {response.status_code}")
except Exception as e:
    print(f"Status error: {e}")