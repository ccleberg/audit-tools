"""
Gathers branch protection rules for a repository.
"""

import requests

GITHUB_TOKEN = 'your_personal_access_token'
ORGANIZATION = 'your_organization'
REPOSITORY = 'your_repository'
TIMEOUT = 30

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_all_branches(org, repo):
    """
    Get all branches in a repository
    """
    all_branches = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/{org}/{repo}/branches?page={page}&per_page=100'
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        page_branches = response.json()
        if not page_branches:
            break
        all_branches.extend(page_branches)
        page += 1
    return all_branches

def get_branch_protection(org, repo, repo_branch):
    """
    Get branch protection settings
    """
    url = f'https://api.github.com/repos/{org}/{repo}/branches/{repo_branch}/protection'
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    if response.status_code == 404:
        return None  # No protection settings for this branch
    response.raise_for_status()
    return response.json()

def get_repository_rulesets(org, repo):
    """
    Get repository rulesets
    """
    url = f'https://api.github.com/repos/{org}/{repo}/rulesets'
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    try:
        # Get all branches in the repository
        branches = get_all_branches(ORGANIZATION, REPOSITORY)
        print(f"Total branches in the repository '{REPOSITORY}': {len(branches)}")

        # Get protection settings for each branch
        for branch in branches:
            branch_name = branch['name']
            protection_settings = get_branch_protection(ORGANIZATION, REPOSITORY, branch_name)
            print(f"\nBranch: {branch_name}")
            if protection_settings:
                print(f"Protection settings: {protection_settings}")
            else:
                print("No protection settings")

        # Get repository rulesets
        rulesets = get_repository_rulesets(ORGANIZATION, REPOSITORY)
        print(f"\nRepository rulesets for '{REPOSITORY}':")
        print(rulesets)

    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
