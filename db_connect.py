

import psycopg2
conn = psycopg2.connect("dbname=mydb user=postgres")
cur = conn.cursor()
cur.execute("INSERT INTO accounts (name)* FROM accounts;")

conn.commit()
cur.close()
conn.close()