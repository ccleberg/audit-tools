#!/bin/bash

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run as root or with sudo."
  exit 1
fi

# Check if the sshd_config file exists
if [ ! -f /etc/ssh/sshd_config ]; then
    echo "Error: /etc/ssh/sshd_config not found."
    exit 1
fi

echo "--- SSH Root Login Audit ---"

# Find the PermitRootLogin setting, ignoring commented-out lines
permit_root_login=$(grep -E "^[[:space:]]*PermitRootLogin" /etc/ssh/sshd_config)

if [ -z "$permit_root_login" ]; then
    echo "PermitRootLogin is not explicitly set. Relying on sshd defaults (usually 'prohibit-password')."
    # In this case, we can assume it's not a simple 'yes', so we can stop.
    exit 0
else
    echo "Found setting: $permit_root_login"
fi


# Check if PermitRootLogin is set to something other than 'no'
if ! echo "$permit_root_login" | grep -q "no"; then
    echo "[WARNING] Root login is permitted."
    echo ""
    echo "Checking for root's authorized_keys file..."

    # Look for an explicitly set AuthorizedKeysFile path
    auth_keys_path_line=$(grep -E "^[[:space:]]*AuthorizedKeysFile" /etc/ssh/sshd_config)

    if [ -n "$auth_keys_path_line" ]; then
        # An explicit path is set. Extract the path.
        # This removes the 'AuthorizedKeysFile' keyword and leading/trailing whitespace.
        auth_keys_path=$(echo "$auth_keys_path_line" | awk '{print $2}')
        echo "sshd_config specifies: $auth_keys_path_line"
        
        # The path might contain '%h', which means the user's home directory.
        # For root, this is /root.
        actual_path=${auth_keys_path/\%h/\/root}
        
    else
        # No explicit path is set, so we check the default location.
        echo "AuthorizedKeysFile not set in sshd_config. Checking default location."
        actual_path="/root/.ssh/authorized_keys"
    fi

    echo "Checking for file at: $actual_path"
    if [ -f "$actual_path" ]; then
        echo "[CRITICAL] Found authorized keys file for root at $actual_path"
        echo "Contents:"
        echo "----------------------------------------"
        cat "$actual_path"
        echo "----------------------------------------"
    else
        echo "[INFO] No authorized keys file found at the specified or default location."
    fi

else
    echo "[OK] PermitRootLogin is set to 'no'. No further checks needed."
fi
