"""
Checks SQL Server user data for compliance with Windows policies.
"""

# Import packages
import pandas as pd

# Load the data into a pandas DataFrame
df_input = pd.read_csv("./data.csv")


# Function to apply rules and generate report
def apply_rules_and_report(df):
    """
    Apply defined rules against the input data.

            Parameters:
                df (pandas.DataFrame): SQL login data

            Returns:
                report (list): List of dictionaries containing test results
    """
    report = []
    for _, row in df.iterrows():
        result = {
            "Name": row["name"],
            "Type Check": "",
            "Policy Check": "",
            "Expiration Check": "",
            "Reason": "",
        }

        # Check the type_desc
        if row["type_desc"] == "SQL_LOGIN":
            result["Type Check"] = "SQL_LOGIN"
        elif row["type_desc"] == "WINDOWS_LOGIN":
            result["Type Check"] = "N/A"
            result["Reason"] = "Refer to Windows password policy."
        else:
            result["Type Check"] = "Manual Review"
            result["Reason"] = "Reviewer to manually review."

        # Check if password policy is enforced
        if row["is_policy_checked"] == 1:
            result["Policy Check"] = "PASS"
            result["Reason"] += """Password policy is enforced. Reviewer to
            check the assigned policy."""
        else:
            result["Policy Check"] = "FAIL"
            result["Reason"] += "Password policy is not enforced."

        # Check if password expiration is enforced
        if row["is_expiration_checked"] == 1:
            result["Expiration Check"] = "PASS"
            result["Reason"] += """Password expiration is enforced. Reviewer to
            check the expiration policy."""
        else:
            result["Expiration Check"] = "FAIL"
            result["Reason"] += "Password expiration is not enforced."

        report.append(result)

    return report


# Main function to run the script
def main():
    """
    Apply defined rules against the input data and print the results.
    """
    # Apply rules and generate report
    report = apply_rules_and_report(df_input)
    report_df = pd.DataFrame(report)

    # Do not truncate output
    pd.set_option("display.expand_frame_repr", True)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", 1000)

    # Print the report
    print(report_df)


if __name__ == "__main__":
    main()
