import pandas as pd

# Load data from a CSV file
sales_data = pd.read_csv('data/sales_data.csv')
# Display first few rows to verify
print(sales_data.head())