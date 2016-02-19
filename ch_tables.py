import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
cur = conn.cursor()

print "ACCOUNTS----------------------------------------"
cur.execute("SELECT * FROM accounts;")
cur.fetchall()
print "SCAN_SESSEIONS----------------------------------------"
cur.execute("SELECT * FROM scan_sessions;")
cur.fetchall()
print "CONTENT_PARAMS----------------------------------------"
cur.execute("SELECT * FROM content_params;")
cur.fetchall()

cur.close()
conn.close()
