

import pandas as pd
import sqlite3

#Increase the maximum number of rows displayed
pd.set_option('display.max_rows', None)

# Replace 'Food Sales.xlsx' with your actual file path
file_path = r"D:\BCIT-NED\7TH SEMESTER\Data WareHouse Mining\Lab Project\Food_Sales.csv"

# Read the Excel file without considering the first row as header
data = pd.read_csv(file_path)

# Print the first few rows to inspect the data
print(data.head(10))

# TRANSFORMATION

# Convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'] + '-2023', format='%d-%b-%Y', errors='coerce')

# Summarize the data
summary = data.describe()

# Enrich the data by adding a new column 'Amount' calculated as Qty * UnitPrice
data['Amount'] = data['Qty'] * data['UnitPrice']


# Drop the original 'TotalPrice' column if needed
data = data.drop('TotalPrice', axis=1)

# Print the transformed data and summary
print("Transformed Data:")
print(data)

print("\nSummary Statistics:")
print(summary)


# Load the dataset
file_path1 = r"D:\BCIT-NED\7TH SEMESTER\Data WareHouse Mining\Lab Project\Used_Car_Dataset.csv"
data1 = pd.read_csv(file_path1)

# Check for missing values in the dataset
null_values = data1.isnull().sum()

# Print missing values before filling
print("Missing values before filling:")
print(null_values)

print(data1.head(10))
# Replace null values in numeric columns with the mean
numeric_columns = data1.select_dtypes(include='number').columns
data1[numeric_columns] = data1[numeric_columns].fillna(data1[numeric_columns].mean())

# Print missing values after filling
print("\nMissing values after filling:")
print(data1.isnull().sum())

# # Check for missing values in 'car_name'
# if data1['car_name'].isnull().any():
#     print("Warning: There are missing values in the 'car_name' column. Handle them before splitting.")

def extract_car_info(car_name):
    car_info = car_name.split(' ', 2)
    model = car_info[0] if len(car_info) > 0 else None
    company = car_info[1] if len(car_info) > 1 else None
    car = car_info[2] if len(car_info) > 2 else None
    return model, company, car

# Apply the function to create new columns
data1[['model', 'company', 'car']] = data1['car_name'].apply(lambda x: pd.Series(extract_car_info(x)))

# Drop the original 'car_name' column if needed
data1 = data1.drop('car_name', axis=1)

# Print the transformed DataFrame
print("\nTransformed DataFrame:")
print(data1.head())

summary_stats = data1.describe()
print("\nSummary Statistics:")
print(summary_stats)

#loading the dataset into database

# Connect to an SQLite database (if it doesn't exist, it will be created)
conn = sqlite3.connect(r'D:\BCIT-NED\7TH SEMESTER\Data WareHouse Mining\AnasDBB.db')

data.to_sql('food', conn, if_exists='replace', index=False)
data1.to_sql('car', conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()



