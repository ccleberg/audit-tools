# Background

I have been an auditor for years, starting with operational/financial
audits and quickly transitioning to technology audits early in my
career.

While performing technology audits, attestations, etc., you will find
that it requires a lot of manual effort if you don\'t use the right
tools to automate as much as possible.

This repository serves as my personal collection of audit tools that I
want to save and re-use later.

## Scope

While I created the scripts and tools within this repository
specifically for the applications I use, I am working to include
edge-cases and niche tools as I can.

For now, refer to the tree below for application coverage.

```shell
tree -I ".git*|venv"
```

```text
.
├── applications
│   ├── github
│   │   ├── github_admins.py
│   │   ├── github_audit_log.py
│   │   ├── github_branch_protections.py
│   │   ├── github_commits.py
│   │   └── README.org
│   └── gitlab
│       ├── approvals.py
│       ├── branch_protections.py
│       ├── passwords.py
│       ├── provisioning.py
│       ├── README.org
│       └── users.py
├── CODEOWNERS
├── databases
│   ├── administrators
│   │   ├── mssql_admins.sql
│   │   ├── mysql_admins_alt.sql
│   │   ├── mysql_admins.sh
│   │   ├── mysql_admins.sql
│   │   ├── oracle_admins_alt.sql
│   │   └── oracle_admins.sql
│   └── passwords
│       └── sql
│           ├── data.csv
│           ├── get_data.sql
│           └── test.py
├── LICENSE
├── operating-systems
│   └── linux
│       ├── passwords.sh
│       ├── README.org
│       └── ssh_root_login.sh
├── project_management
│   ├── alteryx
│   │   └── project_email_reminders.yxmd
│   ├── dash
│   │   └── app.py
│   └── powerbi
│       └── project_dashboard
│           ├── project_dashboard.pbix
│           └── project_data.xlsx
├── README.org
├── requirements.txt
└── sampling
    ├── README.org
    ├── sample-html.png
    ├── sample.html
    └── sample.py
```

# Development

## Python

For the Python scripts, use the following to activate a virtual
environment for consistent packing:

```shell
python3 -m venv venv
source ./venv/bin/activate
pip install PACKAGE_NAME
python3 ./PYTHON_SCRIPT.py
```
