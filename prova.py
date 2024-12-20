
# transaction: transaction_id, transaction_type, date_time, store_id, payment_method, #transaction_price
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
# product will be saved only if we it's the first time that product has been bought, otherwise it will be updated with the new data
# store will be saved only if its the first transaction in the store
# stock i don't think its appropriate right now because we dont start with some values already in the table, but we can do like type of transaction and if it's an import it means it's a delivery so some product has arrived to the store, but the problem is that we dont know with how many items for a product we start and we don't even know with what products we start

# do we suppose that data we receive are correct?
# if we have two rows with the same product_id but a different product_name what we should do?  not discard the second one, because maybe its the second one to be correct

# we are going to use Apache Airflow because we imagine that in a real retail data management, we are not working with a super reactive system where in real time it analyze the single data, we thought it more like a batch automated flow that manage the ingestion and transformation of data at regular intervals, in our case every day at midnight when the shops are closed
# we also chose Apache Airflow because it allows us to incorporate python scripts directly
#Represent workflow in a Directed Acyclic Graph​
#Each node represent a task and the edges between them represent the dependencies
# DAG is a collection of all the tasks i want to run organzed ina a way that reflect their relationship and dependencies
# When a dag run is triggered the tasks are gonna be executed one after another based on their dependencies. Each task has different state in its lifecycle. 
# no status: the initial status, the scheduler create an empty task instance
# 4 different stages the task can be moved on : scheduled -> the scheduler determine the task instance need to be run ; removed; upstream failed; skipped
# scheduled -> then executor put task into a queue and once the worker computation resources are free the state became running and then success; failed or shutdown


# Airflow Xcoms is used to share information between tasks: push information to Xcoms in a task and pull from others.
#by default every functions return value will be automatically pushed into xcoms, never use xcoms to share large data as pandas dataframe
# in airflow creating a dag needs the schedule interval parameter which receives a cron esxpression as a string or a datetime.timedelta object.
# a cron expression is a string comprising 5 fields separeted by white space that represent a set of time as a schedule to execute some routine -> if u know how to use cron expressions u can schedule your dag in any way u want.
# to generate customized schedule interval using cron expression '* * * * *' minute hour day(month) month day(week)  example: 0 3 * * Tue,Fri  -> at 3 am on tuesday and friday

#Using Apache Airflow for data ingestion, we can extend its functionality for performance monitoring:
#Built-in Logging and Monitoring: Airflow provides logs for every task in a DAG. You can monitor task execution times and failure rates from the Airflow UI.
#LAs (Service Level Agreements): You can set SLAs for tasks to monitor if they complete within a defined time. 

# data storage: insert data into a database with models that if not already created are goin to be created by apache airflow and then with some dedicated procedure data are gonna be visualised in graph thanks to Grafana or other visualisation interface.
# presentation on a case scenario : introduction on what we wanted to do, explaining the tools we are using and why and explaining the case and what we did to manage it

# interesting graphs:   # of products sold every day from every store   
#                       most sold product in total
#                       most sold product for every store
#                       store with most products sold
#                       average money spent in a transaction

# question for the first csv file: can you create me a csv file with this information: transaction_id,date_time,payment_method,product_id,product_name,product_description,product_category,unit_price,quantity,discount,store_id,store_city,store_address,store_postalcode,transaction_type, where transaction_id is the id of the transaction (in a transaction there can be more products so there can be more line with a transaction_id, date_time is only in the last 2 months. payment method can be only: cash, card or gift card. the product are clothes and there are 5 stores: Bruxelles, Brugges, Gent, Antwerp and Liege. The transaction_type is for buy and sell so the shop before fullfil the stock and then sell the products. is it possible for you to do a big csv file with at least 10000 rows?

#Data Transformation: From a complicated and unique dataframe to consistent and well structured dataframes, one for each object described in the initial one.
# Data visualization and analisys: After consistently storing data in a database, we can create queries to analyse data and make it understandable and useful for the customers, The integration of Grafana ensures that decision-makers can access insights at a glance, enabling proactive business strategies

#