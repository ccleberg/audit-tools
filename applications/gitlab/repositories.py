"""
List all repositories (projects) for a user or organization in GitLab.
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
USER_ID = "your_user_or_group_id"
TIMEOUT = 30

URL = f"{BASE_URL}/groups/{USER_ID}/projects" # Group URL
# URL = f"{BASE_URL}/users/{USER_ID}/projects" # User URL
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}


def list_projects(user_or_group_id):
    PER_PAGE = 100
    page = 1
    projects = []

    while True:
        response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT, params={"page": page, "per_page": PER_PAGE})

        if response.status_code == 200:
            current_projects = response.json()
            if not current_projects:
                break
            projects.extend(current_projects)
            page += 1
        else:
            print(f"Failed to retrieve projects: {response.status_code} - {response.text}")
            break

    if projects:
        print(f"Projects under ID: {user_or_group_id}:")
        for project in projects:
            print(f"- {project['name']} (ID: {project['id']})")
    else:
        print(f"No projects found for ID: {user_or_group_id}.")

if __name__ == "__main__":
    list_projects(USER_ID)
