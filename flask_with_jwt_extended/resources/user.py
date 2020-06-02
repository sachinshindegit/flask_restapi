import sqlite3
from flask_restful import Resource, reqparse
from flask_with_jwt_extended.models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_refresh_token_required


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


class UserLogin(Resource):
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
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)  # This will create the JWT
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token, # Will be used to access a resource for endpoints where we have mentioned @jwt_required
                'refresh_token': refresh_token # Remains same per login. When access token expires, refresh token is used to refresh access token without asking password
            }, 200

        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)