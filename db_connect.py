import psycopg2
conn = psycopg2.connect("dbname=mydb user=postgres")
cur = conn.cursor()
cur.execute("SELECT * FROM accounts;")

conn.commit()
cur.close()
conn.close()