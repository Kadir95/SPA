import falcon
import rpyc
import json
import sys
import os
import uuid
import pickle

import umsgpack as mp

from falcon_cors import CORS

sys.path.append("../../Lib")
from connections import connect_rpc, services
from token_operations import verify_token
from response_builder import std_response
from auth_operations import take_user_type

data_path = "/home/mzp7/workspace/MEF/SPA/Server/data"

cors = CORS(allow_all_origins=True)

# Later
class MessagePack_Translator(object):
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return
        
        body = req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest(title="Empty request body", description="A valid MessagePack document is required")
        
        try:
            req.context["body"] = mp.loads(body)
        except Exception as err:
            raise falcon.HTTPBadRequest(title="Malformed MassagePack", description="Could not decode request body")
    
    def process_response(self, req, resp, resource):
        if not resp.context["result"]:
            return
        
        resp.body = mp.dumps(resp.context["result"])

class JSON_Translator(object):
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return
        
        body = req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest(title="Empty request body", description="A valid MessagePack document is required")
        
        try:
            req.context["body"] = json.loads(body)
        except Exception as err:
            raise falcon.HTTPBadRequest(title="Malformed MassagePack", description="Could not decode request body")
    
    def process_response(self, req, resp, resource):
        if not resp.context.get("result"):
            return

        # Find a good way to do that (plz)
        resp.context["result"] = pickle.loads(pickle.dumps(resp.context["result"]))

        resp.body = json.dumps(resp.context["result"])

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
        body = req.context.get("body")
        if not body:
            raise falcon.HTTPBadRequest(title="Body is empty")

        if (body.get("email") is None or body.get("password") is None):
            raise falcon.HTTPNotAcceptable(description="email or password is missing on body")
        else:
            data = {
                "email": body.get("email"),
                "password": body.get("password")
            }
            conn = connect_rpc()
            response = conn.root.get_token(data)
            resp.context["result"] = response

class sign_handler:
    auth = {
        "auth_disabled": True
    }

    def on_get(self, req, resp):
        body = req.context.get("body")
        if not body:
            raise falcon.HTTPBadRequest(title="Body is empty")

        if body.get("email") is None or body.get("password") is None or body.get("name") is None:
            raise falcon.HTTPNotAcceptable(description="email, password or name is missing on body")
        else:
            conn = connect_rpc()
            data = {
                "email": body.get("email"),
                "name": body.get("name"),
                "lastname": body.get("lastname"),
                "password": body.get("password"),
                "school_no": body.get("school_no")
            }

            response = conn.root.add_new_user(data)
            resp.context["result"] = response

class try_token_handler:
    def on_get(self, req, resp):
        conn = connect_rpc()
        response = conn.root.verify_token(req.get_header("token"))
        resp.context["result"] = response

class assign_router:
    def on_get(self, req, resp):
        body = req.context.get("body")
        if not body:
            raise falcon.HTTPBadRequest(title="Body is empty")

        assign_as = req.params.get("assign_as")

        user_type = take_user_type(req.context["user"]["email"])

        if user_type is None:
            raise falcon.HTTPBadRequest(title="No user", description="There is no user on system to execute assign process on it")
        
        if user_type != "admin_user":
            raise falcon.HTTPUnauthorized(title="Unauthorized user")

        op = ["instructor", "student", "admin"]

        if assign_as not in op:
            raise falcon.HTTPBadRequest(title="Unsupported operation")

        if body.get("email") is None:
            raise falcon.HTTPBadRequest(title="Email is needed")

        if assign_as == "instructor" or assign_as == "student":
            if body.get("department_id") is None:
                raise falcon.HTTPBadRequest(title="Department_id is needed")

        data = {
            "op": assign_as,
            "email": body.get("email"),
            "department_id": body.get("department_id")
        }

        user_service = connect_rpc(service=services["user_service"])
        response = user_service.root.assign_handler(data)
        resp.context["result"] = response

