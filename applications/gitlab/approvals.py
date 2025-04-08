"""
Extract merge request approval rules and their statuses in GitLab.
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
PROJECT_ID = "your_project_id"
TIMEOUT = 30

URL = f"{BASE_URL}/projects/{PROJECT_ID}/approval_rules"
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

if __name__ == "__main__":
    # Get approval rules
    response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        approval_rules = response.json()
        for rule in approval_rules:
            name = rule["name"]
            approvals_required = rule["approvals_required"]
            rule_type = rule["rule_type"]
            protected_branches = rule["protected_branches"]
            eligible_approvers = rule["eligible_approvers"]
            print(f"Rule: {name}")
            print(f"  Approvals Required: {approvals_required}")
            print(f"  Rule type: {rule_type}")
            for branch in protected_branches:
                branch_name = branch["name"]
                print(f"  Protected Branch: {branch_name}")
            for approver in eligible_approvers:
                approver_username = approver["name"]
                print(f"  Eligible Approver: {approver_username}")
    else:
        print(
            f"Failed to fetch approval rules: {response.status_code}, {response.text}"
        )
