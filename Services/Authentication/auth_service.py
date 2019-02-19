import rpyc
import json
import psycopg2 as postg
from rpyc.utils.server import ThreadedServer

conn = postg.connect(database="spa", user="spa", password="333xwx333", host="172.17.0.2")

class Auth_service(rpyc.Service):
    def exposed_search_username(self, text):
        cur = conn.cursor()
        cur.execute("SELECT * FROM spadb.people WHERE name = '" + text + "'")
        rows = cur.fetchall()
        response =[]
        for row in rows:
            response.append(list(row[-3:]))
        return json.dumps(response)

port = 7878
rypc_server = ThreadedServer(
    Auth_service,
    port=port
    )
rypc_server.start()