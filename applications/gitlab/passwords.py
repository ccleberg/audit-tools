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
        minimum_password_length = settings.get("minimum_password_length", "Not set")
        password_number_required = settings.get("password_number_required", "Not set")
        password_symbol_required = settings.get("password_symbol_required", "Not set")
        password_uppercase_required = settings.get("password_uppercase_required", "Not set")
        password_lowercase_required = settings.get("password_lowercase_required", "Not set")

        print(f"Password Length: {minimum_password_length}")
        print(f"Password Number Required: {password_number_required}")
        print(f"Password Symbol Required: {password_symbol_required}")
        print(f"Password Uppercase Required: {password_uppercase_required}")
        print(f"Password Lowercase Required: {password_lowercase_required}")
    else:
        print(
            f"Failed to fetch application settings: {response.status_code}, {response.text}"
        )

