-- NOTE: Please review the server's "my.cnf" file for default values;
--   OR: run the "SHOW [GLOBAL | SESSION] VARIABLES" command(s) on the database.

-- Authentication methods only
SELECT user, host, plugin FROM mysql.user;

-- Default password configuration only
SHOW GLOBAL VARIABLES LIKE 'validate_password%';
SHOW VARIABLES LIKE 'validate_password%';

-- Authentication methods and MySQL password configurations
-- Reference: https://mariadb.com/kb/en/mysql-user-table/
SELECT * FROM mysql.user
