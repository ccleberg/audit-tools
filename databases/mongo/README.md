# `admins.py`

Dependency:

``` shell
pip install pymongo
```

``` python
python ./admins.py
```

Example output:

``` json
[
  {
    "_id": "admin.admin",
    "user": "admin",
    "db": "admin",
    "roles": [
      {
        "role": "userAdminAnyDatabase",
        "db": "admin"
      },
      {
        "role": "readWriteAnyDatabase",
        "db": "admin"
      },
      {
        "role": "dbAdminAnyDatabase",
        "db": "admin"
      },
      {
        "role": "clusterAdmin",
        "db": "admin"
      }
    ],
    "credentials": {
      "SCRAM-SHA-1": {
        "iterationCount": 10000,
        "salt": "abc123",
        "storedKey": "storedKeyHash",
        "serverKey": "serverKeyHash"
      },
      "SCRAM-SHA-256": {
        "iterationCount": 15000,
        "salt": "def456",
        "storedKey": "storedKeyHash256",
        "serverKey": "serverKeyHash256"
      }
    }
  },
  {
    "_id": "test.user1",
    "user": "user1",
    "db": "test",
    "roles": [
      {
        "role": "readWrite",
        "db": "test"
      }
    ],
    "credentials": {
      "SCRAM-SHA-1": {
        "iterationCount": 10000,
        "salt": "ghi789",
        "storedKey": "storedKeyHashUser1",
        "serverKey": "serverKeyHashUser1"
      }
    }
  },
  {
    "_id": "test.ldapUser",
    "user": "ldapUser",
    "db": "test",
    "roles": [
      {
        "role": "read",
        "db": "test"
      }
    ],
    "userSource": "ldap"
  },
  {
    "_id": "admin.x509User",
    "user": "x509User",
    "db": "$external",
    "roles": [
      {
        "role": "readWrite",
        "db": "admin"
      }
    ],
    "credentials": {
      "MONGODB-X509": {
        "subject": "CN=x509User,OU=OrgUnit,O=Org,L=City,ST=State,C=Country"
      }
    }
  }
]
```
