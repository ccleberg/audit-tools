# `approvals.py`

\\This script requires an active Premium or Ultimate subscription.\*\\

``` bash
python ./approvals.py
```

``` text
Rule: All Members
  Approvals Required: 1
  Rule type: any_approver
Rule: Default
  Approvals Required: 1
  Rule type: regular
  Protected Branch: master
  Eligible Approver: Christian Cleberg
```

# `branch_protections.py`

``` bash
python ./branch_protections.py
```

``` json
[
    {
        "id": 148448212,
        "name": "main",
        "push_access_levels": [
            {
                "id": 185900194,
                "access_level": 40,
                "access_level_description": "Maintainers",
                "deploy_key_id": null,
                "user_id": null,
                "group_id": null
            }
        ],
        "merge_access_levels": [
            {
                "id": 156461000,
                "access_level": 40,
                "access_level_description": "Maintainers",
                "user_id": null,
                "group_id": null
            }
        ],
        "allow_force_push": false,
        "unprotect_access_levels": [],
        "code_owner_approval_required": false,
        "inherited": false
    }
]
```

# `passwords.py`

**This script does not apply to GitLab.com. This is for self-hosted
instances only.**

``` bash
python ./passwords.py
```

``` text
# TODO: Need access to a self-hosted version of GitLab to test this out.
```

# `pipelines.py`

``` bash
python ./pipelines.py
```

``` text
Pipeline ID: 1754222228
  Status: failed
  Ref: master
  Created At: 2025-04-06T03:39:15.065Z
  Duration: N/A seconds
  Configuration: N/A
Pipeline ID: 1754221831
  Status: failed
  Ref: pr-1
  Created At: 2025-04-06T03:37:42.333Z
  Duration: N/A seconds
  Configuration: N/A
Pipeline ID: 1754220271
  Status: failed
  Ref: pr-1
  Created At: 2025-04-06T03:33:38.606Z
  Duration: N/A seconds
  Configuration: N/A
Pipeline ID: 1754214637
  Status: failed
  Ref: master
  Created At: 2025-04-06T03:21:39.902Z
  Duration: N/A seconds
  Configuration: N/A
```

# `provisioning.py`

\\This script requires an active Premium or Ultimate subscription.\*\\

``` bash
python ./provisioning.py
```

``` text
Group: 105300140
    2025-04-08T03:33:17.055Z : Action: member_created, Member: 128029250, Author: 24608590
```

# `repositories.py`

``` shell
python ./repositories.py
```

``` text
# User ID Example
Projects under ID: ccleberg:
- audit-tools (ID: 68757698)
- cleberg.net (ID: 68701468)

# Group ID Example
Projects under ID: phryq:
- Yoshi Cli (ID: 68757750)
- pages-demo (ID: 68757186)
```

# `users.py`

``` bash
python ./users.py
```

``` text
Access Level Roles:
    0  : No access
    5  : Minimal access
    10 : Guest
    15 : Planner
    20 : Reporter
    30 : Developer
    40 : Maintainer
    50 : Owner
    60 : Admin


Group 97083755 Members:
Username: ccleberg, Access Level: 50

Project 68701468 Members:
Username: ccleberg, Access Level: 50
Username: project_68701468_bot_2c7ee010a479c0e48cdb4c7c5cfae886, Access Level: 40
```
