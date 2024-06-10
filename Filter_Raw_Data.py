import pandas as pd

# Define the list of values to filter by
filter_values = ["1", "6", "7", "2611", "9", "13", "24", "2015", "2016", "2017", "2246", "2247", "2248",
                 "2249", "2250", "2251", "2252", "2253", "2254", "2255", "2256", "2257", "2258", "2230",
                 "1414", "1415", "367", "368", "376", "377"]

# Load the CSV file
csv_path = '98-401-X2021006_English_CSV_data_Ontario.csv'
df = pd.read_csv(csv_path,encoding='latin-1')

# Filter the DataFrame
filtered_df = df[df['CHARACTERISTIC_ID'].astype(str).isin(filter_values)]

# Save the filtered DataFrame to a new CSV file
filtered_csv_path = 'filtered_'+ csv_path
filtered_df.to_csv(filtered_csv_path, index=False)

filtered_csv_path
