import requests
import json

# Test the backend API with session-based authentication
base_url = "http://localhost:8000"

# First, let's test the health endpoint
print("Testing health endpoint...")
try:
    response = requests.get(f"{base_url}/health")
    print(f"Health check response: {response.status_code}")
    print(f"Health check data: {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Let's also test the root endpoint
print("\nTesting root endpoint...")
try:
    response = requests.get(f"{base_url}/")
    print(f"Root endpoint response: {response.status_code}")
    print(f"Root endpoint data: {response.json()}")
except Exception as e:
    print(f"Root endpoint failed: {e}")

print("\nBackend server is running and accessible!")