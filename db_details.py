import os
import psycopg2
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = 'monorail.proxy.rlwy.net',
        database = 'railway',
        user = 'postgres',
        password = 'uCvSdWUYewpxUAqxuQFocMlYkfQWVzJB',
        port = 38750
    )

    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS books;')

    cur.execute('''CREATE TABLE books (id serial PRIMARY KEY, 
                                        title varchar(150) NOT NULL,
                                        author varchar(100) NOT NULL,
                                        pages_num int NOT NULL,
                                        review text,
                                        date_added date DEFAULT CURRENT_TIMESTAMP);'''
                )
    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()