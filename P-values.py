import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os

# Constants
TRIAL_START = 6
TRIAL_END = 30
CASE_SWITCH = 23
DAY_CUTOFF = 3.5
SIGNIFICANCE_LEVELS = {'***': 0.001, '**': 0.01, '*': 0.05}
FILE_PREFIX = 'bse_ICAART24_H2_'
FILE_SUFFIX = '_s01_d007_i05_0001_transactions.csv'


# Function to process each file
def process_file(file_name):
    try:
        # Read and process the CSV file
        prices_df = pd.read_csv(file_name)
        prices_df.columns = ['index', 'Day', 'Transactions']
        prices_df['Day'] /= (60 * 60 * 24)  # Convert seconds to days

        # Split data into first and second half
        first_half = prices_df[prices_df['Day'] <= DAY_CUTOFF]['Transactions']
        second_half = prices_df[prices_df['Day'] > DAY_CUTOFF]['Transactions']

        # Perform the Mann-Whitney U test
        _, p_value = stats.mannwhitneyu(first_half, second_half, alternative='two-sided')

        return p_value

    except pd.errors.EmptyDataError:
        print(f"No data in {file_name}")
    except FileNotFoundError:
        print(f"{file_name} does not exist.")
    except Exception as e:
        print(f"An error occurred while processing {file_name}: {e}")

    return None


# Initialize lists to hold p-values and trial IDs
p_values = []
trial_ids = []

# Loop through all files and process them
for i in range(TRIAL_START, TRIAL_END):
    case = "Case2" if i < CASE_SWITCH else "Case1"
    trial_id = f"{FILE_PREFIX}{case}_testing_s{'0' if i < 10 else ''}{i}{FILE_SUFFIX}"
    p_value = process_file(trial_id)

    if p_value is not None:
        p_values.append(p_value)
        trial_ids.append(trial_id)

# Prepare data for plotting
formatted_trial_ids = [f"{str(2*i).zfill(2)}_Traders" for i in range(TRIAL_START, TRIAL_END-1)]

neg_log_pvals = [-np.log10(p) if p > 0 else -np.log10(1e-300) for p in p_values]
colors = ['red' if p <= SIGNIFICANCE_LEVELS['***'] else 'orange' if p <= SIGNIFICANCE_LEVELS['**'] else 'green' if p <=
                                                                                                                   SIGNIFICANCE_LEVELS[
                                                                                                                       '*'] else 'skyblue'
          for p in p_values]

# Plotting
plt.figure(figsize=(15, 5))
bars = plt.bar(formatted_trial_ids, neg_log_pvals, color=colors)

# Add horizontal lines for common significance levels
for level, cutoff in SIGNIFICANCE_LEVELS.items():
    plt.axhline(y=-np.log10(cutoff), color='grey', linestyle='--', lw=0.5)
    plt.text(len(p_values) + 1, -np.log10(cutoff), level, va='center', ha='right', backgroundcolor='white')

# Annotate bars with the p-value
for bar, p_value in zip(bars, p_values):
    if p_value <= SIGNIFICANCE_LEVELS['***']:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{p_value:.1e}", ha='center', va='bottom')

plt.xticks(rotation=90)
plt.xlabel('Number of traders')
plt.ylabel('-log10(p-value)')
plt.title('Statistical Significance of Price Differences Between First 3 Days and Last 3 Days as the Number of Traders Increases')
plt.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=color) for color in ['red', 'orange', 'green', 'skyblue']],
           labels=['p <= 0.001', 'p <= 0.01', 'p <= 0.05', 'not significant'], loc='upper right')
plt.tight_layout()

# Save the figure before showing
plt.savefig("significance_plot.png")
plt.show()
