import falcon
import rpyc
import json

def connect_rpc():
    return rpyc.connect("localhost", 7878)

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

api = falcon.API()
api.add_route("/api/auth", auth_router())
api.add_sink(sign_handler, "/api/sign_in")
api.add_sink(try_token_handler, "/api/try_token")