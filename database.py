conn = psycopg2.connect(database = "retail_data", 
                        user = "admin", 
                        host= 'localhost',
                        password = "admin",
                        port = 5432)