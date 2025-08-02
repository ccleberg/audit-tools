**NOTE**: I used the same
[PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
for all scripts within this folder. Note that you can likely reduce
permissions for certain scripts - it's best practice to define a PAT for
a specific purpose and avoid using a single PAT with broad permissions.

- Personal Access Token:
  - \[x\] Repository Permissions
    - \[x\] Actions: read-only
    - \[x\] Contents: read-only
    - \[x\] Metadata: read-only
    - \[x\] Workflows: read-only
  - \[x\] Organization Permissions
    - \[x\] Administration: read-only

# `github_admins.py`

``` bash
python ./github_admins.py
```

``` text
Members of the organization 'your_organization':

Repositories in the organization 'your_organization':
- demo-repository

Collaborators for the repository 'demo-repository':
- user1: admin
```

# `github_audit_log.py`

**NOTE**: Requires an active GitHub Enterprise subscription.

``` bash
python ./github_audit_log.py
```

``` text
TODO: Need to get an Enterprise subscription to test this script.
```

# `github_branch_protections.py`

``` bash
python ./github_branch_protections.py
```

``` text
Total branches in the repository 'demo-repository': 1

Branch: main
No protection settings

Repository rulesets for 'demo-repository':
[{'id': 2311373, 'name': 'default', 'target': 'branch', 'source_type': 'Repository', 'source': 'phryq/demo-repository', 'enforcement': 'active', 'node_id': 'RRS_lACqUmVwb3NpdG9yec40LV1PzgAjRM0', '_links': {'self': {'href': 'https://api.github.com/repos/phryq/demo-repository/rulesets/2311373'}, 'html': {'href': 'https://github.com/phryq/demo-repository/rules/2311373'}}, 'created_at': '2024-10-19T15:59:35.200-05:00', 'updated_at': '2024-10-19T15:59:35.200-05:00'}]
```

# `github_commits.py`

``` bash
python ./github_commits.py
```

``` text
Total commits in the repository 'demo-repository' on branch 'main': 3

Commit SHA: 13c488a2cdda08e4043f8ef36ced5fdd429e9718
Author: Christian Cleberg <156287552+ccleberg@users.noreply.github.com>
Date: 2024-10-19T20:57:55Z
Message: Merge pull request #2 from phryq/1-test-issue

fixes
URL: https://github.com/phryq/demo-repository/commit/13c488a2cdda08e4043f8ef36ced5fdd429e9718
Files changed:
  - .gitignore (added)
    Additions: 0, Deletions: 0, Changes: 0
  - README.md (removed)
    Additions: 0, Deletions: 4, Changes: 4
  - README.org (added)
    Additions: 7, Deletions: 0, Changes: 7

Commit SHA: 6bfde238a2a34a93ce8ee02082eaf4ab3c189368
Author: Christian Cleberg <hello@cmc.pub>
Date: 2024-10-19T20:56:50Z
Message: fixes
URL: https://github.com/phryq/demo-repository/commit/6bfde238a2a34a93ce8ee02082eaf4ab3c189368
Files changed:
  - .gitignore (added)
    Additions: 0, Deletions: 0, Changes: 0
  - README.md (removed)
    Additions: 0, Deletions: 4, Changes: 4
  - README.org (added)
    Additions: 7, Deletions: 0, Changes: 7

Commit SHA: be1ddf31e08fc790f54d68f8067b7b2f3805f999
Author: Christian Cleberg <156287552+ccleberg@users.noreply.github.com>
Date: 2024-10-19T20:54:08Z
Message: Initial commit
URL: https://github.com/phryq/demo-repository/commit/be1ddf31e08fc790f54d68f8067b7b2f3805f999
Files changed:
  - .github/workflows/auto-assign.yml (added)
    Additions: 19, Deletions: 0, Changes: 19
  - .github/workflows/proof-html.yml (added)
    Additions: 11, Deletions: 0, Changes: 11
  - README.md (added)
    Additions: 4, Deletions: 0, Changes: 4
  - index.html (added)
    Additions: 1, Deletions: 0, Changes: 1
  - package.json (added)
    Additions: 9, Deletions: 0, Changes: 9
```
