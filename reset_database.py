import database_uri
import psycopg2

conn = psycopg2.connect(database_uri.DATABASE_URI)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute('drop table if exists sales_data') 
cursor.execute('drop table if exists sales_summary') 
cursor.execute('drop table if exists stores') 
cursor.execute('drop table if exists products') 
cursor.execute('drop table if exists transactions') 
cursor.execute('drop table if exists stocks') 

conn.commit()

conn.close()