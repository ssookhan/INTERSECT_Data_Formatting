import pandas as pd

filename= "reshaped_filtered_98-401-X2021006_English_CSV_data_Ontario.csv"

# Read the CSV file
df = pd.read_csv(filename)

# Drop rows with any blank (NaN) values
cleaned_df = df.dropna()

# Write the cleaned data to a new CSV file
cleaned_df.to_csv('cleaned_'+ filename, index=False)
