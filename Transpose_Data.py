import pandas as pd

filename= "filtered_98-401-X2021006_English_CSV_data_Ontario.csv"

# Read the original CSV file
df = pd.read_csv(filename)

# Create a pivot table
pivot_df = df.pivot_table(index=['DGUID', 'ALT_GEO_CODE', 'GEO_LEVEL', 'GEO_NAME'],
                          columns='CHARACTERISTIC_NAME',
                          values='C1_COUNT_TOTAL',
                          aggfunc='first').reset_index()

# Flatten the column names
pivot_df.columns.name = None

# Reorder columns to match the desired format
columns_order = ['DGUID', 'ALT_GEO_CODE', 'GEO_LEVEL', 'GEO_NAME',
                 'Population, 2021', 'Population density per square kilometre',
                 'Land area in square kilometres', '  0 to 14 years',
                 '  15 to 64 years', '  65 years and over', '    In bottom decile',
                 '    In second decile', '    In ninth decile', '    In top decile',
                 'Total - Private households by tenure - 25% sample data', '  Owner',
                 '  No certificate, diploma or degree',
                 '  High (secondary) school diploma or equivalency certificate',
                 '  Postsecondary certificate, diploma or degree', 'Unemployment rate',
                 'Total - Labour force aged 15 years and over by occupation - Broad category - National Occupational Classification (NOC) 2021 - 25% sample data',
                 '  Occupation - not applicable', '  All occupations',
                 '    0 Legislative and senior management occupations',
                 '    1 Business, finance and administration occupations',
                 '    2 Natural and applied sciences and related occupations',
                 '    3 Health occupations',
                 '    4 Occupations in education, law and social, community and government services',
                 '    5 Occupations in art, culture, recreation and sport',
                 '    6 Sales and service occupations',
                 '    7 Trades, transport and equipment operators and related occupations',
                 '    8 Natural resources, agriculture and related production occupations',
                 '    9 Occupations in manufacturing and utilities',
                 'Total - Commuting duration for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data']

# Select and reorder columns
pivot_df = pivot_df[columns_order]

# Write the reshaped data to a new CSV file
pivot_df.to_csv('reshaped_'+ filename, index=False)
