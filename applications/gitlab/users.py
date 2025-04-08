"""
Gather all members of specified GitLab groups and projects and their access levels.

        Ref: https://docs.gitlab.com/api/members/
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
GROUP_IDS = ["group_id_1", "group_id_2"]  # Add your group IDs here
PROJECT_IDS = ["project_id_1", "project_id_2"]  # Add your project IDs here
TIMEOUT = 30

HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}


def get_members(url, name):
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        members = response.json()
        print(f"\n{name} Members:")
        for member in members:
            print(
                f"Username: {member['username']}, Access Level: {member['access_level']}"
            )
    else:
        print(
            f"Failed to fetch members for {name}: {response.status_code}, {response.text}"
        )


if __name__ == "__main__":
    access_levels = """Access Level Roles:
    0  : No access
    5  : Minimal access
    10 : Guest
    15 : Planner
    20 : Reporter
    30 : Developer
    40 : Maintainer
    50 : Owner
    60 : Admin
    """
    print(access_levels)

    for group_id in GROUP_IDS:
        group_url = f"{BASE_URL}/groups/{group_id}/members"
        get_members(group_url, f"Group {group_id}")

    for project_id in PROJECT_IDS:
        project_url = f"{BASE_URL}/projects/{project_id}/members"
        get_members(project_url, f"Project {project_id}")
