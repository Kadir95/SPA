# -*- coding: utf-8 -*-
import rpyc
import psycopg2 as postg
import os

services = {
    "auth_service": 7878,
    "user_service": 7879,
    "file_service": 7880,
    "database_service": 7881
}

service_ports_path = os.path.join("Server/Lib/config/service_ports")
if os.path.isfile(service_ports_path):
    fd = open(service_ports_path, "r")
    port_data = list(map(lambda x: [x[0].strip(), int(x[1])], map(lambda x: x.split(":"), fd.readlines())))
    services = dict(port_data)

def connect_rpc(service = services["auth_service"]):
    return rpyc.connect("localhost", service, config={"allow_all_attrs": True, 'allow_public_attrs': True})

def connect_db():
    return postg.connect(database="new_database", user="postgres", password="333xwx333", host="172.17.0.2")

if __name__ == "__main__":
    print(services)