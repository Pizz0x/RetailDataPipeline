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

# transaction: transaction_id, transaction_type, date_time, store_id, payment_method
# transaction_product: product_id, transaction_id, quantity_sold, discount, #total_price
# store: store_id, store_city, store_address, store_postalcode
# product: product_id, product_name, product_description, product_category, unit_price, #total_sold       
# stock: product_id, store_id, #stock_level                                                stock is a table between product and store to see how many product are left //OPTIONAL

# transaction_id, transaction_type, date_time, payment_method, product_id, product_name, product_description, product_category, unit_price, quantity_sold, discount, store_id, store_city, store_address, store_postalcode

# product_description: can be null
# product_category: can be null
# discount can be null
# store_address can be null

# once we receive data, we add it to the table transaction_product cause every row in the csv is about a product in a transaction, then we will add the information in the other relation only if there isnt already that information saved:
# transaction will be saved only if we are in a new transaction
# product will be saved only if we it's the first time that product has been bought
# store will be saved only if its the first transaction in the store
# stock i don't think its appropriate right now because we dont start with some values already in the table, but we can do like type of transaction and if it's an import it means it's a delivery so some product has arrived to the store, but the problem is that we dont know with how many items for a product we start and we don't even know with what products we start

# do we suppose that data we receive are correct?
# if we have two rows with the same product_id but a different product_name what we should do?  not discard the second one, because maybe its the second one to be correct

# we are going to use Apache Airflow because we imagine that in a real retail data management, we are not working with a super reactive system where in real time it analyze the single data, we thought it more like a batch automated flow that manage the ingestion and transformation of data at regular intervals (like every day at midnight when the shops are closed)
# we also chose Apache Airflow because it allows us to incorporate python scripts directly
# DAG is a collection of all the tasks i want to run organzed ina a way that reflect their relationship and dependencies
# When a dag run is triggered the tasks are gonna be executed one after another based on their dependencies. Each task has different state in its lifecycle. 
# no status: the initial status, the scheduler create an empty task instance
# 4 different stages the task can be moved on : scheduled -> the scheduler determine the task instance need to be run ; removed; upstream failed; skipped
# scheduled -> then executor put task into a queue and once the worker computation resources are free the state became running and then success; failed or shutdown


# Airflow Xcoms is used to share information between tasks: push information to Xcoms in a task and pull from others.
#by default every functions return value will be automatically pushed into xcoms