import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
cur = conn.cursor()

cur.execute("CREATE TABLE accounts ( id SERIAL PRIMARY KEY, name text, description text, private bool, created_at timestamp, updated_at timestamp);")

cur.execute("CREATE TABLE scan_sessions ( id SERIAL PRIMARY KEY, account_id integer, publications integer,subscribers integer, subscribtions integer, created_at timestamp);")

cur.execute("CREATE TABLE content_params ( id SERIAL PRIMARY KEY, account_id integer, scan_session_id integer,content_type text,description text, likes integer, comments integer, created_at timestamp);")

conn.commit()
cur.close()

cur = conn.cursor()
cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
print cur.fetchall()

conn.close()
