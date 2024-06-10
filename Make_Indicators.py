import pandas as pd

# Load the CSV file
file_path = 'cleaned_reshaped_filtered_98-401-X2021006_English_CSV_data_Ontario.csv'
df = pd.read_csv(file_path)

# Define the columns for the new CSV
new_columns = {
    'GEOUID': df['ALT_GEO_CODE'],
    'GEO_LEVEL': df['GEO_LEVEL'],
    'GEO_NAME': df['GEO_NAME'],
    'Population Density': df['Population density per square kilometre'],
    'Social Mobility': (
        (7.5 * df['  Less than 15 minutes'] +
         22 * df['  15 to 29 minutes'] +
         37 * df['  30 to 44 minutes'] +
         52 * df['  45 to 59 minutes'] +
         75 * df['  60 minutes and over']) /
        df['Total - Commuting duration for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data']
    ),
    'Age Dependency': df['  15 to 64 years'] / (df['  0 to 14 years'] + df['  65 years and over']),
    'Education Level': (
        df['  No certificate, diploma or degree'] * 0.25 +
        df['  High (secondary) school diploma or equivalency certificate'] * 0.5 +
        df['  Postsecondary certificate, diploma or degree']
    ),
    'Job Diversity': 1 - (
        ((df['    0 Legislative and senior management occupations'] / df['  All occupations']) ** 2 +
         (df['    1 Business, finance and administration occupations'] / df['  All occupations']) ** 2 +
         (df['    2 Natural and applied sciences and related occupations'] / df['  All occupations']) ** 2 +
         (df['    3 Health occupations'] / df['  All occupations']) ** 2 +
         (df['    4 Occupations in education, law and social, community and government services'] / df['  All occupations']) ** 2 +
         (df['    5 Occupations in art, culture, recreation and sport'] / df['  All occupations']) ** 2 +
         (df['    6 Sales and service occupations'] / df['  All occupations']) ** 2 +
         (df['    7 Trades, transport and equipment operators and related occupations'] / df['  All occupations']) ** 2 +
         (df['    8 Natural resources, agriculture and related production occupations'] / df['  All occupations']) ** 2 +
         (df['    9 Occupations in manufacturing and utilities'] / df['  All occupations']) ** 2)
    ),
    'Unemployment Rate': df['Unemployment rate'],
    'Home Ownership Rate': df['  Owner'] / df['Total - Private households by tenure - 25% sample data'],
    'Bottom Income Decile': df['    In bottom decile'] + df['    In second decile'],
    'Top Income Decile': df['    In ninth decile'] + df['    In top decile'],
    'Income Ratio': (df['    In ninth decile'] + df['    In top decile']) / (df['    In bottom decile'] + df['    In second decile'])
}

# Create the new DataFrame
new_df = pd.DataFrame(new_columns)

# Save the new DataFrame to a CSV file
new_csv_path = 'path_to_save_new_csv_file.csv'
new_df.to_csv(new_csv_path, index=False)
