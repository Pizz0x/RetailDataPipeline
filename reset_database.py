import psycopg2
from config import load_config

config = load_config()
conn = psycopg2.connect(**config)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute('drop table if exists sales_data cascade')
cursor.execute('drop table if exists sales_summary cascade') 
cursor.execute('drop table if exists stores cascade') 
cursor.execute('drop table if exists cities cascade') 
cursor.execute('drop table if exists products cascade') 
cursor.execute('drop table if exists transactions cascade') 
cursor.execute('drop table if exists transaction_products cascade') 
cursor.execute('drop table if exists stocks cascade') 

conn.commit()

cursor.execute('''create table cities(store_postalcode int primary key, 
                                    store_city char(20))''')
cursor.execute('''create table stores(store_id int primary key, 
                                    store_address char(30), 
                                    store_postalcode int, 
                                    foreign key (store_postalcode) references cities (store_postalcode) on update cascade on delete cascade)''')
cursor.execute('''create table transactions(transaction_id int primary key, 
                                    payment_method char(20), 
                                    store_id int, 
                                    date_time timestamp, 
                                    transaction_type char(20),
                                    foreign key (store_id) references stores (store_id) on update cascade on delete cascade)''')
cursor.execute('''create table products(product_id int primary key, 
                                    product_name char(20), 
                                    product_description char(50), 
                                    product_category char(20), 
                                    unit_price float, 
                                    total_sold int)''')
cursor.execute('''create table transaction_products(transaction_id int, 
                                    product_id int, 
                                    quantity_sold int, 
                                    discount float, 
                                    total_price float, 
                                    primary key(transaction_id, product_id),
                                    foreign key (transaction_id) references transactions (transaction_id) on update cascade on delete cascade,
                                    foreign key (product_id) references products (product_id) on update cascade on delete cascade)''')
cursor.execute('''create table stocks(store_id int, 
                                    product_id int, 
                                    stock_level int, 
                                    primary key (store_id, product_id),
                                    foreign key (store_id) references stores (store_id) on update cascade on delete cascade,
                                    foreign key (product_id) references products (product_id) on update cascade on delete cascade)''')
cursor.execute('''create table sales_summary(store_id int, 
                                    product_id int, 
                                    total_price float, 
                                    primary key (store_id, product_id),
                                    foreign key (store_id) references stores (store_id) on update cascade on delete cascade,
                                    foreign key (product_id) references products (product_id) on update cascade on delete cascade)''')
cursor.execute('''create table sales_data(transaction_id int, 
                                    date_time timestamp, 
                                    payment_method char(20), 
                                    product_id int, 
                                    product_name char(20), 
                                    product_description char(50), 
                                    product_category char(20), 
                                    unit_price float, 
                                    quantity int, 
                                    discount float, 
                                    store_id int, 
                                    store_city char(20), 
                                    store_address char(30), 
                                    store_postalcode int, 
                                    transaction_type char(20), 
                                    total_price float, 
                                    total_sold int, 
                                    stock_level int,
                                    foreign key (store_postalcode) references cities (store_postalcode) on update cascade on delete cascade,
                                    foreign key (store_id) references stores (store_id) on update cascade on delete cascade,
                                    foreign key (transaction_id) references transactions (transaction_id) on update cascade on delete cascade,
                                    foreign key (product_id) references products (product_id) on update cascade on delete cascade)''')

conn.commit()

conn.close()