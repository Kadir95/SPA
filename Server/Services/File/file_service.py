import rpyc
import json
import jwt
import sys
import os
import uuid
import psycopg2 as postg
from rpyc.utils.server import ThreadedServer

if  os.environ.get("SPACONTAINER"):
    print(os.environ.get("SPACONTAINER"))
    sys.path.append("/Server/Lib")
else:
    sys.path.append("../../Lib")

from connections import connect_rpc, services, connect_db
from token_operations import verify_token, secret
from pdf_split import pdf_qrcode_reader, zip_results, is_zip_done
from db_operations import get_exam_uuid
from network_tools import get_host_ip

host = "localhost"
if os.environ.get("SPACONTAINER"):
    host = get_host_ip()
    log_file = open("/log", "w")
    log_file.write("host ip: %s, port: %d\n" %(host, services["auth_service"]))
    log_file.flush()

class File_service(rpyc.Service):
    ALIASES = ["file_service"]

    def on_connect(self, connection):
        log_file.write("connection received\n")
        log_file.flush()

        if not hasattr(self, "db_conn"):
            self.db_conn = None

        if self.db_conn is None:
            self.db_conn = connect_db()
        elif self.db_conn.closed != 0:
            self.db_conn = connect_db()
    

    def exposed_exam_file(self, data):
        cur = self.db_conn.cursor()

        exam_uuid = uuid.uuid4()
        try:
            cur.execute("UPDATE public.exam SET directory=%s WHERE exam_id=%s;", [str(exam_uuid), data["exam_id"]])
            self.db_conn.commit()
            cur.close()
            return exam_uuid
        except Exception as err:
            self.db_conn.rollback()
            print(err)
            return None
    
    def exposed_split_file(self, exam_id):
        exam_uuid = get_exam_uuid(exam_id)
        if is_zip_done(exam_uuid):
            return exam_uuid
        pdf_qrcode_reader(exam_uuid)
        zip_results(exam_uuid)
        return exam_uuid


port = services["file_service"]
rypc_server = ThreadedServer(
    File_service,
    port=port,
    protocol_config={
        'allow_public_attrs': True,
        "allow_pickle": True
        }
    )
rypc_server.start()