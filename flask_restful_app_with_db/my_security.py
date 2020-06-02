from flask_restful_app_with_db.user import User

def authenticate(username, password):
    user = User.find_by_username(username, password)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_userid(user_id)