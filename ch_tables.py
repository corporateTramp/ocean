import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
cur = conn.cursor()

print "ACCOUNTS----------------------------------------"
cur = conn.cursor()
cur.execute("SELECT * FROM accounts;")
cur.fetchall()
cur.close()
print "SCAN_SESSEIONS----------------------------------------"
cur = conn.cursor()
cur.execute("SELECT * FROM scan_sessions;")
cur.fetchall()
cur.close()

print "CONTENT_PARAMS----------------------------------------"
cur = conn.cursor()
cur.execute("SELECT * FROM content_params;")
cur.fetchall()
cur.close()

conn.close()
