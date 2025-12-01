import requests

# Test profile endpoints
base_url = "http://localhost:8080/api/v1"

# Test GET profile
try:
    response = requests.get(f"{base_url}/users/me")
    print(f"GET /users/me: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"GET error: {e}")

# Test PUT profile
try:
    data = {"name": "Test User", "email": "test@test.com"}
    response = requests.put(f"{base_url}/users/me", json=data)
    print(f"PUT /users/me: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"PUT error: {e}")

# Test PUT preferences
try:
    data = {"email_notifications": True}
    response = requests.put(f"{base_url}/users/me/preferences", json=data)
    print(f"PUT /users/me/preferences: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Preferences error: {e}")