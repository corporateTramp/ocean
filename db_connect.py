import psycopg2
conn = psycopg2.connect("dbname=mydb user=postgres")
cur = conn.cursor()
# cur.execute("CREATE TABLE accounts ( id INT PRIMARY KEY NOT NULL, name character(100), description text, private bool, created_at timestamp, updated_at timestamp);")

conn.commit()
cur.close()
conn.close()