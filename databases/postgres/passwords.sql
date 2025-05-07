-- References:
--           : https://www.postgresql.org/docs/current/view-pg-shadow.html
--           : https://www.postgresql.org/docs/current/auth-password.html
--           : https://www.postgresql.org/docs/current/auth-password.html#AUTH-PASSWORD-ENCRYPTION
--           : https://www.postgresql.org/docs/current/runtime-config.html

-- Defined password configuration
SELECT *
FROM pg_settings
WHERE name LIKE 'password_%';

-- Users and their password configurations
SELECT 
    usename AS user_name,
    passwd AS password,
    valuntil AS valid_until,
    useconfig AS user_config
FROM pg_shadow;