import requests
import bson

from pprint import pprint

admin_token = ""

def test_auth():
    url = "http://10.8.0.2:8000/api/auth"

    payload = {
        "email": "kundakcioglua@mef.edu.tr",
        "password": "333xwx333"
    }

    payload = bson.dumps(payload)

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "4a0a5983-fb41-4353-81b6-aaa6d2a42d44"
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    print(response, response.text)
    
    if response.status_code == 200:
        data = bson.loads(response.content)
        global admin_token
        admin_token = data["token"]
        print(type(admin_token))
        pprint(data)


def test_load():
    pdf_file = open("./data/original_file", "rb")
    pdf = pdf_file.read()

    url = "http://10.8.0.2:8000/api/upload"

    payload = {
        "exam_id": 6,
        "exam_pdf": pdf
    }

    payload = bson.dumps(payload)

    headers = {
        'Content-Type': "application/json",
        'token': str(admin_token),
        'cache-control': "no-cache",
        'Postman-Token': "4a0a5983-fb41-4353-81b6-aaa6d2a42d44"
        }

    pprint(headers)

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response, response.text)

    if response.status_code == 200:
        print(bson.loads(response.content))

def test_download():
    url = "http://10.8.0.2:8000/api/upload"

    payload = {
        "exam_id": 6,
    }

    payload = bson.dumps(payload)

    headers = {
        'Content-Type': "application/json",
        'token': str(admin_token),
        'cache-control': "no-cache",
        'Postman-Token': "4a0a5983-fb41-4353-81b6-aaa6d2a42d44"
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    print(response, response.text)
    
    if response.status_code == 200:
        file = open("./data/result.zip", "wb")
        file.write(bson.loads(response.content)["zip_file"])

test_auth()
test_load()
test_download()