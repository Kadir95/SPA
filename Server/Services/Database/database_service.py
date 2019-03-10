import rpyc
import json
import jwt
import sys
import uuid
import psycopg2 as postg
from rpyc.utils.server import ThreadedServer

sys.path.append("../../Lib")
from connections import connect_rpc, services, connect_db
from token_operations import verify_token, secret
from pdf_split import pdf_qrcode_reader, zip_results
from db_operations import get_exam_uuid
from response_builder import std_response

db_conn = connect_db()

class Database_service(rpyc.Service):
    def exposed_update_handler(self, data):
        cur = db_conn.cursor()

        op = data.get("op")

        if op == "section":
            if data.get("instructor_id"):
                try:
                    cur.execute("UPDATE public.sections SET instructor_id_instructors=%s WHERE section_id = %s;", [data["instructor_id"], data["section_id"]])
                    db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    db_conn.rollback()
                    return std_response(False, message="An error occur")
            elif data.get("section_code"):
                try:
                    cur.execute("UPDATE public.sections SET section_code=%s WHERE section_id = %s;", [data["section_code"], data["section_id"]])
                    db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    db_conn.rollback()
                    return std_response(False, message="An error occur")
            elif data.get("course_id"):
                try:
                    cur.execute("UPDATE public.sections SET course_id_courses=%s WHERE section_id = %s;", [data["course_id"], data["section_id"]])
                    db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    db_conn.rollback()
                    return std_response(False, message="An error occur")
        elif op == "exam":
            if data.get("type"):
                try:
                    cur.execute("UPDATE public.exam SET type=%s WHERE exam_id=%s;", [data["type"], data["exam_id"]])
                    db_conn.commit()
                    cur.close()
                    return std_response(True, message="Operation ended successfully")
                except Exception as err:
                    db_conn.rollback()
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