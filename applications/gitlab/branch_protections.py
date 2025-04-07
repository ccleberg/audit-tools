"""
List all branch protection rules and their configurations in GitLab.
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
PROJECT_ID = "your_project_id"
TIMEOUT = 30

URL = f"{BASE_URL}/projects/{PROJECT_ID}/protected_branches"
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

if __name__ == "__main__":
    # Get protected branches
    response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        protected_branches = response.json()
        for branch in protected_branches:
            name = branch['name']
            push_access_levels = branch['push_access_levels']
            merge_access_levels = branch['merge_access_levels']
            print(f"Branch: {name}")
            print(f"  Push Access Levels: {push_access_levels}")
            print(f"  Merge Access Levels: {merge_access_levels}")
    else:
        print(f"Failed to fetch protected branches: {response.status_code}, {response.text}")