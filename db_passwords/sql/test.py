"""
Checks SQL Server user data for compliance with Windows policies.
"""

# Import packages
import pandas as pd
from io import StringIO

# Sample data as a CSV string
data = """name,principal_id,sid,type,type_desc,is_disabled,create_date,modify_date,default_database_name,default_language_name,credential_id,is_policy_checked,is_expiration_checked,password_hash,IsMustChange,IsLocked,LockoutTime,PasswordLastSetTime,IsExpired,BadPasswordCount,BadPasswordTime,HistoryLength
user1,1,,S,SQL_LOGIN,0,2023-01-15 10:35:00,2023-01-15 10:35:00,master,us_english,NULL,1,0,0x01004086CEB6772AE2356381B9B069D4E02C0185D5A06CFA3822,0,0,,2023-01-15 10:35:00,0,0,,5
user2,267,,S,SQL_LOGIN,0,2023-02-20 20:49:00,2023-02-20 20:49:00,master,us_english,NULL,0,0,0x01003E3A7A6F88A8F548540ECB2043946AC2545120424CCD8782,1,0,,2023-02-20 20:49:00,0,1,2023-02-20 20:50:00,3
user3,268,,S,SQL_LOGIN,0,2023-03-10 11:20:00,2023-03-10 11:20:00,Adminserver,us_english,NULL,1,0,0x010042516769FBC191A67840731CB36B41EFDACC97BE8264281F,0,0,,2023-03-10 11:20:00,0,0,,4
user4,269,,S,SQL_LOGIN,0,2023-04-01 10:40:00,2023-04-01 11:32:00,Adminserver,us_english,NULL,1,0,0x01005F3B351B26E2DB7C7FD3C7ED02B3FD2EDC09BB2BF13DA3E5,0,1,2023-04-01 11:32:00,2023-04-01 10:40:00,0,3,2023-04-01 11:30:00,2
user5,270,,S,SQL_LOGIN,0,2023-05-05 12:33:00,2023-05-05 12:33:00,master,us_english,NULL,1,0,0x0100AE15D55972BB3D6C6283921711CD4A208747888BEEFED71B,0,0,,2023-05-05 12:33:00,0,0,,6
user6,272,,S,SQL_LOGIN,0,2023-06-15 11:46:00,2023-06-15 11:46:00,Adminserver,us_english,NULL,1,1,0x0100F12FAE790FCE0FF356A0948211AE4052653503E1BBC28FAB,0,0,,2023-06-15 11:46:00,0,0,,7
user7,279,,S,SQL_LOGIN,0,2023-07-20 12:50:00,2023-07-20 12:50:00,Adminserver,us_english,NULL,1,1,0x01004856A222264E62219236AB6AC7E5B622F1E53D1CCA2AF9B8,0,0,,2023-07-20 12:50:00,0,0,,8
user8,284,,S,SQL_LOGIN,0,2023-08-25 13:56:00,2023-08-25 13:56:00,master,us_english,NULL,1,1,0x0100723BEDBE69779CD3087C0E60AD69C33CC7E969F78DA2498A,0,0,,2023-08-25 13:56:00,0,0,,9
"""

# Load the data into a pandas DataFrame
df = pd.read_csv(StringIO(data))

# Function to apply rules and generate report
def apply_rules_and_report(df):
    report = []
    for index, row in df.iterrows():
        result = {
            'Name': row['name'],
            'Type Check': '',
            'Policy Check': '',
            'Expiration Check': '',
            'Reason': ''
        }

        # Check the type_desc
        if row['type_desc'] == 'SQL_LOGIN':
            result['Type Check'] = 'SQL_LOGIN'
        elif row['type_desc'] == 'WINDOWS_LOGIN':
            result['Type Check'] = 'N/A'
            result['Reason'] = 'Refer to Windows password policy.'
        else:
            result['Type Check'] = 'Manual Review'
            result['Reason'] = 'Reviewer to manually review.'

        # Check if password policy is enforced
        if row['is_policy_checked'] == 1:
            result['Policy Check'] = 'PASS'
            result['Reason'] += ' Password policy is enforced. Reviewer to check the assigned policy.'
        else:
            result['Policy Check'] = 'FAIL'
            result['Reason'] += ' Password policy is not enforced.'
        
        # Check if password expiration is enforced
        if row['is_expiration_checked'] == 1:
            result['Expiration Check'] = 'PASS'
            result['Reason'] += ' Password expiration is enforced. Reviewer to check the expiration policy.'
        else:
            result['Expiration Check'] = 'FAIL'
            result['Reason'] += ' Password expiration is not enforced.'
        
        report.append(result)
    
    return report

# Main function to run the script
def main():
    # Apply rules and generate report
    report = apply_rules_and_report(df)
    report_df = pd.DataFrame(report)
    
    # Print the report
    print(report_df)

if __name__ == "__main__":
    main()
