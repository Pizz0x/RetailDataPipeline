import pandas as pd

# Load data from a CSV file
sales_data = pd.read_csv('data/sample_sales_data.csv')
# Display first few rows to verify

# Optionaly:  Store the Extracted Data Temporarily

# Data Transormation: 

sales_data['total_price'] = sales_data['quantity'] * sales_data['unit_price']
sales_data['total_sold'] = 0
sales_data['stock_level'] = 0

# PARTITION DATA IN DIFFERENT DATA FRAME AND CLEAN THEM: ONLY A ROW FOR EVERY STORE, PRODUCT, TRANSACTION, ...

#UNIQUE STORE 
stores = sales_data[['store_id', 'store_city', 'store_address', 'store_postalcode']]
unique_stores = set()
stores_toKeep = []
for index, row in stores.iterrows():
    if row['store_id'] not in unique_stores:
        stores_toKeep.append(row)
        unique_stores.add(row['store_id'])

stores = pd.DataFrame(stores_toKeep)

#UNIQUE PRODUCT
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

#UNIQUE TRANSACTION
transactions = sales_data[['transaction_id', 'payment_method', 'store_id', 'date_time', 'transaction_type']]
unique_transactions = set()
transactions_toKeep = []
for index, row in transactions.iterrows():
    if (row['transaction_id'] not in unique_transactions) and (row['store_id'] in unique_stores):
        transactions_toKeep.append(row)
        unique_transactions.add(row['transaction_id'])

transactions = pd.DataFrame(transactions_toKeep)

#UNIQUE STOCK
stocks = sales_data[['store_id', 'product_id', 'stock_level']]
unique_stocks = set()
stocks_toKeep = []
for index, row in stocks.iterrows():
    if (row['store_id'], row['product_id']) not in unique_stocks and (row['store_id'] in unique_stores and row['product_id'] in unique_products):
        stocks_toKeep.append(row)
        unique_stocks.add((row['store_id'], row['product_id']))

stocks = pd.DataFrame(stocks_toKeep)

#NOW THAT WE HAVE ALL TABLES WITH UNIQUE ROW WE CAN IMPLEMENT THE TABLE TRANSACTION_PRODUCTS THAT IS BASICALLY EVERY CORRECT ROW OF THE CSV FILE AND MODIFY THE VALUES OF THE OTHER DATAFRAME
transaction_products = sales_data[['transaction_id', 'product_id', 'quantity', 'discount', 'total_price']]
tp_toKeep = []
for index, row in transaction_products.iterrows():
    if row['product_id'] in unique_products and row['transaction_id'] in unique_transactions:
        tp_toKeep.append(row)
        # refresh the number of products sold
        product_row = products[products['product_id'] == row['product_id']]
        quantity = product_row['total_sold'].values[0] + row['quantity']
        products.loc[products['product_id'] == row['product_id'], 'total_sold'] = quantity
        # refresh the number of products in the stock
        transaction_row = transactions[transactions['transaction_id'] == row['transaction_id']] #transaction row with the right id
        store_id = transaction_row['store_id'].values[0] #store id of the transaction
        stock_row = stocks[(stocks['store_id'] == store_id) & (stocks['product_id'] == row['product_id'])] #stock row with the right id

        # if transaction is Sell we substract to the stock, if the transaction is Buy, we add, otherwise we do nothing
        #print(f"the stock level is {stock_row['stock_level'].values[0]}")
        if stock_row.empty:
            stock_level = row['quantity']
        elif(transaction_row['transaction_type'].values[0] == 'Buy'):
            stock_level = stock_row['stock_level'].values[0] + row['quantity']
        elif(transaction_row['transaction_type'].values[0] == 'Sell'):
            stock_level = stock_row['stock_level'].values[0] - row['quantity']
        else:
            stock_level = stock_row['stock_level'].values[0]
        stocks.loc[(stocks['product_id']==row['product_id']) & (stocks['store_id']==store_id), 'stock_level'] = stock_level


print(products)
print(transactions)
print(stores)
print(stocks)

    
# Store the Extracted Data Temporarily (Optional)