"""
Gather all commits from a specific branch of a repository in a GitHub organization.
"""

import requests

GITHUB_TOKEN = "your_personal_access_token"
ORGANIZATION = "your_organization"
REPOSITORY = "your_repository"
BRANCH = "your_branch"

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Define a timeout value (in seconds)
TIMEOUT = 10


def get_commit_log(org, repo, branch):
    """
    Get the full commit log for a repository branch
    """
    commits = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{org}/{repo}/commits?sha={branch}"
            f"&page={page}&per_page=100"
        )
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        page_commits = response.json()
        if not page_commits:
            break
        commits.extend(page_commits)
        page += 1
    return commits


def get_commit_details(org, repo, sha):
    """
    Get detailed information for a specific commit
    """
    url = f"https://api.github.com/repos/{org}/{repo}/commits/{sha}"
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        # Get the full commit log for the specified branch
        commit_log = get_commit_log(ORGANIZATION, REPOSITORY, BRANCH)
        print(
            f"Total commits in the repository '{REPOSITORY}' on branch "
            f"'{BRANCH}': {len(commit_log)}"
        )

        # Get detailed information for each commit
        for commit in commit_log:
            sha_hash = commit["sha"]
            commit_details = get_commit_details(ORGANIZATION, REPOSITORY, sha_hash)
            print(f"\nCommit SHA: {commit_details['sha']}")
            print(
                f"Author: {commit_details['commit']['author']['name']} "
                f"<{commit_details['commit']['author']['email']}>"
            )
            print(f"Date: {commit_details['commit']['author']['date']}")
            print(f"Message: {commit_details['commit']['message']}")
            print(f"URL: {commit_details['html_url']}")
            print("Files changed:")
            for file in commit_details["files"]:
                print(f"  - {file['filename']} ({file['status']})")
                print(
                    f"    Additions: {file['additions']}, "
                    f"Deletions: {file['deletions']}, "
                    f"Changes: {file['changes']}"
                )
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
