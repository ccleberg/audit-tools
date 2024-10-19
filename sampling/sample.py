"""
Creates a sample from a CSV or Excel file based on user-defined SAMPLE_SIZE.
"""

# Import packages
import pandas as pd

# Define the sample size
SAMPLE_SIZE = 25

# Import the data to a pandas DataFrame
df = pd.read_csv("FILENAME_GOES_HERE.csv")

# ALTERNATIVE: If you use Excel, use this instead. Supports xls, xlsx, xlsm,
# xlsb, odf, ods and odt file extensions.
# df = pd.read_excel("FILENAME_GOES_HERE.xlsx")

# Print totals prior to sampling
print("Dataframe size (rows, columns): ", df.shape)

# Sample
sample = df.sample(SAMPLE_SIZE)
print("Sample size: ", SAMPLE_SIZE)
print("Sample:\n", sample)

# ALTERNATIVE: Replacement Samples
#
# If you want replacement samples (e.g., 10 samples & 3 replacements), you will
# need to increase sample size to the total you want (e.g., 13). If that is
# larger than the population, you will need to use the `replace=True` parameter.
#
# # Sample Size: 25 + 5 replacement samples
# sample_size = 30
# sample = df.sample(30, replace=True)
