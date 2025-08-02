# `passwords.sql`

``` sql
SELECT *
FROM pg_settings
WHERE name LIKE 'password_%';
```

    | name                | setting       | unit | category                                        | short_desc                                      | extra_desc | context | vartype | source  | min_val | max_val | enumvals            | boot_val      | reset_val     | sourcefile | sourceline | pending_restart |
    |---------------------+---------------+------+-------------------------------------------------+-------------------------------------------------+------------+---------+---------+---------+---------+---------+---------------------+---------------+---------------+------------+------------+-----------------|
    | password_encryption | scram-sha-256 |      | Connections and Authentication / Authentication | Chooses the algorithm for encrypting passwords. |            | user    | enum    | default |         |         | {md5,scram-sha-256} | scram-sha-256 | scram-sha-256 |            |            | false           |

``` sql
SELECT 
    usename AS user_name,
    passwd AS password,
    valuntil AS valid_until,
    useconfig AS user_config
FROM pg_shadow;
```

    | user_name | password                                                                                                                              | valid_until            | user_config |
    |-----------+---------------------------------------------------------------------------------------------------------------------------------------+------------------------+-------------|
    | cmc       |                                                                                                                                       |                        |             |
    | testuser  | SCRAM-SHA-256$4096:+NSpEU+8afhJ4BUTkzdKeg==$FGIRcTWr89b42qkLUl4Ntfp4RUpoc3GIpLHqJl/fWZE=:o1UM8YiEj5SLV5l/geMuqXMRi6onWazryn/l+LXYMxU= | 2025-12-31 00:00:00-06 |             |

# `admins.sql`

``` sql
SELECT 
    r.rolname AS role_name,
    r.rolsuper AS is_superuser,
    r.rolinherit AS inherits_privileges,
    r.rolcreaterole AS can_create_roles,
    r.rolcreatedb AS can_create_db,
    r.rolcanlogin AS can_login,
    r.rolreplication AS can_replication,
    r.rolconnlimit AS connection_limit,
    r.rolvaliduntil AS valid_until,
    ARRAY(
        SELECT b.rolname
        FROM pg_auth_members m
        JOIN pg_roles b ON (m.roleid = b.oid)
        WHERE m.member = r.oid
    ) AS member_of
FROM pg_roles r;
```

    | role_name                   | is_superuser | inherits_privileges | can_create_roles | can_create_db | can_login | can_replication | connection_limit | valid_until            | member_of                                                    |
    |-----------------------------+--------------+---------------------+------------------+---------------+-----------+-----------------+------------------+------------------------+--------------------------------------------------------------|
    | cmc                         | true         | true                | true             | true          | true      | true            |               -1 |                        | {}                                                           |
    | pg_database_owner           | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_read_all_data            | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_write_all_data           | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_monitor                  | false        | true                | false            | false         | false     | false           |               -1 |                        | {pg_read_all_settings,pg_read_all_stats,pg_stat_scan_tables} |
    | pg_read_all_settings        | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_read_all_stats           | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_stat_scan_tables         | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_read_server_files        | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_write_server_files       | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_execute_server_program   | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_signal_backend           | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_checkpoint               | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_maintain                 | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_use_reserved_connections | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | pg_create_subscription      | false        | true                | false            | false         | false     | false           |               -1 |                        | {}                                                           |
    | testuser                    | false        | true                | false            | false         | true      | false           |               -1 | 2025-12-31 00:00:00-06 | {}                                                           |
