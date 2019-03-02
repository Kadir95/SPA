import psycopg2 as postg
import connections

def get_user_row(column, email):
    conn = connections.connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.people WHERE email = %s;", [email])
    
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    
    indexes = []
    for colname in column:
        try:
            indexes.append(colnames.index(colname))
        except Exception:
            pass
    
    response = []
    for row in rows:
        temp = []
        for i in indexes:
            temp.append(row[i])
        response.append(temp)

    return response