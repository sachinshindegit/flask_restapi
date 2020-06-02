import sqlite3
from flask_restful import Resource, reqparse
from flask_rest_with_sqlalchemy.models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,  # Making 'username' as mandatory
                        help='This field cannot be left blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,  # Making 'username' as mandatory
                        help='This field cannot be left blank'
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {'Message': 'User created successfully'}


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User delete'}, 200