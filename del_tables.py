import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
cur = conn.cursor()
cur.execute ("DROP TABLE IF EXISTS accounts, scan_sessions, content_params")
conn.commit()
cur.close()

cur = conn.cursor()
cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
print cur.fetchall()

conn.close()
