# -*- coding: utf-8 -*-
def std_response(success, message=None):
    if message is None:
        return {
            "success": success
        }
    else:
        return {
            "success": success,
            "message": message
        }