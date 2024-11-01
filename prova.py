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

# transaction: transaction_id, date_time, store_id, payment_method
# transaction_product: id_artificial, product_id, transaction_id, quantity_sold, discount, total_cost
# store: store_id, store_city, store_address, store_postalcode
# product: product_id, product_name, product_description, product_category, unit_price, total_sold       
# stock: id_artificial, product_id, store_id, stock_level                                                stock is a table between product and store to see how many product are left //OPTIONAL

# transaction_id, date_time, payment_method, product_id, product_name, product_description, product_category, unit_price, quantity_sold, discount, store_id, store_city, store_address, store_postalcode

# product_description: can be null
# product_category: can be null
# discount can be null
# store_address can be null
# if we have two rows with the same product_id but a different product_name what we should do?