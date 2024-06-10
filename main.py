# Python Script for formatting Raw Canada Census Data into INTERSECT expected format

# importing  all the
# functions defined in test.py
from Data_Formatting_Functions import *

# Define filename for download Raw Census Data here
# Download from here, extract and place in same directory as script:
# https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E
csv_path = '98-401-X2021006_English_CSV_data_Ontario.csv'

# Call functions
filterRawData(csv_path)
transposeData(csv_path)
removeNoData(csv_path)
makeIndicators(csv_path)
scaleIndicators(csv_path)
