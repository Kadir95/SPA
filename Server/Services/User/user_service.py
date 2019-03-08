import rpyc
import json
import jwt
import sys
import datetime
import psycopg2 as postg
import hashlib, base64
from rpyc.utils.server import ThreadedServer

sys.path.append("../../Lib")
from connections import connect_rpc, services, connect_db
from response_builder import std_response
from token_operations import secret
import db_operations

conn = connect_db()

class User_service(rpyc.Service):
    def exposed_assign_handler(self, data):
        db_conn = connect_db()
        cur = db_conn.cursor()

        user_id = db_operations.get_user_row(["id"], data["email"])
        user_id = user_id[0] if user_id and len(user_id) > 0 else None
        user_id = user_id[0] if user_id and len(user_id) > 0 else None

        if user_id is None:
            return json.dumps(std_response(False, "There is no user who has <%s> email" %(data["email"])))

        if data["op"] == "instructor":
            try:
                cur.execute("INSERT INTO public.instructors(instructor_id, id_people, department_id_departments) VALUES (%s, %s, %s);", [user_id, user_id, data["department_id"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "User becomes instructor"))
            except Exception as err:
                print(err)
                return json.dumps({
                    "success": False,
                    "message": "Task failed"
                })
        elif data["op"] == "student":
            try:
                cur.execute("INSERT INTO public.students(student_id, id_people, department_id_departments) VALUES (%s, %s, %s);", [user_id, user_id, data["department_id"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "User becomes student"))
            except Exception as err:
                print(err)
                return json.dumps({
                    "success": False,
                    "message": "Task failed"
                })
        elif data["op"] == "admin":
            try:
                cur.execute("INSERT INTO public.admins(admin_id, id_people)VALUES (%s, %s);", [user_id, user_id])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "User becomes admin"))
            except Exception as err:
                print(err)
                return json.dumps({
                    "success": False,
                    "message": "Task failed"
                })
        else:
            return json.dumps({
                "success": False,
                "message": "Operation doesn't match"
            })
    
    def exposed_create_handler(self, data):
        db_conn = connect_db()
        cur = db_conn.cursor()

        if data["op"] == "exam":
            try:
                cur.execute("INSERT INTO public.exam(type) VALUES (%s) RETURNING exam_id;", [data["type"]])
                exam_id = cur.fetchone()[0]
                section_ids = list(map(int, data["section_ids"].split(",")))
                values = [[exam_id, v] for v in section_ids]
                cur.executemany("INSERT INTO public.many_exam_has_many_sections(exam_id_exam, section_id_sections) VALUES (%s, %s);", values)
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "Exam added successfully"))
            except Exception as err:
                print(err)
                return json.dumps(std_response(False, "Task failed"))
        
        elif data["op"] == "section":
            try:
                cur.execute("INSERT INTO public.sections(section_code, course_id_courses, instructor_id_instructors) VALUES (%s, %s, %s);", 
                [data["section_code"], data["course_id"], data["instructor_id"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "Section added successfully"))
            except Exception as err:
                print(err)
                return json.dumps(std_response(False, "Task failed"))
        
        elif data["op"] == "course":
            try:
                cur.execute("INSERT INTO public.courses(name, course_code, department_id_departments) VALUES (%s, %s, %s);", 
                [data["name"], data["course_code"], data["department_id"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "Course added successfully"))
            except Exception as err:
                print(err)
                return json.dumps(std_response(False, "Task failed"))
        
        elif data["op"] == "faculty":
            try:
                cur.execute("INSERT INTO public.faculties(name, university_id_universities) VALUES (%s, %s);", 
                [data["name"], data["university_id"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "Faculty added successfully"))
            except Exception as err:
                print(err)
                return json.dumps(std_response(False, "Task failed"))
        
        elif data["op"] == "department":
            try:
                cur.execute("INSERT INTO public.departments(name, faculty_id_faculties) VALUES (%s, %s);", 
                [data["name"], data["faculty_id"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "Department added successfully"))
            except Exception as err:
                print(err)
                return json.dumps(std_response(False, "Task failed"))
        
        elif data["op"] == "university":
            try:
                cur.execute("INSERT INTO public.universities(name, s_name) VALUES (%s, %s);", 
                [data["name"], data["s_name"]])
                db_conn.commit()
                cur.close()
                return json.dumps(std_response(True, "University added successfully"))
            except Exception as err:
                print(err)
                return json.dumps(std_response(False, "Task failed"))
        
        else:
            return json.dumps(std_response(False, message="Operation doesn't match"))


        

port = services["user_service"]
rypc_server = ThreadedServer(
    User_service,
    port=port
    )
rypc_server.start()