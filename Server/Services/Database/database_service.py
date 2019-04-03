import rpyc
import sys
import os
from rpyc.utils.server import ThreadedServer

if  os.environ.get("SPACONTAINER"):
    print(os.environ.get("SPACONTAINER"))
    sys.path.append("/Server/Lib")
else:
    sys.path.append("../../Lib")

from connections import connect_rpc, services, connect_db
from token_operations import verify_token, secret
from pdf_split import pdf_qrcode_reader, zip_results
from db_operations import get_exam_uuid
from response_builder import std_response
from network_tools import get_host_ip

host = "localhost"
if os.environ.get("SPACONTAINER"):
    host = get_host_ip()
    log_file = open("/log", "w")
    log_file.write("host ip: %s, port: %d\n" %(host, services["auth_service"]))
    log_file.flush()

class Database_service(rpyc.Service):
    ALIASES = ["database_service"]

    def on_connect(self, connection):
        log_file.write("connection received\n")
        log_file.flush()

        if not hasattr(self, "db_conn"):
            self.db_conn = None

        if self.db_conn is None:
            self.db_conn = connect_db()
        elif self.db_conn.closed != 0:
            self.db_conn = connect_db()
    
    def exposed_update_handler(self, data):
        op = data.get("op")

        if op == "section":
            if data.get("instructor_id"):
                try:
                    cur.execute("UPDATE public.sections SET instructor_id_instructors=%s WHERE section_id = %s;", [data["instructor_id"], data["section_id"]])
                    self.db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    self.db_conn.rollback()
                    return std_response(False, message="An error occur")
            elif data.get("section_code"):
                try:
                    cur.execute("UPDATE public.sections SET section_code=%s WHERE section_id = %s;", [data["section_code"], data["section_id"]])
                    self.db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    self.db_conn.rollback()
                    return std_response(False, message="An error occur")
            elif data.get("course_id"):
                try:
                    cur.execute("UPDATE public.sections SET course_id_courses=%s WHERE section_id = %s;", [data["course_id"], data["section_id"]])
                    self.db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    self.db_conn.rollback()
                    return std_response(False, message="An error occur")
        elif op == "exam":
            if data.get("type"):
                try:
                    cur.execute("UPDATE public.exam SET type=%s WHERE exam_id=%s;", [data["type"], data["exam_id"]])
                    self.db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    self.db_conn.rollback()
                    return std_response(False, message="An error occur")
        else:
            return std_response(False, message="Operation doesn't match")

port = services["database_service"]
rypc_server = ThreadedServer(
    Database_service,
    port=port,
    protocol_config={
        'allow_public_attrs': True,
        "allow_pickle": True
        }
    )
rypc_server.start()