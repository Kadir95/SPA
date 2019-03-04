import falcon
import rpyc
import json
import sys

sys.path.append("../../Lib")
from connections import connect_rpc, services
from token_operations import verify_token
from response_builder import std_response

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

class assign_router:
    def on_get(self, req, resp):
        assign_as = req.params.get("assign_as")

        auth_service = connect_rpc()
        user_type = auth_service.root.user_type(req.context["user"]["email"])

        if user_type is None:
            resp.media = {
                "success": False,
                "message": "No user"
            }
            return
        
        if user_type != "admin_user":
            resp.media = {
                "success": False,
                "message": "Unauthorized user"
            }
            return

        op = ["instructor", "student", "admin"]

        if assign_as not in op:
            resp.media = {
                "success": False,
                "message": "assign as parameter could be %s" %(op)
            }
            return

        if req.get_header("email") is None:
            resp.media = {
                "success": False,
                "message": "email is needed"
            }
            return

        if assign_as == "instructor" or assign_as == "student":
            if req.get_header("department_id") is None:
                resp.media = {
                    "success": False,
                    "message": "department_id is needed"
                }
                return

        data = {
            "op": assign_as,
            "email": req.get_header("email"),
            "department_id": req.get_header("department_id")
        }

        user_service = connect_rpc(service=services["user_service"])
        response = user_service.root.assign_handler(data)
        resp.media = json.loads(response)

class create_router:
    def on_get(self, req, resp):
        admin_ops = ["university", "department", "faculty", "course"]
        inst_ops = ["section", "exam"]

        needed_args = {
            "university": ["name", "s_name"],
            "department": ["faculty_id", "name"],
            "faculty": ["university_id", "name"],
            "course": ["department_id", "name", "course_code"],
            "section": ["course_id", "instructor_id", "section_code"],
            "exam": ["section_ids", "type"]
        }

        op = req.params.get("new")

        auth_service = connect_rpc()
        user_type = auth_service.root.user_type(req.context["user"]["email"])

        if user_type is None:
            resp.media = std_response(False, message="No user")
            return
        
        if op not in admin_ops + inst_ops:
            resp.media = std_response(False, message="Unsupported operation")
            return
        
        if op in admin_ops and user_type != "admin_user":
            resp.media = std_response(False, message="Unauthorized user")
            return

        if op in inst_ops and user_type != "instructor_user" and user_type != "admin_user":
            resp.media = std_response(False, message="Unauthorized user")
            return
        
        data = {
            "op": op
        }

        for needed_arg in needed_args[op]:
            if req.get_header(needed_arg) is None:
                resp.media = std_response(False, message="Insufficient arguments")
                return
            data[needed_arg] = req.get_header(needed_arg)

        user_service = connect_rpc(service=services["user_service"])
        response = user_service.root.create_handler(data)
        resp.media = json.loads(response)

api = falcon.API(middleware=[AuthMiddleware()])
api.add_route("/api/assign", assign_router())
api.add_route("/api/create", create_router())

api.add_route("/api/auth", auth_router())
api.add_route("/api/sign_in", sign_handler())
api.add_route("/api/try_token", try_token_handler())