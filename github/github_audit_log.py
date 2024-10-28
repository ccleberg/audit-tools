"""
Extract a specific list of events from the GitHub Audit Log API.

NOTE: REQUIRES A GITHUB ENTERPRISE SUBSCRIPTION TO ACCESS THE API.
"""

import requests

GITHUB_TOKEN = 'your_personal_access_token'
ORGANIZATION = 'your_organization'
TIMEOUT = 30

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_audit_log_events(org, actions):
    """
    Get audit log events for specific actions
    """
    events = []
    page = 1
    while True:
        url = (f'https://api.github.com/orgs/{org}/audit-log?page={page}&per_page=100'
               f'&action={",".join(actions)}')
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        page_events = response.json()
        if not page_events:
            break
        events.extend(page_events)
        page += 1
    return events

if __name__ == '__main__':
    try:
        # Define the actions to filter
        action_filters = ['protected_branch',
                   'repository_branch_protection_evaluation',
                   'repository_ruleset']

        # Get audit log events for the specified actions
        audit_log_events = get_audit_log_events(ORGANIZATION, action_filters)
        print(f"Total audit log events for specified actions: {len(audit_log_events)}")

        # Print detailed information for each event
        for event in audit_log_events:
            print(f"\nEvent ID: {event['@id']}")
            print(f"Action: {event['action']}")
            print(f"Actor: {event['actor']}")
            print(f"Repository: {event.get('repo', 'N/A')}")
            print(f"Created At: {event['created_at']}")
            print(f"Details: {event}")
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
