import requests
import bson

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
        'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTIyNzk1MjAsIm5hbWUiOiJhYmR1bGthZGlyIiwibGFzdG5hbWUiOiJrdW5kYWtjaW9nbHUiLCJzY2hvb2xfbm8iOjQxNTAxMDE3LCJlbWFpbCI6Imt1bmRha2Npb2dsdWFAbWVmLmVkdS50ciIsImV4cGlyZV90aW1lIjoyfQ.jawlwT8oizGgXgqgRXv49mJPS3UXdRz7RoP7sp_42ag",
        'cache-control': "no-cache",
        'Postman-Token': "4a0a5983-fb41-4353-81b6-aaa6d2a42d44"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response, response.text)
    print(bson.loads(response.content))

    assert bson.loads(response.content) == {"success": True, "message": "File transferred successfully"}

test_load()