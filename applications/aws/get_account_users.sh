#!/bin/bash

# This script analyzes all IAM Identity Center assignments for a specific
# AWS account and outputs the details to a single JSON file.
# Corrected Logic: First finds provisioned permission sets, then gets assignments for each.

# --- Configuration ---
ACCOUNT_NAME=""

# --- Prerequisite check ---
if ! command -v aws &> /dev/null || ! command -v jq &> /dev/null; then
    echo "Error: Both AWS CLI and jq are required. Please install them and ensure they are in your PATH."
    exit 1
fi

# --- Step 1: Get Instance details and find the target Account ID ---
echo "Fetching IAM Identity Center and Account details..."

INSTANCE_ARN=$(aws sso-admin list-instances --query "Instances[0].InstanceArn" --output text)
IDENTITY_STORE_ID=$(aws sso-admin list-instances --query "Instances[0].IdentityStoreId" --output text)

if [ -z "$INSTANCE_ARN" ] || [ -z "$IDENTITY_STORE_ID" ]; then
    echo "Error: Could not find IAM Identity Center instance ARN or Identity Store ID."
    exit 1
fi

ACCOUNT_ID=$(aws organizations list-accounts --query "Accounts[?Name=='$ACCOUNT_NAME' && Status=='ACTIVE'].Id" --output text)

if [ -z "$ACCOUNT_ID" ]; then
    echo "Error: Could not find an active AWS account with the name '$ACCOUNT_NAME'."
    exit 1
fi

echo "Successfully found Account '$ACCOUNT_NAME' with ID: $ACCOUNT_ID"
echo "---"

# --- Step 2: Get all Permission Sets provisioned to the account ---
echo "Step 2: Finding all permission sets provisioned to '$ACCOUNT_NAME'..."
PROVISIONED_SETS_ARN=$(aws sso-admin list-permission-sets-provisioned-to-account \
    --instance-arn "$INSTANCE_ARN" \
    --account-id "$ACCOUNT_ID" \
    --query "PermissionSets[]" --output text)

if [ -z "$PROVISIONED_SETS_ARN" ]; then
    echo "No permission sets are provisioned for account '$ACCOUNT_NAME'."
    exit 0
fi

echo "Found provisioned permission sets. Now checking assignments for each..."
echo "---"

# --- Caches to store fetched data ---
declare -A PERMISSION_SET_CACHE
declare -A PRINCIPAL_NAME_CACHE
FINAL_JSON_ARRAY="[]" # Initialize an empty JSON array

# --- Step 3: Loop through each provisioned permission set and get its assignments ---
for PS_ARN in $PROVISIONED_SETS_ARN; do
    
    # Get assignments for this specific permission set in this account
    ACCOUNT_ASSIGNMENTS=$(aws sso-admin list-account-assignments \
        --instance-arn "$INSTANCE_ARN" \
        --account-id "$ACCOUNT_ID" \
        --permission-set-arn "$PS_ARN" \
        --query "AccountAssignments[]" --output json)

    if [ "$(echo "$ACCOUNT_ASSIGNMENTS" | jq 'length')" -eq 0 ]; then
        echo "  -> Permission Set ARN $PS_ARN is provisioned but has no active assignments."
        continue
    fi

    # Since there are assignments, let's get the permission set's details (policies, name)
    # Using a cache to avoid redundant calls if a PS is somehow listed twice
    if [ -z "${PERMISSION_SET_CACHE[$PS_ARN]}" ]; then
        echo "  -> Fetching policies for Permission Set: $PS_ARN"
        PS_NAME=$(aws sso-admin describe-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN" --query "PermissionSet.Name" --output text)
        MANAGED_POLICIES=$(aws sso-admin list-managed-policies-in-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN" --query "AttachedManagedPolicies[].Arn" --output json)
        INLINE_POLICY=$(aws sso-admin get-inline-policy-for-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN" --query "InlinePolicy" --output json)
        
        PERMISSION_SET_CACHE[$PS_ARN]=$(jq -n \
            --arg name "$PS_NAME" \
            --argjson managed "$MANAGED_POLICIES" \
            --argjson inline "$INLINE_POLICY" \
            '{name: $name, policies: {managed_policies: $managed, inline_policy: $inline}}')
    fi
    CACHED_PS_DETAILS=${PERMISSION_SET_CACHE[$PS_ARN]}

    # Now process each assignment found for this permission set
    for row in $(echo "${ACCOUNT_ASSIGNMENTS}" | jq -r '.[] | @base64'); do
        _jq() { echo ${row} | base64 --decode | jq -r ${1}; }
        PRINCIPAL_TYPE=$(_jq '.PrincipalType')
        PRINCIPAL_ID=$(_jq '.PrincipalId')

        # Get Principal (User/Group) Name, using a cache
        if [ -z "${PRINCIPAL_NAME_CACHE[$PRINCIPAL_ID]}" ]; then
            PRINCIPAL_NAME=""
            if [ "$PRINCIPAL_TYPE" == "USER" ]; then
                PRINCIPAL_NAME=$(aws identitystore describe-user --identity-store-id "$IDENTITY_STORE_ID" --user-id "$PRINCIPAL_ID" --query "UserName" --output text 2>/dev/null)
            elif [ "$PRINCIPAL_TYPE" == "GROUP" ]; then
                PRINCIPAL_NAME=$(aws identitystore describe-group --identity-store-id "$IDENTITY_STORE_ID" --group-id "$PRINCIPAL_ID" --query "DisplayName" --output text 2>/dev/null)
            fi
            PRINCIPAL_NAME_CACHE[$PRINCIPAL_ID]=${PRINCIPAL_NAME:-"ID: $PRINCIPAL_ID"}
        fi
        CACHED_PRINCIPAL_NAME=${PRINCIPAL_NAME_CACHE[$PRINCIPAL_ID]}
        
        echo "  -> Found Assignment: ${CACHED_PRINCIPAL_NAME} ($PRINCIPAL_TYPE) -> $(echo "$CACHED_PS_DETAILS" | jq -r .name)"

        # Build the final JSON object for this assignment
        ASSIGNMENT_OUTPUT=$(jq -n \
            --arg principal_type "$PRINCIPAL_TYPE" \
            --arg principal_name "$CACHED_PRINCIPAL_NAME" \
            --argjson ps_details "$CACHED_PS_DETAILS" \
            '{principal: {type: $principal_type, name: $principal_name}, permission_set: $ps_details}')

        FINAL_JSON_ARRAY=$(echo "$FINAL_JSON_ARRAY" | jq --argjson new_entry "$ASSIGNMENT_OUTPUT" '. += [$new_entry]')
    done
done

# --- Step 4: Save the final report ---
OUTPUT_FILENAME="report_${ACCOUNT_NAME}.json"
echo "$FINAL_JSON_ARRAY" | jq '.' > "$OUTPUT_FILENAME"

echo "---"
echo "Success! Report saved to '$OUTPUT_FILENAME'"
echo "The file contains all user/group assignments and their policies for account '$ACCOUNT_NAME'."
