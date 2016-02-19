import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
cur = conn.cursor()
cur.execute ("DROP TABLE IF EXISTS accounts, scan_sessions, content_params")
conn.commit()
cur.close()
conn.close()

