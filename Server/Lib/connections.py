import rpyc
import psycopg2 as postg

services = {
    "auth_service": 7878,
    "user_service": 7879
}

def connect_rpc(service = services["auth_service"]):
    return rpyc.connect("localhost", service)

def connect_db():
    return postg.connect(database="new_database", user="postgres", password="333xwx333", host="172.17.0.3")
