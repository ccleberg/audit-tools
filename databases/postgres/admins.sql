-- References:
--           : https://www.postgresql.org/docs/current/user-manag.html
--           : https://www.postgresql.org/docs/current/view-pg-roles.html
--           : https://www.postgresql.org/docs/current/catalog-pg-auth-members.html

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