-- NOTE: Please review the server's "my.cnf" file for default values;
--   OR: run the "SHOW [GLOBAL | SESSION] VARIABLES" command(s) on the database.

-- Authentication methods only
SELECT user, host, plugin FROM mysql.user;

-- Default password configuration only
SHOW GLOBAL VARIABLES LIKE 'validate_password%';
SHOW VARIABLES LIKE 'validate_password%';

-- Authentication methods and MySQL password configurations
sql
SELECT 
    u.user,
    u.host,
    u.plugin,
    gp.authentication_string,
    gp.password_lifetime,
    gp.password_require_current
FROM 
    mysql.user u
JOIN 
    mysql.global_priv gp ON u.user = gp.user AND u.host = gp.host
WHERE 
    u.plugin IN ('mysql_native_password', 'caching_sha2_password');