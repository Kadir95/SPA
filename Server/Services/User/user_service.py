import rpyc
import json
import jwt
import sys
import datetime
import psycopg2 as postg
import hashlib, base64
from rpyc.utils.server import ThreadedServer

sys.path.append("../../Lib")
from connections import connect_rpc, services, connect_db
import db_operations

conn = connect_db()

secret = "tikitikitemponeserambocarıbururucineserambo"

class User_service(rpyc.Service):
    def exposed_echo(self, text):
        return json.dumps({"text": text})
    
    def exposed_create_instructor(self, data):
        auth_service = connect_rpc()

        token = data["token"]
        token_verification_json = auth_service.root.verify_token(token)
        token_verification_json = json.loads(token_verification_json)

        if token_verification_json["success"]:
            token_payload = token_verification_json["payload"]
            
            email = data["email"]
            user_type = auth_service.root.user_type(token_payload["email"])
            if user_type is not None and user_type == "admin_user":
                response = db_operations.get_user_row(["id"], email)
                response = response[0]
                if len(response) == 0:
                    return json.dumps({
                        "success": False,
                        "message": "No user who has <%s> email" %(email)
                    })
                
                response = response[0]

                conn = connect_db()
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO public.instructors(instructor_id, id_people) VALUES (%s, %s);", [response, response])
                except Exception:
                    conn.rollback()
                    return json.dumps({
                        "success": False,
                        "message": "The user who has <%s> email is already instructor" %(email)
                    })
                conn.commit()

                return json.dumps({
                    "success": True,
                    "message": "The user who has <%s> email added into instructors list" %(email)
                })
            else:
                return json.dumps({
                    "success": False,
                    "message": "Permission denied"
                })
        else:
            return token_verification_json

port = services["user_service"]
rypc_server = ThreadedServer(
    User_service,
    port=port
    )
rypc_server.start()