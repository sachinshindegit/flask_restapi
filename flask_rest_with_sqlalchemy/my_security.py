from flask_rest_with_sqlalchemy.models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username, password)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)