# Import packages
import pandas as pd
import math

# Load data
df = pd.read_csv("FILENAME_GOES_HERE.csv")

# ALTERNATIVE: If you use Excel, use this instead. Supports xls, xlsx, xlsm,
# xlsb, odf, ods and odt file extensions.
# df = pd.read_excel("FILENAME_GOES_HERE.xlsx")

# Print totals prior to sampling
print("Dataframe size (rows, columns):", df.shape)

# User-defined parameters
SAMPLE_SIZE = 25
STRATIFY_COLUMN = "Category"  # <- Change this to your column name

# Define stratum proportions (as fractions)
# Example: if you have categories A, B, and C
stratum_proportions = {"A": 0.4, "B": 0.4, "C": 0.2}

# Validate proportions sum to 1
if not math.isclose(sum(stratum_proportions.values()), 1.0):
    raise ValueError("Stratum proportions must sum to 1.")

# Check that all strata exist in the data
missing_strata = set(stratum_proportions.keys()) - set(df[STRATIFY_COLUMN].unique())
if missing_strata:
    raise ValueError(
        f"Strata {missing_strata} not found in column '{STRATIFY_COLUMN}'."
    )

# Perform stratified sampling
samples = []
for stratum, proportion in stratum_proportions.items():
    stratum_df = df[df[STRATIFY_COLUMN] == stratum]
    n_samples = math.floor(SAMPLE_SIZE * proportion)
    if n_samples > len(stratum_df):
        raise ValueError(
            f"Not enough data in stratum '{stratum}' to sample {n_samples} rows."
        )
    stratum_sample = stratum_df.sample(n=n_samples, random_state=42)
    samples.append(stratum_sample)

# Combine all stratum samples into one DataFrame
final_sample = pd.concat(samples).reset_index()

# If needed, randomly sample extra rows to fill any rounding gap
current_sample_size = len(final_sample)
if current_sample_size < SAMPLE_SIZE:
    remaining = SAMPLE_SIZE - current_sample_size
    remaining_sample = df.sample(n=remaining, random_state=42)
    final_sample = pd.concat([final_sample, remaining_sample])

# Print sample results
print("Final sample size:", final_sample.shape[0])
print("Sample breakdown by stratum:\n", final_sample[STRATIFY_COLUMN].value_counts())
print("\nSample:\n", final_sample)

# Optionally, save the sample to a new CSV
# final_sample.to_csv("sample_output.csv", index=False)
