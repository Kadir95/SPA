import falcon
import rpyc
import json
import sys

sys.path.append("../../Lib")
from connections import connect_rpc, services

class auth_router:
    def on_get(self, req, resp):
        if (req.get_header("email") is None or req.get_header("password") is None):
            resp.media = {
                "success": False,
                "message": "There is no value about email or password"
            }
        else:
            data = {
                "email": req.get_header("email"),
                "password": req.get_header("password")
            }
            conn = connect_rpc()
            response = conn.root.get_token(data)
            resp.media = json.loads(response)

def sign_handler(req, resp):
    if req.get_header("email") is None or req.get_header("password") is None or req.get_header("name") is None:
        resp.media = {
            "success": False,
            "message": "Not enough argument. email, password and name are must"
        }
    else:
        conn = connect_rpc()
        data = {
            "email": req.get_header("email"),
            "name": req.get_header("name"),
            "lastname": req.get_header("lastname"),
            "password": req.get_header("password"),
            "school_no": req.get_header("school_no")
        }

        response = conn.root.add_new_user(data)
        resp.media = json.loads(response)

def try_token_handler(req, resp):
    if req.get_header("token") is None:
        resp.media = {
            "success": False,
            "message": "There is no token on request"
        }
    else:
        conn = connect_rpc()
        response = conn.root.verify_token(req.get_header("token"))
        resp.media = json.loads(response)

def user_handler(req, resp):
    conn = connect_rpc(service= services["user_service"])
    resp.media = json.loads(conn.root.echo(req.get_header("text")))

def user_type(req, resp):
    user_service = connect_rpc(service=services["user_service"])
    auth_service = connect_rpc()

    if req.get_header("email") is not None and req.get_header("token") is not None:
        data = {
            "email": req.get_header("email"),
            "token": req.get_header("token")
        }
        
        resp.media = json.loads(user_service.root.create_instructor(data))
    else:
        resp.media = {
            "success": False,
            "message": "token and email should be mentioned"
        }

api = falcon.API()
api.add_route("/api/auth", auth_router())
api.add_sink(sign_handler, "/api/sign_in")
api.add_sink(try_token_handler, "/api/try_token")
api.add_sink(user_handler, "/api/user")
api.add_sink(user_type, "/api/user/type")