# `aws_iam_users.sh`

*Note*: This example uses an account titled `cmc`, which has access provisioned to it through IAM.

``` bash
./aws_iam_users.sh
```

``` text
Fetching IAM Identity Center and Account details...
Successfully found Account 'cmc' with ID: 214941490075
---
Step 2: Finding all permission sets provisioned to 'cmc'...
Found provisioned permission sets. Now checking assignments for each...
---
  -> Fetching policies for Permission Set: arn:aws:sso:::permissionSet/ssoins-68041bff81588aa3/ps-6ea9be6a2332b891
  -> Found Assignment: testgroup1 (GROUP) -> AdministratorAccess
  -> Found Assignment: iamtestuser1 (USER) -> AdministratorAccess
  -> Found Assignment: testgroup2 (GROUP) -> AdministratorAccess
  -> Fetching policies for Permission Set: arn:aws:sso:::permissionSet/ssoins-68041bff81588aa3/ps-590510f2a285016d
  -> Found Assignment: iamtestuser1 (USER) -> Billing
---
Success! Report saved to 'report_cmc.json'
The file contains all user/group assignments and their policies for account 'cmc'.
```

``` bash
cat report_cmc.json
```

```json
[
  {
    "principal": {
      "type": "GROUP",
      "name": "testgroup1"
    },
    "permission_set": {
      "name": "AdministratorAccess",
      "policies": {
        "managed_policies": [
          "arn:aws:iam::aws:policy/AdministratorAccess"
        ],
        "inline_policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"Statement2\",\"Effect\":\"Deny\",\"Action\":[\"a4b:*\"],\"Resource\":[\"*\"]}]}"
      }
    }
  },
  {
    "principal": {
      "type": "USER",
      "name": "iamtestuser1"
    },
    "permission_set": {
      "name": "AdministratorAccess",
      "policies": {
        "managed_policies": [
          "arn:aws:iam::aws:policy/AdministratorAccess"
        ],
        "inline_policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"Statement2\",\"Effect\":\"Deny\",\"Action\":[\"a4b:*\"],\"Resource\":[\"*\"]}]}"
      }
    }
  },
  {
    "principal": {
      "type": "GROUP",
      "name": "testgroup2"
    },
    "permission_set": {
      "name": "AdministratorAccess",
      "policies": {
        "managed_policies": [
          "arn:aws:iam::aws:policy/AdministratorAccess"
        ],
        "inline_policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"Statement2\",\"Effect\":\"Deny\",\"Action\":[\"a4b:*\"],\"Resource\":[\"*\"]}]}"
      }
    }
  },
  {
    "principal": {
      "type": "USER",
      "name": "iamtestuser1"
    },
    "permission_set": {
      "name": "Billing",
      "policies": {
        "managed_policies": [
          "arn:aws:iam::aws:policy/job-function/Billing"
        ],
        "inline_policy": ""
      }
    }
  }
]
```
