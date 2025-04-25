#!/bin/bash

# Function to extract and format password complexity parameters from /etc/pam.d/system-auth
extract_password_params() {
    echo "Checking /etc/pam.d/system-auth for password parameters..."
    
    if [ -f /etc/pam.d/system-auth ]; then
        # Extract the line containing the password complexity parameters
        param_line=$(grep -E 'difok=.* minlen=.* dcredit=.* ocredit=.* ucredit=.* lcredit=.* minclass=.* maxsequence=.*' /etc/pam.d/system-auth)
        
        if [ -n "$param_line" ]; then
            echo "Password complexity parameters found:"
            echo "$param_line"
            echo ""
            
            # Extract individual parameters using regex
            minlen=$(echo "$param_line" | grep -oP 'minlen=\K\d+')
            lcredit=$(echo "$param_line" | grep -oP 'lcredit=\K\d+')
            ucredit=$(echo "$param_line" | grep -oP 'ucredit=\K\d+')
            dcredit=$(echo "$param_line" | grep -oP 'dcredit=\K\d+')
            ocredit=$(echo "$param_line" | grep -oP 'ocredit=\K\d+')
            minclass=$(echo "$param_line" | grep -oP 'minclass=\K\d+')
            
            # Note: These parameters might not be present in the same line, so we set default values if not found
            remember=$(grep -oP 'remember=\K\d+' /etc/pam.d/system-auth || echo "N/A")
            retry=$(grep -oP 'retry=\K\d+' /etc/pam.d/system-auth || echo "N/A")
            unlock_time=$(grep -oP 'unlock_time=\K\d+' /etc/pam.d/system-auth || echo "N/A")
            
            # Format the extracted parameters into a table
            echo "Formatted Password Complexity Parameters:"
            echo "---------------------------------------------------"
            echo -e "Minlen     : $minlen characters"
            echo -e "Lcredit    : $lcredit lowercase"
            echo -e "Ucredit    : $ucredit uppercase"
            echo -e "Dcredit    : $dcredit numbers"
            echo -e "Ocredit    : $ocredit special"
            echo -e "Remember   : $remember password history"
            echo -e "Minclass   : $minclass character types"
            echo -e "Retry      : $retry incorrect passwords"
            echo -e "Unlock_time: $unlock_time seconds until unlocked"
        else
            echo "No password complexity parameters found in /etc/pam.d/system-auth."
        fi
    else
        echo "/etc/pam.d/system-auth file not found."
    fi
}

# Function to analyze /etc/login.defs
analyze_login_defs() {
    echo "Analyzing /etc/login.defs..."
    if [ -f /etc/login.defs ]; then
        echo "Contents of /etc/login.defs:"
        cat /etc/login.defs
        echo ""
        
        # Analysis
        echo "Login restrictions and parameters in /etc/login.defs:"
        grep -E 'PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN|PASS_WARN_AGE|UID_MIN|UID_MAX|GID_MIN|GID_MAX|LOGIN_RETRIES|LOGIN_TIMEOUT|UID|GID' /etc/login.defs
        echo ""
    else
        echo "/etc/login.defs file not found."
    fi
}

# Main script execution
echo "Starting analysis of authentication and login parameters..."
extract_password_params
analyze_login_defs
echo "Analysis complete."