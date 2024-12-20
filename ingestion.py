import pandas as pd
#from sqlalchemy import create_engine
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values
from config import load_config

### 1. DATA INGESTION

sales_data = pd.read_csv('data/transaction_data.csv') # Load data from a CSV file
# Store the Extracted Data Temporarily (Optional)

### 2. DATA TRANSFORMATION
removed_rows = []
# 2.1 CLEAN ERRORS AND DUPLICATE ROWS

sales_toKeep = []
for index, row in sales_data.iterrows():
    date_time = datetime.strptime(row['date_time'], '%m/%d/%Y %H:%M')
    now = datetime.now()
    if (row['quantity'] < 1):
        removed_row_with_reason = row.to_dict()
        removed_row_with_reason['reason'] = 'The product sold in this row has a quantity minor than 1'
        removed_rows.append(removed_row_with_reason)
    elif (row['discount'] > 1):
        removed_row_with_reason = row.to_dict()
        removed_row_with_reason['reason'] = 'The product sold in this row has a discount greater than 100%'
        removed_rows.append(removed_row_with_reason)
    elif (date_time > now):
        removed_row_with_reason = row.to_dict()
        removed_row_with_reason['reason'] = f'This transaction has a register date: {date_time} greater than the actual time {now}'
        removed_rows.append(removed_row_with_reason)
    else:
        sales_toKeep.append(row)

sales_data = pd.DataFrame(sales_toKeep)

unique_sales = set()
sales_toKeep = []
for index, row in sales_data.iterrows():
    if (row['transaction_id'], row['product_id']) not in unique_sales:
        sales_toKeep.append(row)
        unique_sales.add((row['transaction_id'], row['product_id']))
    else:
        removed_row_with_reason = row.to_dict()
        removed_row_with_reason['reason'] = 'The row is a duplicate, it has the same transaction_id and product_id of an already saved row'
        removed_rows.append(removed_row_with_reason)

sales_data = pd.DataFrame(sales_toKeep)

#print(sales_data)
# 2.2 CLEAN ROWS WITH SAME ID BUT DIFFERENT FIELDS FOR EVERY TYPE OF DATA FRAME

# get all the rows where store_id is the same and see if there are rows with some of the stores field different, do this even for products and transactions
tmp_removed_rows = []
store = sales_data.groupby('store_id')
rows_toKeep = []
for store_id, row in store:
    # get the sum of the row with the same exact transaction fields and leave the bigger one
    counter = row.groupby(['store_city', 'store_address', 'store_postalcode']).size()
    max = counter.idxmax()
    max_row = row[(row['store_city'] == max[0]) & (row['store_address'] == max[1]) & (row['store_postalcode'] == max[2])]
    rows_toKeep.append(max_row)
    # add the rows that are excluded for a precise store_id in temporary removed rows
    tmp_removed_rows = row[~((row['store_city'] == max[0]) & (row['store_address'] == max[1]) & (row['store_postalcode'] == max[2]))]
    # add the reason of the removal and append the temporary removed rows to removed rows
    for _, removed_row in tmp_removed_rows.iterrows():
        removed_row_with_reason = removed_row.to_dict()
        removed_row_with_reason['reason'] = f'The row has been removed for store_id: {store_id} with a less frequent combination'
        removed_rows.append(removed_row_with_reason)
sales_data = pd.concat(rows_toKeep, ignore_index=True)
#print(sales_data)

transaction = sales_data.groupby('transaction_id')
rows_toKeep = []
for transaction_id, row in transaction:
    # get the sum of the row with the same exact transaction fields and leave the bigger one
    counter = row.groupby(['payment_method', 'store_id', 'date_time', 'transaction_type']).size()
    max = counter.idxmax()
    max_row = row[(row['payment_method'] == max[0]) & (row['store_id'] == max[1]) & (row['date_time'] == max[2]) & (row['transaction_type'] == max[3])]
    rows_toKeep.append(max_row)
    # add the rows that are excluded for a precise store_id in temporary removed rows
    tmp_removed_rows = row[~((row['payment_method'] == max[0]) & (row['store_id'] == max[1]) & (row['date_time'] == max[2]) & (row['transaction_type'] == max[3]))]
    # add the reason of the removal and append the temporary removed rows to removed rows
    for _, removed_row in tmp_removed_rows.iterrows():
        removed_row_with_reason = removed_row.to_dict()
        removed_row_with_reason['reason'] = f'The row has been removed for transaction_id: {transaction_id} with a less frequent combination'
        removed_rows.append(removed_row_with_reason)

sales_data = pd.concat(rows_toKeep, ignore_index=True)

