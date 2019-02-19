import falcon
import rpyc
import json

class ping_router:
    def on_get(self, req, resp):
        
        conn = rpyc.connect("localhost", 7878)
        response = conn.root.search_username("_name")
        resp.media = json.loads(response)

def sign_handler(req, resp):
    pass

api = falcon.API()
api.add_route('/ping', ping_router())