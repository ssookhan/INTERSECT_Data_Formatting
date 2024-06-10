import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the CSV data
df = pd.read_csv('indicators_98-401-X2021006_English_CSV_data_Ontario.csv')

# Columns to be scaled
columns_to_scale = [
    'Population Density', 'Social Mobility', 'Age Dependency', 'Education Level',
    'Job Diversity', 'Unemployment Rate', 'Home Ownership Rate',
    'Bottom Income Decile', 'Top Income Decile', 'Income Ratio'
]

# Ensure that only numeric columns are considered for scaling
for column in columns_to_scale:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Initialize a new DataFrame to hold the scaled data
scaled_df = df.copy()

# Group by 'GEO_LEVEL' and apply log transformation followed by min-max scaling
min_max_scaler = MinMaxScaler(feature_range=(0, 6))

for category, group in df.groupby('GEO_LEVEL'):
    # Handle NaN and infinite values within the columns to be scaled
    group[columns_to_scale] = group[columns_to_scale].replace([np.inf, -np.inf], np.nan)
    group[columns_to_scale] = group[columns_to_scale].fillna(group[columns_to_scale].mean())

    # Apply log transformation (adding a small constant to avoid log(0))
    log_transformed = np.log1p(group[columns_to_scale])

    # Apply Min-Max Scaling to get values in the range 0-6
    min_max_scaled = min_max_scaler.fit_transform(log_transformed)

    # Round the scaled values to the nearest whole number
    scaled_df.loc[group.index, columns_to_scale] = np.round(min_max_scaled)

# Save the scaled DataFrame to a new CSV file
scaled_df.to_csv('scaled_data_log_minmax_rounded.csv', index=False)

print(
    "Log transformation followed by min-max scaling and rounding completed and saved to 'scaled_data_log_minmax_rounded.csv'")
