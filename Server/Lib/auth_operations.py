import connections

user_types = ["admin_user", "instructor_user", "student_user", "normal_user"]

def take_user_type(email):
    auth_service = connections.connect_rpc()
    user_type = auth_service.root.user_type(email)
    return user_type