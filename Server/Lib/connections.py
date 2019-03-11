# -*- coding: utf-8 -*-
import rpyc
import psycopg2 as postg

services = {
    "auth_service": 7878,
    "user_service": 7879,
    "file_service": 7880,
    "database_service": 7881
}

def connect_rpc(service = services["auth_service"]):
    return rpyc.connect("localhost", service, config={"allow_all_attrs": True, 'allow_public_attrs': True})

def connect_db():
    return postg.connect(database="new_database", user="postgres", password="333xwx333", host="172.17.0.2")

def conncet_mongo():
    return MongoClient("172.17.0.2", 27017)
