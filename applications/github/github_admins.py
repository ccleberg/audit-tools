"""
Gather all members of a GitHub organization, all repos within that organization,
and list each user's permission per repo.
"""

import requests

GITHUB_TOKEN = "your_personal_access_token"
ORGANIZATION = "your_organization"
TIMEOUT = 30

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_org_members(org):
    """
    Get members of an organization
    """
    url = f"https://api.github.com/orgs/{org}/members"
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_org_repos(org):
    """
    Get repositories of an organization
    """
    url = f"https://api.github.com/orgs/{org}/repos"
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_repo_collaborators(org, repo):
    """
    Get collaborators of a repository with their permissions
    """
    url = f"https://api.github.com/repos/{org}/{repo}/collaborators"
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_user_permissions(org, repo, user):
    """
    Get a user's permissions for a repository
    """
    url = f"https://api.github.com/repos/{org}/{repo}/collaborators/{user}/permission"
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


# Main script
if __name__ == "__main__":
    # Get organization members
    members = get_org_members(ORGANIZATION)
    print(f"Members of the organization '{ORGANIZATION}':")
    for member in members:
        print(f"- {member['login']}")

    # Get organization repositories
    repositories = get_org_repos(ORGANIZATION)
    print(f"\nRepositories in the organization '{ORGANIZATION}':")
    for repository in repositories:
        print(f"- {repository['name']}")

    # Get collaborators for each repository and their permissions
    for repository in repositories:
        repository_name = repository["name"]
        collaborators = get_repo_collaborators(ORGANIZATION, repository_name)
        print(f"\nCollaborators for the repository '{repository_name}':")
        for collaborator in collaborators:
            user_login = collaborator["login"]
            permissions = get_user_permissions(
                ORGANIZATION, repository_name, user_login
            )
            print(f"- {user_login}: {permissions['permission']}")
