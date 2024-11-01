import pandas as pd

# Load data from a CSV file
sales_data = pd.read_csv('data/sales_data.csv')
# Display first few rows to verify
#print(sales_data.head())
# cycle to check all the row of the file:
for index, row in sales_data.iterrows():
    val = True
    if(row['transaction_id'] is None):
        val = False
    
# Store the Extracted Data Temporarily (Optional)