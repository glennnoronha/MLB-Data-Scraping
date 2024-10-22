import pandas as pd

# Step 1: Load the CSV file
data = pd.read_csv('hitting_stats.csv')

# Step 2: Convert relevant columns to numeric
numeric_cols = ['BA', 'HR', 'RBI', 'OBP', 'SLG', 'SB', 'BB', 'PA']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Option 1: Drop rows with any NaN values in the relevant columns
# data = data.dropna(subset=numeric_cols)

# Option 2: Fill NaN values with 0
data[numeric_cols] = data[numeric_cols].fillna(0)

# print the updated DataFrame
print(data)