product = sales_data.groupby('product_id')
rows_toKeep = []
for product_id, row in product:
    # get the sum of the row with the same exact transaction fields and leave the bigger one
    counter = row.groupby(['product_name', 'product_description', 'product_category', 'unit_price']).size()
    max = counter.idxmax()
    max_row = row[(row['product_name'] == max[0]) & (row['product_description'] == max[1]) & (row['product_category'] == max[2]) & (row['unit_price'] == max[3])]
    rows_toKeep.append(max_row)
    # add the rows that are excluded for a precise store_id in temporary removed rows
    tmp_removed_rows = row[~((row['product_name'] == max[0]) & (row['product_description'] == max[1]) & (row['product_category'] == max[2]) & (row['unit_price'] == max[3]))]
    # add the reason of the removal and append the temporary removed rows to removed rows
    for _, removed_row in tmp_removed_rows.iterrows():
        removed_row_with_reason = removed_row.to_dict()
        removed_row_with_reason['reason'] = f'The row has been removed for product_id: {product_id} with a less frequent combination'
        removed_rows.append(removed_row_with_reason)

sales_data = pd.concat(rows_toKeep, ignore_index=True)

#save the removed rows in a txt file
with open('removed_rows.txt', 'w') as f:
    for row in removed_rows:
        f.write(str(row) + '\n')

# pd.DataFrame(removed_rows).to_csv('removed_rows.csv', index=False)

# 2.3 CREATE DERIVED FIELDS
sales_data['total_price'] = sales_data['quantity'] * sales_data['unit_price'] * (1 - sales_data['discount'])  # Declare new calculated fields
sales_data['transaction_price'] = 0
sales_data['total_sold'] = 0
sales_data['stock_level'] = 0

sales_summary = sales_data.groupby(['store_id','product_id']).agg({'total_price': 'sum'})  # to watch best products, best store and best products per store

#print(sales_summary)
# 2.4 PARTITION DATA IN DIFFERENT DATA FRAME

# CITIES
cities = sales_data[['store_postalcode', 'store_city']]
unique_cities = set()
cities_to_keep = []
for index, row in cities.iterrows():
    if row['store_postalcode'] not in unique_cities:
        cities_to_keep.append(row)
        unique_cities.add(row['store_postalcode'])

cities = pd.DataFrame(cities_to_keep)

# STORES
stores = sales_data[['store_id', 'store_address', 'store_postalcode']]
unique_stores = set()
stores_toKeep = []
for index, row in stores.iterrows():
    if row['store_id'] not in unique_stores:
        stores_toKeep.append(row)
        unique_stores.add(row['store_id'])

stores = pd.DataFrame(stores_toKeep)

# cities
cities = sales_data[['store_postalcode', 'store_city']]
unique_cities = set()
cities_to_keep = []
for index, row in cities.iterrows():
    if row['store_postalcode'] not in unique_cities:
        cities_to_keep.append(row)
        unique_cities.add(row['store_postalcode'])

cities = pd.DataFrame(cities_to_keep)

# PRODUCTS
products = sales_data[['product_id', 'product_name', 'product_description', 'product_category', 'unit_price', 'total_sold']]
unique_products = set()
# List to store rows that should be kept
products_toKeep = []
# Iterate over each row to check for duplicates and keep unique rows
for index, row in products.iterrows():
    # If product_id is not in unique_product_ids, it's a unique product
    if (row['product_id'] not in unique_products):
        products_toKeep.append(row)
        unique_products.add(row['product_id'])

# Create a new DataFrame with only the unique products
products = pd.DataFrame(products_toKeep)

# TRANSACTIONS
transactions = sales_data[['transaction_id', 'payment_method', 'store_id', 'date_time', 'transaction_type', 'transaction_price']]
unique_transactions = set()
transactions_toKeep = []
for index, row in transactions.iterrows():
    if (row['transaction_id'] not in unique_transactions) and (row['store_id'] in unique_stores):
        transactions_toKeep.append(row)
        unique_transactions.add(row['transaction_id'])

transactions = pd.DataFrame(transactions_toKeep)

# STOCKS
stocks = sales_data[['store_id', 'product_id', 'stock_level']]
unique_stocks = set()
stocks_toKeep = []
for index, row in stocks.iterrows():
    if (row['store_id'], row['product_id']) not in unique_stocks and (row['store_id'] in unique_stores and row['product_id'] in unique_products):
        stocks_toKeep.append(row)
        unique_stocks.add((row['store_id'], row['product_id']))

stocks = pd.DataFrame(stocks_toKeep)

