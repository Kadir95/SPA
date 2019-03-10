# -*- coding: utf-8 -*-
import jwt
from response_builder import std_response

secret = "tikitikitemponeserambocaribururucineserambo"

def verify_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms="HS256")
        return {
            "success": True,
            "payload": payload
        }
    except jwt.ExpiredSignatureError as err:
        return std_response(False, message="expired token")
    except jwt.DecodeError as err:
        return std_response(False, message="decode error")
    # easter egg :)
    return std_response(False, message="python failed successfully!")