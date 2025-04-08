"""
Verify if password policies are enforced in a self-hosted GitLab instance.

    Ref: https://docs.gitlab.com/api/settings/
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
TIMEOUT = 30

URL = f"{BASE_URL}/application/settings"
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

if __name__ == "__main__":
    # Get application settings
    response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        settings = response.json()
        password_length = settings.get("password_length", "Not set")
        password_complexity = settings.get("password_complexity", "Not set")

        print(f"Password Length: {password_length}")
        print(f"Password Complexity: {password_complexity}")
    else:
        print(
            f"Failed to fetch application settings: {response.status_code}, {response.text}"
        )
