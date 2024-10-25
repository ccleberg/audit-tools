/*
References:
1. https://learn.microsoft.com/en-us/sql/relational-databases/security/password-policy
2. https://learn.microsoft.com/en-us/sql/t-sql/functions/loginproperty-transact-sql
*/

SELECT
    name,
    principal_id,
    sid,
    type,
    type_desc,
    is_disabled,
    create_date,
    modify_date,
    default_database_name,
    default_language_name,
    credential_id,
    is_policy_checked,
    is_expiration_checked,
    password_hash,
    LOGINPROPERTY(name, 'IsMustChange') AS IsMustChange,
    LOGINPROPERTY(name, 'IsLocked') AS IsLocked,
    LOGINPROPERTY(name, 'LockoutTime') AS LockoutTime,
    LOGINPROPERTY(name, 'PasswordLastSetTime') AS PasswordLastSetTime,
    LOGINPROPERTY(name, 'IsExpired') AS IsExpired,
    LOGINPROPERTY(name, 'BadPasswordCount') AS BadPasswordCount,
    LOGINPROPERTY(name, 'BadPasswordTime') AS BadPasswordTime,
    LOGINPROPERTY(name, 'HistoryLength') AS HistoryLength
FROM sys.sql_logins;
