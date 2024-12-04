import psycopg2
from config import load_config

config = load_config()
conn = psycopg2.connect(**config)
conn.autocommit = True
cursor = conn.cursor()
sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
cursor.execute(sql)
for i in cursor.fetchall():
    print(i)

# def connect(config):
#     """ Connect to the PostgreSQL database server """
#     try:
#         # connecting to the PostgreSQL server
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 # Execute your SQL query here
#                 cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        
#                 # Fetch and print results
#                 for row in cur.fetchall():
#                     print(row[0])
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(error)




# if __name__ == '__main__':
#     config = load_config()
#     connect(config)