class create_router:
    def on_get(self, req, resp):
        body = req.context.get("body")
        if not body:
            raise falcon.HTTPBadRequest(title="Body is empty")

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

        user_type = take_user_type(req.contex["user"]["email"])

        if not op:
            raise falcon.HTTPBadRequest(title="There is no 'change' params")

        if user_type is None:
            raise falcon.HTTPBadRequest(title="No user")
        
        if op not in admin_ops + inst_ops:
            raise falcon.HTTPBadRequest(title="Unsupported operation")
        
        if op in admin_ops and user_type != "admin_user":
            raise falcon.HTTPBadRequest(title="Unauthorized user")

        if op in inst_ops and user_type != "instructor_user" and user_type != "admin_user":
            raise falcon.HTTPBadRequest(title="Unauthorized user")
        
        data = {
            "op": op
        }

        for needed_arg in needed_args[op]:
            if body.get(needed_arg) is None:
                raise falcon.HTTPBadRequest(title="Insufficient arguments")
            data[needed_arg] = body.get(needed_arg)

        user_service = connect_rpc(service=services["user_service"])
        response = user_service.root.create_handler(data)
        resp.context["result"] = response

class upload_router:
    def on_post(self, req, resp):
        user_type = take_user_type(req.contex["user"]["email"])

        if user_type is None:
            resp.media = std_response(False, message="No user")
            return
        
        if user_type != "instructor_user":
            resp.media = std_response(False, message="Unauthorized user")
            return

        if req.get_header("exam_id") is None:
            resp.media = std_response(False, message="There is no exam_id")
            return

        data = {
            "exam_id": req.get_header("exam_id")
        }

        file_service = connect_rpc(service=services["file_service"])
        exam_uuid = file_service.root.exam_file(data)

        if exam_uuid is None:
            resp.media = std_response(False, message="Task failed")
            return

        file_dir = os.path.join(data_path, str(exam_uuid))
        os.makedirs(file_dir)
        file_dir = os.path.join(file_dir, "original_file")
        file = open(file_dir, "wb")
        file.write(req.stream.read())
        file.close()

        resp.media = std_response(True, message="File transferred successfully")
    
    def on_get(self, req, resp):
        user_type = take_user_type(req.contex["user"]["email"])

        if user_type is None:
            resp.media = std_response(False, message="No user")
            return
        
        if user_type != "instructor_user":
            resp.media = std_response(False, message="Unauthorized user")
            return

        if req.get_header("exam_id") is None:
            resp.media = std_response(False, message="There is no exam_id")
            return
        
        file_service = connect_rpc(service=services["file_service"])
        exam_uuid = file_service.root.split_file(req.get_header("exam_id"))

        resp.downloadable_as = 'attachment; filename="report.zip"'
        resp.stream = open(os.path.join(data_path, exam_uuid, "result.zip"), "rb")

class update_router:
    def on_get(self, req, resp):
        body = req.context.get("body")
        if not body:
            raise falcon.HTTPBadRequest(title="Body is empty")

        ops = ["section", "exam"]

        needed_args = {
            "section": ["section_id", ["instructor_id", "section_code", "course_id"]],
            "exam": ["exam_id", ["type"]]
        }

        user_type = take_user_type(req.context["user"]["email"])

        if user_type not in ["admin_user", "instructor_user"]:
            raise falcon.HTTPBadRequest(title="No user")

        op = req.params.get("change") or False

        if not op:
            raise falcon.HTTPBadRequest(title="There is no 'change' params")

        if op not in ops:
            raise falcon.HTTPBadRequest(title="Unsupported operation")

        data = {
            "op": op
        }

        for arg in needed_args[op]:
            if isinstance(arg, list):
                count = 0
                for nested_arg in arg:
                    if body.get(nested_arg):
                        data[nested_arg] = body.get(nested_arg)
                        count += 1
                if count != 1:
                    if count == 0:
                        raise falcon.HTTPBadRequest(title="Insufficient arguments")
                    else:
                        raise falcon.HTTPBadRequest(title="Too many arguments")
            else:
                if not body.get(arg):
                    raise falcon.HTTPBadRequest(title="Insufficient arguments")
                data[arg] = body.get(arg)
        
        database_service = connect_rpc(service=services["database_service"])
        response = database_service.root.update_handler(data)
        resp.context["result"] = response

class list_router:
    def on_get(self, req, resp):
        resp.context["result"] = req.context["body"]["message"]

api = falcon.API(
    middleware=[
        AuthMiddleware(),
        JSON_Translator(),
        cors.middleware
        ]
    )

api.add_route("/api/assign", assign_router())
api.add_route("/api/create", create_router())
api.add_route("/api/upload", upload_router())
api.add_route("/api/list", list_router())
api.add_route("/api/update", update_router())

api.add_route("/api/auth", auth_router())
api.add_route("/api/sign_in", sign_handler())
api.add_route("/api/try_token", try_token_handler())