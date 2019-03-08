# -*- coding: utf-8 -*-
import jwt

secret = "tikitikitemponeserambocaribururucineserambo"

def verify_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms="HS256")
        return {
            "success": True,
            "payload": payload
        }
    except jwt.ExpiredSignatureError as err:
        return {
            "success": False,
            "message": "expired token"
        }
    except jwt.DecodeError as err:
        return {
            "success": False,
            "message": "decode error"
        }
    # easter egg :)
    return {
        "success": False,
        "message": "python failed successfully!"
    }