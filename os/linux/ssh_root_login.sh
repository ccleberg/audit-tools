#!/bin/bash

# Find the PermitRootLogin setting in the sshd_config file
permit_root_login=$(grep -E "^[[:space:]]*PermitRootLogin" /etc/ssh/sshd_config)

# Echo the setting for the user
echo "Current PermitRootLogin setting:"
echo "$permit_root_login"

# Check if PermitRootLogin is set to something other than 'no'
if ! echo "$permit_root_login" | grep -q "no"; then
  echo ""
  echo "PermitRootLogin is not set to 'no'. Checking for AuthorizedKeysFile location..."
  grep -E "^[[:space:]]*AuthorizedKeysFile" /etc/ssh/sshd_config
fi
