-- Global Permissions
SELECT ... FROM mysql.user;

-- Database Permissions
SELECT ... FROM mysql.db
WHERE db = @db_name;

-- Table Permissions
SELECT ... FROM mysql.tables
WHERE db = @db_name;

-- Column Permissions
SELECT ... FROM mysql.columns_priv
WHERE db = @db_name;

-- Password Configuration
SHOW GLOBAL VARIABLES LIKE 'validate_password%';
SHOW VARIABLES LIKE 'validate_password%';
