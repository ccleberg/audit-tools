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
            if event["entity_type"] == "User":
                action = event["action"]
                username = event["target_details"]
                created_at = event["created_at"]
                timestamp = event["created_at"]
                if action in ["create", "destroy"]:
                    print(
                        f"Action: {action}, Username: {username}, Date: {created_at}, Timestamp: {timestamp}"
                    )
    else:
        print(f"Failed to fetch audit events: {response.status_code}, {response.text}")
