"""
Track user creation and deletion events in GitLab with timestamps.
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
GROUP_ID = "your_group_id"
TIMEOUT = 30

URL = f"{BASE_URL}/groups/{GROUP_ID}/audit_events"
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

if __name__ == "__main__":
    # Get audit events
    response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        audit_events = response.json()
        for event in audit_events:
            if event["entity_type"] == "User" or event["entity_type"] == "Group":
                action = event["event_name"]
                member_id = event["details"].get("member_id")
                created_at = event["created_at"]
                author = event["author_id"]
                if action in ["member_created", "member_destroyed", "member_updated"]:
                    print(
                        f"Group: {GROUP_ID}\n",
                        f"   {created_at} : Action: {action}, Member: {member_id}, Author: {author}",
                    )
    else:
        print(f"Failed to fetch audit events: {response.status_code}, {response.text}")
