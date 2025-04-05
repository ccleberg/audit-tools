"""
Gather all members of a GitLab group and their access levels.
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
GROUP_ID = "your_group_id"
TIMEOUT = 30

URL = f"{BASE_URL}/groups/{GROUP_ID}/members"
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

if __name__ == "__main__":
    # Get group members
    response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        members = response.json()
        for member in members:
            print(
                f"Username: {member['username']}, Access Level: {member['access_level']}"
            )
    else:
        print(f"Failed to fetch group members: {response.status_code}, {response.text}")
