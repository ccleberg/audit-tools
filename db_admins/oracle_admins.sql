SELECT
    grantee AS "User",
    privilege AS "Privilege"
FROM
    dba_sys_privs
WHERE
    grantee IN (SELECT DISTINCT grantee FROM dba_sys_privs)
UNION ALL
SELECT
    grantee AS "User",
    privilege AS "Privilege"
FROM
    dba_tab_privs
WHERE
    grantee IN (SELECT DISTINCT grantee FROM dba_tab_privs);
