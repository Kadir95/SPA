import falcon
import rpyc
import json
import sys

sys.path.append("../../Lib")
from connections import connect_rpc, services
from token_operations import verify_token

class AuthMiddleware(object):
    def __init__(self, exempt_routes=None, exempt_methods=None):
        # self.backend = connect_rpc() 
        self.exempt_routes = exempt_routes or []
        self.exempt_methods = exempt_methods or ['OPTIONS']

    def _get_auth_settings(self, req, resource):
        auth_settings = getattr(resource, 'auth', {})
        auth_settings['exempt_routes'] = self.exempt_routes
        if auth_settings.get('auth_disabled'):
            auth_settings['exempt_routes'].append(req.path)

        key = 'exempt_methods'
        auth_settings[key] = auth_settings.get(key) or getattr(self, key)

        return auth_settings
    
    def process_resource(self, req, resp, resource, params):
        auth_setting = self._get_auth_settings(req, resource)
        if (req.uri_template in auth_setting['exempt_routes'] or
            req.method in auth_setting['exempt_methods']):
            return

        token = req.get_header("token")
        if token == None:
            raise falcon.HTTPUnauthorized(description="There must be token")

        response = verify_token(token)

        if response["success"] == False:
            raise falcon.HTTPUnauthorized(description=response["message"])

        req.context['user'] = response["payload"]

class auth_router:
    auth = {
        "auth_disabled": True
    }

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

class sign_handler:
    auth = {
        "auth_disabled": True
    }

    def on_get(self, req, resp):
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

class try_token_handler:
    def on_get(self, req, resp):
        conn = connect_rpc()
        response = conn.root.verify_token(req.get_header("token"))
        resp.media = json.loads(response)

class user_handler:
    def on_get(self, req, resp):
        conn = connect_rpc(service= services["user_service"])
        resp.media = json.loads(conn.root.echo(req.get_header("text")))

class user_type:
    def on_get(self, req, resp):
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

class add_university:
    def on_get(self, req, resp):
        data = {
            "email": req.context["user"]["email"],
            "university_name": req.get_header("university_name"),
            "university_sname": req.get_header("university_sname")
        }

        if data["university_name"] is None or data["university_sname"] is None:
            resp.media = {
                "success": False,
                "message": "university_name or university_sname aren't mentioned"
            }
            return
        
        user_service = connect_rpc(service=services["user_service"])

        resp.media = json.loads(user_service.root.add_university(data))

api = falcon.API(middleware=[AuthMiddleware()])
api.add_route("/api/auth", auth_router())
api.add_route("/api/sign_in", sign_handler())
api.add_route("/api/try_token", try_token_handler())
api.add_route("/api/user", user_handler())
api.add_route("/api/user/type", user_type())
api.add_route("/api/user/add_university", add_university())