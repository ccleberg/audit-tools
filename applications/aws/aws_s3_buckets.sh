#!/bin/bash

# --- Configuration ---
# File to store the final report
REPORT_FILE="s3_full_public_access_audit.csv"
# The region to use for the initial global list-buckets call (e.g., 'us-east-1')
MASTER_REGION="us-east-1" 

# AWS Regions to check for bucket location. Add more regions if your organization uses them.
AWS_REGIONS="us-east-1 us-west-2 eu-central-1 ap-southeast-2"

# --- Initialization ---
echo "BucketName,Region,PAB_FullyRestricted,Policy_IsPublic,ACL_AllUsersRead,ACL_AllUsersWrite,OverallPublicStatus" > "$REPORT_FILE"
echo "Starting FULL S3 Public Access Audit for the CURRENT account..."
echo "---"

# 1. Retrieve all bucket names
echo "1. Retrieving all bucket names..."
BUCKET_LIST=$(aws s3api list-buckets --region "$MASTER_REGION" --query 'Buckets[].Name' --output text)

if [ -z "$BUCKET_LIST" ]; then
    echo "✅ No S3 buckets found in this account."
    exit 0
fi

# 2. & 3. Iterate through each bucket to find location and run checks
for BUCKET_NAME in $BUCKET_LIST; do
    
    echo "Processing bucket: $BUCKET_NAME"
    BUCKET_REGION=""

    # 2. Find the bucket region
    for REGION in $AWS_REGIONS; do
        BUCKET_LOCATION_RESPONSE=$(aws s3api get-bucket-location --bucket "$BUCKET_NAME" --region "$REGION" 2>/dev/null)
        if [ $? -eq 0 ]; then
            LOCATION_CONSTRAINT=$(echo "$BUCKET_LOCATION_RESPONSE" | jq -r '.LocationConstraint')
            BUCKET_REGION=${LOCATION_CONSTRAINT:-"us-east-1"}
            break
        fi
    done
    
    if [ -z "$BUCKET_REGION" ]; then
        echo "  ⚠️ WARNING: Could not determine region for $BUCKET_NAME. Skipping all checks."
        echo "$BUCKET_NAME,UNKNOWN,N/A,N/A,N/A,N/A,UNKNOWN" >> "$REPORT_FILE"
        continue
    fi
    
    echo "  Region determined: $BUCKET_REGION"

    # --- Variables for the three checks ---
    PAB_FULLY_RESTRICTED="UNKNOWN"
    POLICY_IS_PUBLIC="UNKNOWN"
    ACL_ALL_USERS_READ="FALSE"
    ACL_ALL_USERS_WRITE="FALSE"
    OVERALL_PUBLIC_STATUS="FALSE" # Assume safe until proven otherwise

    # --- CHECK A: Public Access Block (PAB) ---
    PAB_STATUS=$(aws s3api get-public-access-block --bucket "$BUCKET_NAME" --region "$BUCKET_REGION" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        # PAB Missing is the highest risk state.
        PAB_FULLY_RESTRICTED="CRITICAL-MISSING"
        OVERALL_PUBLIC_STATUS="TRUE - PAB Missing"
    else
        # Check if ALL four PAB flags are true
        PAB_CONFIG=$(echo "$PAB_STATUS" | jq -r '.PublicAccessBlockConfiguration')
        if [ "$(echo "$PAB_CONFIG" | jq -r '.BlockPublicAcls and .IgnorePublicAcls and .BlockPublicPolicy and .RestrictPublicBuckets')" = "true" ]; then
            PAB_FULLY_RESTRICTED="TRUE"
        else
            PAB_FULLY_RESTRICTED="FALSE-VULNERABLE"
        fi
    fi

    # --- CHECK B: Bucket Policy Status (If S3 service thinks it's public) ---
    POLICY_STATUS=$(aws s3api get-bucket-policy-status --bucket "$BUCKET_NAME" --region "$BUCKET_REGION" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        POLICY_IS_PUBLIC=$(echo "$POLICY_STATUS" | jq -r '.PolicyStatus.IsPublic')
        if [ "$POLICY_IS_PUBLIC" = "true" ]; then
            OVERALL_PUBLIC_STATUS="TRUE - Policy"
        fi
    else
        # Expected error if no bucket policy exists, treat as NOT public via policy.
        POLICY_IS_PUBLIC="No Policy"
    fi

    # --- CHECK C: Bucket ACLs (for AllUsers group) ---
    ACL_RESPONSE=$(aws s3api get-bucket-acl --bucket "$BUCKET_NAME" --region "$BUCKET_REGION" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        # Find if any grant to 'http://acs.amazonaws.com/groups/global/AllUsers' exists
        
        # Check for READ access
        if echo "$ACL_RESPONSE" | jq -e '.Grants[] | select(.Grantee.URI=="http://acs.amazonaws.com/groups/global/AllUsers") | select(.Permission | test("READ|FULL_CONTROL"))' >/dev/null; then
            ACL_ALL_USERS_READ="TRUE"
            if [ "$OVERALL_PUBLIC_STATUS" = "FALSE" ]; then
                 OVERALL_PUBLIC_STATUS="TRUE - ACL Read"
            fi
        fi

        # Check for WRITE access (often less common for public, but still public exposure)
        if echo "$ACL_RESPONSE" | jq -e '.Grants[] | select(.Grantee.URI=="http://acs.amazonaws.com/groups/global/AllUsers") | select(.Permission | test("WRITE|FULL_CONTROL"))' >/dev/null; then
            ACL_ALL_USERS_WRITE="TRUE"
            if [ "$OVERALL_PUBLIC_STATUS" = "FALSE" ]; then
                 OVERALL_PUBLIC_STATUS="TRUE - ACL Write"
            fi
        fi
    else
        ACL_ALL_USERS_READ="ACL Check Failed"
        ACL_ALL_USERS_WRITE="ACL Check Failed"
    fi
    
    # Final check for PAB failure (PAB is the highest authority)
    if [ "$PAB_FULLY_RESTRICTED" = "CRITICAL-MISSING" ]; then
        OVERALL_PUBLIC_STATUS="TRUE - PAB Missing (CRITICAL)"
    elif [ "$OVERALL_PUBLIC_STATUS" != "FALSE" ] && [ "$PAB_FULLY_RESTRICTED" != "TRUE" ]; then
        # If the bucket is found public by Policy or ACL AND PAB isn't fully set, confirm it's public
        : # Status already set by Policy or ACL check above
    fi


    # --- Save the output as CSV ---
    echo "$BUCKET_NAME,$BUCKET_REGION,$PAB_FULLY_RESTRICTED,$POLICY_IS_PUBLIC,$ACL_ALL_USERS_READ,$ACL_ALL_USERS_WRITE,\"$OVERALL_PUBLIC_STATUS\"" >> "$REPORT_FILE"
    echo "  Final Status: $OVERALL_PUBLIC_STATUS"

done

echo "---"
echo "✅ Audit Complete."
echo "Final report saved to **$REPORT_FILE**"
cat "$REPORT_FILE"