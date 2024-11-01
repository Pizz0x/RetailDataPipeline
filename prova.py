import pandas as pd

# Create a sample CSV file to simulate retail sales data
data = {
    "transaction_id": [101, 102, 103, 104, 105],
    "date": ["2023-10-01", "2023-10-01", "2023-10-02", "2023-10-02", "2023-10-03"],
    "store_id": [1, 2, 1, 3, 2],
    "product_id": [1001, 1002, 1001, 1003, 1002],
    "product_name": ["Shampoo", "Soap", "Shampoo", "Conditioner", "Soap"],
    "quantity_sold": [3, 5, 2, 7, 3],
    "unit_price": [5.99, 1.99, 5.99, 6.99, 1.99],
    "total_sales": [17.97, 9.95, 11.98, 48.93, 5.97]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_path = "data/sample_sales_data.csv"
df.to_csv(csv_path, index=False)

csv_path