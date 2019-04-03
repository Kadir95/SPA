import rpyc
import json
import jwt
import sys
import os
import datetime
import psycopg2 as postg
import hashlib, base64
from rpyc.utils.server import ThreadedServer

if  os.environ.get("SPACONTAINER"):
    print(os.environ.get("SPACONTAINER"))
    sys.path.append("/Server/Lib")
else:
    sys.path.append("../../Lib")

from connections import connect_rpc, services, connect_db
from token_operations import verify_token, secret
from auth_operations import user_types
from response_builder import std_response
from network_tools import get_host_ip

host = "localhost"
if os.environ.get("SPACONTAINER"):
    host = get_host_ip()
    log_file = open("/log", "w")
    log_file.write("host ip: %s, port: %d\n" %(host, services["auth_service"]))
    log_file.flush()

class Auth_service(rpyc.Service):
    ALIASES = ["auth_service"]

    def _take_care_password(self, password, salt):
        hash_password = hashlib.pbkdf2_hmac("sha256", str.encode(password), str.encode(salt), 1024)
        hash_password = base64.encodebytes(hash_password)
        return hash_password.decode().strip()

    def on_connect(self, connection):
        log_file.write("connection received\n")
        log_file.flush()

        if not hasattr(self, "db_conn"):
            self.db_conn = None

        if self.db_conn is None:
            self.db_conn = connect_db()
        elif self.db_conn.closed != 0:
            self.db_conn = connect_db()

    def exposed_add_new_user(self, data):
        cur = self.db_conn.cursor()

        hash_password = self._take_care_password(data["password"], data["email"])

        try:
            cur.execute("INSERT INTO public.people(password, name, lastname, school_no, email) VALUES (%s, %s, %s, %s, %s);", [
                hash_password,
                data["name"],
                data["lastname"],
                data["school_no"],
                data["email"]
                ])
        except Exception as e:
            self.db_conn.rollback()
            cur.close()
            return std_response(False, message="An error occur on operation")
        
        self.db_conn.commit()
        cur.close()

        return std_response(True, message="new user added successfully")
        
    def exposed_get_token(self, data):
        cur = self.db_conn.cursor()

        email = data["email"]
        password = data["password"]

        hash_password = self._take_care_password(password, email)

        cur.execute("SELECT * FROM public.people WHERE email = %s AND password = %s", [email, hash_password])
        rows = cur.fetchall()
        cur.close()

        response = []
        for row in rows:
            response.append(row)

        if len(response) == 0:
            return std_response(False, message="Wrong email or password")

        response = response[0]

        user_id = response[0]
        token = jwt.encode({
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            "name": response[2],
            "lastname": response[3],
            "school_no": response[4],
            "email": response[5],
            "expire_time": 2
        }, secret, algorithm="HS256")

        return {
            "success": True,
            "token_type": "jwt",
            "token": token.decode()
        }

    def exposed_user_type(self, email):
        if email is not None:
            cur = self.db_conn.cursor()
            cur.execute("""select P.id, A.admin_id, I.instructor_id, S.student_id from ((
                            (public.people as P left join public.admins as A on P.id = A.admin_id)
                            left join public.instructors as I on P.id = I.instructor_id) 
                            left join public.students as S on P.id = S.student_id)
                            where P.email = %s;""", [email])
            rows = cur.fetchall()
            cur.close()

            response = []
            for row in rows:
                response.append(row)
            
            if len(response) == 0:
                return None    
            response = response[0]

            if response[1] is not None:
                return user_types[0]
            elif response[2] is not None:
                return user_types[1]
            elif response[3] is not None:
                return user_types[2]
            else:
                return user_types[3]
        else: 
            return None
        
    def exposed_verify_token(self, token):
        return verify_token(token)

port = services["auth_service"]
rypc_server = ThreadedServer(
    Auth_service,
    port=port,
    protocol_config={
        'allow_public_attrs': True,
        "allow_pickle": True
        }
    )
rypc_server.start()