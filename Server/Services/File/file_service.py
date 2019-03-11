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
from pdf_split import pdf_qrcode_reader, zip_results, is_zip_done
from db_operations import get_exam_uuid

class File_service(rpyc.Service):
    def exposed_exam_file(self, data):
        db_conn = connect_db()
        cur = db_conn.cursor()

        exam_uuid = uuid.uuid4()
        try:
            cur.execute("UPDATE public.exam SET directory=%s WHERE exam_id=%s;", [str(exam_uuid), data["exam_id"]])
            db_conn.commit()
            cur.close()
            return exam_uuid
        except Exception as err:
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