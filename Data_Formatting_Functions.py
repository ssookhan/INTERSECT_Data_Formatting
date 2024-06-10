# Data_Formatting_Functions.py
# Dr. Shane Sookhan
# November, 2023
# Functions for formatting Canada Census Data into Expected format for INTERSECT

# Import required libraries
import pandas as pd
import os.path
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def filterRawData(csv_path):
    """Function for filtering Canada Census Data for Indicators used by INTERSECT"""

    if os.path.isfile('filtered_' + csv_path):
        print('filtered_' + csv_path+' already exists.')
    else:
        # Define the list of values to filter by
        filter_values = ["1", "6", "7", "2611", "2612", "2613", "2614", "2615", "2616", "9", "13", "24", "2015",
                         "2016", "2017", "2246", "2247", "2248", "2249", "2250", "2251", "2252", "2253", "2254",
                         "2255", "2256", "2257", "2258", "2230", "1414", "1415", "365", "367", "368", "376", "377"]

        # Load the CSV file
        print('Loading ' + csv_path + ' CSV file (this can take a while...)')
        df = pd.read_csv(csv_path, encoding='latin-1')

        # Filter the DataFrame
        print('Filtering CSV file')
        filtered_df = df[df['CHARACTERISTIC_ID'].astype(str).isin(filter_values)]

        # Save the filtered DataFrame to a new CSV file
        print('Saving ' + 'filtered_' + csv_path)
        filtered_csv_path = 'filtered_' + csv_path
        filtered_df.to_csv(filtered_csv_path, index=False)

        filtered_csv_path


def transposeData(csv_path):
    """Function for transposing columns of Filtered Census Data into expected format for INTERSECT"""

    if os.path.isfile('reshaped_' + 'filtered_' + csv_path):
        print('reshaped_' + 'filtered_' + csv_path+' already exists.')
    else:
        # Set filename to filtered CSV
        filename = 'filtered_' + csv_path

        # Read the filtered CSV file
        print('Loading ' + filename + ' CSV file (this can take a while...)')
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
                         '  15 to 64 years', '  65 years and over',
                         'Total - Adjusted after-tax economic family income decile group for the population in private households - 100% data',
                         '    In bottom decile',
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
                         'Total - Commuting duration for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data',
                         '  Less than 15 minutes',
                         '  15 to 29 minutes',
                         '  30 to 44 minutes',
                         '  45 to 59 minutes',
                         '  60 minutes and over',]

        # Select and reorder columns
        print('Transposing ' + filename)
        pivot_df = pivot_df[columns_order]

        # Write the reshaped data to a new CSV file
        print('Saving ' + 'reshaped_' + filename)
        pivot_df.to_csv('reshaped_' + filename, index=False)


def removeNoData(csv_path):
    """Function for removing any rows that are missing indicators for INTERSECT"""

    if os.path.isfile('cleaned_' + 'reshaped_' + 'filtered_' + csv_path):
        print('cleaned_' + 'reshaped_' + 'filtered_' + csv_path+' already exists.')
    else:
        # Set filename to reshaped CSV
        filename = 'reshaped_' + 'filtered_' + csv_path

        # Read the CSV file
        print('Loading ' + filename)
        df = pd.read_csv(filename)

        # Drop rows with any blank (NaN) values
        print('Cleaning ' + filename)
        cleaned_df = df.dropna()

        # Write the cleaned data to a new CSV file
        print('Saving ' + 'cleaned_' + filename)
        cleaned_df.to_csv('cleaned_' + filename, index=False)


def makeIndicators(csv_path):
    """Function for making the INTERSECT indicators from the formatted Canada census data"""

    if os.path.isfile('indicators_' + csv_path):
        print('indicators_' + csv_path + ' already exists.')
    else:
        # Set filename to cleaned CSV
        file_path = 'cleaned_' + 'reshaped_' + 'filtered_' + csv_path
        print('Loading ' + file_path)
        df = pd.read_csv(file_path)

        # Define the columns for the new CSV
        print('Calculating Indicators')
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
                    df[
                        'Total - Commuting duration for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data']
            ),
            'Age Dependency': df['  15 to 64 years'] / (df['  0 to 14 years'] + df['  65 years and over']),
            'Education Level': (
                    (df['  No certificate, diploma or degree'] * 0.25 +
                    df['  High (secondary) school diploma or equivalency certificate'] * 0.5 +
                    df['  Postsecondary certificate, diploma or degree'])/
                    df['Population, 2021']
            ),
            'Job Diversity': 1 - (
                ((df['    0 Legislative and senior management occupations'] / df['  All occupations']) ** 2 +
                 (df['    1 Business, finance and administration occupations'] / df['  All occupations']) ** 2 +
                 (df['    2 Natural and applied sciences and related occupations'] / df['  All occupations']) ** 2 +
                 (df['    3 Health occupations'] / df['  All occupations']) ** 2 +
                 (df['    4 Occupations in education, law and social, community and government services'] / df[
                     '  All occupations']) ** 2 +
                 (df['    5 Occupations in art, culture, recreation and sport'] / df['  All occupations']) ** 2 +
                 (df['    6 Sales and service occupations'] / df['  All occupations']) ** 2 +
                 (df['    7 Trades, transport and equipment operators and related occupations'] / df[
                     '  All occupations']) ** 2 +
                 (df['    8 Natural resources, agriculture and related production occupations'] / df[
                     '  All occupations']) ** 2 +
                 (df['    9 Occupations in manufacturing and utilities'] / df['  All occupations']) ** 2)
            ),
            'Unemployment Rate': df['Unemployment rate'],
            'Home Ownership Rate': df['  Owner'] / df['Total - Private households by tenure - 25% sample data'],
            'Bottom Income Decile': (df['    In bottom decile'] + df['    In second decile']) /
            df['Total - Adjusted after-tax economic family income decile group for the population in private households - 100% data'],
            'Top Income Decile': (df['    In ninth decile'] + df['    In top decile']) /
            df['Total - Adjusted after-tax economic family income decile group for the population in private households - 100% data'],
            'Income Ratio': (df['    In ninth decile'] + df['    In top decile']) / (
                        df['    In bottom decile'] + df['    In second decile'])
        }

        # Create the new DataFrame
        new_df = pd.DataFrame(new_columns)

        # Save the new DataFrame to a CSV file
        print('Saving ' + 'indicators_' + csv_path)
        new_csv_path = 'indicators_' + csv_path
        new_df.to_csv(new_csv_path, index=False)


def scaleIndicators(csv_path):
    """Function for min-max scaling the INTERSECT indicators using a Log Transformation scaling method"""

    if os.path.isfile('scaled_' + csv_path):
        print('scaled_' + csv_path + ' already exists.')
    else:
        # Load the CSV data
        df = pd.read_csv('indicators_' + csv_path)

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
        scaled_df.to_csv('scaled_' + csv_path, index=False)

        print(
            "Log transformation followed by min-max scaling and rounding completed and saved to " + 'scaled_' + csv_path)