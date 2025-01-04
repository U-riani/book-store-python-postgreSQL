import psycopg2

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host='monorail.proxy.rlwy.net',
        database='railway',
        user='postgres',
        password='uCvSdWUYewpxUAqxuQFocMlYkfQWVzJB',
        port=38750
    )

    cur = conn.cursor()

    # Check if the books table already exists to avoid recreation on each run
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'books');")
    exists = cur.fetchone()[0]

    if not exists:
        cur.execute('''CREATE TABLE books (id serial PRIMARY KEY, 
                                           title varchar(150) NOT NULL,
                                           author varchar(100) NOT NULL,
                                           pages_num int NOT NULL,
                                           review text,
                                           date_added date DEFAULT CURRENT_TIMESTAMP);'''
                    )
        conn.commit()
    else:
        print("Table 'books' already exists.")
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
