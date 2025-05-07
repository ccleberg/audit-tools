#!/bin/bash

# Default report file
REPORT_FILE="report.txt"
TRIM_COMMENTS=false

# Function to log section header
log_section() {
    echo -e "\n\n" >> "$REPORT_FILE"
    echo "==========================================" >> "$REPORT_FILE"
    echo "# SECTION $1: $2" >> "$REPORT_FILE"
    echo "==========================================" >> "$REPORT_FILE"
}

# Function to log file content
log_file_content() {
    FILE_PATH="$1"
    FILE_NAME=$(basename "$FILE_PATH")
    echo "## $FILE_NAME" >> "$REPORT_FILE"
    if [[ -f $FILE_PATH ]]; then
        if $TRIM_COMMENTS; then
            # Trim comments (lines starting with # or empty lines)
            grep -vE '^\s*#|^\s*$' "$FILE_PATH" >> "$REPORT_FILE"
        else
            cat "$FILE_PATH" >> "$REPORT_FILE"
        fi
    else
        echo "File $FILE_PATH not found!" >> "$REPORT_FILE"
    fi
}

# Function to log command output
log_command_output() {
    echo "## $1" >> "$REPORT_FILE"
    $2 >> "$REPORT_FILE" 2>&1
}

# Check for sudo privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script requires sudo privileges. Please enter your password."
    exec sudo "$0" "$@"
fi

# Parse command-line arguments
while getopts "t" opt; do
    case $opt in
        t)
            TRIM_COMMENTS=true
            REPORT_FILE="report_trimmed.txt"
            ;;
        *)
            echo "Usage: $0 [-t]  # Use -t to trim comments from files"
            exit 1
            ;;
    esac
done

# Initialize report file
> "$REPORT_FILE"  # Clear the file if it exists

# ASCII Header
cat << "EOF" >> "$REPORT_FILE"
  _     ___ _   _ _   ___  __   ___  ____    ____  _____ ____   ___  ____ _____ 
 | |   |_ _| \ | | | | \ \/ /  / _ \/ ___|  |  _ \| ____|  _ \ / _ \|  _ \_   _|
 | |    | ||  \| | | | |\  /  | | | \___ \  | |_) |  _| | |_) | | | | |_) || |  
 | |___ | || |\  | |_| |/  \  | |_| |___) | |  _ <| |___|  __/| |_| |  _ < | |  
 |_____|___|_| \_|\___//_/\_\  \___/|____/  |_| \_\_____|_|    \___/|_| \_\|_|  
EOF

# Log Script Info
log_section "00" "Script Info"
echo "Execution Date and Time: $(date)" >> "$REPORT_FILE"
echo "Script Name: $0" >> "$REPORT_FILE"

if [[ $(whoami) == "root" ]]; then
    echo "User Running the Script: root (called by: $SUDO_USER)" >> "$REPORT_FILE"
else
    echo "User Running the Script: $(whoami)" >> "$REPORT_FILE"
fi

# Log System Info
log_section "01" "System Info"
log_command_output "Hostname" "hostname"
log_command_output "Kernel Version" "uname -r"
log_file_content "/etc/os-release"
log_command_output "IP Address" "hostname -I"

# Log Password Parameters
log_section "02" "Password Parameters"
log_file_content "/etc/pam.d/system-auth"
log_file_content "/etc/login.defs"

# Log Users
log_section "03" "Users"
log_file_content "/etc/passwd"
log_file_content "/etc/group"

# Log Admins
log_section "04" "Admins"
log_file_content "/etc/sudoers"
log_command_output "Sudo Group" "getent group sudo"
log_command_output "Wheel Group" "getent group wheel"
log_command_output "Root User" "getent passwd 0"

# Log SSH Configuration
log_section "05" "SSH Configuration"
log_file_content "/etc/ssh/sshd_config"

# Log Logging Configuration
log_section "06" "Logging Configuration"
log_file_content "/etc/syslog.conf"
log_file_content "/etc/logrotate.conf"

# Log Jobs
log_section "07" "Jobs"
log_command_output "Sudo Crontab" "sudo crontab -l"
log_file_content "/etc/cron.allow"

# Log Security Status
log_section "08" "Security Status"
log_command_output "SELinux Status" "sestatus"
log_command_output "AppArmor Status" "aa-status"

# Log Firewall Rules
log_section "09" "Firewall Rules"
log_command_output "Iptables Rules" "sudo iptables -L"

# Log Open Ports
log_section "10" "Open Ports"
log_command_output "Netstat" "netstat -tuln"

# Set report ownership
if [[ $(whoami) == "root" ]]; then
    chown "$SUDO_USER" "$REPORT_FILE"
fi