#NOW THAT WE HAVE ALL TABLES WITH UNIQUE ROW WE CAN IMPLEMENT THE TABLE TRANSACTION_PRODUCTS AND MODIFY THE CALCULATED VALUES OF THE OTHER DATAFRAME
transaction_products = sales_data[['transaction_id', 'product_id', 'quantity', 'discount', 'total_price']]
tp_toKeep = []
for index, row in transaction_products.iterrows():
    if row['product_id'] in unique_products and row['transaction_id'] in unique_transactions:
        tp_toKeep.append(row)
        # UPDATE NUMBER OF PRODUCT SOLD
        product_row = products[products['product_id'] == row['product_id']]
        transaction_row = transactions[transactions['transaction_id'] == row['transaction_id']] #transaction row with the right id
        if transaction_row['transaction_type'].values[0] == 'sell':
            quantity = product_row['total_sold'].values[0] + row['quantity']
            products.loc[products['product_id'] == row['product_id'], 'total_sold'] = quantity
        # UPDATE THE TRANSACTION PRICE
        transaction_row = transactions[transactions['transaction_id'] == row['transaction_id']]
        transaction_price = transaction_row['transaction_price'].values[0] + row['total_price']
        transactions.loc[transactions['transaction_id'] == row['transaction_id'], 'transaction_price'] = transaction_price    
        # UPDATE NUMBER OF PRODUCT IN THE STOCK
        store_id = transaction_row['store_id'].values[0] #store id of the transaction
        stock_row = stocks[(stocks['store_id'] == store_id) & (stocks['product_id'] == row['product_id'])] #stock row with the right id

        # if transaction is Sell we substract to the stock, if the transaction is Buy we add, otherwise we do nothing
        #print(f"the stock level is {stock_row['stock_level'].values[0]}")
        if stock_row.empty:
            stock_level = row['quantity']
        elif(transaction_row['transaction_type'].values[0] == 'buy'):
            stock_level = stock_row['stock_level'].values[0] + row['quantity']
        elif(transaction_row['transaction_type'].values[0] == 'sell'):
            stock_level = stock_row['stock_level'].values[0] - row['quantity']
        else:
            stock_level = stock_row['stock_level'].values[0]
        stocks.loc[(stocks['product_id']==row['product_id']) & (stocks['store_id']==store_id), 'stock_level'] = stock_level

stocks = pd.DataFrame(stocks)
sales_data = pd.DataFrame(sales_data)
sales_summary = pd.DataFrame(sales_summary)


### 3. DATA STORAGE 

config = load_config()
conn = psycopg2.connect(**config)
conn.autocommit = True
cursor = conn.cursor()

# 3.1 Insert Stores in the Database
cities_tuples = [tuple(x) for x in cities.to_numpy()]
sql1 = """
insert into cities (store_postalcode, store_city)
values %s
on conflict(store_postalcode) do nothing;
"""
execute_values(cursor, sql1, cities_tuples)


stores_tuples = [tuple(x) for x in stores.to_numpy()]
sql2 = """

INSERT INTO stores (store_id, store_address, store_postalcode)
VALUES %s
ON CONFLICT(store_id) DO NOTHING;
"""
execute_values(cursor, sql2, stores_tuples)

# 3.2 Insert Transactions in the Database
transactions_tuples = [tuple(x) for x in transactions.to_numpy()]
sql3 = """
INSERT INTO transactions (transaction_id, payment_method, store_id, date_time, transaction_type, transaction_price)
VALUES %s
ON CONFLICT(transaction_id) DO NOTHING;
"""
execute_values(cursor, sql3, transactions_tuples)

# 3.3 Insert Products in the Database
products_tuples = [tuple(x) for x in products.to_numpy()]
sql4 = """
INSERT INTO products (product_id, product_name, product_description, product_category, unit_price, total_sold)
VALUES %s
ON CONFLICT(product_id) 
DO UPDATE SET
    unit_price = EXCLUDED.unit_price,
    total_sold = products.total_sold + EXCLUDED.total_sold;
"""
execute_values(cursor, sql4, products_tuples)

# 3.4 Insert Transaction Products in the Database
transaction_products_tuples = [tuple(x) for x in transaction_products.to_numpy()]
sql5 = """
INSERT INTO transaction_products (transaction_id, product_id, quantity_sold, discount, total_price)
VALUES %s
ON CONFLICT(product_id, transaction_id) DO NOTHING;
"""
execute_values(cursor, sql5, transaction_products_tuples)

stocks_tupels = [tuple(x) for x in stocks.to_numpy()]
sql6 = """
INSERT INTO stocks (store_id, product_id, stock_level)
VALUES %s
ON CONFLICT(store_id, product_id) DO NOTHING;
"""

# 3.5 Stocks in the Database
stocks_tuples = [tuple(int(x) for x in row) for row in stocks.to_numpy()]
sql6 = """
INSERT INTO stocks (store_id, product_id, stock_level)
VALUES %s ON CONFLICT(store_id, product_id) 
DO UPDATE SET
    stock_level = stocks.stock_level + EXCLUDED.stock_level;
"""
execute_values(cursor, sql6, stocks_tuples)


# #sql1 = '''select * from sales_data'''
# #cursor.execute(sql1)
# sql2 = '''select * from sales_summary'''
# cursor.execute(sql2)
# sql3 = '''select * from stores'''
# cursor.execute(sql3)
# sql4 = '''select * from products'''
# cursor.execute(sql4)
# sql5 = '''select * from transactions'''
# cursor.execute(sql5)
# sql6 = '''select * from stocks'''
# cursor.execute(sql6)

# for i in cursor.fetchall():
#     print(i)


